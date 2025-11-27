import allure
import jsonschema
import requests

from tests.schema.conftest import create_pet
from tests.schema.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпадает с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпадает с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемыми"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания нового питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload ['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_adding_full_pet_data(self):
        with allure.step("Подготовка данных для создания нового питомца с полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "category питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "tags питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение данных о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response_json['id'] == pet_id


    @allure.title("Обновление информации о питомце")
    def test_update_info_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id":pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response_json['id'] == pet_id
            assert response_json['name'] == "Buddy Updated"
            assert response_json['status'] == "sold"

    @allure.title("Удаление питомца по id")
    def test_delete_info_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step(f"Удаление питомца с ID {pet_id}"):
           response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа: 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Отправить GET-запрос на /pet/{petId} для проверки удаления"):
            get_response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа: 404"):
            assert get_response.status_code == 404, f"Ожидался статус 404, получен {get_response.status_code}"



