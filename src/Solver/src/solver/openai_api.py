from openai import OpenAI

client = OpenAI()

math_tutor_prompt = r'''
You are a helpful dutch math tutor. You will be given a math equation via a Python dictionary. It contains the equation and the final answer, and your goal is to work step-by-step towards the solution. You will ultimately arrive at the same final answer as provided.
For each step, provide only the outcome as an equation and use the explanation field to clarify the reasoning in dutch. You use language suitable for a dutch third-grader and explain the steps as clearly as possible. 
When providing the outcome of each step, use '\\[' and '\\]' for display math notation and '\\(' and '\\)' for inline math notation. For example, if the outcome of a step is '2x + 3 = 7', you should write '\\[2x + 3 = 7\\]'. If in the explanation you use '2x + 3', you should write '\\(2x + 3\\)'.
The final answer should be boxed. So if the final answer is 'x = 5', you should write '\\[\\boxed{x = 5}\\]'. If you have multiple solutions, you should format them as '\\[\\boxed{1) \\quad x = 1}\\]<br>\\[\\boxed{2) \\quad x = -1}\\]'. Always use double slashes: \\ instead of a single slash: \. Also use double slashes when using commands like \\text
'''

example_question1 = r'''
{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}
'''

example_answer1 = r'''
{
    "steps": [
        {
            "explanation": "We beginnen beginnen met de volgende vergelijking:",
            "output": "\\[3x - 7 = 5x + 3\\]"
        },
        {
            "explanation": "We doen eerst aan beide kanten van de vergelijking \\(-5x\\) om alle \\(x\\) termen naar links te halen:",
            "output": "\\[-2x - 7 = 3\\]"
        },
        {
            "explanation": "Nu doen we aan beide kanten van de vergelijking \\(+7\\) om alle getallen rechts te krijgen:",
            "output": "\\[-2x = 10\\]"
        },
        {
            "explanation": "En nu kunnen we beide kanten delen door \\(-2\\). We vinden dan:",
            "output": "\\[x = -5\\]"
        }
    ],
    "final_answer": "\\[\\boxed{x = -5}\\]"
}
'''

example_question2 = r'''
{'equation_text': 'x^2 - 6x + 12 = -x^2 + 8', 'equation_interpret': 'x^2 - 6*x + 12 = -x^2 + 8', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), 'x^{2} - 6 x + 12 = 8 - x^{2}', ('De oplossingen zijn:', {'latex': False}), '1) \\quad x = 1', '2) \\quad x = 2']}
'''

example_answer1 = r'''
{
    "steps": [
        {
            "explanation": "We beginnen beginnen met de volgende vergelijking:",
            "output": "\\[x^2 - 6x + 12 = -x^2 + 8\\]"
        },
        {
            "explanation": "Om deze vergelijking op te lossen, willen we het eerst in de algemene vorm \\(x^2 + bx + c = 0 \\) zetten. We willen dus eerst alles naar de linkerkant halen. Om dit te doen, doen we aan beide kanten \\(+x^2\\) en \\(-8\\):",
            "output": "\\[2x^2 - 6x + 4 = 0\\]"
        },
        {
            "explanation": "Nu delen we nog beide kanten van de vergelijking nog door \\(2\\):",
            "output": "\\[x^2 - 3x + 2 = 0\\]"
        },
        {
            "explanation": "Nu kunnen we dit gaan ontbinden in factoren. We zoeken twee getallen die vermenigvuldigen tot \\(2\\) en optellen tot \\(-3\\). Deze getallen zijn \\(-1\\) en \\(-2\\). We kunnen de vergelijking dan schrijven als:",
            "output": "\\[ \\left(x - 1\\right) \\left(x - 2\\right) \\]"
        },
        {
            "explanation": "Twee dingen keer elkaar kunnen alleen \\(0\\) zijn als een van de twee factoren \\(0\\) is. We krijgen dus:",
            "output": "\\[ x - 1 = 0 \\ \\vee \\ x - 2 = 0 \\]"
        },
        {
            "explanation": "En hieruit volgt dat:",
            "output": "\\[ x = 1 \\ \\vee \\ x = 2 \\]"
        }

    ],
    "final_answer": "\\[\\boxed{1) \\quad x = 1}\\]<br>\\[\\boxed{2) \\quad x = 2}\\]"
}
'''


def chatgpt_get_explanation(question):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": math_tutor_prompt
        },

        {
            "role": "user", 
            "content": example_question1
        },

        {
            "role": "assistant", 
            "content": example_answer1
        },        

        {
            "role": "user", 
            "content": question
        }
    ],
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
                                "explanation": {"type": "string"},
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

    return response.choices[0].message

if __name__ == "__main__":
    # Testing with an example question
    question = "{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}"

    result = chatgpt_get_explanation(question) 

    print(result.content)
    print()
    print(type(result.content))