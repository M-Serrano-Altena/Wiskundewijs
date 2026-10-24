import ast
import html
import json
import multiprocessing
import os
import queue
import time
import traceback
from typing import Any

import mistune
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import url_has_allowed_host_and_scheme

from src.Solver.src.solver import openai_api
from src.Solver.src.solver.output import OutputLine, OutputOptions
from src.Solver.src.solver.safe_parsing import UnsafeInputError, validate_user_input
from src.Solver.src.solver.solve_calculations import math_interpreter

from .forms import EquationForm, QuestionForm
from .solver_pipeline import SolveResult, describe_for_explanation, solve_for_view

SOLVE_TIMEOUT_SECONDS = 30


def serve_search_index(request: HttpRequest) -> JsonResponse:
    with open(os.path.join(settings.STATIC_ROOT, 'search', 'search_index.json')) as f:
        data = json.load(f)
    return JsonResponse(data)


def redirect_view(request: HttpRequest, path: str) -> HttpResponse:
    url = '/' + path
    if url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
        return redirect(url)
    return HttpResponseBadRequest("Bad redirect URL")


def add_solution_text(solution_text: str, new_text: str, options: OutputOptions | None = None) -> str:
    """Add a line of solver output to the solution HTML. LaTeX lines are shown in a box."""
    options = options or {}
    new_line = options.get("new_line", True)
    latex = options.get("latex", True)

    # The text comes from the solver and contains (part of) the user's input, so it's escaped.
    # MathJax reads the text after the browser has unescaped it, so the LaTeX still works.
    new_text = html.escape(new_text, quote=False)

    if isinstance(new_line, bool):
        line_breaks = "<br>" if new_line else ""
    else:
        line_breaks = new_line * "<br>"

    if latex:
        return f"<span class='arithmatex'>{solution_text}{line_breaks}\\[\\boxed{{{new_text}}}\\]</span>"
    return f"{solution_text}{line_breaks}{new_text}<br>"


def outputs_to_html(outputs: list[OutputLine]) -> str:
    solution_text = ""
    for output in outputs:
        if isinstance(output, tuple):
            text, options = output
            # inline maths in text lines is written as $...$
            text = text.replace('$', '\\(', 1).replace('$', '\\)', 1)
            solution_text = add_solution_text(solution_text, text, options)
        else:
            solution_text = add_solution_text(solution_text, output)

    return add_solution_text(solution_text, "", {"latex": False})


def _solve_in_process(equation_text: str, angle_mode: str, result_queue: Any) -> None:
    result_queue.put(solve_for_view(equation_text, angle_mode))


def solve_with_timeout(equation_text: str, angle_mode: str) -> SolveResult | None:
    """Solve in a separate process, so a calculation that takes too long can be stopped. None on timeout."""
    result_queue: Any = multiprocessing.Queue()
    process = multiprocessing.Process(target=_solve_in_process, args=(equation_text, angle_mode, result_queue))
    process.start()
    try:
        # get the result before joining: the process can only exit once its result has been read
        return result_queue.get(timeout=SOLVE_TIMEOUT_SECONDS)
    except queue.Empty:
        return None
    finally:
        process.join(timeout=1)
        if process.is_alive():
            process.terminate()
            process.join()


def _error_result(equation_text: str, message: str, interpret: str | None = None) -> SolveResult:
    return SolveResult(
        equation_text=equation_text,
        equation_interpret=interpret if interpret is not None else equation_text,
        outputs=[(message, {"latex": False})],
        plot=False,
        numerical=False,
    )


def solve_equation_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return render(request, 'oplosser/equation_form.html', {'form': EquationForm(), 'title': "Vergelijking Oplosser"})

    start_time = time.time()
    form = EquationForm(request.POST)
    angle_mode = request.POST.get("angle_mode", "automatic")
    if not form.is_valid():
        return render(request, 'oplosser/equation_form.html', {'form': form, 'title': "Vergelijking Oplosser"})

    equation_text: str = form.cleaned_data['equation_text']
    try:
        validate_user_input(equation_text)
        result = solve_with_timeout(equation_text, angle_mode)
        if result is None:
            result = _error_result(equation_text, "Error: Berekening duurt te lang", interpret=math_interpreter(equation_text))
    except UnsafeInputError:
        result = _error_result(equation_text, "Error: Deze invoer wordt niet ondersteund")

    print(f"Solving - Time taken: {time.time() - start_time}")

    solution_text = outputs_to_html(result.outputs)
    if result.plot_error:
        solution_text += "<br>Error: Plot kon niet worden gegenereerd"

    if not result.numerical and "error" in solution_text.casefold():
        data_chatgpt = "error"
    else:
        data_chatgpt = str(describe_for_explanation(result))

    context = {
        'equation_text': equation_text,
        'equation_interpret': result.equation_interpret,
        'solutions': solution_text,
        'plot': result.plot,
        'title': 'Vergelijking Oplosser',
        'data_chatgpt': data_chatgpt,
    }
    if result.plot:
        context.update({'plot_data': result.plot_data, 'x_range': result.x_range, 'y_range': result.y_range})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'result': render_to_string('oplosser/equation_result.html', context)})

    return render(request, 'oplosser/equation_form.html', {'form': form, 'title': "Vergelijking Oplosser"})


def check_display_math(string: str, final: bool = False) -> str:
    condition = not ((not (r"\[" in string and r"\]" in string)) ^ (not (r"\\[" in string and r"\\]" in string)))
    if condition and string != '':
        if final and "boxed" not in string:
            string = rf"\\boxed{{{string}}}"

        string = rf"\\[{string}\\]"

    elif final and "boxed" not in string:
        parts = string.split(r"\[")
        if len(parts) > 1:
            string = parts[1]

        string = string.split(r"\]")[0]
        string = rf"\\[\boxed{{{string}}}\\]"

    return check_forward_slash(string)


def check_forward_slash(string: str) -> str:
    r"""Undo tab and form feed characters that came from \t and \f in LaTeX (like \theta, \frac)."""
    return string.replace('\t', '\\t').replace('\f', '\\f')


def escape_model_text(text: str) -> str:
    """Escape text from the language model, but keep the line breaks it adds."""
    escaped = html.escape(text, quote=False)
    for line_break in ("&lt;br&gt;", "&lt;br/&gt;", "&lt;br /&gt;"):
        escaped = escaped.replace(line_break, "<br>")
    return escaped


NUMERICAL_EXPLANATION = 'Voor numerieke oplossingen is er geen uitleg mogelijk <span style="arithmatex">\\( \\phantom{.} \\)</span><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc.--><path d="M256 512a256 256 0 1 0 0-512 256 256 0 1 0 0 512zm-96.7-123.3c-2.6 8.4-11.6 13.2-20 10.5s-13.2-11.6-10.5-20C145.2 326.1 196.3 288 256 288s110.8 38.1 127.3 91.3c2.6 8.4-2.1 17.4-10.5 20s-17.4-2.1-20-10.5C340.5 349.4 302.1 320 256 320s-84.5 29.4-96.7 68.7zM144.4 208a32 32 0 1 1 64 0 32 32 0 1 1-64 0zm192-32a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg></span>'

EXAMPLE_EXPLANATION = {"steps": [{"explanation": "We beginnen met de volgende vergelijking:", "output": "\\[\\sin(x) = \\dfrac{1}{2} \\sqrt{3}\\]"}, {"explanation": "Om dit op te lossen, moeten we eerst aan beide kanten een sinus hebben. Op de eenheidscirkel kunnen we aflezen dat we \\(\\frac{1}{2} \\sqrt{3}\\) kunnen schrijven als de sinus van \\(x = \\frac{1}{3} \\pi\\):", "output": "\\[\\sin(x) = \\sin \\left( \\dfrac{1}{3}\\pi \\right) \\]"}, {"explanation": "Nu kunnen we dit oplossen met de algemene oplossing voor een sinus:", "output": "\\[x = \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\, \\vee \\, x = \\pi - \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\]"}, {"explanation": "Hierbij is \\(n\\) een geheel getal (dit geven we ook aan als \\(n \\in \\mathbb{Z}\\) ). We kunnen de vergelijking nog verder versimpelen tot:", "output": "\\[x = \\dfrac{1}{3}\\pi + n \\cdot 2\\pi \\, \\vee \\, x = \\dfrac{2}{3}\\pi + n \\cdot 2\\pi \\]"}, {"explanation": "Dit is de formule voor alle oplossingen, maar we kunnen ook nog de oplossingen in het domein \\( \\left[ 0, 2\\pi \\right] \\) bepalen. We vullen dan alle gehele getallen in voor \\(n\\) die ons een uitkomst tussen \\(0\\) en \\(2\\pi\\) geven. <br> In dit geval is dat alleen voor \\( n=1 \\), dus we vinden als oplossingen:", "output": "\\[ x = \\dfrac{1}{3} \\pi \\, \\vee \\, x = \\dfrac{2}{3} \\pi \\]"}], "final_answer": "\\[\\boxed{1) \\quad x = \\frac{\\pi}{3} \\approx 1.04720}\\]<br>\\[\\boxed{2) \\quad x = \\frac{2 \\pi}{3} \\approx 2.09440}\\]"}


def explanation_to_html(explanation_raw: dict[str, Any]) -> str:
    explanation = ""
    for step in explanation_raw['steps']:
        explanation += escape_model_text(check_forward_slash(step["explanation"])) + "<br><br>"
        explanation += escape_model_text(check_display_math(rf"{step['output']}")) + "<br>"

    final_answer = escape_model_text(check_display_math(explanation_raw['final_answer'], final=True))
    return explanation + "We krijgen dus als eindantwoord:" + "<br><br>" + final_answer


def explain_equation_base(request: HttpRequest, use_chatgpt: bool = False) -> JsonResponse:
    start_time = time.time()
    if request.method != 'GET':
        return JsonResponse({'explanation': "Geen uitleg beschikbaar", 'generation_success': False})

    if use_chatgpt:
        data_chatgpt = request.GET.get("data_chatgpt")
        if data_chatgpt is None:
            return JsonResponse({'explanation': "Geen uitleg beschikbaar", 'generation_success': False})

        data_chatgpt = html.unescape(data_chatgpt)
        if data_chatgpt in ("Geen uitleg beschikbaar", "error"):
            return JsonResponse({'explanation': "Geen uitleg beschikbaar", 'generation_success': False})
        if data_chatgpt == "numeriek":
            return JsonResponse({'explanation': NUMERICAL_EXPLANATION, 'generation_success': False})

        try:
            chatgpt_response = check_forward_slash(openai_api.get_explanation(data_chatgpt))
            explanation_raw = ast.literal_eval(chatgpt_response)
        except Exception:
            traceback.print_exc()
            return JsonResponse({'explanation': "Geen uitleg beschikbaar", 'generation_success': False})
    else:
        explanation_raw = ast.literal_eval(check_forward_slash(str(EXAMPLE_EXPLANATION)))

    explanation = explanation_to_html(explanation_raw)
    print(f"Explanation - Time taken: {time.time() - start_time}")
    return JsonResponse({'explanation': explanation, 'generation_success': use_chatgpt})


def explain_equation_dummy(request: HttpRequest) -> JsonResponse:
    return explain_equation_base(request, use_chatgpt=False)


def explain_equation(request: HttpRequest) -> JsonResponse:
    return explain_equation_base(request, use_chatgpt=True)


def format_answer(answer_question: str) -> str:
    # escape=True: HTML in the model's answer is shown as text instead of being run
    markdown = mistune.create_markdown(escape=True)

    answer_question = check_forward_slash(answer_question)
    answer_question = answer_question.replace("\\", r"\\")
    return str(markdown(answer_question))


def answer_question(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return render(request, 'equation_result.html', {'form': QuestionForm()})

    start_time = time.time()
    form = QuestionForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'answer': "Geen uitleg beschikbaar"})

    explanation = request.POST.get("explanation")
    question = form.cleaned_data.get("question")
    if explanation is None or question is None:
        return JsonResponse({'answer': "Er is iets mis gegaan. Probeer het anders opnieuw."})

    try:
        chatgpt_response = openai_api.answer_question(explanation, question)
        answer = format_answer(ast.literal_eval(chatgpt_response)["response"])
    except Exception:
        traceback.print_exc()
        answer = "Er is iets mis gegaan. Probeer het anders opnieuw."

    print(f"Answer Question - Time taken: {time.time() - start_time}")
    return JsonResponse({'answer': answer})
