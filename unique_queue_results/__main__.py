import asyncio
import random
import time
from tkinter import N

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from framework_tasks import proccess_pending_tasks, FrameworkTask
from framework_result import FrameworkResults


def blocking_task(text: str, sleep_time: int) -> str:
    """This function simulates a long proccessing task"""
    print(f"Blocking function STARTED. For {text}/{sleep_time}")
    time.sleep(sleep_time)
    print(f"Blocking function ENDED for {text}/{sleep_time}")
    return text


async def submit_new_task(text: str) -> str:
    """Wrapper function to provide feedback to user when text is entered"""

    print("Submitting new task with text entered...")
    time_to_sleep = random.randint(1, 10)  # nosec
    task_value = await FrameworkTask(
        func=blocking_task,
        args=[
            f"You said: {text} and this function will sleep for {time_to_sleep}",
            time_to_sleep,
        ],
    ).submit_task()

    print(
        f"Get the results from the function in place. Your results where: {task_value}"
    )


async def generate_sample_data():
    """Create some content to be displayed to showcase retrieving unique
    value from a queue."""

    test_results = []

    for _ in range(20):
        time_to_sleep = random.randint(1, 10)  # nosec
        test_results.append(
            FrameworkTask(
                func=blocking_task,
                args=[
                    f"This function number {_} ran for {time_to_sleep}",
                    time_to_sleep,
                ],
            ).submit_task()
        )

    for task in asyncio.as_completed(test_results):
        result = await task
        print(f"Task result is: {result}")


async def background_proccess_loop():
    """The coroutine that runs in background and processing items in"""
    try:
        while True:
            await proccess_pending_tasks(FrameworkResults.queue)
            await asyncio.sleep(0.5)

    except asyncio.CancelledError:
        print("Background task cancelled.")


async def interactive_shell():
    """
    Straight out of command prompt_toolkit example: asyncio-prompt. This
    example code helps display async capabilities of concepts.
    """
    # Create Prompt.
    session = PromptSession("Say something: ")

    # Run echo loop. Read text from stdin, and create task from stdin.
    while True:
        try:
            result = await session.prompt_async()
            asyncio.create_task(submit_new_task(result))
        except (EOFError, KeyboardInterrupt):
            return


async def run_demo():
    """Helper function to isolate main running event loop from generating sample data"""
    with patch_stdout():
        background_task = asyncio.create_task(background_proccess_loop())
        try:
            await interactive_shell()
        finally:
            background_task.cancel()
        print("Quitting event loop. Bye.")


async def main():
    asyncio.gather(run_demo(), generate_sample_data())


if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("Received exit, exiting")
