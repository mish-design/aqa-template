import pytest
import allure
from playwright.sync_api import sync_playwright
from utils import attach  # Предполагается, что attach.py содержит функции add_page_source() и add_screenshot()


def pytest_addoption(parser):
    """
    Добавляем опции:
      --base-url : базовый URL для тестов
      --browser  : выбор браузера (chromium, firefox, webkit)
      --headless : запуск в headless-режиме (true/false)
    """
    parser.addoption(
        "--base-url",
        action="store",
        default="https://example.com",
        help="Base URL for testing."
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser type: chromium, firefox, or webkit."
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run in headless mode (true/false)."
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    """Возвращает базовый URL."""
    return pytestconfig.getoption("--base-url")


@pytest.fixture(scope="session")
def chosen_browser(pytestconfig):
    """Возвращает тип браузера."""
    return pytestconfig.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(pytestconfig):
    """Преобразует значение headless в булево."""
    return pytestconfig.getoption("--headless").lower() == "true"


@pytest.fixture(scope="session")
def playwright_browser(chosen_browser, headless_mode):
    """Инициализирует Playwright и запускает выбранный браузер."""
    with sync_playwright() as p:
        if chosen_browser == "chromium":
            browser_instance = p.chromium.launch(headless=headless_mode)
        elif chosen_browser == "firefox":
            browser_instance = p.firefox.launch(headless=headless_mode)
        elif chosen_browser == "webkit":
            browser_instance = p.webkit.launch(headless=headless_mode)
        else:
            raise ValueError(f"Unknown browser type: {chosen_browser}")
        yield browser_instance
        browser_instance.close()


@pytest.fixture
def page(playwright_browser, request, base_url):
    """
    Создаёт новый контекст и вкладку (page) для каждого теста.
    При падении теста прикрепляет HTML и скриншот в Allure.
    """
    context = playwright_browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    # При желании можно сразу открыть базовый URL:
    # page.goto(base_url)

    yield page

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        attach.add_page_source(page, name="HTML on failure")
        attach.add_screenshot(page, name="Screenshot on failure")

    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Сохраняет результаты теста в атрибуты item.rep_*,
    чтобы фикстура page могла определить, упал ли тест.
    """
    outcome = yield
    result = outcome.get_result()
    setattr(item, f"rep_{result.when}", result)
