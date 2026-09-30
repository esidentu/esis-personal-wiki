import ollama

DEFAULT_MODEL = "gemma3:4b"


class LocalModel:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self._client = ollama.Client()

    def generate(self, system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
        response = self._client.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            options={"temperature": temperature},
        )
        return response["message"]["content"]

    def chat(self, system_prompt: str, messages: list[dict], temperature: float = 0.7) -> str:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = self._client.chat(
            model=self.model_name,
            messages=full_messages,
            options={"temperature": temperature},
        )
        return response["message"]["content"]

    def is_available(self) -> bool:
        try:
            self._client.list()
            return True
        except Exception:
            return False

    def get_model_info(self) -> dict:
        try:
            info = self._client.show(self.model_name)
            return {
                "name": self.model_name,
                "family": info.get("details", {}).get("family", "unknown"),
                "parameter_size": info.get("details", {}).get("parameter_size", "unknown"),
                "quantization": info.get("details", {}).get("quantization_level", "unknown"),
            }
        except Exception:
            return {"name": self.model_name, "family": "unknown", "parameter_size": "unknown", "quantization": "unknown"}
