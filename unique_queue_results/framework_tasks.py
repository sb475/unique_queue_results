import asyncio
from concurrent.futures import ThreadPoolExecutor
import dataclasses
import multiprocessing
import queue
from time import sleep
from typing import Any, Callable, List
from uuid import uuid4
from framework_result import FrameworkResults


@dataclasses.dataclass
class FrameworkTask:
    """This class creates a task and automatically submits it to a queue for processing."""

    func: Callable
    args: list = dataclasses.field(default_factory=list)
    kwds: dict = dataclasses.field(default_factory=dict)
    task_id: str = dataclasses.field(default_factory=lambda: str(uuid4()))

    async def submit_task(self) -> str:
        """Submits a task to the framework queue for processing, but promises a
        future to the calling location/function. Wrapper future for the future from task being
        processed"""
        FrameworkResults.queue.put(self)
        results = self.results()
        return await results

    def run_task(self):
        """This is how the task should run. Can be overwritten for different task variations
        if required."""
        return self.func(*self.args, **self.kwds)

    async def results(self):
        """Returns the awaitied coroutine and results. If key is not present yet, This means the
        task is still in queue and coroutine should sleep to free up resources."""
        while self.task_id not in FrameworkResults.map.keys():
            await asyncio.sleep(1)
        else:
            return FrameworkResults.map.pop(self.task_id)

def get_pending_tasks(task_queue: queue.Queue):
    """Pull any tasks in queue and reutrn an array of Tasks"""
    received_tasks = []
    while not task_queue.empty():
        try:
            task: FrameworkTask = task_queue.get_nowait()
        except queue.Empty:
            return None
        else:
            received_tasks.append(task)
            task_queue.task_done()
        return received_tasks
    else:
        return None


    
async def proccess_pending_tasks(task_queue: queue.Queue):
    """This function calls helper function to get items in queue and create a task to run task in executor
    without blocking."""
    
    
    loop = asyncio.get_running_loop()
    tasks_to_run = get_pending_tasks(task_queue)
    if tasks_to_run is None:
        await asyncio.sleep(.5)
    else:
        loop.create_task(run_tasks_in_executor(loop, tasks_to_run))

       
async def run_tasks_in_executor(loop, task_list):
    """Assigns the return of task run in executor to dictionary, this allows specific results to be identified instead of
    standard"""
    max_threads: int = multiprocessing.cpu_count()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
           
            # running_tasks = [map_and_run_task(loop, executor, task) for task in tasks_to_run]
            for task in task_list:
                FrameworkResults.map[task.task_id] = await loop.run_in_executor(executor, task.run_task)

