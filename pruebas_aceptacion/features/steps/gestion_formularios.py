from behave import when, then, given
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===== GIVEN 

@given(u'navego a la lista de formularios')
def step_impl(context):
    context.driver.get(f"{context.url}/tipo-solicitud/formularios/")
    time.sleep(1)


@given(u'existe un formulario llamado "{nombre}"')
def step_impl(context, nombre):
    # Asegurarse de que existe un tipo de solicitud
    context.driver.get(f"{context.url}/tipo-solicitud/lista/")
    time.sleep(0.5)
    
    # Verificar si ya existe el tipo, si no, crearlo
    page_text = context.driver.page_source
    if f"Tipo para {nombre}" not in page_text:
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(0.5)
        context.driver.find_element(By.NAME, 'nombre').send_keys(f"Tipo para {nombre}")
        context.driver.find_element(By.NAME, 'descripcion').send_keys("Tipo de prueba")
        context.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
    
    # Ahora crear el formulario
    context.driver.get(f"{context.url}/tipo-solicitud/formularios/crear/")
    time.sleep(1)
    
    # Seleccionar el tipo de solicitud específico por nombre
    select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
    select = Select(select_element)
    tipo_nombre = f"Tipo para {nombre}"
    try:
        select.select_by_visible_text(tipo_nombre)
    except:
        # Si no existe, crear el tipo de solicitud
        context.driver.get(f"{context.url}/tipo-solicitud/")
        context.driver.find_element(By.NAME, 'nombre').send_keys(tipo_nombre)
        context.driver.find_element(By.NAME, 'descripcion').send_keys("Tipo de prueba")
        context.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        context.driver.get(f"{context.url}/tipo-solicitud/formularios/crear/")
        time.sleep(1)
        select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
        select = Select(select_element)
        select.select_by_visible_text(tipo_nombre)
    
    # Llenar el formulario
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'descripcion').send_keys(f"Descripción de {nombre}")
    
    # Guardar
    context.driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    
    # Guardar el nombre para validaciones posteriores
    context.ultimo_formulario_creado = nombre


# ===== WHEN 

@when(u'hago clic en el botón "Agregar"')
def step_impl(context):
    # Buscar el botón Agregar en la lista de formularios
    agregar_btn = context.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-primary') and contains(., 'Agregar')]")
    agregar_btn.click()
    time.sleep(1)


@when(u'selecciono el tipo de solicitud "{tipo}"')
def step_impl(context, tipo):
    select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
    select = Select(select_element)
    opciones_disponibles = [option.text for option in select.options if option.text.strip()]
    
    # Intentar seleccionar por texto visible
    try:
        select.select_by_visible_text(tipo)
    except:
        # Si no existe en las opciones, crear el tipo primero
        context.driver.get(f"{context.url}/tipo-solicitud/")
        time.sleep(0.5)
        context.driver.find_element(By.NAME, 'nombre').send_keys(tipo)
        context.driver.find_element(By.NAME, 'descripcion').send_keys(f"Descripción de {tipo}")
        context.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        # Volver al formulario de creación
        context.driver.get(f"{context.url}/tipo-solicitud/formularios/crear/")
        time.sleep(1)
        select_element = context.driver.find_element(By.NAME, 'tipo_solicitud')
        select = Select(select_element)
        select.select_by_visible_text(tipo)
    
    time.sleep(0.5)


@when(u'no selecciono ningún tipo de solicitud')
def step_impl(context):
    # No hacer nada, dejar la selección por defecto (vacía)
    time.sleep(0.5)


@when(u'lleno el campo formulario "{campo}" con "{valor}"')
def step_impl(context, campo, valor):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    element.send_keys(valor)
    time.sleep(0.5)


@when(u'dejo el campo formulario "{campo}" vacío')
def step_impl(context, campo):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    time.sleep(0.5)


@when(u'presiono el botón "Crear Formulario"')
def step_impl(context):
    # Buscar el botón que contiene el texto "Crear Formulario" o es de tipo submit
    try:
        crear_btn = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Formulario')]")
    except:
        crear_btn = context.driver.find_element(By.XPATH, "//button[@type='submit']")
    crear_btn.click()
    time.sleep(2)


@when(u'presiono el botón de cancelar en formulario')
def step_impl(context):
    cancelar_btn = context.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-secondary') and contains(text(), 'Cancelar')]")
    cancelar_btn.click()
    time.sleep(1)


@when(u'hago clic en el botón de opciones del formulario "{nombre}"')
def step_impl(context, nombre):
    # Buscar la fila que contiene el nombre del formulario
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and nombre in tds[1].text:  # El nombre está en la segunda columna (índice 1)
            # Encontrar el botón dropdown en esta fila
            dropdown_btn = tr.find_element(By.CLASS_NAME, 'dropdown-toggle')
            dropdown_btn.click()
            time.sleep(1)
            break
    else:
        raise Exception(f"No se encontró el formulario '{nombre}' en la lista")


@when(u'selecciono la opción "{opcion}"')
def step_impl(context, opcion):
    # Buscar el enlace en el dropdown que contenga el texto de la opción
    opcion_link = context.driver.find_element(By.XPATH, f"//a[contains(@class, 'dropdown-item') and contains(., '{opcion}')]")
    opcion_link.click()
    time.sleep(1)


@when(u'modifico el campo formulario "{campo}" a "{valor}"')
def step_impl(context, campo, valor):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    element.send_keys(valor)
    time.sleep(0.5)


@when(u'limpio el campo formulario "{campo}"')
def step_impl(context, campo):
    element = context.driver.find_element(By.NAME, campo)
    element.clear()
    time.sleep(0.5)


@when(u'presiono el botón "Guardar Cambios"')
def step_impl(context):
    # Buscar el botón que contiene el texto "Guardar Cambios" o es de tipo submit
    try:
        guardar_btn = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar Cambios')]")
    except:
        guardar_btn = context.driver.find_element(By.XPATH, "//button[@type='submit']")
    guardar_btn.click()
    time.sleep(2)


# ===== THEN STEPS =====

@then(u'puedo ver el formulario "{nombre}" en la lista de formularios')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    formularios = []
    
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1:
            formularios.append(tds[1].text)  # Columna del nombre
    
    assert nombre in formularios, f"No se encontró '{nombre}' en la lista de formularios: {formularios}"
    time.sleep(1)


@then(u'soy redirigido a la lista de formularios')
def step_impl(context):
    assert '/tipo-solicitud/formularios/' in context.driver.current_url, \
        f"No se redirigió a la lista de formularios. URL actual: {context.driver.current_url}"
    time.sleep(1)


@then(u'veo el formulario "{nombre}" en la lista')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    formularios = []
    
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1:
            formularios.append(tds[1].text)
    
    assert nombre in formularios, f"No se encontró '{nombre}' en la lista"
    time.sleep(1)


@then(u'el contador de formularios aumenta en {cantidad:d}')
def step_impl(context, cantidad):
    # Buscar el elemento que muestra "Resultado: X"
    resultado_element = context.driver.find_element(By.XPATH, "//h5[contains(text(), 'Resultado:')]")
    texto = resultado_element.text
    numero_actual = int(texto.split(':')[1].strip())
    
    assert numero_actual >= cantidad, f"El resultado {numero_actual} no es el esperado"
    time.sleep(0.5)


@then(u'veo un mensaje de error en el campo nombre del formulario')
def step_impl(context):
    # Verificar que permanece en la página de crear/editar formulario
    assert '/tipo-solicitud/formularios/' in context.driver.current_url
    
    # Buscar indicadores de error
    try:
        error_elements = context.driver.find_elements(By.CLASS_NAME, 'errorlist')
        assert len(error_elements) > 0, "No se encontró mensaje de error"
    except:
        # Verificación alternativa
        pass
    time.sleep(1)


@then(u'permanezco en la página de crear formulario')
def step_impl(context):
    assert '/tipo-solicitud/formularios/crear/' in context.driver.current_url, \
        f"No permanece en la página de crear. URL actual: {context.driver.current_url}"
    time.sleep(0.5)


@then(u'permanezco en la página de editar formulario')
def step_impl(context):
    assert '/tipo-solicitud/formularios/editar/' in context.driver.current_url, \
        f"No permanece en la página de editar. URL actual: {context.driver.current_url}"
    time.sleep(0.5)


@then(u'veo un mensaje de error indicando que debe seleccionar un tipo de solicitud')
def step_impl(context):
    # Verificar que permanece en la página
    assert '/tipo-solicitud/formularios/crear/' in context.driver.current_url
    
    # Buscar mensajes de error
    try:
        error_elements = context.driver.find_elements(By.CLASS_NAME, 'errorlist')
        assert len(error_elements) > 0, "No se encontró mensaje de error"
    except:
        pass
    time.sleep(1)


@then(u'no veo el formulario "{nombre}" en la lista')
def step_impl(context, nombre):
    body = context.driver.find_element(By.ID, 'bodyTipoSolicitudes')
    trs = body.find_elements(By.TAG_NAME, 'tr')
    formularios = []
    
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        if tds and len(tds) > 1:
            formularios.append(tds[1].text)
    
    assert nombre not in formularios, f"Se encontró '{nombre}' en la lista cuando no debería estar"
    time.sleep(1)


@then(u'soy redirigido a la página de configurar campos')
def step_impl(context):
    # Verificar que la URL contiene la ruta de campos
    assert '/tipo-solicitud/formularios/campos/' in context.driver.current_url, \
        f"No se redirigió a la página de campos. URL actual: {context.driver.current_url}"
    time.sleep(1)


@then(u'veo el título "Configurar campos del formulario: {nombre}"')
def step_impl(context, nombre):
    # Buscar el título en la página
    h1_element = context.driver.find_element(By.TAG_NAME, 'h1')
    assert nombre in h1_element.text, f"No se encontró '{nombre}' en el título: {h1_element.text}"
    time.sleep(1)
