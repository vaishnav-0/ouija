from litellm import completion


class Mistral:
    def __init__(self, ghost, model="ollama/mistral:7b-instruct"):
        with open(ghost) as f:
            self.system_prompt = f.read()
            self.system_prompt += ("Your responses should be cryptic, chilling, and limited to characters found on a "
                                   "traditional Ouija board (letters A-Z, numbers 0-9, 'Yes', 'No', and 'Goodbye')")

        self.model = model
        self.messages = [
            {"content": self.system_prompt, "role": "system"}
        ]

    def __call__(self, question, **kwargs):
        self.messages.append({"content": question, "role": "user"})
        answer = completion(
            model=self.model,
            messages=self.messages,
            api_base="http://localhost:11434"
        )

        text = answer["choices"][0].message.content
        agent = answer["choices"][0].message.role

        self.messages.append({"content": text, "role": agent})

        return text


if __name__ == '__main__':
    mistral = Mistral("ghosts/1.txt")

    while True:
        question = input("Question: ")
        answer = mistral(question)
        print(answer)
