# pages/product_page.py (patch snippet)
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    ADD_TO_CART_BTN = (By.ID, "button-cart")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "div#content h1")

    def wait_for_product_page(self):
        self.wait_for_element_visible(self.PRODUCT_TITLE)

    def add_to_cart(self):
        self.wait_for_element_visible(self.ADD_TO_CART_BTN)
        self.click(self.ADD_TO_CART_BTN)

    def get_success_alert(self):
        try:
            el = self.wait_for_element_visible(self.SUCCESS_ALERT, timeout=8)
            return el.text
        except Exception:
            return ""
