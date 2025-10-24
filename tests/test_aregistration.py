# tests/test_registration.py
import pytest
from pages.registration_page import RegistrationPage
from pages.home_page import HomePage
from utils.excel_utils import read_excel_data

@pytest.mark.usefixtures("setup")
class TestRegistration:

    @pytest.mark.parametrize("firstname,lastname,email,telephone,password,confirm,subscribe",
                             read_excel_data("data/test_data.xlsx", "registration"))
    def test_register_user(self, firstname, lastname, email, telephone, password, confirm, subscribe):
        home = HomePage(self.driver)
        home.open_register_page()          # navigate to Register page
        reg_page = RegistrationPage(self.driver)
        reg_page.register_user(firstname, lastname, email, telephone, password, confirm, subscribe)

        msg = reg_page.get_success_message()
        # accept either classic success message or Account page title/header
        assert ("Your Account Has Been Created!" in msg) or ("Account" in msg) or ("Success" in msg)
