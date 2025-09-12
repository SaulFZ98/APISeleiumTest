from unittest import expectedFailure

import  pytest # utilizado para ejecutar pruebas
import allure # utilizado para el reporte e ingresar metadatos
import requests # para hacer peticiones HTTp a la API
import uuid #para generar identificadores aleatorios


BASE_URL = "http://127.0.0.1:8000" # definimos la URL de la API de FastApi con uvicorn


@allure.feature("User Management - Negative") # este decorador define una categoria principal o funcionalidad de alti nivel a la que pertenece la prueba y en el reporte de allure agrupara todas las pruebas de esta categoria
@allure.story("Create user with invalid data") # este decorador define una historia especifica de usuario o caso de uso dentro del fearure, en el reporte tambien permite agrupar varias pruebas que prueben el mismo comportamiento
@allure.tag("negative")
@allure.severity(allure.severity_level.NORMAL) # asigna el nivel de severidad o prioridad de la prueba y en allure te permite filtrar por severidad, normal= error funcional comun, blocker= bloquea la app completamente si falla, critical= afecta funcionalidad clave, minor=detalle o fallo poco grave, TRIVIAL=visual texto.etc
# es un decorador de pytest utlizamos parametrize porque permite ejecutar la misma prueba multiples veces con diferentes datos de entrada sin tener que escribir funciones separadas ,pasandole una lista de diccionarios (data) que representa los distintos escenarios
@pytest.mark.parametrize("data,expected_field",[
    ({"email": "x@example.com", "age": 30}, "name"),
    ({"name": "Test User", "age": 30}, "email"),
    ({"name": "Test User", "email": "test@example.com"}, "age"),
])

def test_create_user_invalid_input(data, expected_field): # se llama todas las entradas de data
    response = requests.post(f"{BASE_URL}/users",json=data)
    assert response.status_code == 422   # 422 es unprocessable entity es la respuesta esperada cuando FastAPi no puede validar los datos por errores en el esquema gracias a pydantic
    error = response.json() #convierte la respuesta en un diccionario de python
    assert any(expected_field in str(item["loc"]) for item in error["detail"]) #detail es una lista de errores donde cada error es un diccionario con : loc=la ubicacion del error ejemplo ("body","name"), msg:mensaje del error, type: tipo de error
    #for item in error["detail"] estamos iterando sobre todos los errores devueltos
    #item["loc"] es una lista como ["body,"name"] al hacer str(item["loc"]) se convierte en un string "['body', 'name']" Esto facilita hacer búsquedas por texto (como "name" in ...") sin tener que comparar listas.
    #expected_field in str(item["loc"]) Esto verifica si el campo esperado (por ejemplo "name") está en la ubicación del error.
    #any devuelve true si al menos una de las iteraciones devuelve true

@allure.feature("User Management - Negative")
@allure.story("Update non-existent user")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative")
def test_update_non_existent_user():
    fake_id = str(uuid.uuid4()) # genera IDs aleatorios
    update_data = {
        "name": "update",
        "email": "update@test.com",
        "age": 25
    }
    response = requests.put(f"{BASE_URL}/users{fake_id}",json=update_data)
    assert response.status_code == 404




@allure.feature("User Management - Negative")
@allure.story("Delete non-existent user")
@allure.tag("negative")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_non_exitent_user():
    fake_id = str(uuid.uuid4())
    response = requests.delete(f"{BASE_URL}/users/{fake_id}")
    assert response.status_code == 404

