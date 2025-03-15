from hw2menti.simple_backend.src.task_tracker.models import BaseHTTPClient


class CloudflareAI(BaseHTTPClient):
    def __init__(self, api_url: str, api_key: str):
        super().__init__(api_url, api_key)

    def process_request(self, task_text: str) -> str:
        payload = {
            "model": "mistral",  # Или другая модель
            "messages": [
                {"role": "system", "content": "Ты помощник для решения задач."},
                {"role": "user", "content": f"Как решить задачу? {task_text}"},
            ],
        }

        response = self._send_request("POST", "", payload)
        return response.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа")