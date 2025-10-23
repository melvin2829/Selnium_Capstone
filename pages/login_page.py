# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL = (By.ID, "input-email")
    PASSWORD = (By.ID, "input-password")
    LOGIN_BTN = (By.XPATH, "//input[@value='Login']")
    ALERT = (By.CSS_SELECTOR, ".alert-danger")

    def wait_for_login_page(self):
        self.wait_for_element_visible(self.EMAIL)

    def login(self, email, password):
        self.wait_for_login_page()
        self.enter_text(self.EMAIL, email)
        self.enter_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_alert_message(self):
        try:
            return self.get_text(self.ALERT)
        except:
            return ""
