
import pytest
import requests
import allure

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    """Фикстура для создания питомца"""
    with allure.step("Создание питомца через фикстуру"):
        payload = {
            "id": 1,
            "name": "Buddy",
            "status": "available"
        }
        response = requests.post(url=f"{BASE_URL}/pet", json=payload)
        assert response.status_code == 200
        return response.json()

@pytest.fixture(scope="function")
def update_pet():
    """Фикстура для обновления питомца"""
    with allure.step("Подготовка данных для обновления питомца в фикстуре"):
        payload = {
            "id": 12,
            "name": "Buddy Updated",
            "status": "sold"
        }
    return payload

@pytest.fixture(scope="function")
def delete_pet():
    """Фикстура для удаления питомца"""
    def _delete_pet(pet_id):
        with allure.step(f"Удаление питомца с ID {pet_id}"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            return response
    return _delete_pet


