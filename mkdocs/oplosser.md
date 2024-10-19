---
hide:
  - navigation
  - toc
  - feedback

search:
  exclude: true
---

*empty*

## Mogelijke Opties
- **Vergelijkingen Omschrijven:** $\phantom{.}$ De $y$ in een vergelijking wordt vrijgemaakt. Bijvoorbeeld: $\phantom{.}$ $2y - 4x = 8 \quad \longrightarrow \quad y = 2x + 4$<br><br><br>

- **Ongelijkheden Oplossen:** 
    + $\phantom{.}$ <span style="font-size: 21px;">`>`</span> voor *groter dan*: $\phantom{.} >$
    + $\phantom{.}$ <span style="font-size: 21px;">`<`</span> voor *kleiner dan*: $\phantom{.} <$
    + $\phantom{.}$ <span style="font-size: 21px;">`>=`</span> voor *groter of gelijk aan*: $\phantom{.} \geq$
    + $\phantom{.}$ <span style="font-size: 21px;">`<=`</span> voor *kleiner of gelijk aan*: $\phantom{.} \leq$
    + $\phantom{.}$ <span style="font-size: 21px;">`!=`</span> voor *niet gelijk aan* $\phantom{.} \neq$: <br><br><br>

- **Afgeleides nemen:** 
    + **Eerste Afgeleide:** $\phantom{.^{....}}$ <span style="font-size: 19px;">`diff(f(x))`</span> $= \dfrac{d}{d x} f{\left(x \right)} \phantom{^{..}} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`diff(x^2 + 3x + 1)`</span> $= \dfrac{d}{d x}\left(x^2 + 3x + 1\right) = 2x + 3$ <br><br>
    + **n-de Afgeleide:** $\phantom{.}$ <span style="font-size: 19px;">`diff(f(x), n)`</span> $= \dfrac{d^{n}}{d x^{n}} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`diff(x^2 + 3x + 1, 2)`</span> $= \dfrac{d^{2}}{d x^{2}} \left(x^2 + 3x + 1\right) = 2$ <br> $\phantom{mmmmmmmm.} \Longrightarrow$ $n$ is hoe vaak je de afgeleide neemt (dus $n=2$ is de dubbele afgeleide)<br> $\phantom{mmmmmmmm.} \Longrightarrow$ Als je expliciet de variabele wilt benoemen waarover je afleidt: $\phantom{.}$ <span style="font-size: 19px;">`diff(f(t), t, n)`</span> $= \dfrac{d^{n}}{d t^{n}} f{\left(t \right)}$ <br><br><br>

- **Integreren:** 
    + **Primitieve:** $\phantom{mmm.^{..}}$  <span style="font-size: 19px;">`integrate(f(x))`</span> $= \int f(x) \, dx \phantom{mmmm..^.} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`integrate(x^2)`</span> $= \int x^2 \, dx = \dfrac{x^3}{3} + C$ 
    + **Bepaalde Integraal:** $\phantom{.}$ <span style="font-size: 19px;">`integrate(f(x), (a, b))`</span> $= \int_{a}^{b} f(x) \, dx \quad \longrightarrow \quad$ <span style="font-size: 19px;">`integrate(x^2, (0, 1))`</span> $= \int_{0}^{1} x^2 \, dx = \dfrac{1}{3}$ <br> $\phantom{mmmmmmmm.} \Longrightarrow$ $a$ en $b$ zijn hier de begin- en eindgrenzen van de integraal. <br> $\phantom{mmmmmmmm.} \Longrightarrow$ Als je expliciet de variabele wilt benoemen waarover je integreert: $\phantom{.}$ <span style="font-size: 19px;">`integrate(f(t), (t, a, b))`</span> $= \int_{a}^{b} f(t) \, dt$<br><br><br>

- **Limieten:** 
    + **Continue Limieten:** $\phantom{.}$ <span style="font-size: 19px;">`limit(f(x), a)`</span> $= \lim\limits_{x \, \to \, a} f{\left(x \right)} \phantom{.} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`limit((2x - 1)/x, inf)`</span> $= \lim\limits_{x \, \to \, \infty} \dfrac{2x - 1}{x} = 2$ <br>
    + **Rechterlimiet:** $\phantom{.}$ <span style="font-size: 19px;">`limit(f(x), a, '+')`</span> $= \lim\limits_{x \, \downarrow \, a} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`limit(1/x, 0, '+')`</span> $= \lim\limits_{x \, \downarrow \, 0} \dfrac{1}{x} = \infty$ <br>
    + **Linkerlimiet:** $\phantom{.e}$ <span style="font-size: 19px;">`limit(f(x), a, '-')`</span> $= \lim\limits_{x \, \uparrow \, a} f{\left(x \right)} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`limit(1/x, 0, '-')`</span> $= \lim\limits_{x \, \uparrow \, 0} \dfrac{1}{x} = -\infty$ <br><br> 
    
    $\phantom{mmmmmmmm.} \Longrightarrow$ Een rechter- of linkerlimiet bij een continue functie wordt vanzelf omgezet naar een continu limiet <br>
    $\phantom{mmmmmmmm.} \Longrightarrow$ Een continu limiet bij een discontinue functie wordt een rechterlimiet <br><br><br><br>

- **Variabele Invullen:** $\phantom{.}$ <span style="font-size: 19px;">`subs(f(x), a)`</span> $= f(a)$ $\phantom{n..n,n}$ $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`subs(x^2 + 3x + 1, 5)`</span> $= \left. x^2 + 3x + 1 \right|_{\substack{ x=5 }} = 41$ <br><br> $\phantom{mmmmmmmn..}$ <span style="font-size: 19px;">`subs(diff(f(x)), a)`</span> $= f'(a)$ $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`subs(diff(x^2 + 3x + 1), 5)`</span> $= \left. \dfrac{d}{d x} \left(x^{2} + 3 x + 1\right) \right|_{\substack{ x=5 }} = 13$ <br><br>

    $\phantom{mmmmmmmm.} \Longrightarrow$ Als je expliciet de variabele wilt benoemen die je vervangt: $\phantom{.}$ <span style="font-size: 19px;">`subs(f(t), t, a)`</span> $= f(a)$<br><br><br><br>

*<span style="font-size: 21px;"><strong>Opmerking:</strong> </span> <span style="font-size: 18px;">In plaats van </span>* <span style="font-size: 19px;">`optie(f(x))`</span> *<span style="font-size: 18px;">kun je ook</span>* <span style="font-size: 19px;">`f(x).optie()`</span> *<span style="font-size: 18px;">gebruiken. Dus:</span>*

- **Afgeleides:** $\phantom{mmm..}$ <span style="font-size: 19px;">`f(x).diff()`</span> $= \dfrac{d}{d x} f{\left(x \right)}$ $\phantom{mm^{..}}$ en $\quad$ <span style="font-size: 19px;">`f(x).diff(2)`</span> $= \dfrac{d^{2}}{d x^{2}} f\left(x \right)$

- **Integralen:** $\phantom{mmm..^.}$ <span style="font-size: 19px;">`f(x).integrate()`</span> $= F(x)$ $\quad$ en $\quad$ <span style="font-size: 19px;">`f(x).integrate((a, b))`</span> $= \int_{a}^{b} f(x) \, dx$

- **Limieten:** $\phantom{mmmm..}$ <span style="font-size: 19px;">`f(x).limit(a)`</span> $= \lim\limits_{x \, \to \, a} f{\left(x \right)}$

- **Variabele Invullen:** $\phantom{.}$ $\phantom{.}$ <span style="font-size: 19px;">`f(x).subs(a)`</span> $= f(a)$

****

## Mogelijke Functies

- **Wortels:**
    + <span style="font-size: 19px;">`sqrt(x)`</span> $= \sqrt{x}; \phantom{m.} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`sqrt(4)`</span> $= \sqrt{4} = 2$
    + <span style="font-size: 19px;">`cbrt(x)`</span> $= \sqrt[3]{x}; \phantom{m.} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`cbrt(8)`</span> $= \sqrt[3]{8} = 2$
    + <span style="font-size: 19px;">`root(x, n)`</span> $= \sqrt[n]{x}; \quad \longrightarrow \quad$ <span style="font-size: 19px;">`root(16, 4)`</span> $= \sqrt[4]{16} = 2$ <br><br>

- **Goniometrische Functies:**
    + <span style="font-size: 19px;">`sin(x)`</span> $= \sin(x)$ met inverse <span style="font-size: 19px;">`arcsin(x)`</span> $= \arcsin(x) \quad$ (op een rekenmachine $\sin^{-1}(x)$)
    + <span style="font-size: 19px;">`cos(x)`</span> $= \cos(x)$ met inverse <span style="font-size: 19px;">`arccos(x)`</span> $= \arccos(x) \quad$ (op een rekenmachine $\cos^{-1}(x)$)
    + <span style="font-size: 19px;">`tan(x)`</span> $= \tan(x)$ met inverse <span style="font-size: 19px;">`arctan(x)`</span> $= \arctan(x) \quad$ (op een rekenmachine $\tan^{-1}(x)$) <br><br>

- **Absolute Waarde:** $\phantom{.}$ <span style="font-size: 19px;">`|x|`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`|-2|`</span> $= |\! - \! 2| = 2$ $\quad$ <br><br>

- **Exponentieel:** $\phantom{m..^.}$ <span style="font-size: 19px;">`e^x`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`e^(2x + 3)`</span> $= e^{2x + 3}$  $\quad$ <br><br>

- **Logaritmes:** 
    + **Grondgetal e:** $\phantom{mm.}$ <span style="font-size: 19px;">`ln(x)`</span> $\phantom{m.^{..}} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`ln(e^4)`</span> $= \ln(e^4) = 4$
    + **Grondgetal 10:** $\phantom{m..}$ <span style="font-size: 19px;">`log(x)`</span> $\phantom{m.} \quad \longrightarrow \quad$ <span style="font-size: 19px;">`log(100)`</span> $= \ ^{10} \! \log(100) = 2$
    + **Ander Grondgetal:** $\phantom{.}$ <span style="font-size: 19px;">`log(x, n)`</span> $\quad \longrightarrow \quad$ <span style="font-size: 19px;">`log(8, 2)`</span> $= \ ^{2} \! \log(8) = 3$

****

## Mogelijke Constantes
- <span style="font-size: 19px;">`pi`</span> $= \pi \approx 3.14159265358979$
- <span style="font-size: 19px;">`e`</span> $= e \approx 2.71828182845905$
- <span style="font-size: 19px;">`inf`</span> $= \infty$
- <span style="font-size: 19px;">`goldenratio`</span> $= \phi \approx 1.61803398874989$
