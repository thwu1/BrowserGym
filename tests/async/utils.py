import browsergym.async_core
import logging
import playwright.async_api
import pytest


# setup code, executed ahead of first test
@pytest.fixture(scope="session", autouse=True)
def setup_playwright(playwright: playwright.async_api.Playwright):
    # bugfix: re-use pytest-playwright's playwright instance in browsergym
    # https://github.com/microsoft/playwright-python/issues/2053
    browsergym.async_core._set_global_playwright(playwright)
    logging.info("Browsergym is using the playwright instance provided by pytest-playwright.")
