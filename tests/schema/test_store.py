import allure
import requests
import pytest


BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_placing_an_order(self):


        with allure.step("Отправка запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200


        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId питомца не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Получение ID заказа"):
            orderId = 1

        with allure.step("Отправка запроса на получение данных о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{orderId}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response_json['id'] == orderId

    @allure.title("Удаление заказа по id")
    def test_delete_info_order(self):
        with allure.step("Получение ID заказа"):
            orderId = 1

        with allure.step(f"Удаление заказа с ID {orderId}"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{orderId}")

        with allure.step("Проверка статуса ответа: 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Отправить GET-запрос на /store/order/{orderId} для проверки удаления"):
            get_response = requests.get(url=f"{BASE_URL}/store/order/{orderId}")

        with allure.step("Проверка статуса ответа: 404"):
            assert get_response.status_code == 404, f"Ожидался статус 404, получен {get_response.status_code}"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение данных несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпадает с ожидаемым"



    @allure.title("Получение инвентаря в магазине")
    def test_get_inventory_store(self):
        with allure.step("Отправка запроса на получение инвентаря в магазине"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпадает с ожидаемым"

        with allure.step("Проверка точного соответствия инвентаря"):
            expected_inventory = {"approved": 57, "delivered": 50}

            assert response_json == expected_inventory, f"Инвентарь не соответствует ожидаемому. Ожидалось: {expected_inventory}, получено: {response_json}"










