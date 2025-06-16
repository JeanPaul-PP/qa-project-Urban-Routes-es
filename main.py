import time
from selenium import webdriver
import data
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import pages
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    driver = None

    @classmethod
    #def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        #from selenium.webdriver import DesiredCapabilities
        #capabilities = DesiredCapabilities.CHROME
        #capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        #cls.driver = webdriver.Chrome()
    def setup_class(cls):
        # Esta linea fue creada con ayuda del tutor debido a la version de linux que uso, sin esto el codigo no me funciona
        service = Service('/home/JP/Downloads/WebDriver/bin/chromedriver')
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.pages = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        self.driver.implicitly_wait(10)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_click_tariff_comfort(self):

        self.pages.click_tariff_comfort()
        assert self.driver.find_element(*UrbanRoutesPage.tariff_comfort).is_displayed()

    def test_number_phone(self):
        self.pages.click_add_number_phone()
        assert self.driver.find_element(*UrbanRoutesPage.add_number_phone).is_displayed()

    def test_saved_number(self):
        self.pages.save_number(data.phone_number)
        assert self.driver.find_element(*UrbanRoutesPage.code_number_phone).is_displayed()

    def test_code_number(self):
        assert self.driver.find_element(*UrbanRoutesPage.button_confirm).is_displayed()
        code = retrieve_phone_code(self.driver)
        self.pages.set_code_number_phone(code)

    def test_set_pyment_method(self):
        self.pages.set_pyment_method()
        assert self.driver.find_element(*UrbanRoutesPage.number_card).is_displayed()

    def test_set_add_card(self):
        self.pages.set_add_card(data.card_number)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_add_card(data.card_number)
        assert self.driver.find_element(*UrbanRoutesPage.code_card).is_displayed()

    def test_set_code_card(self):
        assert self.driver.find_element(*UrbanRoutesPage.code_card).is_displayed()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_code_card(data.card_code)


    def test_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message(data.message_for_driver)
        message_element = self.driver.find_element(*UrbanRoutesPage.message)
        assert message_element.get_property('value') == data.message_for_driver

    def test_set_ask(self):
        self.pages.set_ask()
        checkbox = self.driver.find_element(*UrbanRoutesPage.ask_for_blanket)
        assert 'slider round' in checkbox.get_attribute("class") or checkbox.is_selected()

    def test_add_ice(self):
        self.pages.add_ice()


    @classmethod
    def teardown_class(cls):
        time.sleep(2)
        cls.driver.quit()
