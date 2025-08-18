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

Learnt about Semaphores as one of the solutions as well as conditional variable 
patterns used in similar ways. I Also learnt about the BlockingQueue in java to 
see how languages solve this problem differently.

I then continued to follow the python tutorial


