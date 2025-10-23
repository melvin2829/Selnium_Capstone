# tests/test_login.py (only the test method shown)
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.excel_utils import read_excel_data

@pytest.mark.usefixtures("setup")
class TestLogin:

    @pytest.mark.parametrize("username,password,expected", read_excel_data("data/test_data.xlsx", "login"))
    def test_login(self, username, password, expected):
        home = HomePage(self.driver)
        # ensure we're logged out so Login page is reachable
        home.ensure_logged_out()

        home.open_login_page()             # navigate to Login page
        login_page = LoginPage(self.driver)
        login_page.login(username, password)
        if expected == "Login Successful":
            assert "My Account" in self.driver.title or "Account" in self.driver.page_source
        else:
            assert "Warning" in login_page.get_alert_message()
