from http.client import responses
import pytest
#import allure
import requests
import uuid

#define la url base donde esta corriendo la api localmente con uvicorn
BASE_URL = "http://127.0.0.1:8000"


def test_create_user():
    data = {
        "name": "test user",
        "email": "test@example.com",
        "age": 25
    }
    #f significa formatted string literal es la forma en que python crea lo que se llama un f-string similar a .format() pero mas rapido
    response = requests.post(f"{BASE_URL}/users",json=data)
    assert response.status_code in (200,201)
    result = response.json() # Convierte la respuesta (que viene en formato JSON) a un diccionario de Python.
    assert result["name"] == data["name"]
    assert result["email"] == data["email"]
    assert result["age"] == data["age"]
    assert "id" in result




def test_get_user():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code ==200
    assert isinstance(response.json(),list)




def test_update_user():
    #primero creamos el usuario
    data = {
        "name": "update test",
        "email": "update@example.com",
        "age": 23
    }
    post_response = requests.post(f"{BASE_URL}/users",json=data)
    user_id = post_response.json()["id"]

    #luego actualizamos

    update_data ={
        "name": "Updated User",
        "email": "updated@example.com",
        "age": 35
    }

    put_response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    assert put_response.status_code == 200
    result = put_response.json()
    assert result["name"] == update_data ["name"]
    assert result["email"] == update_data["email"]
    assert result["age"] == update_data["age"]




def test_delete_user():
    #crear usuario a eliminar

    data = {
        "name": "Delete Me",
        "email": "deleteme@example.com",
        "age": 99
    }

    post_response = requests.post(f"{BASE_URL}/users",json=data)
    user_id = post_response.json()["id"]

    #eliminar usuario
    delete_response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert delete_response.status_code == 204


    #verificar que ya no existe
    get_response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert get_response.status_code == 404


def test_cuatro():
    print("demo cuatro")
