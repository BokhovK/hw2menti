import abc
import requests

class BaseHTTPClient(abc.ABC):
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers or {}

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
            url = f"{self.base_url}{endpoint}"
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response.json()

    def post(self, endpoint: str, data: dict) -> dict:
        return self._request('POST', endpoint, data=data)

    def get(self, endpoint: str) -> dict:
        return self._request('GET', endpoint)

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