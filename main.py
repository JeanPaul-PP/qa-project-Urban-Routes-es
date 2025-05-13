import time
from sys import executable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

# Clase pagina principal, ingresar direcciones y atributo
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
    button_confirm = (By.XPATH, '//*[contains(text(), "Confirmar")]')
    pyment_method = (By.CLASS_NAME, 'pp-text')
    add_card = (By.CLASS_NAME, 'pp-plus-container')
    number_card = (By.ID, 'number')
    code_card = (By.NAME, 'code')
    click = (By.CSS_SELECTOR, '.plc')
    click_add = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    add_button = (By.XPATH, '//button[contains(text(), "Agregar")]')
    message = (By.ID, 'comment')
    ask_for_blanket = (By.CSS_SELECTOR, '.slider.round')
    add_ice_cream = (By.CLASS_NAME, 'counter-plus')
    reserver = (By.CSS_SELECTOR, '.smart-button')

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

    # Pedir un taxi y seleciccionar Tarifa Comfort
    def click_tariff_comfort(self):
        self.driver.find_element(*self.request_taxi_button).click()
        self.driver.find_element(*self.tariff_comfort).click()

    # Agregar numero de telefono
    def set_add_number_phone(self, phone_number):
        self.driver.find_element(*self.number_phone).click()
        self.driver.find_element(*self.add_number_phone).send_keys(phone_number)
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.next_button)).click()

    # Ingresar numero de confirmacion
    def set_code_number_phone(self, code):
        self.driver.find_element(*self.code_number_phone).send_keys(code)
        self.driver.find_element(*self.button_confirm).click()

    # Seleccionar metodo de pago
    def set_pyment_method(self):
        self.driver.find_element(*self.pyment_method).click()
        self.driver.find_element(*self.add_card).click()

    # Agregar numero de tarjeta
    def set_add_card(self, card_number):
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.number_card)).send_keys(card_number)

    # Agregar codigo de tarjeta
    def set_code_card(self, card_code):
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.code_card)).send_keys(card_code)
        self.driver.find_element(*self.click).click()
        self.driver.find_element(*self.add_button).click()
        self.driver.find_element(*self.click_add).click()

    # Mensaje y Requisitos del pedido
    def set_message(self, message_for_driver):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.message)).send_keys(message_for_driver)
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.ask_for_blanket)).click()
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.add_ice_cream)).click()
        WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(self.add_ice_cream)).click()
        self.driver.find_element(*self.reserver).click()

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
        service = Service('/home/JP/Downloads/WebDriver/bin/chromedriver')

        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()


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
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_tariff_comfort()

    def test_number_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_add_number_phone(data.phone_number)
        code = retrieve_phone_code(self.driver)
        routes_page.set_code_number_phone(code)

    def test_set_pyment_method(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_pyment_method()

    def test_set_add_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_add_card(data.card_number)

    def test_set_code_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_code_card(data.card_code)

    def test_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message(data.message_for_driver)



    @classmethod
    def teardown_class(cls):
        time.sleep(30)
        cls.driver.quit()
