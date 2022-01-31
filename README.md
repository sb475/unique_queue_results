# unique_queue_results

This is a concept project that addresses issue with asynchronously processing user input and creating a threaded task from it.

## Description
This is a concept project about asynchronously processing user input and creating a threaded task from it. It makes use
of prompt_toolkit becuase...well I think it's  a really powerfull library and I like the way it looks. Intgration with 
asynchio is very easy to use and fantastic.

## The Issue
Displayed with this project is user entering input, and a "Task" being created. Tasks can be submitted to a queue for processing. Processing tasks if arbitrary and pretty straightforward. The problem? How do I get the the results back? Popping the first time in the queue does not work as there is no gurantee the result from the queue will be the one I want, particularly if I have tasks being called from different parts of an application.

## The Solution/Concept
To address this, I use a map for the results. The map uses a task_id as the key and value is the coroutine that is the 
task to be run. When a function submits a task, it returns a coroutine that uses the main check to determine if the task_id exists in the map. If the key does exist, then it returns the future, if it does not, it sleeps to try again.
No key in the map means that the task has not been processed yet, ideal for large number of tasks that may be pending in queue.

## Usage
This project makes use of poetry. Download and install if not already.

`poetry install`
`poetry shell`
`python3 unqiue_queue_results`