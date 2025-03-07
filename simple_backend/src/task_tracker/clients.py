import abc
import requests

class BaseHTTPClient(abc.ABC):
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers or {}

    def post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    @abc.abstractmethod
    def process_response(self, response: dict) -> dict:
        """
        Абстрактный метод для обработки ответа.
        """
        pass

class LLMClient(BaseHTTPClient):
    def __init__(self, api_key: str):
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        super().__init__(base_url="https://api.cloudflare.com/client/v4/llm/", headers=headers)

    def process_response(self, response: dict) -> dict:
        return {"explanation": response.get("explanation", "Нет пояснения")}

    def get_task_solution(self, task_text: str) -> str:
        payload = {
            "prompt": f"Объясни, как решить задачу: {task_text}",
            "model": "example-model"
        }
        response = self.post("explain", data=payload)
        processed = self.process_response(response)
        return processed.get("explanation", "")