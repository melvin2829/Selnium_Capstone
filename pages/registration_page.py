# pages/registration_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    FIRSTNAME = (By.ID, "input-firstname")
    LASTNAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM = (By.ID, "input-confirm")
    SUBSCRIBE_YES = (By.XPATH, "//input[@name='newsletter' and @value='1']")
    SUBSCRIBE_NO = (By.XPATH, "//input[@name='newsletter' and @value='0']")
    PRIVACY_POLICY = (By.NAME, "agree")
    CONTINUE_BTN = (By.XPATH, "//input[@value='Continue']")
    SUCCESS_MSG = (By.CSS_SELECTOR, "#content h1")

    def wait_for_registration_page(self):
        self.wait_for_element_visible(self.FIRSTNAME)

    def register_user(self, firstname, lastname, email, telephone, password, confirm, subscribe):
        self.wait_for_registration_page()
        self.enter_text(self.FIRSTNAME, firstname)
        self.enter_text(self.LASTNAME, lastname)
        self.enter_text(self.EMAIL, email)
        self.enter_text(self.TELEPHONE, telephone)
        self.enter_text(self.PASSWORD, password)
        self.enter_text(self.CONFIRM, confirm)

        if str(subscribe).strip().lower().startswith("y"):
            self.click(self.SUBSCRIBE_YES)
        else:
            self.click(self.SUBSCRIBE_NO)
        self.click(self.PRIVACY_POLICY)
        self.click(self.CONTINUE_BTN)

    def get_success_message(self):
        # Try to return the success heading; otherwise fallback to page title or "Account" header
        try:
            elems = self.driver.find_elements(*self.SUCCESS_MSG)
            if elems:
                return elems[0].text.strip()
        except Exception:
            pass

        # fallback to page title or a generic Account header on page
        try:
            title = self.driver.title
            if title:
                return title.strip()
        except Exception:
            pass

        # last fallback: try another heading inside content
        try:
            other = self.driver.find_elements(By.CSS_SELECTOR, "#content h2")
            if other:
                return other[0].text.strip()
        except Exception:
            pass

        return ""
