from openai import OpenAI

client = OpenAI()

math_tutor_prompt = '''
Je bent een behulpzame wiskundeleraar. Je krijgt een wiskundevergelijking voorgelegd via een python dictionary. Het bevat de vergelijking en het eindantwoord, en jouw doel is om stapsgewijs naar de oplossing te werken. Uiteindelijk kom je op hetzelfde eindantwoord als dat je hebt gekregen. 
Voor elke stap geef je alleen de uitkomst als een vergelijking en gebruik je het uitlegveld om de redenatie te verduidelijken. Je gebruikt simpel taalgebruik en probeert de stappen zo duidelijk mogelijk uit te leggen.

'''

def get_math_solution(question):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": math_tutor_prompt
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

# Testing with an example question
question = "{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}"

result = get_math_solution(question) 

print(result.content)