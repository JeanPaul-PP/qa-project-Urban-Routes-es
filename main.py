import time
from sys import executable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import data
from selenium.webdriver.chrome.service import Service

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

# Clase, pagina principal, ingresar direcciones y atributo
class UrbanRoutesPage:

    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    tariff_comfort = (By.XPATH, '//div[@class="tariff-cards"]/div[5]')
    number_phone = (By.CSS_SELECTOR, '.np-button')
    add_number_phone = (By.ID, 'phone')
    next_button = (By.CSS_SELECTOR, '.button.full')
    code_number_phone = (By.ID, 'code')
    button_confirm = (By.LINK_TEXT, 'Confirmar')
    pyment_method = (By.CLASS_NAME, 'pp-text')
    add_card = (By.CLASS_NAME, 'pp-plus-container')
    number_card = (By.ID, 'number')
    code_card = (By.ID, 'code')
    add_button = (By.CSS_SELECTOR, '.button.full.disabled')
    message = (By.CLASS_NAME, 'input-container')
    ask_for_blanket = (By.CSS_SELECTOR, '.slider.round')
    add_ice_cream = (By.CLASS_NAME, 'counter-plus')

    # Constructor
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, address_from):
        self.driver.find_element(*self.from_field).send_keys(address_from)

    def set_to(self, address_to):
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_request_taxi_button(self):
        self.driver.find_element(*self.request_taxi_button).click()

    def click_tariff_comfort(self):
        self.driver.find_element(*self.tariff_comfort).click()

    def click_number_phone(self):
         self.driver.find_element(*self.number_phone).click()

    def set_add_number_phone(self, phone_number):
        self.driver.find_element(*self.add_number_phone).send_keys(phone_number)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_code_number_phone(self, code):
        WebDriverWait(self.driver, 63).until(expected_conditions.visibility_of_element_located(self.code_number_phone))
        self.driver.find_element(*self.code_number_phone).send_keys(code)

    def click_button_confirm(self):
        self.driver.find_element(*self.button_confirm).click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        #from selenium.webdriver import DesiredCapabilities
        #capabilities = DesiredCapabilities.CHROME
        #capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        #cls.driver = webdriver.Chrome()

        service = Service('/home/JP/Downloads/WebDriver/bin/chromedriver')
        cls.driver = webdriver.Chrome(service=service)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        self.driver.implicitly_wait(10)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_request_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_request_taxi_button()

    def test_click_tariff_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_tariff_comfort()

    def test_number_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_number_phone()
        routes_page.set_add_number_phone(data.phone_number)
        routes_page.click_next_button()
        code = retrieve_phone_code(driver=self.driver)
        routes_page.set_code_number_phone(code)



    @classmethod
    def teardown_class(cls):
        time.sleep(2)
        cls.driver.quit()
