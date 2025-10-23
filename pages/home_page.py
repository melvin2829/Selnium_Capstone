# pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

class HomePage(BasePage):
    SEARCH_BOX = (By.NAME, "search")
    SEARCH_BTN = (By.CSS_SELECTOR, "div#search button")
    MY_ACCOUNT = (By.CSS_SELECTOR, "a[title='My Account']")
    MY_ACCOUNT_FALLBACK = (By.XPATH, "//span[text()='My Account']")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    LOGIN_LINK = (By.LINK_TEXT, "Login")

    # Locators for logout handling
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    ACCOUNT_LINKS = (By.CSS_SELECTOR, "ul.dropdown-menu li a")  # links inside My Account dropdown

    def _open_account_dropdown(self):
        """
        Try to open the My Account dropdown using the main locator.
        Falls back to the visible text span or JS click.
        """
        try:
            # primary attempt
            self.click(self.MY_ACCOUNT)
        except Exception:
            # fallback: try visible text span
            try:
                self.click(self.MY_ACCOUNT_FALLBACK)
            except Exception:
                # last resort: find element then JS click
                el = self.wait_for_element_present(self.MY_ACCOUNT, timeout=5)
                self.driver.execute_script("arguments[0].click();", el)

    def open_login_page(self):
        """
        Open My Account -> Login. If dropdown is flaky, falls back to direct login URL.
        """
        try:
            self._open_account_dropdown()
            self.click(self.LOGIN_LINK)
        except TimeoutException:
            # fallback: navigate directly to login page (OpenCart typical route)
            try:
                self.driver.get(self.driver.current_url.rstrip("/") + "/index.php?route=account/login")
            except Exception:
                raise

    def open_register_page(self):
        """
        Open My Account -> Register. Falls back to direct register URL if needed.
        """
        try:
            self._open_account_dropdown()
            self.click(self.REGISTER_LINK)
        except TimeoutException:
            try:
                self.driver.get(self.driver.current_url.rstrip("/") + "/index.php?route=account/register")
            except Exception:
                raise

    def ensure_logged_out(self):
        """
        Ensure the session is logged out. Tries dropdown Logout, page links, and final URL fallback.
        Safe to call before opening Login page.
        """
        try:
            # try opening dropdown (safe)
            try:
                self._open_account_dropdown()
            except Exception:
                # dropdown may not open; continue to other checks
                pass

            # try clicking Logout inside dropdown
            try:
                self.click(self.LOGOUT_LINK)
                return
            except Exception:
                # fallback: search for any 'Logout' link in the menu/list
                try:
                    elems = self.driver.find_elements(*self.ACCOUNT_LINKS)
                    for e in elems:
                        if e.text.strip().lower() == "logout":
                            try:
                                e.click()
                                return
                            except Exception:
                                self.driver.execute_script("arguments[0].click();", e)
                                return
                except Exception:
                    pass

            # last resort: go to standard OpenCart logout URL
            try:
                self.driver.get(self.driver.current_url.rstrip("/") + "/index.php?route=account/logout")
            except Exception:
                pass

        except Exception:
            # swallow errors — caller will attempt to open login page anyway
            pass

    def search_product(self, product):
        """
        Search for a product using the search box and submit.
        """
        search_box = self.wait_for_element_visible(self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(product)
        # press ENTER to submit search
        search_box.send_keys("\n")
