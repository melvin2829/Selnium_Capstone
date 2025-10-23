# pages/cart_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class CartPage(BasePage):
    CART_BTN = (By.ID, "cart")  # top-level cart element
    VIEW_CART_LINK = (By.CSS_SELECTOR, "#cart .dropdown-menu a[href*='route=checkout/cart']")
    PRODUCTS_IN_CART = (By.CSS_SELECTOR, "table.table tbody tr")

    def open_cart(self):
        # click cart to open dropdown
        try:
            self.click(self.CART_BTN)
        except Exception:
            # fallback: click by JS
            el = self.wait_for_element_present(self.CART_BTN, timeout=5)
            self.driver.execute_script("arguments[0].click();", el)

        # wait briefly for dropdown menu to populate then click fresh element
        for attempt in range(5):
            try:
                link = self.wait_for_element_visible(self.VIEW_CART_LINK, timeout=3)
                try:
                    link.click()
                    return
                except Exception:
                    self.driver.execute_script("arguments[0].click();", link)
                    return
            except Exception:
                time.sleep(0.5)
                continue
        # last resort: navigate directly to cart page
        try:
            self.driver.get(self.driver.current_url.rstrip("/") + "/index.php?route=checkout/cart")
        except Exception:
            raise

    def get_products_count(self):
        elems = self.driver.find_elements(*self.PRODUCTS_IN_CART)
        return len(elems)
