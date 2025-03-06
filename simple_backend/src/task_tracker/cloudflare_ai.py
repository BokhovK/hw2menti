import requests

class CloudflareAI:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate_solution(self, task_text: str) -> str:
        """
        Отправляет текст задачи в LLM модель Cloudflare и получает ответ.
        """
        payload = {
            "model": "mistral",  
            "messages": [
                {"role": "system", "content": "Ты помощник для решения задач."},
                {"role": "user", "content": f"Как решить следующую задачу? {task_text}"},
            ],
        }

        response = requests.post(self.api_url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Нет решения")
        else:
            return "Ошибка при генерации решения"
            