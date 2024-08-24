from openai import OpenAI
import json
import os

try:
    with open('/etc/config.json') as config_file:
        config = json.load(config_file)

    OPENAI_API_KEY = config['OPENAI_API_KEY']
except FileNotFoundError:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

math_tutor_prompt = r'''
You are a helpful dutch math tutor. You will be given a math equation via a Python dictionary. It contains the equation and the final answer, and your goal is to work step-by-step towards the solution. You will ultimately arrive at the same final answer as provided.
For each step, provide only the outcome as an equation and use the explanation field to clarify the reasoning in dutch. You use language suitable for a dutch third-grader and explain the steps as clearly as possible. 
When providing the outcome of each step, use '\\[' and '\\]' for display math notation and '\\(' and '\\)' for inline math notation. For example, if the outcome of a step is '2x + 3 = 7', you should write '\\[2x + 3 = 7\\]'. If in the explanation you use '2x + 3', you should write '\\(2x + 3\\)'.
The final answer should be boxed. So if the final answer is 'x = 5', you should write '\\[\\boxed{x = 5}\\]'. If you have multiple solutions, you should format them as '\\[\\boxed{1) \\quad x = 1}\\]<br>\\[\\boxed{2) \\quad x = -1}\\]'. Always use double slashes: \\ when writing math notation.
'''

example_question1 = r'''
{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}
'''

example_answer1 = r'''
{
    "steps": [
        {
            "explanation": r"We beginnen beginnen met de volgende vergelijking:",
            "output": r"\\[3x - 7 = 5x + 3\\]"
        },
        {
            "explanation": r"We doen eerst aan beide kanten van de vergelijking \\(-5x\\) om alle \\(x\\) termen naar links te halen:",
            "output": r"\\[-2x - 7 = 3\\]"
        },
        {
            "explanation": r"Nu doen we aan beide kanten van de vergelijking \\(+7\\) om alle getallen rechts te krijgen:",
            "output": r"\\[-2x = 10\\]"
        },
        {
            "explanation": r"En nu kunnen we beide kanten delen door \\(-2\\). We vinden dan:",
            "output": r"\\[x = -5\\]"
        }
    ],
    "final_answer": r"\\[\\boxed{x = -5}\\]"
}
'''

example_question2 = r'''
{'equation_text': 'x^2 - 6x + 12 = -x^2 + 8', 'equation_interpret': 'x^2 - 6*x + 12 = -x^2 + 8', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), 'x^{2} - 6 x + 12 = 8 - x^{2}', ('De oplossingen zijn:', {'latex': False}), '1) \\quad x = 1', '2) \\quad x = 2']}
'''

example_answer2 = r'''
{
    "steps": [
        {
            "explanation": r"We beginnen beginnen met de volgende vergelijking:",
            "output": r"\\[x^2 - 6x + 12 = -x^2 + 8\\]"
        },
        {
            "explanation": r"Om deze vergelijking op te lossen, willen we het eerst in de algemene vorm \\(x^2 + bx + c = 0 \\) zetten. We willen dus eerst alles naar de linkerkant halen. Om dit te doen, doen we aan beide kanten \\(+x^2\\) en \\(-8\\):",
            "output": r"\\[2x^2 - 6x + 4 = 0\\]"
        },
        {
            "explanation": r"Nu delen we nog beide kanten van de vergelijking nog door \\(2\\):",
            "output": r"\\[x^2 - 3x + 2 = 0\\]"
        },
        {
            "explanation": r"Nu kunnen we dit gaan ontbinden in factoren. We zoeken twee getallen die vermenigvuldigen tot \\(2\\) en optellen tot \\(-3\\). Deze getallen zijn \\(-1\\) en \\(-2\\). We kunnen de vergelijking dan schrijven als:",
            "output": r"\\[ \\left(x - 1\\right) \\left(x - 2\\right) \\]"
        },
        {
            "explanation": r"Twee dingen keer elkaar kunnen alleen \\(0\\) zijn als een van de twee factoren \\(0\\) is. We krijgen dus:",
            "output": r"\\[ x - 1 = 0 \\, \\vee \\, x - 2 = 0 \\]"
        },
        {
            "explanation": r"En hieruit volgt dat:",
            "output": r"\\[ x = 1 \\, \\vee \\, x = 2 \\]"
        }

    ],
    "final_answer": r"\\[\\boxed{1) \\quad x = 1}\\]<br>\\[\\boxed{2) \\quad x = 2}\\]"
}
'''

example_question3 = r'''
{'equation_text': 'sin(x) = 1/2 \\sqrt{3}', 'equation_interpret': 'sin(x) = 1/2*sqrt(3)', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '\\sin{\\left(x \\right)} = \\frac{\\sqrt{3}}{2}', ('De oplossingen zijn:', {'latex': False}), 'x = \\left\\{2 n \\pi + \\frac{2 \\pi}{3}\\; \\middle|\\; n \\in \\mathbb{Z}\\right\\} \\cup \\left\\{2 n \\pi + \\frac{\\pi}{3}\\; \\middle|\\; n \\in \\mathbb{Z}\\right\\}', ('Oplossingen in het domein $[0, 2\\pi]$:', {'latex': False, 'new_line': 2}), '1) \\quad x = \\frac{\\pi}{3} \\approx 1.04720', '2) \\quad x = \\frac{2 \\pi}{3} \\approx 2.09440']}
'''

example_answer3 = r'''
{
    "steps": [
        {
            "explanation": r"We beginnen met de volgende vergelijking:",
            "output": r"\\[\\sin(x) = \\dfrac{1}{2} \\sqrt{3}\\]"
        },
        {
            "explanation": r"Om dit op te lossen, moeten we eerst aan beide kanten een sinus hebben. Op de eenheidscirkel kunnen we aflezen dat we \\(\\dfrac{1}{2} \\sqrt{3}\\) kunnen schrijven als de sinus van \\(x = \\dfrac{1}{3} \\pi :\\)",
            "output": r"\\[\\sin(x) = \\sin \\left( \\dfrac{1}{3}\\pi \\right) \\]"
        },
        {
            "explanation": r"Nu kunnen we dit oplossen met de algemene oplossing voor een sinus:",
            "output": r"\\[x = \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\, \\vee \\, x = \\pi - \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\]"
        },
        {
            "explanation": r"Hierbij is \\(n\\) een geheel getal (dit geven we aan met \\(n \\in \\mathbb{Z}\\) ). We kunnen de vergelijking nog verder versimpelen tot:",
            "output": r"\\[x = \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\, \\vee \\, x = \\dfrac{2}{3}\\pi + n \\cdot 2\\pi \\]"
        },
        {
            "explanation": r"Dit is de formule voor alle oplossingen, maar we kunnen ook nog de oplossingen in het domein \\( \\left[ 0, 2\\pi \\right] \\) bepalen. We vullen dan gehele getallen in voor \\(n\\) zodat we alle oplossingen tussen \\(0\\) en \\(2\\pi\\) krijgen. <br><br>In dit geval zijn de oplossingen alleen tussen \\(0\\) en \\(2\\pi\\) als \\( n=0 \\), dus we krijgen als oplossingen:",
            "output": r"\\[ x = \\dfrac{1}{3} \\pi \\, \\vee \\, x = \\dfrac{2}{3} \\pi \\]"
        },


    ],
    "final_answer": r"\\[\\boxed{1) \\quad x = \\frac{\\pi}{3} \\approx 1.04720}\\]<br>\\[\\boxed{2) \\quad x = \\frac{2 \\pi}{3} \\approx 2.09440}\\]"
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
            "content": example_question2
        },
        {
            "role": "assistant", 
            "content": example_answer2
        },  

        {
            "role": "user", 
            "content": example_question3
        },
        {
            "role": "assistant", 
            "content": example_answer3
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

    return response.choices[0].message

if __name__ == "__main__":
    # Testing with an example question
    question = "{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}"

    result = chatgpt_get_explanation(question) 

    print(result.content)
    print()
    print(type(result.content))