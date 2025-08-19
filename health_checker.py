import http.server
import socketserver
import threading
import time
from typing import Optional


class HealthState:
    """Thread-safe class to store the application's health state."""

    def __init__(self):
        self._lock = threading.Lock()
        self._ready = threading.Event()
        self._last_heartbeat: Optional[float] = None

    def set_ready(self):
        """Signal that the application is ready."""
        self._ready.set()

    def is_ready(self) -> bool:
        """Check if the application is ready."""
        return self._ready.is_set()

    def record_heartbeat(self):
        """Record a liveness heartbeat."""
        with self._lock:
            self._last_heartbeat = time.monotonic()

    def is_alive(self, timeout_seconds: int = 30) -> bool:
        """
        Check if the application is alive based on the last heartbeat.
        Returns False if a heartbeat has never been recorded or if it's too old.
        """
        with self._lock:
            if self._last_heartbeat is None:
                return False
            return (time.monotonic() - self._last_heartbeat) < timeout_seconds


class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
    """A custom request handler for health checks."""

    # This is a class-level attribute that will be set before the server starts.
    # It allows us to pass the shared health state into the request handler.
    health_state: HealthState

    def do_GET(self):
        """Handle GET requests for /healthz and /readyz."""
        if self.path == "/healthz":
            self._handle_liveness()
        elif self.path == "/readyz":
            self._handle_readiness()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _handle_liveness(self):
        """Handles the liveness probe."""
        if self.health_state.is_alive():
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b"Service Unavailable: Liveness probe failed")

    def _handle_readiness(self):
        """Handles the readiness probe."""
        if self.health_state.is_ready():
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b"Service Unavailable: Not ready")

    def log_message(self, format: str, *args):
        """Suppress the default log messages for quiet operation."""
        return


class HealthChecker:
    """Runs the health check web server in a background thread."""

    def __init__(self, state: HealthState, port: int = 8080):
        self.state = state
        self.port = port
        self.thread: Optional[threading.Thread] = None

    def start(self):
        """Starts the health check server in a daemon thread."""

        # We need to subclass the handler to pass the state into it.
        # This is a bit of a quirk of the http.server module.
        class CustomHandler(HealthCheckHandler):
            health_state = self.state

        # The TCPServer needs to be instantiated with the custom handler class.
        httpd = socketserver.TCPServer(("", self.port), CustomHandler)

        # Start the server in a background thread.
        # The thread is set as a daemon so it won't block program exit.
        self.thread = threading.Thread(target=httpd.serve_forever)
        self.thread.daemon = True
        self.thread.start()
