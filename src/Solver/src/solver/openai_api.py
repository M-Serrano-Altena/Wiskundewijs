

from openai import OpenAI
"""
This module provides an interface to interact with the OpenAI API for generating explanations and answering questions
related to mathematical problems. It defines a `ChatGPT` class that encapsulates the functionality to manage 
explanation and question contexts, interact with the OpenAI API, and process responses.
Classes:
    ChatGPT: A class to interact with the OpenAI API for generating explanations and answering questions.
Functions:
    change_dir(func): A decorator to change the working directory to the directory of the current file before executing 
                      the decorated function and revert back to the original directory after execution.
    add_explanation_context(self): Adds the context for explanations by reading prompt files from the 'openai_prompts/explanation' directory.
    get_explanation(self, solution_solver): Sends a request to the OpenAI API to get an explanation for the provided solution solver.
    add_questions_context(self): Adds the context for questions by reading prompt files from the 'openai_prompts/questions' directory.
    add_user_input(self, message): Adds a user input message to the question context.
    add_chatgpt_reply(self, message): Adds a ChatGPT reply message to the question context.
    reply_to_question(self, user_question): Sends a request to the OpenAI API to get a reply for the provided user question.
    reset_chatgpt(self): Resets the question context to its initial state.
    amt_questions_asked(self): Returns the number of questions asked so far.
"""
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

class ChatGPT():
    """
    A class to interact with OpenAI's GPT model for generating explanations and answering questions.
    Attributes:
    -----------
    current_path : str
        The current working directory.
    openai_api_path : str
        The directory path where the OpenAI API related files are located.
    _explanation_messages : list
        A list to store messages related to explanations.
    _question_messages : list
        A list to store messages related to questions.
    Methods:
    --------
    change_dir(func):
        A decorator to change the working directory to the OpenAI API path before executing a function and revert back after execution.
    add_explanation_context():
        Adds the context for explanations by reading from predefined prompt files.
    get_explanation(solution_solver):
        Generates an explanation for a given solution using the GPT model.
    add_questions_context():
        Adds the context for questions by reading from predefined prompt files.
    add_user_input(message):
        Adds a user input message to the question messages.
    add_chatgpt_reply(message):
        Adds a ChatGPT reply message to the question messages.
    reply_to_question(user_question):
        Generates a reply to a user's question using the GPT model.
    reset_chatgpt():
        Resets the question messages and reinitializes the context.
    amt_questions_asked():
        Returns the number of questions asked by the user.
    """
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
        """
        A decorator to temporarily change the working directory to the OpenAI API path 
        while executing the decorated function, and then revert back to the original path.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The wrapped function with directory change functionality.
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            os.chdir(self.openai_api_path)
            result = func(self, *args, **kwargs)
            os.chdir(self.current_path)
            return result
        return wrapper
    
    @change_dir
    def add_explanation_context(self):
        """
        Adds explanation context to the OpenAI API interaction.
        This method changes the current working directory to the specified OpenAI API path,
        reads the explanation prompt and example question-answer pairs from the 'openai_prompts/explanation' directory,
        and appends them to the `_explanation_messages` list with appropriate roles ('system', 'user', 'assistant').
        Finally, it reverts the working directory to the original path.
        Raises:
            FileNotFoundError: If any of the required files are not found in the specified directory.
            IOError: If there is an error reading any of the files.
        """
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
        """
        Generates an explanation for the given solution using the OpenAI API.
        Args:
            solution_solver (str): The solution for which an explanation is needed.
        Returns:
            str: The explanation generated by the OpenAI API.
        Raises:
            OpenAIError: If there is an error in the API request.
        """
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
        """
        Adds the context for question answering to the internal message list.

        This function reads the content of the "question_answerer_prompt.txt" file 
        located in the "openai_prompts/questions" directory and appends it to the 
        `_question_messages` list as a dictionary with the role set to "system" 
        and the content set to the file's content.

        Raises:
            FileNotFoundError: If the "question_answerer_prompt.txt" file does not exist.
            IOError: If there is an error reading the file.
        """
        directory = os.path.join("openai_prompts", "questions")
        with open(os.path.join(directory, "question_answerer_prompt.txt")) as file:
            self._question_messages.append({"role": "system", "content": file.read()})

    def add_user_input(self, message):
        """
        Adds a user input message to the list of question messages.

        Args:
            message (str): The user input message to be added.
        """
        self._question_messages.append({"role": "user", "content": message})

    def add_chatgpt_reply(self, message):
        """
        Adds a reply from ChatGPT to the list of question messages.

        Args:
            message (str): The reply message from ChatGPT to be added.
        """
        self._question_messages.append({"role": "assistant", "content": message})

    def reply_to_question(self, user_question):
        """
        Generates a reply to the user's question using the OpenAI API.
        This method sends the user's question to the OpenAI API and processes the response.
        The response is expected to be in a JSON schema format with a specific structure.
        Args:
            user_question (str): The question posed by the user.
        Returns:
            str: The reply generated by the OpenAI API.
        """
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
        """
        Resets the ChatGPT conversation by clearing the list of question messages
        and re-adding the initial context for questions.

        This method is useful for starting a new conversation or clearing the
        current state of the conversation.
        """
        self._question_messages = []
        self.add_questions_context()

    def amt_questions_asked(self):
        """
        Calculate the number of questions asked based on the length of the question messages.

        This method computes the number of questions asked by taking the length of the 
        `_question_messages` list, subtracting 2, and then performing integer division by 2. 
        The result is then compared with 0, and the maximum value between the computed result 
        and 0 is returned.

        Returns:
            int: The number of questions asked, ensuring a non-negative result.
        """
        return max(0, (len(self._question_messages) - 2) // 2)


if __name__ == "__main__":
    # Testing with an example question
    question = "{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}"
    chatgpt = ChatGPT()
    result = chatgpt.get_explanation(question) 
    print(chatgpt._explanation_messages)
    print()
    print(result)