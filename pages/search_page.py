# pages/search_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchPage(BasePage):
    # each product block in results
    PRODUCTS = (By.CSS_SELECTOR, "div.product-layout")
    PRODUCT_NAME = (By.CSS_SELECTOR, "div.caption h4 a")
    NO_RESULTS = (By.XPATH, "//p[contains(text(), 'There is no product that matches the search criteria.')]")

    def is_no_results(self):
        try:
            self.wait_for_element_visible(self.NO_RESULTS, timeout=5)
            return True
        except:
            return False

    def click_product_by_index(self, index=0):
        # wait for products and click the product at index
        self.wait_for_elements_visible(self.PRODUCT_NAME)
        products = self.driver.find_elements(*self.PRODUCT_NAME)
        if len(products) > index:
            products[index].click()
        else:
            raise Exception("No products found to click")

    def get_product_names(self):
        self.wait_for_elements_visible(self.PRODUCT_NAME)
        return [e.text for e in self.driver.find_elements(*self.PRODUCT_NAME)]
