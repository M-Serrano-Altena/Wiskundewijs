## **Introductie Primitieven**

Een primitieve is eigenlijk precies het omgekeerde van een afgeleide. Stel we hebben bijvoorbeeld de volgende afgeleide:

$$f'(x) = 3x^2$$

En we willen bepalen wat de originele functie $f(x)$ is. Misschien zou je kunnen bedenken dat de functie dat hier bij hoort de volgende vorm heeft:

$$f(x) = x^3,$$

want als we $f(x)$ nu afleiden, dan krijgen we inderdaad $3x^2$. Maar we weten ook dat de afgeleide van een *constante* (dus een los getal zonder $x$) gelijk is aan $0$. We kunnen dus elke willekeurige constante bij $f(x)$ optellen en dan blijft de afgeleide $3x^2$. 

Dus bijvoorbeeld:

$$f_6(x) = x^3 + 6 \longrightarrow f_6'(x) = 3x^2$$

$$f_{13}(x) = x^3 + 13 \longrightarrow f_{13}'(x) = 3x^2$$

Omdat we elk willekeurig getal kunnen toevoegen, schrijven we het algemener op:

$$f(x) = x^3 + c$$

en deze $c$ noemen we de **integratieconstante**.

Wat we net hebben gedaan heet *primitiveren*. We bepalen dan de zogenaamde *primitieve* van een functie. Een primitieve is eigenlijk een functie die met afleiden weer terug gaat naar de originele functie. En we noteren een primitieve met een hoofdletter. Dus als:

$$g(x) = 3x^2,$$

dan is de primitieve:

$$G(x) = x^3 + c.$$

Net zoals bij de afgeleides hebben we bij primitiveren een tabel met veel voorkomende functies en hun primitieven.

???+ Belangrijk
    ### **Tabel met veel voorkomende functies**

    | Functie                            | Primitieve                                   |
    | ---------------------------------- | -------------------------------------------- |
    | $\large{f(x) = 0}$                 | $\large{F(x) = c}$                          |
    | $\large{f(x) = a}$                 | $\large{F(x) = ax + c}$                          |
    | $\large{f(x) = ax^n}$              | $\large{F(x) = \dfrac{1}{n + 1} \cdot ax^{n+1} + c}$           |
    | $\large{f(x) = e^x}$               | $\large{F(x) = e^x + c}$                        |
    | $\large{f(x) = a^x}$               | $\large{F(x) = \dfrac{a^x}{\ln(a)} + c}$         |
    | $\large{f(x) = \dfrac{1}{x}}$      | $\large{F(x) = \ln &#124; x &#124;}$         |
    | $\large{f(x) = \ln(x)}$            | $\large{F(x) = x \ln(x) - x + c}$                |
    | $\large{f(x) = \ ^a \! \log(x)}$   | $\large{F(x) = \dfrac{1}{\ln(a)} \cdot \left(x \ln(x) - x \right) + c}$ |
    | $\large{f(x) = \sin(x)}$           | $\large{F(x) = -\cos(x) + c}$                  |
    | $\large{f(x) = \cos(x)}$           | $\large{F(x) = \sin(x) + c}$                 |

    waarbij $n$ en $a$ constantes zijn (losse getallen zonder $x$). 
    
    $c$ is de zogenaamde *integratieconstante*. Deze constante komt er bij elke functie die je primitiveert erbij. Als we de primitieve zouden afleiden, dan zou deze constante namelijk weer verdwijnen.

    <br>

    ### **Regels**

    Bij primitiveren hebben we geen [productregel](/afgeleide/#regels) of [quotiëntregel](/afgeleide/#regels), maar wel de [somregel](/afgeleide/#regels) en (deels) de omgekeerde [kettingregel](/afgeleide/#regels).

    |               | Functie                            | Primitieve                                                                                            |
    | ------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
    | Somregel      | $\large{f(x) = g(x) + h(x)}$       | $\large{F(x) = G(x) + H(x)}$                                                                       |                                                 |
    | Kettingregel  | $\large{f(x) = f(ax + b)}$           | $\large F(x) = \frac{1}{a} \cdot F(ax + b)$ |

    ***<p style="text-align: left;font-size:17px;">Let op!</p>***
    
    De kettingregel voor primitieven geldt alleen voor lineaire functies als binnenste functie. Er mag namelijk geen extra $x$ term bij komen door de kettingregel. Want door die extra $x$ term zou de afgeleide van deze primitieve niet meer de originele functie zijn.

### **Voorbeelden**

??? example "Voorbeeld 1: Bepaal de primitieve van $f(x) = 2x^2$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = 2x^2$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Deze functie is van de vorm $f(x) = ax^n$, met hier $a=2$ en $n=2$. Om de primitieve te bepalen bij zo'n vorm, moeten we eerst de macht $+1$ doen. Dus de $2$ in de macht wordt nu een $3$. En daarna doen we $1$ gedeeld door deze nieuwe macht ervoor (en vergeet de $+c$ niet):

    $$\large{F(x) = \dfrac{1}{3} \cdot 2 x^3 + c}$$

    Als we dit versimpelen, dan vinden we:

    !!! quote ""
        $$\large{F(x) = \dfrac{2}{3}x^3 + c}$$


??? example "Voorbeeld 2: Bepaal de primitieve van $f(x) = x^3 + 6x - 4$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = x^3 + 6x - 4$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Bij [Regels](#regels) zien we dat we bij primitiveren ook de somregel kunnen gebruiken, net zoals bij afgeleides. We kunnen dus van elke term apart de primitieve bepalen. Bij de eerste twee doen we de macht $+1$ en zetten we een factor $1$ gedeeld door deze nieuwe macht ervoor: <br><br>
    
    - Functie: $\quad x^{3}$ $\qquad \Longrightarrow \qquad$ Primitieve: $\quad \dfrac{1}{4}x^4$
    - Functie: $\quad 6x$ $\qquad \Longrightarrow \qquad$ Primitieve: $\quad \dfrac{1}{2} \cdot 6x^2 = 3x^2$

    <br><br>
    De laatste term is gewoon een constante, dus van de vorm $f(x) = a$. De primitieve van deze vorm is $F(x) = ax$, dus plakken gewoon een $x$ aan het getal vast: <br><br>

    - Functie: $\quad -4$ $\qquad \Longrightarrow \qquad$ Primitieve: $\quad -4x$

    <br><br>
    Als we dit nu allemaal samenvoegen (en $+c$ toevoegen), vinden we:

    !!! quote ""
        $$\large{F(x) = \dfrac{1}{4}x^4 + 3x^2 - 4x + c}$$


??? example "Voorbeeld 3: Bepaal de primitieve van $f(x) = (3x - 7)^2$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = (3x - 7)^2$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen werken we eerst de [haakjes](/basisvaardigheden/#kwadratisch-haakjes-wegwerken) uit:

    $$\large{f(x) = 9x^2 - 42x + 49}$$

    Nu kunnen we de primitieve nemen van de losse termen. Bij de eerste twee termen doen we de macht $+1$ en dan een factor $1$ gedeeld door deze nieuwe macht ervoor. Bij het losse getal voegen we alleen een $x$ toe:

    $$\large{F(x) = \dfrac{1}{3} \cdot 9x^3 - \dfrac{1}{2} \cdot 42x^2 + 49x + c}$$

    Als we dit versimpelen, dan vinden we:

    !!! quote ""
        $$\large{F(x) = 3x^3 - 21x^2 + 49x + c}$$


??? example "Voorbeeld 4: Bepaal de primitieve van $f(x) = 6\sqrt{x}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = 6\sqrt{x}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we het eerst schrijven in de vorm $f(x) = ax^n$. We doen dit door de wortel eerst als macht $\frac{1}{2}$ te schrijven:

    $$\large{f(x) = 6x^{\frac{1}{2}}}$$

    Nu staat de functie wel in de vorm $f(x) = ax^n$. Om deze vorm te primitiveren, doen we de macht $+1$. Dus van een macht $\frac{1}{2}$ gaan we naar een macht $1 \frac{1}{2}$. Daarna zetten we een factor van $1$ gedeeld door deze nieuwe macht ervoor:

    $$\large{F(x) = \dfrac{1}{1 \frac{1}{2}} \cdot 6x^{1 \frac{1}{2}} + c}$$

    Als we dit versimpelen:

    $$\large{F(x) = \dfrac{2}{3} \cdot 6x^{1 \frac{1}{2}} + c}$$

    $$\large{F(x) = 4x^{1 \frac{1}{2}} + c}$$

    We hadden in de vraag geen breuk in de macht, dus dat moeten we weer schrijven met wortels. We hebben een macht $1 \frac{1}{2}$, dus dat kunnen we schrijven als $x \sqrt{x}$. De $x$ komt van de $1$ in de macht, de $\sqrt{x}$ komt van de $\frac{1}{2}$.
    
    We krijgen dus:

    !!! quote ""
        $$\large{F(x) = 4x\sqrt{x} + c}$$


??? example "Voorbeeld 5: Bepaal de primitieve van $f(x) = \dfrac{3x\sqrt{x}}{2x^3}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = \dfrac{3x\sqrt{x}}{2x^3}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit te primitiveren, moeten we deze functie eerst schrijven in de vorm $f(x) = ax^n$. Om dit te doen schrijven we de wortel eerst als een macht $\frac{1}{2}$:

    $$\large{f(x) = \dfrac{3x \cdot x^{\frac{1}{2}}}{2x^3}}$$

    We kunnen nu de $x$ termen in de teller combineren. We hebben twee $x$ termen keer elkaar, dus moeten we de machten bij elkaar op tellen. We weten dat $x = x^1$, dus krijgen we:

    $$\large{f(x) = \dfrac{3x^{1 + \frac{1}{2}}}{2x^3}}$$

    $$\large{f(x) = \dfrac{3x^{1 \frac{1}{2}}}{2x^3}}$$

    Nu kunnen we de twee overige $x$ termen door elkaar delen. Als we twee $x$ termen met elkaar delen, doen we de machten juist min elkaar:

    $$\large{f(x) = \dfrac{3}{2} \cdot x^{1 \frac{1}{2} - 3}}$$

    En nu kunnen we de macht versimpelen:

    $$\large{f(x) = \dfrac{3}{2} x^{-1 \frac{1}{2}}}$$

    Nu staat de functie in de vorm $f(x) = ax^n$ en kunnen we het primitiveren. We doen dan de macht $+1$ en halen een factor $1$ gedeeld door deze nieuwe macht ervoor. We krijgen dus als nieuwe macht $-1\frac{1}{2} + 1 = - \frac{1}{2}$:

    $$\large{F(x) = \dfrac{1}{-\frac{1}{2}} \cdot \dfrac{3}{2} x^{-\frac{1}{2}} + c}$$

    En als we dit versimpelen:

    $$\large{F(x) = -2 \cdot \dfrac{3}{2} x^{-\frac{1}{2}} + c}$$

    $$\large{F(x) = -3x^{-\frac{1}{2}} + c}$$

    We hadden in de vraag geen negatieve of breuk in de macht, dus dat moeten we weer schrijven als breuk en met wortels. We veranderen eerst de '$-$' in de macht met een breuk:

    $$\large{F(x) = -3 \cdot \dfrac{1}{x^{\frac{1}{2}}} + c}$$

    En de macht $\frac{1}{2}$ kunnen we ook schrijven als wortel:

    $$\large{F(x) = -3 \cdot \dfrac{1}{\sqrt{x}} + c}$$

    Als laatst kunnen we nog eventueel de $3$ in de breuk zetten:

    !!! quote ""
        $$\large{F(x) = - \dfrac{3}{\sqrt{x}} + c}$$


??? example "Voorbeeld 6: Bepaal de primitieve van $f(x) = 5\cos(x)$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = 5\cos(x)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    De primitieve van een cosinus kunnen we vinden in de [tabel](#tabel-met-veel-voorkomende-functies). We zien daar dat dit $\sin(x)$ is. In ons geval hebben we nog een factor $5$, maar die kunnen we er gewoon lekker voor laten staan: 

    !!! quote ""
        $$\large{F(x) = 5\sin(x) + c}$$



??? example "Voorbeeld 7: Bepaal de primitieve van $f(x) = \sin(2x)$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = \sin(2x)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    De primitieve van een sinus kunnen we opzoeken in de [tabel](#tabel-met-veel-voorkomende-functies). We zien daar dat dit $-\cos(x)$ is. Om onze functie $\sin(2x)$ te primitiveren, zou onze eerste gok misschien zijn:

    $$\large{\widetilde{F}(x) = -\cos(2x) + c}$$

    Maar als we dit weer gaan afleiden, dan krijgen we door de [kettingregel](/afgeleide/#regels) een extra factor $2$ ervoor:
    
    $$\large{\widetilde{F}'(x) = 2\sin(2x) \neq f(x)}$$
    
    Omdat we deze factor niet willen, moeten we die bij de primitieve weg compenseren door $\frac{1}{2}$ ervoor toe te voegen:

    !!! quote ""
        $$\large{F(x) = -\dfrac{1}{2}\cos(2x) + c}$$

    <br>

    (Nu geldt er namelijk wel weer $F'(x) = f(x)$ )



??? example "Voorbeeld 8: Bepaal de primitieve van $f(x) = e^{4x + 7}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = e^{4x + 7}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben hier te maken met een $e$ macht en we weten dat de afgeleide van een $e$ macht zichzelf is. Dit betekent dus ook dat de primitieve van een $e$ macht zichzelf moet zijn. Dus als eerste gok proberen we:

    $$\large{\widetilde{F}(x) = e^{4x + 7}}$$

    Maar als we deze functie weer afleiden, krijgen we door de [kettingregel](/afgeleide/#regels) een extra factor $4$ ervoor:

    $$\large{\widetilde{F}'(x) = 4 \cdot e^{4x + 7} \neq f(x)}$$

    Omdat we deze factor niet willen, compenseren we hem weg door in de primitieve $\frac{1}{4}$ toe te voegen:

    !!! quote ""
        $$\large{F(x) = \dfrac{1}{4}e^{4x + 7} + c}$$

    (Nu geldt er namelijk wel weer $F'(x) = f(x)$ )


??? example "Voorbeeld 9: Bepaal de primitieve van $f(x) = \dfrac{14}{x}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = \dfrac{14}{x}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    *Let op!* We hebben hier een functie van de vorm $f(x) = \dfrac{1}{x}$, en niet van de vorm $f(x) = ax^n$.
    
    De primitieve van deze vorm kunnen we opzoeken in de [tabel](#tabel-met-veel-voorkomende-functies). We vinden daar dat het $F(x) = \ln|x|$ is. In ons geval hebben we nog een extra factor $14$, maar die kunnen we er gewoon lekker voor laten staan:

    !!! quote ""
        $$\large{F(x) = 14\ln|x|}$$



??? example "Voorbeeld 10: Bepaal de primitieve van $f(x) = \ ^2 \! \log(x)$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = \ ^2 \! \log(x)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Deze functie is van de vorm $f(x) = \ ^a \! \log(x)$, met hier $a=2$. De primitieve van deze vorm kunnen we opzoeken in de [tabel](#tabel-met-veel-voorkomende-functies). Daar vinden we dat het van de vorm $F(x) = \dfrac{1}{\ln(a)} \cdot \left( x \ln(x) - x \right) + c$ is. In ons geval wordt dat dus:

    !!! quote ""
        $$\large{F(x) = \frac{1}{\ln(2)} \cdot \left( x \ln(x) - x \right) + c}$$



??? example "Voorbeeld 11: Bepaal de primitieve van $f(x) = \ln(9x - 2)$"
    **<p style="text-align: center;font-size:20px;">Bepaal de primitieve van de functie $f(x) = \ln(9x - 2)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**


    Deze functie is van de vorm $f(x) = \ln(x)$. In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van deze vorm $F(x) = x \ln(x) - x + c$ is. In ons geval hebben we geen $x$ maar $9x - 2$. We moeten dus alle $x$ in deze vorm vervangen voor $9x - 2$:

    $$\large{\widetilde{F}(x) = (9x - 2) \ln(9x-2) - (9x - 2) + c}$$

    Maar als we dit afleiden, dan zouden we door de [kettingregel](/afgeleide/#regels) een extra factor $9$ krijgen. Om die weg te compenseren, voegen wij een factor $\dfrac{1}{9}$ toe aan onze primitieve:

    $$\large{F(x) = \dfrac{1}{9} \cdot \left( (9x - 2) \ln(9x - 2) - (9x - 2) \right) + c}$$

    Dit kunnen we eventueel nog iets verder versimpelen:

    $$\large{F(x) = (x - \dfrac{2}{9}) \ln(9x - 2) - (x - \dfrac{2}{9}) + c}$$

    Omdat we al de integratieconstante $c$ hebben toegevoegd, kunnen we de $\frac{2}{9}$ op het einde weg laten. De integratieconstante $c$ staat namelijk al voor elk mogelijk getal, dus de extra $\frac{2}{9}$ voegt niks toe:

    !!! quote ""
        $$\large{F(x) = (x - \dfrac{2}{9}) \ln(9x - 2) - x + c}$$

<hr style="height: 1.5px; background-color: #575757; border: none;">