from behave import when, then, given
from selenium.webdriver.common.by import By
import time

@given(u'que ingreso al sistema')
def step_impl(context):
    context.driver.get(context.url)


@given(u'seleccion el menú Tipo de solicitudes')
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, 'Tipo solicitudes').click()
    time.sleep(1)


@given(u'escribo en la caja de texto nombre "{nombre}" y en la descripción "{descripcion}"')
def step_impl(context, nombre, descripcion):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'descripcion').send_keys(descripcion)
    time.sleep(1)



@when(u'presiono el botón Agregar')
def step_impl(context):
    context.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    time.sleep(1)



@then(u'puedo ver el tipo "{nombre}" en la lista de tipos de solicitudes.')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    tipo_solicitud = []
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        tipo_solicitud.append(tds[0].text)
    assert nombre in tipo_solicitud, f"{str(tipo_solicitud)}"
    time.sleep(10)


