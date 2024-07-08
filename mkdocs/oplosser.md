---
hide:
  - navigation
  - toc
  - feedback
---

*empty*

## Mogelijke Opties
- **Vergelijkingen Omschrijven:** Vergelijkingen met $y$ en $x$ worden omgeschreven om $y$ vrij te maken. Daarna worden de snijpunten met de $x$-as bepaald.<br><br>

- **Afgeleides nemen:** 
    + **Eerste Afgeleide:** $\phantom{.}$ <span style="font-size: 19px;">`diff(f(x))`</span> $= \dfrac{d}{d x} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`diff(x^2 + 3x + 1)`</span> $= 2x + 3$ <br><br>
    + **n-de Afgeleide:** $\phantom{.}$ <span style="font-size: 19px;">`diff(f(x), x, n)`</span> $= \dfrac{d^{n}}{d x^{n}} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`diff(x^2 + 3x + 1, x, 2)`</span> $= \dfrac{d^{2}}{d x^{2}}\left(x^2 + 3x + 1\right) = 2$ <br> $\phantom{mmmmmmmm.} \Longrightarrow$ De losse $x$ is hier de variabele waarover je de afgeleide neemt <br> $\phantom{mmmmmmmm.} \Longrightarrow$ $n$ is hoe vaak je de afgeleide neemt (dus $n=2$ is de dubbele afgeleide)<br><br>

- **Integreren:** 
    + **Primitieve:** $\phantom{.}$  <span style="font-size: 19px;">`integrate(f(x))`</span> $= \int f(x) \, dx \quad \longrightarrow \quad$ <span style="font-size: 19px;">`integrate(x^2)`</span> $= \int x^2 \, dx = \dfrac{x^3}{3} + C$ <br><br>
    + **Bepaalde Integraal:** $\phantom{.}$ <span style="font-size: 19px;">`integrate(f(x), (x, a, b))`</span> $= \int_{a}^{b} f(x) \, dx \quad \longrightarrow \quad$ <span style="font-size: 19px;">`integrate(x^2, (x, 0, 1))`</span> $= \int_{0}^{1} x^2 \, dx = \dfrac{1}{3}$ <br> $\phantom{mmmmmmmm.} \Longrightarrow$ De losse $x$ is hier de integratievariabele (dus de $x$ in $dx$) <br> $\phantom{mmmmmmmm.} \Longrightarrow$ $a$ en $b$ zijn hier de begin- en eindgrenzen van de integraal. <br><br>

- **Limieten:** 
    + **Continue Limieten:** $\phantom{.}$ <span style="font-size: 19px;">`limit(f(x), x, a)`</span> $= \lim\limits_{x \to a} f{\left(x \right)} \phantom{..} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`limit((2x - 1)/x, x, inf)`</span> $= \lim\limits_{x \to \infty} \dfrac{2x - 1}{x} = 2$ <br><br>
    + **Rechterlimiet:** $\phantom{.}$ <span style="font-size: 19px;">`limit(f(x), x, a, '+')`</span> $= \lim\limits_{x \ \downarrow \ a} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`limit(1/x, x, 0, '+')`</span> $= \lim\limits_{x \ \downarrow \ 0} \dfrac{1}{x} = \infty$ <br><br>
    + **Linkerlimiet:** $\phantom{.e}$ <span style="font-size: 19px;">`limit(f(x), x, a, '-')`</span> $= \lim\limits_{x \ \uparrow \ a} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`limit(1/x, x, 0, '-')`</span> $= \lim\limits_{x \ \uparrow \ 0} \dfrac{1}{x} = -\infty$ <br><br> 
    
    $\Longrightarrow$ Een rechter- of linkerlimiet bij een continue functie wordt vanzelf omgezet naar een continu limiet <br>
    $\Longrightarrow$ Een continu limiet bij een discontinue functie wordt een rechterlimiet <br><Br>


## Mogelijke Functies
- **Machten:** $\phantom{.}$ <span style="font-size: 19px;">`x^n` of `x**n`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`x^2` of `x**2`</span> $= x^2 \quad$ (allebei goed, kies wat je liever gebruikt) <br><br>

- **Wortels:**
    + <span style="font-size: 19px;">`sqrt(x)`</span> $= \sqrt{x}; \phantom{m} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`sqrt(4)`</span> $= \sqrt{4} = 2$
    + <span style="font-size: 19px;">`cbrt(x)`</span> $= \sqrt[3]{x}; \phantom{m} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`cbrt(8)`</span> $= \sqrt[3]{8} = 2$
    + <span style="font-size: 19px;">`root(x, n)`</span> $= \sqrt[n]{x}; \quad \longrightarrow \quad$ <span style="font-size: 19px;">`root(16, 4)`</span> $= \sqrt[4]{16} = 2$ <br><br>

- **Goniometrische Functies:**
    + <span style="font-size: 19px;">`sin(x)`</span> $= \sin(x)$ met inverse <span style="font-size: 19px;">`asin(x)`</span> $= \arcsin(x) \quad$ (rekenmachine $\sin^{-1}(x)$)
    + <span style="font-size: 19px;">`cos(x)`</span> $= \cos(x)$ met inverse <span style="font-size: 19px;">`acos(x)`</span> $= \arccos(x) \quad$ (rekenmachine $\cos^{-1}(x)$)
    + <span style="font-size: 19px;">`tan(x)`</span> $= \tan(x)$ met inverse <span style="font-size: 19px;">`atan(x)`</span> $= \arctan(x) \quad$ (rekenmachine $\tan^{-1}(x)$) <br><br>

- **Absolute Waarde:** $\phantom{.}$ <span style="font-size: 19px;">`|x|` of `abs(x)`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`|-2|`</span> $= |-2| = 2$ $\phantom{.}$ <span style="font-size: 19px;">en</span> $\phantom{.}$ <span style="font-size: 19px;">`abs(-2)`</span> $= |-2| = 2$ $\quad$ (allebei goed, kies wat je liever gebruikt) <br><br>

- **Exponententieel:** $\phantom{..}$ <span style="font-size: 19px;">`e^x` of `exp(x)`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`e^(2x)`</span> $= e^{2x}$ $\phantom{.}$ <span style="font-size: 19px;">en</span> $\phantom{.}$ <span style="font-size: 19px;">`exp(2x)`</span> $= e^{2x} \quad$ (allebei goed, kies wat je liever gebruikt) <br><br>

- **Logaritmes:** 
    + **Grondgetal e:** $\phantom{mm.}$ <span style="font-size: 19px;">`ln(x)`</span> $\phantom{m..} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`ln(e^4)`</span> $= \ln(e^4) = 4$
    + **Grondgetal 10:** $\phantom{m..}$ <span style="font-size: 19px;">`log(x)`</span> $\phantom{m.} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`log(100)`</span> $= \ ^{10} \! \log(100) = 2$
    + **Ander Grondgetal:** $\phantom{.}$ <span style="font-size: 19px;">`log(x, n)`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`log(8, 2)`</span> $= \ ^{2} \! \log(8) = 3$