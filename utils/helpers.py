from selenium.webdriver.common.action_chains import ActionChains

def hover_element(driver, element):
    ActionChains(driver).move_to_element(element).perform()

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)

def click_using_js(driver, element):
    driver.execute_script("arguments[0].click();", element)

def take_screenshot(driver, file_name):
    driver.save_screenshot(file_name)
