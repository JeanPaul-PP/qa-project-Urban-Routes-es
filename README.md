Nombre del Proyecto:
QA Automatizada - Urban Routes

Descripción del Proyecto:
Este proyecto consiste en la automatización de pruebas funcionales para Urban Routes, una plataforma web de solicitud de taxis. A través de la herramienta Selenium, se automatizan las acciones clave del usuario como:

Seleccionar direcciones de origen y destino
Escoger tarifas de viaje
Agregar un metodo de pago
Ingresar número de teléfono y validar el código de confirmación
Personalizar el pedido con mensaje, opciones y confirmación de reserva

El propósito principal es validar el flujo completo de una solicitud de viaje, asegurando la estabilidad de la plataforma y detectando errores funcionales en su interfaz

Tecnologías y Técnicas Utilizadas:

Python 3.13: Lenguaje principal del proyecto.
Selenium WebDriver: Herramienta para automatización de navegadores web.
Pytest: Framework de testing para la ejecución estructurada de pruebas.
Google Chrome + ChromeDriver: Navegador y controlador utilizados para pruebas.
Explicit Waits (WebDriverWait): Sincronización robusta para asegurar que los elementos estén disponibles antes de interactuar con ellos.

Instrucciones para Ejecutar las Pruebas:
1. Instala las dependencias necesarias:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
2. Asegúrate de tener ChromeDriver instalado:
Debes tener chromedriver compatible con tu versión de Google Chrome y ubicado en
3. Prepara el archivo data.py:
Este archivo debe contener los datos necesarios para las pruebas. Ejemplo:
urban_routes_url = "https://urbanroutes.example.com"
address_from = "Av. Siempre Viva 123"
address_to = "Calle Falsa 456"
phone_number = "0999999999"
card_number = "4111111111111111"
card_code = "123"
message_for_driver = "Por favor, traer manta y 2 helados"
4. Ejecuta los tests:
Desde tu terminal o PyCharm.

