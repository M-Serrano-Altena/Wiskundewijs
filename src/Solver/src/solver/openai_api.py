"""Step-by-step explanations of the solver's answers, and answers to follow-up questions, via OpenAI.

The prompts and example question/answer pairs are in the openai_prompts directory. Every request
builds its own list of messages, so conversations of different visitors never mix.
"""

from __future__ import annotations

import json
import os
from functools import cache
from pathlib import Path
from typing import Any

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

PROMPTS_DIR = Path(__file__).parent / "openai_prompts"
MODEL = "gpt-4o-mini"

# Typed as Any because the "json_schema" response format is newer than the type hints of the
# installed openai version.
EXPLANATION_FORMAT: Any = {
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
                        "properties": {"explanation": {"type": "string"}, "output": {"type": "string"}},
                        "required": ["explanation", "output"],
                        "additionalProperties": False,
                    },
                },
                "final_answer": {"type": "string"},
            },
            "required": ["steps", "final_answer"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

ANSWER_FORMAT: Any = {
    "type": "json_schema",
    "json_schema": {
        "name": "math_reasoning_reply",
        "schema": {
            "type": "object",
            "properties": {"response": {"type": "string"}},
            "required": ["response"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}


def _api_key() -> str | None:
    try:
        with open("/etc/config.json") as config_file:
            return json.load(config_file)["OPENAI_API_KEY"]
    except (FileNotFoundError, KeyError):
        return os.getenv("OPENAI_API_KEY")


@cache
def _client() -> OpenAI:
    # created on first use, so the rest of the site works without an API key
    return OpenAI(api_key=_api_key())


@cache
def _explanation_context() -> tuple[ChatCompletionMessageParam, ...]:
    """The system prompt followed by the example questions and answers."""
    directory = PROMPTS_DIR / "explanation"
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": (directory / "explanation_prompt.txt").read_text(encoding="utf-8")}
    ]

    amount_examples = len(list(directory.glob("example_question*.txt")))
    for i in range(1, amount_examples + 1):
        messages.append({"role": "user", "content": (directory / f"example_question{i}.txt").read_text(encoding="utf-8")})
        messages.append({"role": "assistant", "content": (directory / f"example_answer{i}.txt").read_text(encoding="utf-8")})

    return tuple(messages)


@cache
def _question_prompt() -> str:
    return (PROMPTS_DIR / "questions" / "question_answerer_prompt.txt").read_text(encoding="utf-8")


def _reply(messages: list[ChatCompletionMessageParam], response_format: Any) -> str:
    response = _client().chat.completions.create(model=MODEL, messages=messages, response_format=response_format)
    return response.choices[0].message.content or ""


def get_explanation(solver_output: str) -> str:
    """A step-by-step explanation of the solver's output, as JSON with "steps" and "final_answer"."""
    messages = [*_explanation_context(), {"role": "user", "content": solver_output}]
    return _reply(messages, EXPLANATION_FORMAT)


def answer_question(explanation: str, question: str) -> str:
    """An answer to a question about an explanation, as JSON with a "response"."""
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": _question_prompt()},
        {"role": "user", "content": explanation},
        {"role": "user", "content": question},
    ]
    return _reply(messages, ANSWER_FORMAT)


if __name__ == "__main__":
    example = "{'equation_text': '3x - 7 = 5x + 3', 'equation_interpret': '3*x - 7 = 5*x + 3', 'outputs': [('Vereenvoudigde Vergelijking:', {'latex': False}), '3 x - 7 = 5 x + 3', ('De oplossing is:', {'latex': False}), 'x = -5']}"
    print(get_explanation(example))
