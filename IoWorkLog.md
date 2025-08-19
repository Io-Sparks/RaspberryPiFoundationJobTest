15/08
Loaded up my IDE - got Gemini to tell me about 
the brief as I was going to have to learn the problem space.

I created a repo in github and sorted readme, license 
and the initial .gitignore to get things started so I could
share.

added a blank git repo
`git init`

pulled in the main branch from github
`git remote add origin git@github.com:Io-Sparks/RaspberryPiFoundationJobTest.git`
`git pull origin main`
`git checkout main`
added this work log and the gitignore
`git add IoWorkLog.md TASK_1_-_Conveyor_Belt_Challenge__2_.pdf`
`git commit -m "Initial Commit at project beginning."`

Added in core components of the simulation

Added unit testing 

Added optimisations and experiments to see what effects
changing different parts of the configuration would have
please run with 
`python simulation.py --belt-length 15 --num-worker-pairs 3 --strategy team`

Added Dockerfile to bring consistency between environments.
Didnt add kubernetes and associated checks that would manage a lot of 
scalability aspects as it adds a lot of complexity that is 
unneccesary at this stage 



