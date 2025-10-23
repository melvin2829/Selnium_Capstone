# tests/test_search_add_to_cart.py
import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.excel_utils import read_excel_data

@pytest.mark.usefixtures("setup")
class TestSearchAddToCart:

    @pytest.mark.parametrize("product", read_excel_data("data/test_data.xlsx", "search"))
    def test_search_add_to_cart(self, product):
        home_page = HomePage(self.driver)
        home_page.search_product(product[0] if isinstance(product, list) else product)
        search_page = SearchPage(self.driver)
        # optional: check there are results
        if search_page.is_no_results():
            pytest.skip("No search results for: " + (product[0] if isinstance(product, list) else product))
        search_page.click_product_by_index(0)   # click first search result
        product_page = ProductPage(self.driver)
        product_page.wait_for_product_page()
        product_page.add_to_cart()
        # some sites update cart async, wait for success alert
        assert "Success" in product_page.get_success_alert()
        cart_page = CartPage(self.driver)
        cart_page.open_cart()
        assert cart_page.get_products_count() > 0
