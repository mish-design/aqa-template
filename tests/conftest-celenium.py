import pytest
from selene import browser
from selenium import webdriver

from utils import attach  # <-- Если у вас есть модуль для прикреплений (скриншоты, логи, видео)


def pytest_addoption(parser):
    """
    Добавляем кастомную опцию для указания base_url.
    Пример запуска:
      pytest --base-url="https://stage.example.com"
    """
    parser.addoption(
        "--base-url",
        action="store",
        default="https://my-website.com",
        help="Base URL для тестирования."
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    """
    Фикстура, возвращающая base_url, полученный из командной строки (или из default).
    """
    return pytestconfig.getoption("--base-url")


@pytest.fixture(scope="function", autouse=True)
def remote_browser(base_url):
    """
    Универсальная фикстура, создающая WebDriver (Chrome) на удалённом сервере (Selenoid).
    После теста прикрепляем скриншоты, логи, видео и завершаем сессию.
    """
    capabilities = {
        "browserName": "chrome",
        "browserVersion": "114.0",  # При необходимости укажите другую версию
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "screenResolution": "1920x1080x24",
            "sessionTimeout": "5m"
        }
    }
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Можно выключить, если хотите видеть браузер
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.set_capability("selenoid:options", capabilities)
    # Быстрая загрузка страниц
    options.page_load_strategy = "eager"

    driver = webdriver.Remote(
        command_executor="https://selenoid.mish.design/wd/hub",  # Замените на свой URL
        options=options
    )
    driver.implicitly_wait(10)
    browser.config.driver = driver
    browser.config.timeout = 10.0
    driver.maximize_window()

    # При желании можно сразу открыть base_url
    # browser.open(base_url)

    yield driver

    # В конце теста (Teardown) - прикрепить логи и скриншоты
    if "attach" in globals():
        attach.add_html(browser)
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_video(browser)
    driver.quit()
