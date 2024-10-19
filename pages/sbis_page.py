from utils.base_page import BasePage
from selenium.webdriver.common.by import By
import os
import re

class SbisPage(BasePage):
    CONTACTS_BUTTON = (By.XPATH, "//a[contains(text(), 'Контакты')]")
    TENSOR_BANNER = (By.XPATH, "//a[@class='sbisru-Contacts__logo-tensor mb-12']")
    REGION_ELEMENT = (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    PARTNERS_LIST = (By.XPATH, "//div[@class='sbisru-Contacts-List__name sbisru-Contacts-List--ellipsis sbisru-Contacts__text--md pb-4 pb-xm-12 pr-xm-32']")
    FOOTER_LOCAL_VERSIONS_LINK = (By.XPATH, "//a[@class='sbisru-Footer__link' and @href='/download']")
    DOWNLOAD_PLUGIN_BUTTON = (By.XPATH, "//a[@href='https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe']")

    def open_contacts(self):
        self.click_element(self.CONTACTS_BUTTON)

    def click_tensor_banner(self):
        self.click_element(self.TENSOR_BANNER)

    def get_region_element(self):
        return self.find_element(self.REGION_ELEMENT)

    def get_partners_list(self):
        partners = self.find_elements(self.PARTNERS_LIST)
        partners_list = []

        for partner in partners:
            partners_list.append(partner.text)

        return partners_list

    def change_region(self, region_name):
        self.click_element(self.REGION_ELEMENT)
        self.click_element((By.XPATH, f"//span[@title='{region_name}']"))

    def go_to_local_versions(self):
        self.click_element(self.FOOTER_LOCAL_VERSIONS_LINK)

    def download_plugin(self):
        self.click_element(self.DOWNLOAD_PLUGIN_BUTTON)

    def verify_download(self):
        download_path = f"{os.path.dirname(os.getcwd())}\\download"
        expected_size_mb = re.search(r'\d{1,}.\d{1,}', self.find_element(self.DOWNLOAD_PLUGIN_BUTTON).text).group()
        files = os.listdir(download_path)
        plugin_file = [f for f in files if f.endswith(".exe")]

        if not plugin_file:
            raise FileNotFoundError("Файл плагина не был найден в папке загрузок.")

        file_path = os.path.join(download_path, plugin_file[0])
        file_size = os.path.getsize(file_path) / (1024 * 1024)

        assert abs(file_size - float(expected_size_mb)) < 0.1, f"Размер файла не совпадает. Ожидалось {expected_size_mb} MB, получено {file_size} MB"
        print(f"Файл плагина успешно скачан и совпадает по размеру: {file_size:.2f} MB")
