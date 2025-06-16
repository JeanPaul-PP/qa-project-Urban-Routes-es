from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import data
import helpers

# Clase pagina principal, ingresar direcciones y atributo
class UrbanRoutesPage:

    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, '.button.round')
    tariff_comfort = (By.XPATH, '//div[@class="tariff-cards"]/div[5]')
    number_phone = (By.CSS_SELECTOR, '.np-text')
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
    def click_add_number_phone(self):
        self.driver.find_element(*self.number_phone).click()

    # Guardar numero de telefono
    def save_number(self, phone_number):
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

    def set_ask(self):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.ask_for_blanket)).click()

    def add_ice(self):
        element = self.driver.find_element(*self.add_ice_cream)
        ActionChains(self.driver).double_click(element).perform()