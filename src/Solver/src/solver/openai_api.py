from openai import OpenAI
import json
import os
from functools import wraps

try:
    with open('/etc/config.json') as config_file:
        config = json.load(config_file)

    OPENAI_API_KEY = config['OPENAI_API_KEY']
except FileNotFoundError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

question_answerer_prompt = r'''
You are a knowledgeable Dutch math tutor, here to help students with their questions regarding mathematical concepts and problems. 

When responding, you should:
1. **Contextualize the Explanation**: Use the provided explanation as a foundation for your answer. Reference specific parts of the explanation when relevant.
2. **Clarify User Questions**: If the user's question is unclear, ask for clarification. Ensure that you understand what the user is asking before providing a detailed answer.
3. **Provide Examples**: Whenever applicable, include relevant examples to illustrate your points. This helps in better understanding of the concepts.
4. **Maintain a Friendly Tone**: Your language should be friendly and approachable, suitable for a third-grader. Avoid jargon unless it's clearly explained.
5. **Encourage Further Questions**: End your responses by encouraging the user to ask more questions if they need further clarification or assistance.
6. **Properly Format Answer**: When providing the outcome of each step, use '\\[' and '\\]' for display math notation and '\\(' and '\\)' for inline math notation. For example if you use '2x + 3' in the explanation, you should write '\\(2x + 3\\)'.

Remember to be patient and clear in your explanations, as some concepts may be challenging for younger learners.
'''

class ChatGPT():
    def __init__(self, previous_explanation=None):
        self.current_path = os.getcwd()
        self.openai_api_path = os.path.dirname(__file__)        
        self._explanation_messages = []
        self.add_explanation_context()
        
        self._question_messages = []
        self.add_questions_context()
        if previous_explanation:
            self.add_user_input(previous_explanation)


    def change_dir(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            os.chdir(self.openai_api_path)
            result = func(self, *args, **kwargs)
            os.chdir(self.current_path)
            return result
        return wrapper
    
    @change_dir
    def add_explanation_context(self):
        os.chdir(self.openai_api_path)

        directory = os.path.join("openai_prompts", "explanation")
        with open(os.path.join(directory, "explanation_prompt.txt")) as file:
            self._explanation_messages.append({"role": "system", "content": file.read()})

        for i in range(1, len(os.listdir(directory)) // 2 + 1):
            question_answer_pair = (f"example_question{i}.txt", f"example_answer{i}.txt")
            for j, filename in enumerate(question_answer_pair):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as file:
                    explanation = file.read()

                self._explanation_messages.append({"role": "user" if j == 0 else "assistant" , "content": explanation})

        os.chdir(self.current_path)

    def get_explanation(self, solution_solver):
        self._explanation_messages.append({"role": "user", "content": solution_solver})

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=self._explanation_messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "math_reasoning",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": r"string"},
                                    "output": {"type": "string"}
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False
                            }
                        },
                        "final_answer": {"type": "string"}
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
        )

        reply = response.choices[0].message.content
        return reply
    
    @change_dir
    def add_questions_context(self):
        directory = os.path.join("openai_prompts", "questions")
        with open(os.path.join(directory, "question_answerer_prompt.txt")) as file:
            self._question_messages.append({"role": "system", "content": file.read()})

    def add_user_input(self, message):
        self._question_messages.append({"role": "user", "content": message})

    def add_chatgpt_reply(self, message):
        self._question_messages.append({"role": "assistant", "content": message})

    def reply_to_question(self, user_question):
        self.add_user_input(user_question)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self._question_messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "math_reasoning_reply",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "response": {"type": "string"}  # Structure to capture the reply
                        },
                        "required": ["response"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )

        reply = response.choices[0].message.content
        self.add_chatgpt_reply(reply)

        return reply
    
    def reset_chatgpt(self):
        self._question_messages = []
        self.add_questions_context()

    def amt_questions_asked(self):
        return max(0, (len(self._question_messages) - 2) // 2)


if __name__ == "__main__":
    # Testing with an example question
    question = "{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}"
    chatgpt = ChatGPT()
    result = chatgpt.get_explanation(question) 
    print(chatgpt._explanation_messages)
    print()
    print(result)