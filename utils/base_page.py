from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator, timeout=30):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    def click_element(self, locator, timeout=30):
        element = self.find_element(locator, timeout)
        element.click()

    def get_element_attribute(self, locator, attribute, timeout=30):
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
