# Wiskundewijs

The code behind [wiskundewijs.com](https://wiskundewijs.com): maths explanations for Dutch secondary school, plus an equation solver (the *oplosser*) that solves equations, inequalities and calculations, shows the steps and plots the graphs.

The site has two parts:

- **The pages** are Markdown files in `mkdocs/`, turned into HTML by [MkDocs](https://www.mkdocs.org/) with the Material theme.
- **The oplosser** is a Django app (`oplosser/`) built on the solver in `src/Solver/`. Django also serves the MkDocs pages.

## Repository layout

| Path | What's there |
| --- | --- |
| `mkdocs/` | The Markdown sources of all pages, plus images, JavaScript, CSS and theme overrides (`mkdocs/overrides/`). |
| `mkdocs.yml` | MkDocs configuration: navigation, theme, footer, analytics. |
| `hooks/` | MkDocs hooks. `copyright_year.py` fills in `{year}` in the footer with the year the site was built. |
| `docs/` | Django app that serves the built pages. `docs/static/mkdocs_build/` is the MkDocs output (committed to git). |
| `oplosser/` | Django app for the solver: views, forms, templates, and the scripts `run_updates.bat` uses. |
| `wiskundewijs/` | Django project: `settings.py`, `urls.py`, `wsgi.py`. |
| `src/Solver/` | The solver (see [The solver](#the-solver)) and its tests. |
| `src/<topic>/` | Manim scripts that made the animations and interactive graphs. Not used by the website. |
| `staticfiles/` | Output of `collectstatic`: the files Django serves as static files (committed to git). |
| `requirements.txt` | Exact versions of everything the website needs. |
| `requirements-dev.txt` | Also the tools for tests and checks (pytest, pip-audit, Django type hints). |
| `requirements-content.txt` | Tools for making the animations in `src/` (manim, matplotlib, plotly). |
| `pyrightconfig.json` | Type checking settings for pyright and Pylance. |
| `.github/dependabot.yml` | Lets Dependabot open a pull request when packages have updates. |

`netlify.toml` and `runtime.txt` are from an older Netlify setup and aren't used by the server.

## How the parts fit together

1. `mkdocs build` turns `mkdocs/` into HTML in `docs/static/mkdocs_build/`.
2. `collectstatic` copies that output (plus the oplosser's static files) to `staticfiles/`.
3. The oplosser page needs the same header, navigation and footer as the other pages. So its Django template `oplosser/templates/oplosser/base.html` is generated from the built page `mkdocs_build/oplosser/index.html` by `oplosser/update_base.py`.
4. Django serves the pages (`docs/`) and the oplosser at `/oplosser/`. Solving an equation goes like this:
   - the form in `equation_form.html` posts the equation to `oplosser/views.py`
   - the view checks the input and runs the solver in a separate process, which is stopped after 30 seconds
   - the view turns the result into HTML with `equation_result.html`
   - Plotly draws the graph in the browser, and MathJax 2 renders the formulas

## Setting up on your own computer

You need Python 3.12 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (on Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
python manage.py runserver
```

Then open http://127.0.0.1:8000/. Without `/etc/config.json` the development settings are used: `DEBUG` on and a development secret key.

To make the animations in `src/`, also run `pip install -r requirements-content.txt`. Manim also needs some programs that pip can't install (see the [manim installation guide](https://docs.manim.community/en/stable/installation.html)).

## Publishing changes

### 1. Build the pages

After changing pages in `mkdocs/` (or `mkdocs.yml`), run `run_updates.bat`, or the same steps by hand:

```bash
mkdocs build                                   # mkdocs/ -> docs/static/mkdocs_build/
python oplosser/update_search.py               # add the oplosser to the search index
python oplosser/update_sitemap.py              # add the oplosser to sitemap.xml
python manage.py collectstatic --noinput --clear   # -> staticfiles/
copy /Y docs\static\mkdocs_build\oplosser\index.html oplosser\templates\oplosser\base.html
python oplosser/update_base.py                 # turn that page into the Django template
```

Use `cp docs/static/mkdocs_build/oplosser/index.html oplosser/templates/oplosser/base.html` instead of `copy` outside Windows.

`update_base.py` does three things:

- puts the Django `{% block content %}` where the page content goes
- points the theme's CSS, JS and images at Django's static files
- replaces MathJax 3 with MathJax 2

The last one matters because the oplosser uses MathJax 2, and loading both breaks MathJax (and with it the Plotly graph).

### 2. Check before committing

```bash
pytest                          # solver tests (about 1.5 minutes)
npx pyright                     # type checking; needs Node.js. Or check the Problems tab in VS Code (Pylance)
pip-audit -r requirements.txt   # known vulnerabilities in the packages
python manage.py check
```

### 3. Commit, push and update the server

The built files (`docs/static/mkdocs_build/`, `staticfiles/` and `base.html`) are committed, so the server doesn't need to build anything. On the server:

```bash
cd /path/to/Wiskundewijs
git pull
source /path/to/venv/bin/activate     # the virtual environment Apache uses
pip install -r requirements.txt       # only needed when requirements.txt changed
python manage.py migrate              # only does something after a Django update
sudo systemctl reload apache2         # or restart apache2, so Django loads the new code
```

## The server configuration

`settings.py` reads `/etc/config.json` if it exists. It's outside the repository, so the secrets never end up on GitHub:

```json
{
    "SECRET_KEY": "a long random string",
    "OPENAI_API_KEY": "sk-...",
    "DEBUG": false,
    "HSTS_SECONDS": 3600
}
```

Only `SECRET_KEY` is required. `DEBUG` is off unless the file turns it on. You can make a new secret key with `python -c "import secrets; print(secrets.token_urlsafe(50))"`.

> **First deploy after this change:** the server's `settings.py` was edited by hand to read `/etc/config.json` and turn `DEBUG` off. The `settings.py` in the repository now does that itself, so throw away the local edit before pulling: `git checkout -- wiskundewijs/settings.py`, then `git pull`.

With `DEBUG` off, these security settings are used:

- **`SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`.** Browsers only send these cookies over HTTPS, so nobody can read them on an open wifi network. (The CSRF cookie protects the oplosser's forms.)
- **`SECURE_HSTS_SECONDS`** (HSTS). It tells browsers to always use HTTPS for wiskundewijs.com, even if someone types `http://`. It starts at one hour. Once you're sure HTTPS works, set `HSTS_SECONDS` in `config.json` to `31536000` (a year). Don't do that while unsure: browsers then refuse plain HTTP for that long.
- **`CSRF_TRUSTED_ORIGINS`** lists the HTTPS addresses of the site.

`python manage.py check --deploy` lists what Django still recommends. The remaining warnings are deliberate:

- `X_FRAME_OPTIONS` stays `SAMEORIGIN` because the pages show the interactive graphs in frames.
- `SECURE_SSL_REDIRECT` is better done by Apache. Plain `http://wiskundewijs.com` currently gives a *403 Forbidden*. An Apache redirect to HTTPS fixes that for visitors who type the address without `https://`, for example in `/etc/apache2/sites-available/000-default.conf`:

  ```apache
  <VirtualHost *:80>
      ServerName wiskundewijs.com
      ServerAlias www.wiskundewijs.com
      Redirect permanent / https://wiskundewijs.com/
  </VirtualHost>
  ```

## Updating dependencies

`requirements.txt` has exact versions, so the server gets exactly what was tested. Dependabot (`.github/dependabot.yml`) opens a pull request when there are security fixes, and once a month for other updates. For such a pull request, or when updating by hand:

1. Install the new versions locally: `pip install -r requirements-dev.txt`.
2. Run `pytest`, `pip-audit -r requirements.txt` and `mkdocs build`, and try a few equations in the oplosser.
3. If everything works, merge, and run `pip install -r requirements.txt` on the server.

To update everything at once, install the newest versions of the packages and write down the exact versions:

```bash
pip install --upgrade "Django>=5.2,<6" whitenoise django-crispy-forms crispy-bootstrap4 sympy numpy scipy regex pylatexenc mistune openai beautifulsoup4 lxml Markdown mkdocs mkdocs-material pymdown-extensions gunicorn
pip freeze > requirements.txt
```

Do this in an environment with only the website's packages, otherwise `pip freeze` lists everything else installed too. Django 5.2 is a long-term support version with security updates until April 2028.

**pip-audit** checks the installed versions against a database of known vulnerabilities. `pip-audit -r requirements.txt` prints *No known vulnerabilities found*, or a table of the affected packages with the version that fixes each one. It's a quicker way to see what Dependabot would warn about.

**MkDocs Material** announces that it reaches end of life on 5 May 2027, with security fixes until then. Its successor, [Zensical](https://zensical.org), is made by the same team and can read the existing `mkdocs.yml`.

## The solver

The solver is in `src/Solver/src/solver/`:

| Module | What it does |
| --- | --- |
| `math_parser.py` | Turns what users type (`2x^2 + sinx = 1`, LaTeX, `√`, `π`, ...) into text SymPy can read (`2*x^2 + sin(x) = 1`). |
| `safe_parsing.py` | `safe_sympify`, which turns that text into SymPy expressions without being able to run Python code (see below). |
| `solve_calculations.py` | The `Solve` class: parses the equation, finds the solutions and writes the output lines. |
| `systems.py` | Systems of equations (`x + y = 10; x - y = 2`), solved exactly or numerically. |
| `vector_equations.py` | Calculations and equations with vectors and matrices. |
| `numeric.py` | Numerical root finding, for equations SymPy can't solve exactly. |
| `plotting.py` | The Plotly graph: both sides of the equation, intersections and vertical asymptotes. |
| `latex_printer.py` | LaTeX output the way it's written at school: mixed fractions, `x = a + k·2π`, `arcsin`. |
| `linear_algebra.py` | `vect(...)`, `matrix(...)` and vector operations like `grad`, `dot` and `cross`. |
| `degree_functions.py` | `arcsin` and friends giving degrees, for degree mode. |
| `sympy_custom_funcs.py` | `LOCALS`: the functions available in the input. |
| `output.py` | The output line format the view turns into HTML. |
| `openai_api.py` | The ChatGPT explanation and questions feature. |

`oplosser/solver_pipeline.py` connects the solver to the view: it solves, then makes the plot data.

The graph is calculated with many points, far beyond the visible part (so you can pan). Before the data is sent, `plotting.simplify_traces` removes the points that make no visible difference with the [Ramer–Douglas–Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm). It also rounds the coordinates to 7 digits. `SIMPLIFY_TOLERANCE` sets how far the graph may move: 0.02% of the visible size, so less than a pixel. That takes `1/x = 2` from 2.8 MB to 5 kB.

### Why the input can't run code

`sympy.sympify` evaluates text with Python's `eval`, so input like `__import__('os').system(...)` would run on the server. Everything goes through `safe_sympify` instead:

- **Input rules.** Text with `__`, or with strings other than `'+'` and `'-'` (used by `limit(1/x, 0, '+')`), is refused.
- **No built-ins.** The text is evaluated without Python's built-in functions (`open`, `getattr`, `eval`, ...) and without the SymPy functions that evaluate text, run programs or plot. Unknown names, like `open`, just become maths symbols.
- **Escaped output.** All output is HTML-escaped before it's shown, so input like `<script>` appears as text.

Never use `sp.sympify(some_string)` in the solver: use `safe_sympify`. (`sp.sympify` on numbers or SymPy objects is fine.)

### Tests

- `src/Solver/src/solver/test_math_parser.py` tests the input parser.
- `src/Solver/tests/test_safe_parsing.py` tests that code can't get through.
- `src/Solver/tests/test_golden.py` runs about 200 inputs (`golden_inputs.py`) through the solver. It compares the output and the plot data with `golden_outputs.json`, so a change to the solver can't silently change what users see.

When you change the solver's output on purpose, record the new output and check the diff of `golden_outputs.json` before committing:

```bash
PYTHONHASHSEED=0 python -m src.Solver.tests.golden --record      # Linux/macOS/Git Bash
set PYTHONHASHSEED=0 && python -m src.Solver.tests.golden --record  # Windows cmd
```

`PYTHONHASHSEED=0` matters: without it Python orders sets differently every run, and some solutions are listed in a different order.

## Known issues and ideas

- **Quirks in the solver's output.** The golden tests deliberately keep these as they are:
  - `1/x = 2` shows the heading "Het domein van x is:" with nothing under it.
  - `sin(x) = 0.5` gives the general solution as `x = 0.5235987… + k·2π` instead of `x = 1/6 π + k·2π`.
  - `e^(x - 5) = sqrt(2x)` shows the unsolved set before the numerical solutions.
- **The explanation feature (ChatGPT)** isn't connected at the moment. If it's turned back on, it needs a limit on how often it can be used per visitor. Each explanation and question costs an API call.
