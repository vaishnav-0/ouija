import json

import requests

from constants import BASE_PROMPT


class Mistral:
    def __init__(self, ghost):
        with open(ghost) as f:
            self.system_prompt = f.read()
            self.system_prompt += BASE_PROMPT

        self.url = 'http://localhost:1234/v1/chat/completions'
        self.headers = {'Content-Type': 'application/json'}
        self.data = {
            "messages": [],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }

        self.messages = [
            {"content": self.system_prompt, "role": "system"}
        ]

    def _api_call(self):
        data = self.data
        data["messages"] = self.messages
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        return response.json()["choices"][0]["message"]

    def __call__(self, question, **kwargs):
        self.messages.append({"content": question, "role": "user"})
        answer = self._api_call()

        text = answer["content"].split("\n")[0]
        agent = answer["role"]

        if ":" in text:
            text = text.split(":")[-1]

        if len(text.split(" ")) > 2:
            text = " ".join(text.split(" ")[:2])

        text = text.strip()

        if text == "":
            text = "No"

        self.messages.append({"content": text, "role": agent})

        return text


if __name__ == '__main__':
    mistral = Mistral("ghosts/Caligula.txt")

    while True:
        q = input("Question: ")
        a = mistral(q)
        print("Answer:", a)
