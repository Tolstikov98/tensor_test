from utils.base_page import BasePage
from selenium.webdriver.common.by import By

class TensorPage(BasePage):
    POWER_IN_PEOPLE_BLOCK = (By.XPATH, "//p[text()='Сила в людях']")
    LEARN_MORE_BUTTON = (By.XPATH, "//a[@class='tensor_ru-link tensor_ru-Index__link' and @href='/about']")
    IMAGES = (By.XPATH, "//div[@class='tensor_ru-About__block3-image-wrapper']")

    def check_power_in_people_exists(self):
        return self.find_element(self.POWER_IN_PEOPLE_BLOCK)

    def click_learn_more(self):
        self.click_element(self.LEARN_MORE_BUTTON)

    def check_images_size(self):
        images = self.find_elements(self.IMAGES)
        sizes = [(img.size['width'], img.size['height']) for img in images]
        return all(size == sizes[0] for size in sizes)
