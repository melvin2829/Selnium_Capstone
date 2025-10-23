# tests/conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Import config AFTER project-root conftest has inserted project root on sys.path
from config.config import BROWSER, BASE_URL, IMPLICIT_WAIT, WINDOW_SIZE

@pytest.fixture(params=[BROWSER], scope="class")
def setup(request):
    """
    Browser fixture that launches the browser, navigates to BASE_URL,
    assigns driver to the test class (request.cls.driver) and quits after tests.
    """
    browser = request.param
    if browser.lower() == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser.lower() == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        raise Exception("Browser not supported: " + str(browser))

    driver.implicitly_wait(IMPLICIT_WAIT)
    try:
        driver.set_window_size(*WINDOW_SIZE)
    except Exception:
        pass
    driver.get(BASE_URL)

    # attach to class so tests can use self.driver
    request.cls.driver = driver
    yield

    try:
        driver.quit()
    except Exception:
        pass


# Screenshot on failure hook (keeps what you had)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = getattr(item.instance, "driver", None)
        if driver:
            screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = os.path.join(screenshots_dir, f"{item.name}.png")
            try:
                driver.save_screenshot(file_name)
            except Exception:
                pass
