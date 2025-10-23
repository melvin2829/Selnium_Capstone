# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selexc
from selenium.webdriver.common.by import By
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def wait_for_element_present(self, locator, timeout=20):
        w = WebDriverWait(self.driver, timeout)
        return w.until(EC.presence_of_element_located(locator))

    def wait_for_element_visible(self, locator, timeout=20):
        w = WebDriverWait(self.driver, timeout)
        return w.until(EC.visibility_of_element_located(locator))

    def wait_for_elements_visible(self, locator, timeout=20):
        w = WebDriverWait(self.driver, timeout)
        return w.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator, timeout=20, attempts=3):
        """
        Robust click: waits for element to be clickable, retries on stale element
        and falls back to JS click if normal click fails.
        """
        for attempt in range(attempts):
            try:
                w = WebDriverWait(self.driver, timeout)
                element = w.until(EC.element_to_be_clickable(locator))
                try:
                    element.click()
                    return
                except Exception:
                    # fallback: JS click
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        return
                    except Exception:
                        pass
            except selexc.StaleElementReferenceException:
                time.sleep(0.5)
                continue
            except selexc.TimeoutException:
                # let caller handle timeout if last attempt
                if attempt == attempts - 1:
                    raise
                time.sleep(0.5)
                continue
        # final attempt: try to find element fresh and JS click
        el = self.wait_for_element_present(locator, timeout=5)
        self.driver.execute_script("arguments[0].click();", el)

    def enter_text(self, locator, text):
        el = self.wait_for_element_visible(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        el = self.wait_for_element_visible(locator)
        return el.text
