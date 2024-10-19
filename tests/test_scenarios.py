import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_prefs = {
        "download.default_directory": f"{os.path.dirname(os.getcwd())}\\download",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_first_scenario(driver):
    driver.get("https://sbis.ru/")
    sbis_page = SbisPage(driver)
    sbis_page.open_contacts()

    sbis_page.click_tensor_banner()

    driver.switch_to.window(driver.window_handles[1])

    tensor_page = TensorPage(driver)

    assert tensor_page.check_power_in_people_exists(), "Блок 'Сила в людях' не найден"

    tensor_page.click_learn_more()

    assert driver.current_url == "https://tensor.ru/about", "URL 'Подробнее' не совпадает"

    assert tensor_page.check_images_size(), "Размеры фотографий не совпадают"


def test_second_scenario(driver):
    driver.get("https://sbis.ru/")
    sbis_page = SbisPage(driver)

    sbis_page.open_contacts()

    assert "Нижегородская обл." == sbis_page.get_region_element().text, "Регион не определен корректно"

    partners_nn = sbis_page.get_partners_list()
    partners_list = ['СБИС-Софт', 'СБИС - Нижний Новгород', 'АБТ Сервисы для бизнеса', 'СБИС-Софт, Нижегородский район',
                     'СБИС-Софт, Автозаводский район', 'СБИС-Софт, Сормовский район', 'КомплектСофт',
                     'ИП Тряскина Е.А.', 'ИнфоТех', 'ИП Сибиркин А.П.', 'СБИС - Дзержинск', 'ЭксперТ',
                     'ООО "БИЗНЕСЦЕНТР"', 'ИП Варварин А.Л.', 'Бухгалтер', 'Бочин Евгений Кузьмич ИП',
                     'ИП Шулдыков А.Н', 'ИП Горелов А.Л.', 'ООО "Диалог"', 'ИП Серова Н.Е.'
                     ]

    assert partners_nn == partners_list, "Неправильный список партнеров"

    sbis_page.change_region("Камчатский край")
    time.sleep(5)

    assert "Камчатский край" == sbis_page.get_region_element().text, "Регион не определен корректно"

    partners_kk = sbis_page.get_partners_list()

    assert partners_kk != partners_list, "Список партнеров не изменился"

    assert driver.current_url == 'https://sbis.ru/contacts/41-kamchatskij-kraj?tab=clients', "URL не содержит информации о регионе"

    assert "Камчатский край" in driver.title, "Заголовок не обновился"

def test_third_scenario(driver):
    driver.get("https://sbis.ru/")
    sbis_page = SbisPage(driver)

    sbis_page.go_to_local_versions()
    time.sleep(5)

    sbis_page.download_plugin()
    time.sleep(10)

    sbis_page.verify_download()
