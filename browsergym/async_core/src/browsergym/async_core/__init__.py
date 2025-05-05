__version__ = "0.13.3"

import playwright.async_api

# we use a global playwright instance
_PLAYWRIGHT = None


def _set_global_playwright(pw: playwright.async_api.Playwright):
    global _PLAYWRIGHT
    _PLAYWRIGHT = pw


async def _get_global_playwright():
    global _PLAYWRIGHT
    if not _PLAYWRIGHT:
        pw = await playwright.async_api.async_playwright().start()
        _set_global_playwright(pw)

    return _PLAYWRIGHT


# register the open-ended task
from .registration import register_task
from .task import OpenEndedTask

register_task(OpenEndedTask.get_task_id(), OpenEndedTask)