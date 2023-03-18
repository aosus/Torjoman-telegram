import asyncio


async def _gather_with_concurrency(number_of_parller_tasks: int, *tasks):
    """
    run many functions in parallel

    Args:
        number_of_parller_tasks (int): Number of parallel tasks

    Returns:
        list: Results of tasks
    """
    semaphore = asyncio.Semaphore(number_of_parller_tasks)

    async def sem_task(task):
        async with semaphore:
            return await task

