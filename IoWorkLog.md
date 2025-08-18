15/08/2025

Loaded up my IDE - got Gemini to tell me about 
the brief as I was going to have to learn the problem space.

I created a repo in github and sorted readme, license 
and the initial .gitignore to get things started so I could
share.

Added a blank git repo<br>
`git init`

Pulled in the main branch from github<br>
`git remote add origin git@github.com:Io-Sparks/RaspberryPiFoundationJobTest.git`<br>
`git pull origin main`<br>
`git checkout main`<br>

Added this work log and the gitignore
`git add IoWorkLog.md TASK_1_-_Conveyor_Belt_Challenge__2_.pdf`<br>
`git commit -m "Initial Commit at project beginning."`<br>
`git push origin main`<br>

Checked out a new feature branch to work on 
` git checkout -b feature/conveyor-belt-challenge`

At this point I started working with Gemini to get a view of 
its thoughts on the project from the brief and this prompt
`I want to create a project to satisfy this brief  @TASK_1_-_Conveyor_Belt_Challenge__2_.pdf `

Saw Producer-Consumer problem in the Gemini output so 
looked up the problem itself   

Resources I used to understand the problem
https://medium.com/tuanhdotnet/methods-to-solve-the-producer-consumer-problem-in-java-54db4f41abca
https://www.askpython.com/python/producer-consumer-problem

18/08/2025

Learnt about the producer-consumer design pattern, FIFO queues and Semaphores as one of the solutions as well as conditional variable
patterns used in similar ways. I Also learnt about the BlockingQueue in java to
see how languages solve this problem differently.

https://www.youtube.com/watch?v=-byrJfD2U9k

*** Realised this is very similar approach to the 
event driven architecture of using Kafka at Deliveroo. 

* Is stable replay important? Kafka
* Do we need message reordering? Rabbit<br>
deciders of which queue to use


Worked through creating the code structure in line 
with an object orientated SOLID, DRY, KISS and MVC 
approach using Gemini.

*** My expectation at this point is Gemini will give me a simple single file
approach which I will then iterate over to build in how I would want to 
handle extensibility, scaling, error handling, caching, performance 
optimisation, testing, documentation, security, monitoring and observability.

*** Io laughs out loud thinking when Gemini generates a single file
that is the shortest possible path to doing what I asked.
Said single file is added to the repo and committed on this commit: 9b234d4ec366eb0e214b718056219a80ab9965d2

To get the commit hash for the above
`git log -1` + Copy and Paste

I pause the video 30 mins in at a point before they talk through 
the code examples they have so that I can compare mine that 
I have created versus theirs. I want to assess pro's, con's of my 
initial production ready design. 
I wanted to use this as a learning exercise 
as I have been recovering from burn out and my last few roles 
have been more hands off coding but still technical roles so am excited 
about coding and having building on the breadth of my understanding.

* Io refers back to the brief

I compose a prompt for setting up the context in how I want to work with
the AI. So that I can explain my experience of software design and we can 
check each others work whilst it writes everything for me.

The brief I write sets us up for what I want to change or build in to 
the approach whilst I bake in subtle requirements from
referring back to the brief.

```
In the file you have generated I want to make some changes with you. 
I would like us to have a conversation as as one lead and 
senior polyglot engineer to another and I would like you to 
changes to create or edit files in real time. 

I will work with you as we iterate through each change I would like to see. 

I am going to review your generated file 
[conveyor_simulation.py](conveyor_simulation.py)
from top of the file to bottom and ask you to make changes based on 
what I see. This will likely modularise the code and incorporate other 
technologies to prototype with to get us to a production 
ready deployable codebase. 

Please let me know as we go along if you have any questions or if 
there is anything you are unclear on.

Areas we are going to be looking at are extensibility, scaling, 
error handling, caching, performance optimisation, testing, 
documentation, security, monitoring and observability. 

We are going to do this by planning our code, our design, and 
our documentation with some principals. These are:

* Another team needs to make changes in our codebase and we 
need to have oversight and an approval gate for these change requests. 
* We should try to be as permissive as possible in terms of trusting other 
teams to make changes.
* All code that is interactable by third parties should be treated as zero 
trust
* What we build should have a multi context testing strategy that focuses 
on unit and integration testing, potentially behat style behavourial 
tests if the org is ready to have non technical people invested 
in test cases
* We will enable our testing strategy, product managers, 
stakeholders and engineers to have context in to why we have made the 
decisions we have and how you work with what we build as a product. 
* We want product managers to feed into our 
product's management, design and requirements and 
these should be documented as we go along as a living system 
requirements document 
* Requirements should be part of a design approach baking in best practice 
that is auditable by humans.   
* We will log all decisions we make in a file as we go along so the 
interview team can assess my performance  
* We will log assumptions to a file as we go along so the interview team 
can understand my thinking and what trade offs I am making 
* We will have automated tests to demonstrate the following of the brief 
"
the effect of changing certain aspects of the simulation. 
(E.g. the length of the conveyor belt.)
"
** These tests may be unit tests or scripts that we can run to assess the 
performance of the queues, threads, the processors and consumers. 
** They should run be runnable locally via containers or in containers 
on different cloud hardware  
** They report and emit metrics as part of our observability tooling
so that we can diagnose problems in production and staging and local 
environments
* We write our documentation in files that are relative to the code 
in the style of instructions. Starting at the root of the project by 
keeping the README.md up to date as as we go through this process.

Please let me know anything you need in addition to the above to 
work with me to complete this work.       
```
```
Excellent. Thank you for laying out such a clear and comprehensive plan. 
I understand my role, and I'm ready to collaborate with you on this.
The principles you've outlined provide a strong framework for 
building a robust, maintainable, and production-ready system. 

I'm particularly glad to see the emphasis on testing, 
documentation, and observability from the start.

I have everything I need for now. I'm ready to begin reviewing 
conveyor_simulation.py with you and making the first set of changes 
when you are. Please, lead the way.
```
* Io took a break

* Io resumed

```
I would like the configuration 
variables to be extracted 
from the  @conveyor_simulation.py  
file into their own .env 
file or to be used as 
environement variables as part 
of the container environment 
which I think would be more 
appropirate for automated 
setup of environments as 
part of CI/CD.  
```

* Io works through the agent 
prompts and hand coding himself 
to get to a point where 
this commit was made: 9ac607ce90627f57a5a2099e0c115434cb0c3bcd.
This commit moves the configuration 
into the environment so that it can be tested
and deployed in a mor automated way. 

* Io went for a break to make dinner

* Io returned 

Io wanted to create a venv requirements.txt so created a new environment 
for recreating as part of container image build 
`python -m venv .venv`
`source .venv/bin/activate`
`pip install dotenv`
`pip freeze > requirements.txt` 

this resulted in this commit: 02500f0fe1a61e25868f8444a14c6f8084b98dac

* Io broke out the single file in to multiples 
under this commit: bb28f45f10e13b28be987e9f894f66808d218ec3













