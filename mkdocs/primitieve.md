# *De Primitieve Functie*

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

    Bij primitiveren hebben we geen [productregel](afgeleide.md#regels) of [quotiëntregel](afgeleide.md#regels), maar wel de [somregel](afgeleide.md#regels) en (deels) de omgekeerde [kettingregel](afgeleide.md#regels).

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

    Om dit op te lossen werken we eerst de [haakjes](basisvaardigheden.md#kwadratisch-haakjes-wegwerken) uit:

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

    Om dit te primitieveren, moeten we deze functie eerst schrijven in de vorm $f(x) = ax^n$. Om dit te doen schrijven we de wortel eerst als een macht $\frac{1}{2}$:

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

    Maar als we dit weer gaan afleiden, dan krijgen we door de [kettingregel](afgeleide.md#regels) een extra factor $2$ ervoor:
    
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

    Maar als we deze functie weer afleiden, krijgen we door de [kettingregel](afgeleide.md#regels) een extra factor $4$ ervoor:

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

    Maar als we dit afleiden, dan zouden we door de [kettingregel](afgeleide.md#regels) een extra factor $9$ krijgen. Om die weg te compenseren, voegen wij een factor $\dfrac{1}{9}$ toe aan onze primitieve:

    $$\large{F(x) = \dfrac{1}{9} \cdot \left( (9x - 2) \ln(9x - 2) - (9x - 2) \right) + c}$$

    Dit kunnen we eventueel nog iets verder versimpelen:

    $$\large{F(x) = (x - \dfrac{2}{9}) \ln(9x - 2) - (x - \dfrac{2}{9}) + c}$$

    Omdat we al de integratieconstante $c$ hebben toegevoegd, kunnen we de $\frac{2}{9}$ op het einde weg laten. De integratieconstante $c$ staat namelijk al voor elk mogelijk getal, dus de extra $\frac{2}{9}$ voegt niks toe:

    !!! quote ""
        $$\large{F(x) = (x - \dfrac{2}{9}) \ln(9x - 2) - x + c}$$


## **Introductie Integralen**
We kunnen *integralen* gebruiken om een oppervlakte onder een grafiek te bepalen. Maar hoe werkt het en hoe lossen we zo'n integraal op?

### **Oppervlakte onder een grafiek**

Stel we willen de oppervlakte $V$ bepalen onder deze grafiek, hoe doen we dat?

<figure markdown>
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/Oppervlakte onder de grafiek.svg){ width="500" }
    <figcaption>Figuur 1. Functie geplot met oppervlakte $V$ onder de grafiek.</figcaption>
</figure>

Deze oppervlakte heeft een lastige vorm, dus we kunnen het niet zomaar bepalen door lengte keer breedte te gebruiken... Of toch wel? 

Als we deze oppervlakte $V$ indelen in allemaal kleine rechthoeken, dan kunnen we de oppervlaktes van alle rechthoekjes bij elkaar optellen. En deze totale oppervlakte zou dan hetzelfde zijn als de oppervlakte $V$.

<figure markdown>
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/Oppervlakte onder de grafiek (met 10 rechthoeken).svg){ width="500" }
    <figcaption>Figuur 2. Functie geplot met $10$ rechthoeken onder de grafiek. De breedte van de rechthoeken is $\Delta x$. De hoogte is de waarde van de functie bij de $x$ waar de rechthoek begint.</figcaption>
</figure>

De oppervlakte van één rechthoek kunnen we bepalen door lengte keer breedte te doen. De breedte van alle rechthoeken is hetzelfde, dus die noemen we $\Delta x$. Maar de lengte (hier hoogte) is afhankelijk van welke rechthoek we naar kijken.

Laten we bijvoorbeeld kijken naar het eerste rechthoekje. De hoogte van deze rechthoek is het $y$-coördinaat van de functie bij het begin van deze rechthoek. Dus als de rechthoek begint bij $x_1$, dan is de hoogte $f(x_1)$. De oppervlakte van het eerste rechthoekje wordt dan dus:

$$\textrm{Opp rechthoek 1} = f(x_1) \cdot \Delta x$$

En op dezelfde manier is de oppervlakte van rechthoek $2$:

$$\textrm{Opp rechthoek 2} = f(x_2) \cdot \Delta x$$

En zo kunnen we verder gaan voor de andere rechthoeken. De totale oppervlakte wordt dan:

$$\textrm{Opp alle rechthoeken} = f(x_1) \cdot \Delta x + f(x_2) \cdot \Delta x + f(x_3) \cdot \Delta x \ + \ ...$$

Dit wordt een beetje een gedoe om helemaal uit te schrijven, dus we schrijven het iets korter op:

$$\textrm{Opp alle rechthoeken} = \sum_{i=1}^{10} f(x_i) \cdot \Delta x$$

Hier is $\sum$ het sommatieteken. We zeggen hier dus eigenlijk "verander $i$ steeds van $1$ tot $10$ en tel al deze termen bij elkaar op".

Het enige probleem is dat dit niet helemaal hetzelfde is als oppervlakte $V$ (zie Figuur 2). We hebben namelijk aan de bovenkant een paar stukjes van $V$ niet meegenomen. Het is dus alleen maar een *benadering*.

Maar we kunnen de benadering wel beter maken door meer rechthoeken te gebruiken. Dit zijn er bijvoorbeeld $100$: 

<figure markdown>
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/Oppervlakte onder de grafiek (met 100 rechthoeken).svg){ width="500" }
    <figcaption>Figuur 3. Functie geplot met $100$ rechthoeken onder de grafiek.</figcaption>
</figure>

Dit is bijvoorbeeld al een stuk beter. Het is nog steeds niet precies hetzelfde als oppervlakte $V$, maar we komen steeds meer in de buurt. We hebben nu dus:

$$\textrm{Opp alle rechthoeken} = \sum_{i=1}^{100} f(x_i) \cdot \Delta x$$

Als we meer rechthoekjes gebruiken, wordt de breedte van elke rechthoek ($\Delta x$) ook steeds kleiner. Dus als we deze breedte oneindig klein zouden kunnen maken, dan wordt onze benadering zó goed, dat het eigenlijk geen benadering meer is. 

We kunnen dus de oppervlakte van $V$ bepalen door oneindig veel rechthoeken te gebruiken. Om dit te doen laten we de breedte $\Delta x$ naar $0$ gaan:

$$V = \lim_{\Delta x \ \to \ 0} \ \sum_{i=1}^{n} f(x_i) \cdot \Delta x$$

En dit kunnen we ook noteren als:

$$V = \int_a^b f(x) \, dx$$

We schrijven $dx$ in plaats van $\Delta x$ om aan te geven dat het om een oneindig kleine afstand gaat. $a$ en $b$ zijn hier de grenzen van het oppervlak. Dus $a$ is het $x$-coördinaat van het begin van de oppervlakte, $b$ het $x$-coördinaat van het einde van de oppervlakte. Voor oppervlakte $V$ van Figuur 1 zou dus gelden: $a=9$ en $b=13$.

Deze notatie noemen we een *integraal*. En het mooie van zo'n integraal is dat we nu niet meer de oppervlakte van elke rechthoek apart bij elkaar op hoeven te tellen. Met oneindig veel rechthoeken zou je namelijk een tijdje bezig zijn... <br><br>

### **Integralen Uitwerken**

We kunnen een *integraal* uitwerken door de primitieve te gebruiken. Laten we hiernaar kijken met behulp van een voorbeeld. Stel we hebben bijvoorbeeld de volgende functie:

$$f(x) = 6x^2$$

In Figuur 1 is deze functie geschetst met een oppervlakte $V$ onder deze grafiek. 

<figure markdown>
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = 6x^2.svg){ width="500" }
    <figcaption>Figuur 4. De grafiek $f(x) = 6x^2$ geplot met oppervlakte $V$. Deze oppervlakte onder de functie $f(x)$ gaat van $x=0$ tot $x=1$.</figcaption>
</figure>

Zoals we bij de sectie [Oppervlakte onder een grafiek](#oppervlakte-onder-een-grafiek) hebben gezien, kunnen we de oppervlakte $V$ bepalen met een integraal. Een integraal heeft de volgende vorm:

$$V = \int_a^b f(x) \, dx,$$

waarbij $a$ en $b$ de grenzen zijn van de oppervlakte. Dus in ons geval start de oppervlakte van $V$ bij $x=0$ en eindigt bij $x=1$:

$$V = \int_0^1 f(x) \, dx$$

Nu vullen we $f(x)$ ook in:

$$V = \int_0^1 6x^2 \, dx$$

Nu moeten we de functie *integreren*. Dit is eigenlijk hetzelfde als primitiveren, alleen dan moeten we daarna nog de grenzen invullen:

$$V = \int_a^b f(x) \, dx = \left[ \, F(x) \, \right]_a^b = F(b) - F(a)$$

Laten we dus eerst de functie primitiveren. 

We hebben $6x^2$ als functie en dit is van de vorm $f(x) = ax^n$. Om deze vorm te primitiveren, moeten we de macht $+1$ doen en dan $1$ gedeeld door deze nieuwe macht ervoor zetten. 

We hadden een macht van $2$, dus dat wordt nu een $3$. En we zetten dan een factor $\frac{1}{3}$ ervoor:

$$F(x) = \dfrac{1}{3} \cdot 6 x^{3} + c$$

Als we dit versimpelen, krijgen we:

$$F(x) = 2 x^{3} + c$$

Onze integraal wordt dus:

$$V = \left[ \, 2x^3 + c \, \right]_0^1$$

Nu moeten we de grenzen gaan invullen en min elkaar doen. We krijgen dan dus:

$$V = 2 \cdot 1^3  + c - \left( 2 \cdot 0^3 + c \right)$$

$$V = 2 + c - c$$

We hebben $c - c$, dus dat wordt gewoon $0$:

!!! quote ""
    $$\large{V = 2}$$

<br>

De oppervlakte van $V$ is dus $2$.

Zoals we hier kunnen zien, doen we de $c$'s min elkaar en vallen ze tegen elkaar weg. Dit is altijd het geval bij dit soort integralen met grenzen, dus hoeven we hier de $+c$ term niet op te schrijven. 

Dus:

$$V = \int_0^1 6x^2 \, dx$$

wordt:

$$V = \left[ \, 2x^3 \, \right]_0^1 = 2 \cdot 1^3 - 2 \cdot 0^3 = 2$$


???+ Belangrijk

    #### **<span style="font-size: 18px;">Algemene Vorm</span>**

    Een integraal los je op door de primitieve te bepalen en daarna de grenzen in te vullen: 

    $$\large{V = \int_a^b f(x) \, dx = \left[ \, F(x) \, \right]_a^b = F(b) - F(a)}$$

    Hier zijn $a$ en $b$ de grenzen van de integraal. Dus bij een oppervlakte is $a$ de linkergrens van de oppervlakte, en $b$ de rechtergrens.


??? note "Bepaalde en Onbepaalde Integralen"
    We hebben net gekeken naar *bepaalde* integralen. Dit zijn integralen met grenzen, dus van de vorm:

    $$\large{V = \int_a^b f(x) \, dx = \left[\, F(x) \, \right]_a^b = F(b) - F(a)}$$

    <br>

    We hebben ook *onbepaalde* integralen. Dit zijn integralen zonder grenzen. Dit lijkt misschien ingewikkeld, maar eigenlijk is het gewoon een andere manier om een primitieve op te schijven:

    $$\large{\int f(x) \, dx = F(x)}$$


??? note "Negatieve Integralen"
    Als een oppervlakte onder de $x$-as ligt, geeft dit een negatieve bijdrage aan een integraal. In het voorbeeld hierboven hebben we gezien dat de oppervlakte $V$ van Figuur 4 gelijk aan $2$ is:

    $$\large{V = \int_0^1 6x^2 \, dx = 2}$$

    Maar als we niet $6x$ gebruiken, maar $-6x$, dan wordt onze integraal ook negatief:

    $$\large{V_2 = \int_0^1 -6x^2 \, dx}$$

    $$\large{V_2 = \left[ \, -2x^3 \, \right]_0^1}$$

    $$\large{V_2 = -2 \cdot 1^3 - -2 \cdot 0^3}$$

    $$\large{V_2 = -2}$$

    En als we deze nieuwe functie tekenen, dan zien we dat we precies dezelfde oppervlakte krijgen als net, maar dan nu onder de $x$-as.

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = -6x^2.svg){ width="500" }
        <figcaption>Figuur 5. De grafiek $f(x) = -6x^2$ geplot met oppervlakte $V$. Deze oppervlakte onder de functie $f(x)$ gaat van $x=0$ tot $x=1$.</figcaption>
    </figure>

    <br>

    Dit betekent dus ook dat als we een even grote oppervlakte boven de $x$-as hebben als onder de $x$-as, dat de integraal $0$ wordt.

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = sin(x).svg){ width="500" }
        <figcaption>Figuur 6. De grafiek $f(x) = \sin(x)$ geplot met oppervlakte $I$ en $II$. Samen gaan deze oppervlaktes van $x=-\pi$ tot $x=\pi$. Omdat $I$ boven de $x$-as even groot is als $II$ onder de $x$-as, is de totale oppervlakte $0$.</figcaption>
    </figure>

    ??? abstract "Bewijs dat de totale oppervlakte van Figuur 6 uitkomt op $0$"
        We kunnen dit zelf ook gewoon berekenen met de kennis die we nu hebben. De oppervlakte onder $f(x) = \sin(x)$ gaat van $-\pi$ tot $\pi$. Onze integraal wordt dus:

        $$\large{V = \int_{-\pi}^{\pi} \sin(x) \, dx}$$

        We kunnen in de [tabel](#tabel-met-veel-voorkomende-functies) zien dat de primitieve van $\sin(x)$ is $-\cos(x)$:

        $$\large{V = \left[ \, -\cos(x) \, \right]_{-\pi}^{\pi}}$$

        Nu vullen we de grenzen in:

        $$\large{V = -\cos(\pi) - -\cos(-\pi)}$$

        $$\large{V = -\cos(\pi) + \cos(-\pi)}$$

        We weten dat zowel $\cos(\pi)$ als $\cos(-\pi)$ is $-1$, dus:

        $$\large{V = - -1 + -1}$$

        $$\large{V = 1 - 1}$$

        !!! quote ""
            $$\large{V = 0}$$



#### **<span style="font-size: 21px;">Voorbeelden</span>**

??? example "Voorbeeld 1: Los op $I = \int_1^4 3x \, dx$"
    **<p style="text-align: center;font-size:20px;">Los op $I = \int_1^4 3x \, dx$</p>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we eerst de functie $3x$ primitiveren. Deze functie is van de vorm $f(x) = ax^n$. Om de primitieve van deze vorm te bepalen, doen we de macht $+1$ en zetten $1$ gedeeld door deze nieuwe macht ervoor. We gaan dus van een macht $1$ naar een $2$ en zetten een factor $\frac{1}{2}$ ervoor:

    $$\large{I = \left[ \, \dfrac{1}{2} \cdot 3x^2 \, \right]_1^4}$$

    De integratieconstante $c$ mogen we weglaten omdat het toch wegvalt als we de grenzen invullen. Als we dit verder versimpelen, krijgen we:

    $$\large{I = \left[ \, 1 \dfrac{1}{2} x^2 \, \right]_1^4}$$

    Nu kunnen we de grenzen gaan invullen:

    $$\large{I = 1 \dfrac{1}{2} \cdot 4^2 - 1 \dfrac{1}{2} \cdot 1^2}$$

    En als we dit uitwerken, dan vinden we:

    $$\large{I = 1 \dfrac{1}{2} \cdot 16 - 1 \dfrac{1}{2}}$$

    $$\large{I = 24 - 1 \dfrac{1}{2}}$$

    !!! quote ""
        $$\large{I = 22 \dfrac{1}{2}}$$


??? example "Voorbeeld 2: Los op $I = \int_{-2}^{2} 2x^3 - 6x^2 + x - 3 \, dx$"
    **<p style="text-align: center;font-size:20px;">Los op $I = \int_{-2}^{2} 2x^3 - 6x^2 + x - 3 \, dx$</p>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we eerst de functie primitiveren. 
    
    - De eerste $3$ termen hebben de vorm $f(x) = ax^n$ (we weten namelijk dat $x = x^1$). Dus daar doen we de macht $+1$ en zetten $1$ gedeeld door deze nieuwe macht ervoor. 
    
    - De laatste term is een los getal zonder $x$, dus daar voegen we gewoon een $x$ toe.

    We krijgen dus:

    $$\large{I = \left[ \, \dfrac{1}{4} \cdot 2x^4 + \dfrac{1}{3} \cdot -6x^3 + \dfrac{1}{2} x^2 - 3x \, \right]_{-2}^{2}}$$

    Als we dit versimpelen, krijgen we:

    $$\large{I = \left[ \, \dfrac{1}{2} x^4 - 2x^3 + \dfrac{1}{2} x^2 - 3x \, \right]_{-2}^{2}}$$

    Nu vullen we de grenzen in:

    $$\large{I = \dfrac{1}{2} \cdot 2^4  - 2 \cdot 2^3 + \dfrac{1}{2} \cdot 2^2 - 3 \cdot 2 - \left( \dfrac{1}{2} \cdot (-2)^4 - 2 \cdot (-2)^3 + \dfrac{1}{2} \cdot (-2)^2 - 3 \cdot -2 \right)}$$

    En als we dit uitwerken, krijgen we:

    $$\large{I = \dfrac{1}{2} \cdot 16 - 2 \cdot 8 + \dfrac{1}{2} \cdot 4 - 6 - \left( \dfrac{1}{2} \cdot 16 - 2 \cdot -8 + \dfrac{1}{2} \cdot 4 + 6 \right)}$$

    $$\large{I = 8 - 16 + 2 - 6 - \left( 8 + 16 + 2 + 6 \right)}$$

    $$\large{I = -12 - \left( 32 \right)}$$

    !!! quote ""
        $$\large{I = -44}$$



??? example "Voorbeeld 3: Bereken de oppervlakte van vlakdeel $V$ onder de functie $f(x) = -x^2 + 2x + 3$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = -x^2 + 2x + 3$, de $x$-as en de $y$-as.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$.</span>**

    **<span style="font-size: 17px;">b) De lijn $x=p$ verdeelt $V$ in twee gelijke oppervlaktes. Bepaal $p$ op $3$ decimalen nauwkeurig.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Laten we eerst een schets maken zodat we een beetje de situatie kunnen begrijpen:

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = -x^2 + 2x + 3.svg){ width="500" }
        <figcaption>Figuur 1. De grafiek $f(x) = -x^2 + 2x + 3$ geplot met vlakdeel $V$. Vlakdeel $V$ wordt ingesloten door $f(x)$, de $x$-as en de $y$-as.</figcaption>
    </figure>

    Om de oppervlakte $V$ te bepalen, schrijven we eerst de [algemene vorm](#algemene-vorm) van een integraal op:

    $$\large{V = \int_a^b f(x) \, dx}$$

    Om dit op te lossen moeten we eerst de grenzen bepalen. We weten dat $V$ begint bij de $y$-as, dus bij $x=0.$ Vlakdeel $V$ eindigt bij het rechter snijpunt met de $x$-as, dus die moeten we eerst bepalen.

    De [snijpunten met de $x$-as](kwadratische_vergelijkingen.md#snijpunten-met-de-x-as) bepalen we door de volgende vergelijking op te lossen:

    $$\large{f(x) = 0}$$

    Dus als we $f(x)$ invullen:

    $$\large{-x^2 + 2x + 3 = 0}$$

    Om dit op te lossen, doen we eerst alles keer $-1$:

    $$\large{x^2 - 2x - 3 = 0}$$

    We kunnen dit nu oplossen door het te [ontbinden in factoren](kwadratische_vergelijkingen.md#ontbinden-in-factoren). We moeten dus twee getallen verzinnen die keer elkaar $-3$ zijn en plus elkaar $-2$. 
    
    Na een paar combinaties te proberen, vinden we de factoren $-3$ en $1$. We krijgen dus:

    $$\large{(x - 3)(x + 1) = 0}$$

    Hieruit volgt:

    $$\large{x - 3 = 0 \ \vee \ x + 1 = 0}$$

    $$\large{x = 3 \ \vee \ x = -1}$$

    We wilden het rechter snijpunt weten, dus we gebruiken het snijpunt $x=3$. De grenzen van de integraal zijn dus $a=0$ en $b=3$:

    $$\large{V = \int_0^3 f(x) \, dx}$$

    Nu kunnen we $f(x)$ invullen:

    $$\large{V = \int_0^3 -x^2 + 2x + 3 \, dx}$$

    Dit zijn allemaal termen plus elkaar, dus we kunnen gewoon alle losse termen apart integreren. 
    
    - De eerste twee termen zijn van de vorm $f(x) = ax^n$, want we kunnen $2x$ schrijven als $2x^1$. Om deze vorm te primitiveren, doen we doen we de macht $+1$ en dan $1$ gedeeld door deze nieuwe macht ervoor. 
    
    - De laatste term is alleen een getal, dus daar plakken we gewoon een $x$ aan vast.

    We krijgen dus:

    $$\large{V = \left[ \, -\dfrac{1}{3}x^3 + \dfrac{1}{2} \cdot 2x^2 + 3x \, \right]_0^3}$$

    En als we dit versimpelen:

    $$\large{V = \left[ \, -\dfrac{1}{3}x^3 + x^2 + 3x \, \right]_0^3}$$

    Nu kunnen we de grenzen invullen en min elkaar doen:

    $$\large{V = -\dfrac{1}{3} \cdot 3^3 + 3^2 + 3 \cdot 3 - \left( -\dfrac{1}{3} \cdot 0^3 + 0^2 + 3 \cdot 0 \right)}$$

    Als we dit versimpelen, vinden we:

    $$\large{V = -\dfrac{1}{3} \cdot 27 + 9 + 9 - (0)}$$

    $$\large{V = -9 + 18}$$

    !!! quote ""
        $$\large{V = 9}$$

    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We weten dat de lijn $x=p$ het vlakdeel $V$ verdeelt in twee gelijke oppervlaktes. Laten we dit weer schetsen zodat we de situatie beter kunnen begrijpen:

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = -x^2 + 2x + 3 (gesplitst).svg){ width="500" }
        <figcaption>Figuur 2. De grafiek $f(x) = -x^2 + 2x + 3$ geplot met vlakdeel $V$ verdeelt in $2$ gelijke delen. De twee delen worden gesplitst door de lijn $x=p$.</figcaption>
    </figure>

    We weten uit vraag a) dat de totale oppervlakte $V=9$ is, dus de oppervlakte van $I$ en $II$ zijn beide $4 \frac{1}{2}$:

    $$\large{I = 4\dfrac{1}{2} = II}$$

    We kunnen oppervlakte $I$ ook schrijven als integraal:

    $$\large{I = \int_0^p -x^2 + 2x + 3 \, dx}$$

    Oppervlakte $I$ gaat van $0$ tot $p$, dus vandaar dat dat ook de grenzen in de integraal zijn. We gebruiken hier oppervlakte $I$ om $p$ te bepalen, maar we hadden ook oppervlakte $II$ kunnen gebruiken. Het enige verschil is dat de grenzen dan niet van $0$ tot $p$ zouden gaan, maar van $p$ tot $3$. 
    
    Omdat we net gezegd hebben dat $I = 4 \dfrac{1}{2}$, krijgen we de volgende vergelijking:

    $$\large{\int_0^p -x^2 + 2x + 3 \, dx = 4 \dfrac{1}{2}}$$

    We kunnen nu de functie integreren (zie eventueel weer vraag a) ):

    $$\large{\left[ \, -\dfrac{1}{3} x^3 + x^2 + 3x \, \right]_0^p = 4 \dfrac{1}{2}}$$

    Nu vullen we de grenzen in:

    $$\large{-\dfrac{1}{3} p^3 + p^2 + 3p - \left( -\dfrac{1}{3} 0^3 + 0^2 + 30 \right) = 4 \dfrac{1}{2}}$$

    $$\large{-\dfrac{1}{3} p^3 + p^2 + 3p = 4 \dfrac{1}{2}}$$

    Dit is een vergelijking met een derdemacht, dus dit is lastig om met de hand op te lossen. Maar gelukkig stond er in de vraag geen algebraïsch of exact, dus mogen we het met onze grafische rekenmachine oplossen.

    We voeren in:

    $$\large{\left\{ \begin{array}{ l l } y_1 = -\dfrac{1}{3} x^3 + x^2 + 3x  \\ y_2 = 4 \dfrac{1}{2} \end{array} \right.}$$

    De optie intersect geeft:

    $$\large{\left\{ \begin{array}{ l l l } x_1 = -2.563913...  \\ x_2 = 1.209095... \\ x_3 = 4.354817... \end{array} \right.}$$

    We hebben hier $3$ oplossingen, maar welke van deze $3$ oplossingen is $p$? 
    
    We weten dat $p$ in het vlakdeel $V$ ligt, dus het moet een waarde tussen $0$ en $3$ zijn. Als we kijken naar de $3$ oplossingen, dan zien we dat alleen $x_2$ tussen $0$ en $3$ ligt. Oftewel:
    
    $$\large{p = 1.209095...}$$
    
    We moesten afronden op $3$ decimalen, dus we krijgen als eindantwoord:

    !!! quote ""
        $$\large{p \approx 1.209}$$


    
??? example "Voorbeeld 4: Bereken exact de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \cos(x)$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \cos(x)$, de lijn $x = \frac{1}{6} \pi$ en de lijn $x = p$, met $\frac{1}{6} \pi < p < \pi$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$ voor $p = \frac{2}{3} \pi$.</span>**

    **<span style="font-size: 17px;">b) Bepaal $p$ als $V$ precies $\dfrac{1}{2}$ is.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Als eerst maken we een schets om de situatie beter te kunnen begrijpen:

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = cos(x).svg){ width="500" }
        <figcaption>Figuur 3. De grafiek $f(x) = \cos(x)$ geplot met vlakdeel $V$. Het vlakdeel $V$ gaat van $x = \frac{1}{6} \pi$ tot $x = \frac{2}{3} \pi$.</figcaption>
    </figure>

    Om de oppervlakte van $V$ te berekenen moeten we de volgende integraal opstellen:

    $$\large{V = \int_{\frac{1}{6} \pi}^{\frac{2}{3} \pi} \cos(x) \, dx}$$

    In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van $\cos(x)$ is $\sin(x)$:

    $$\large{V = \left[ \, \sin(x) \, \right]_{\frac{1}{6} \pi}^{\frac{2}{3} \pi}}$$ 

    Nu vullen we de grenzen in:

    $$\large{V = \sin(\frac{2}{3} \pi) - \sin(\frac{1}{6} \pi)}$$ 

    En als we dit uitwerken, vinden we:

    !!! quote ""
        $$\large{V = \dfrac{1}{2} \sqrt{3} - \dfrac{1}{2}}$$

    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    Nu hebben willen we $p$ weten wanneer er geldt dat $V=\frac{1}{2}$. We hebben de integraal bij a) al berekend, we moeten alleen de grenzen nog aanpassen. De nieuwe grenzen die we nu hebben zijn $x = \frac{1}{6} \pi$ en $x = p$:

    $$\large{V = \int_{\frac{1}{6} \pi}^{p} \cos(x) \, dx}$$

    $$\large{V = \left[ \, \sin(x) \, \right]_{\frac{1}{6} \pi}^{p}}$$ 

    Nu vullen we deze grenzen in:

    $$\large{V = \sin(p) - \sin(\frac{1}{6} \pi)}$$ 

    En als we dit versimpelen:

    $$\large{V = \sin(p) - \frac{1}{2}}$$

    We wilden $p$ weten wanneer $V = \frac{1}{2}$, dus moeten we de volgende vergelijking oplossen:

    $$\large{\sin(p) - \frac{1}{2} = \frac{1}{2}}$$

    We halen eerst alle getallen naar rechts door aan beide kanten $+\frac{1}{2}$ te doen:

    $$\large{\sin(p) = 1}$$

    Om dit op te lossen moeten we eerst aan beide kanten een sinus hebben. We kunnen op de [eenheidscirkel](goniometrie.md#de-eenheidscirkel) aflezen dat bij $\frac{1}{2} \pi$ de sinus $1$ is, dus:

    $$\large{\sin(p) = \sin(\frac{1}{2} \pi)}$$

    Nu kunnen we de [algemene oplossing](goniometrie.md) gebruiken voor een sinus:

    $$\large{p = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ p = \pi - \frac{1}{2} \pi + k \cdot 2 \pi}$$

    $$\large{p = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ p = \frac{1}{2} \pi + k \cdot 2 \pi}$$

    In dit geval hebben we twee keer dezelfde set oplossingen, dus dit wordt gewoon:

    $$\large{p = \frac{1}{2} \pi + k \cdot 2 \pi}$$

    We hadden in de vraag gegeven gekregen dat $p$ tussen $\frac{1}{6} \pi$ en $\pi$ ligt. Dit betekent dus dat we moeten kijken welke gehele getallen $k$ kan zijn zodat de oplossing tussen $\frac{1}{6} \pi$ en $\pi$ ligt. 
    
    In dit geval hebben we alleen maar $1$ oplossing bij $k=0$:

    !!! quote ""
        $$\large{p = \frac{1}{2} \pi}$$ 



??? example "Voorbeeld 5: Bereken de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \dfrac{2}{x}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \dfrac{2}{x}$, de $x$-as, de lijn $x=-1$ en de lijn $x=p$, met $p < -1$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$ met $p = 1000$.</span>**

    **<span style="font-size: 17px;">b) Bepaal de factor waarmee $p$ moet toenemen om de oppervlakte van $V$ te verdubbelen.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Laten we als eerst een schets maken om de situatie beter te kunnen begrijpen:

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = 2 !divide! x.svg){ width="500" }
        <figcaption>Figuur 4. De grafiek $f(x) = \dfrac{1}{x}$ geplot met vlakdeel $V$. Het vlakdeel $V$ gaat van $x = -1000$ (te groot om weer te geven in de schets) tot $x = -1$.</figcaption>
    </figure>

    Om dit op te lossen moeten we eerst de integraal opstellen. We hebben de grenzen al gekregen, dus onze integraal wordt:

    $$\large{V = \int_{-1000}^{-1} \dfrac{2}{x} \, dx}$$
    
    In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van $\dfrac{1}{x}$ is $\ln|x|$. Nu hebben we nog een extra factor $2$, maar die kunnen we er gewoon voor laten staan:

    $$\large{V = \left[ \, 2\ln|x| \, \right]_{-1000}^{-1}}$$

    Als we de grenzen invullen, krijgen we:

    $$\large{V = 2\ln|-1| \ - \ 2\ln|-1000|}$$

    En nu zien we waarom de absolute waarde nemen hier zo belangrijk is. Want een logaritme van een negatief getal bestaat niet. Maar gelukkig maakt de absolute waarde het weer positief:

    $$\large{V = 2\ln(1) - 2\ln(1000)}$$

    Het logaritme van $1$ is altijd $0$ (want $e^0$ is $1$), dus we kunnen dit versimpelen naar:

    $$\large{V = -2\ln(1000)}$$

    We kunnen eventueel de $1000$ nog schrijven als $10^3$ en dan de derde macht uit de $\ln$ halen:

    $$\large{V = 3\cdot -2\ln(10)}$$

    !!! quote ""
        $$\large{V = -6\ln(10)}$$

    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We willen dat de oppervlakte van $V$ verdubbelt, dus onze nieuwe oppervlakte wordt:

    $$\large{V = 2 \cdot -6\ln(10)}$$

    $$\large{V = -12\ln(10)}$$

    We willen dus bepalen bij welke $p$ een grens van $x=p$ een oppervlakte geeft van $V = -12\ln(10)$.
    
    We hebben de integraal bij a) al berekend, alleen laten we de $p$ nu staan in plaats van $-1000$ in te vullen:

    $$\large{V = \int_{p}^{-1} \dfrac{2}{x} \, dx}$$

    $$\large{V = \left[ \, 2\ln|x| \, \right]_{p}^{-1}}$$

    Nu vullen we deze grenzen in:

    $$\large{V = 2\ln|-1| \ - \ 2\ln|p|}$$

    We weten dat $\ln(1)$ is $0$, dus dit kunnen we versimpelen naar:

    $$\large{V = -2\ln|p|}$$

    En nu kunnen we zeggen dit gelijk moet zijn aan de $-12\ln(10)$ die we net hebben berekend:

    $$\large{-2\ln|p| = -12\ln(10)}$$

    En deze vergelijking kunnen we gaan oplossen om $p$ te bepalen. We beginnen met aan beide kanten te delen door $-2$:

    $$\large{\ln|p| = 6\ln(10)}$$

    Om de logaritmes weg te werken, stoppen we de $6$ eerst in de logaritme als macht:

    $$\large{\ln|p| = \ln(10^6)}$$

    Nu kunnen we de logaritme aan beide kanten weghalen:
    
    $$\large{|p| = 10^6}$$

    We hebben nu dat $|p|$ gelijk is aan $10^6$, dus dit betekent dat er twee opties zijn:

    $$\large{p = 10^6 \ \vee \ p = -10^6}$$

    We hebben in de vraag gekregen dat $p < 1$, dus de juiste oplossing is:

    $$\large{p = -10^6}$$

    $$\large{p = -1 \, 000 \, 000}$$

    We moesten in de vraag bepalen met welke factor $p$ groter werd. $p$ is van $-1000$ naar $-1 \, 000 \, 000$ gegaan, en dit is een toename van een factor $1000$. Dus we krijgen als eindantwoord:

    !!! quote ""
        $$\large{\textrm{Toename met een factor } 1000}$$ 


??? example "Voorbeeld 6: Bereken exact de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \sqrt{x}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \sqrt{x}$, de $x$-as en de lijn $x = p$, met $p > 1$. Vlakdeel $W$ wordt ingesloten door de grafiek van $f(x)$, de $x$-as, de lijn $x=2$ en de lijn $x = 2p$</p>*

    <br>

    **<span style="font-size: 17px;"> Bereken exact de oppervlakte van vlakdeel $V$ als vlakdeel $W$ een factor $\sqrt{2}$ groter is dan $V$.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    Als eerst is het handig om een schets te maken, zodat we beter kunnen begrijpen wat we moeten doen:

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = sqrt(x).svg){ width="500" }
        <figcaption>Figuur 5. De grafiek $f(x) = \sqrt{x}$ geplot met vlakdeel $V$ en $W$. Vlakdeel $W$ is $\sqrt{2}$ keer groter dan vlakdeel $V$.</figcaption>
    </figure>

    Laten we eerst de oppervlakte van vlakdeel $V$ uitdrukken in $p$. Vlakdeel $V$ ligt tussen $x=0$ en $x=p$:

    $$\large{V = \int_0^p \sqrt{x} \, dx}$$

    Om dit op te lossen, willen we $\sqrt{x}$ eerst schrijven in de vorm $f(x) = ax^n$. We doen dit door de wortel te schrijven als een macht $\frac{1}{2}$:

    $$\large{V = \int_0^p x^{\frac{1}{2}} \, dx}$$

    Nu staat het in de vorm $f(x) = ax^n$ en kunnen we het gaan integreren. We doen dan de macht $+1$ en zetten $1$ gedeeld door deze nieuwe macht ervoor:

    $$\large{V = \left[ \, \dfrac{1}{1 \frac{1}{2}} \cdot x^{1\frac{1}{2}} \, \right]_0^p}$$

    En dit kunnen we versimpelen naar:

    $$\large{V = \left[ \, \dfrac{2}{3} x^{1\frac{1}{2}} \, \right]_0^p}$$

    Nu vullen we de grenzen in:

    $$\large{V = \dfrac{2}{3} p^{1\frac{1}{2}} - \dfrac{2}{3} \cdot 0^{1\frac{1}{2}}}$$

    $$\large{\boxed{V = \dfrac{2}{3} p^{1\frac{1}{2}}}}$$

    Nu doen we hetzelfde met de oppervlakte van $W$. Het is dezelfde functie, maar dan met andere grenzen. De grenzen gaan nu van $x=2$ tot $x=2p$:

    $$\large{W = \int_2^{2p} x^{\frac{1}{2}} \, dx}$$

    $$\large{W = \left[ \, \dfrac{2}{3} x^{1\frac{1}{2}} \, \right]_2^{2p}}$$

    En nu vullen we weer de grenzen in:

    $$\large{W = \dfrac{2}{3} (2p)^{1\frac{1}{2}} - \dfrac{2}{3} \cdot 2^{1\frac{1}{2}}}$$

    Als we dit versimpelen, krijgen we:

    $$\large{\boxed{W = \dfrac{4\sqrt{2}}{3} p^{1\frac{1}{2}} - \dfrac{4\sqrt{2}}{3}}}$$

    Nu dat we $V$ en $W$ hebben uitgedrukt in $p$, kunnen we een vergelijking opstellen. We weten namelijk dat:

    $$\large{W = \sqrt{2} \cdot V}$$

    Nu kunnen we allebei de oppervlaktes invullen en de vergelijking oplossen om $p$ te vinden:

    $$\large{\dfrac{4\sqrt{2}}{3} p^{1\frac{1}{2}} - \dfrac{4\sqrt{2}}{3} = \sqrt{2} \cdot \dfrac{2}{3} p^{1\frac{1}{2}}}$$

    $$\large{\dfrac{4\sqrt{2}}{3} p^{1\frac{1}{2}} - \dfrac{4\sqrt{2}}{3} = \dfrac{2\sqrt{2}}{3} p^{1\frac{1}{2}}}$$

    Nu kunnen we de termen met $p$ aan de linkerkant zetten en het getal rechts:

    $$\large{\dfrac{4\sqrt{2}}{3} p^{1\frac{1}{2}} - \dfrac{2\sqrt{2}}{3} p^{1\frac{1}{2}} = \dfrac{4\sqrt{2}}{3}}$$

    De ene term met $p^{1 \frac{1}{2}}$ heeft een factor $\frac{4\sqrt{2}}{3}$ en de andere heeft een factor $\frac{2\sqrt{2}}{3}$. Het enige verschil is dus dat de ene een $4$ heeft en de andere een $2$, dus we kunnen ze gewoon samenvoegen door $4 - 2$ te doen:

    $$\large{\dfrac{2\sqrt{2}}{3} p^{1\frac{1}{2}} = \dfrac{4\sqrt{2}}{3}}$$

    Nu delen we beide kanten door $\frac{2\sqrt{2}}{3}$:

    $$\large{p^{1\frac{1}{2}} = 2}$$

    We kunnen nu $p$ vrijmaken door beide kanten tot de macht $\dfrac{1}{1 \frac{1}{2}}$ te doen:

    $$\large{p = 2^{\frac{1}{1 \frac{1}{2}}}}$$

    Dit kunnen we nog versimpelen naar:

    $$\large{p = 2^{\frac{2}{3}}}$$

    Nu dat we $p$ hebben gevonden, kunnen we het in de formule voor $V$ stoppen om de oppervlakte van $V$ te bepalen:

    $$\large{V = \dfrac{2}{3} \cdot \left( 2^{\frac{2}{3}} \right)^{1\frac{1}{2}}}$$

    En als we dit uitwerken, vinden we:

    $$\large{V = \dfrac{2}{3} \cdot 2}$$

    !!! quote ""
        $$\large{V = 1 \dfrac{1}{3}}$$



??? example "Voorbeeld 7: Bereken de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$, de $x$-as en de buitenste twee snijpunten met de $x$-as.</p>*

    <br>

    **<span style="font-size: 17px;">Bereken de oppervlakte van $V$ op $2$ decimalen nauwkeurig.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Laten we eerst beginnen met het maken van een schets, zodat we de situatie een beetje kunnen begrijpen:

    <figure markdown>
    ![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = (4x-7)^3 -10x + 18.svg){ width="500" }
        <figcaption>Figuur 6. De grafiek $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$ geplot met vlakdeel $V$. Vlakdeel $V$ ligt tussen de buitenste twee snijpunten met de $x$-as.<figcaption>
    </figure>

    Om de oppervlakte $V$ te kunnen bepalen, moeten we eerst de grenzen weten. En we komeh hier achter door de [snijpunten met de $x$-as](kwadratische_vergelijkingen.md#snijpunten-met-de-x-as) te bepalen. We moeten dan de volgende vergelijkingen oplossen:

    $$\large{f(x) = 0}$$
    
    En als we $f(x)$ invullen:

    $$\large{\left( 4x - 7 \right)^3 - 10x + 18 = 0}$$

    In de vraag staat geen algebraïsch of exact, dus we mogen onze grafische rekenmachine gebruiken om dit op te lossen.

    We voeren in:

    $$\large{\left\{ \begin{array}{ l l } y_1 = \left( 4x - 7 \right)^3 - 10x + 18  \\ y_2 = 0 \end{array} \right.}$$

    De optie intersect geeft:

    $$\large{\left\{ \begin{array}{ l l l } x_1 \approx 1.33175  \\ x_2 \approx 1.80084 \\ x_3 \approx 2.1174 \end{array} \right.}$$

    De buitenste twee snijpunten zijn dus $x_1 \approx 1.33175$ en $x_3 \approx 2.1174$. Dit zijn dus ook onze grenzen. 
    
    Hiermee kunnen we nu de integraal opstellen:

    $$\large{V = \int_{1.33175}^{2.1174} \left( 4x - 7 \right)^3 - 10x + 18} \, dx$$ 

    Nu moeten we deze functie primitiveren. 
    
    - De eerste twee termen zijn van de vorm $f(x) = ax^n$. Om de primitieve te bepalen van deze vorm, moeten we de macht $+1$ doen en $1$ gedeeld door deze nieuwe macht ervoor zetten. 
    
    - De laatste term is gewoon een constante (getal zonder $x$), dus daar plakken we gewoon een $x$ aan vast.

    We krijgen dus:

    $$\large{\widetilde{V} = \left[ \, \dfrac{1}{4} \left( 4x - 7 \right)^4 - \dfrac{1}{2} \cdot 10x^2 + 18x \, \right]_{1.33175}^{2.1174}}$$ 

    Maar als we de eerste term zouden afleiden, dan krijgen we door de productregel een extra factor $4$. Omdat we die factor niet willen hebben, moeten we bij de primitieve deze weg compenseren door een extra factor $\frac{1}{4}$ toe te voegen:

    $$\large{V = \left[ \, \dfrac{1}{4} \cdot \dfrac{1}{4} \left( 4x - 7 \right)^4 - \dfrac{1}{2} \cdot 10x^2 + 18x \, \right]_{1.33175}^{2.1174}}$$ 

    Dit kunnen we nog iets versimpelen:

    $$\large{V = \left[ \, \dfrac{1}{16} \left( 4x + 7 \right)^4 - 5x^2 + 18x \, \right]_{1.33175}^{2.1174}}$$

    Nu moeten we de grenzen invullen en min elkaar doen:

    $$\large{V = \dfrac{1}{16} \left( 4 \cdot 2.1174 - 7 \right)^4 - 5 \cdot 2.1174^2 + 18 \cdot 2.1174 - \left( \dfrac{1}{16} \left( 4 \cdot 1.33175 - 7 \right)^4 - 5 \cdot 1.33175^2 + 18 \cdot 1.33175 \right)}$$

    En als we dit uitrekenen met een rekenmachine, dan vinden we:

    $$\large{V = 0.3944768187654191...}$$

    We moesten dit op twee decimalen nauwkeurig schrijven, dus ons eindantwoord wordt:

    !!! quote ""
        $$\large{V \approx 0.39}$$



## **Oppervlakte tussen twee grafieken**

We hebben net gekeken naar oppervlaktes onder allemaal verschillende grafieken. Maar kunnen we ook een oppervlakte bepalen dat tussen twee grafieken ligt? 

Laten we kijken naar de volgende functies:

$$\large{\left\{ \begin{array}{ l l } f(x) =  6 - x^2  \\ g(x) = x + 4 \end{array} \right.}$$

Stel dat we de oppervlakte tussen deze twee functies willen bepalen, hoe pakken we dat aan?

In Figuur 1 hieronder zijn de twee functies geplot met het vlakdeel $V$ dat tussen de twee functies in ligt:

<figure markdown>
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = 6 - x^2; g(x) = x + 4.svg){ width="500" }
    <figcaption>Figuur 1. Grafiek geplot met de functies $f(x) =  6 - x^2$ en $g(x) = x + 4$. Vlakdeel $V$ ligt tussen de twee functies in.<figcaption>
</figure>

We kunnen de oppervlakte van $V$ berekenen door de oppervlakte onder $f(x)$ min de oppervlakte onder $g(x)$ te doen. Kijk maar naar deze twee oppervlaktes:

<figure markdown>
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = 6 - x^2; g(x) = x + 4 (Opp I).svg){ width="500" }
![Functie met oppervlakte V onder de grafiek](assets/images/primitieven/f(x) = 6 - x^2; g(x) = x + 4 (Opp II).svg){ width="500" }
    <figcaption>Figuur 2. Grafiek geplot met de functies $f(x) =  6 - x^2$ en $g(x) = x + 4$. Vlakdeel $I$ is de oppervlakte onder $f(x)$, vlakdeel $II$ is de oppervlakte onder $g(x)$.<figcaption>
</figure>

Als we deze twee oppervlaktes min elkaar doen, houden we alleen maar het gedeelte van $I$ over dat boven $g(x)$ ligt. En dat is precies vlakdeel $V$ van Figuur 1. We kunnen dus schrijven:

$$V = I - II$$

En de oppervlaktes van $I$ en $II$ kunnen we gewoon bepalen met integralen. We zien in Figuur 2 dat beide oppervlaktes dezelfde grenzen hebben, namelijk de snijpunten tussen de twee functies. We kunnen aflezen dat dit de punten $x=-1$ en $x=2$ zijn. Onze integralen worden dan:

$$I = \int_{-1}^2 f(x) \, dx$$

$$II = \int_{-1}^2 g(x) \, dx$$

Met deze informatie kunnen we een vergelijking voor $V$ opstellen:

$$V = \int_{-1}^2 f(x) \, dx - \int_{-1}^2 g(x) \, dx$$

En omdat deze twee integralen dezelfde grenzen hebben, kunnen we het [schrijven als $1$ integraal](#twee-integralen-combineren):

$$\boxed{V = \int_{-1}^2 \left( f(x) - g(x) \right) \, dx}$$

Dit is dus de integraal om een oppervlakte tussen twee functies te bepalen. 

Laten we nu $f(x)$ en $g(x)$ invullen:

$$V = \int_{-1}^2 \left( 6 - x^2 - \left( x+4 \right) \right) \, dx$$

En als we dit versimpelen:

$$V = \int_{-1}^2 \left( 6 - x^2 - x - 4 \right) \, dx$$

$$V = \int_{-1}^2 \left(- x^2 - x + 2 \right) \, dx$$

Nu kunnen we deze functie gaan integreren:

- De eerste twee termen zijn van de vorm $f(x) = ax^n$ (want we kunnen de $x$ term schrijven als $x^1$). Om deze vorm te primitiveren, moeten we de macht $+1$ doen. Daarna zetten we een factor van $1$ gedeeld door deze niuwe macht vóór de term.

- De laaste term is een constante (een los getal zonder $x$). Om een constante te primitiveren, moeten we er gewoon een $x$ aanvast plakken.

Als we dit gebruiken, dan krijgen we:

$$V = \left[- \dfrac{1}{3}x^3 - \dfrac{1}{2} x^2 + 2x \right]_{-1}^2$$

Nu vullen we de grenzen in:

$$V = - \dfrac{1}{3} \cdot 2^3 - \dfrac{1}{2} \cdot 2^2 + 2 \cdot 2 - \left(- \dfrac{1}{3} \cdot (-1)^3 - \dfrac{1}{2} \cdot (-1)^2 + 2 \cdot -1 \right)$$

En als we dit uitwerken, dan krijgen we:

$$V = - \dfrac{1}{3} \cdot 8 - \dfrac{1}{2} \cdot 4 + 4 - \left(- \dfrac{1}{3} \cdot -1 - \dfrac{1}{2} \cdot 1 - 2 \right)$$

$$V = - 2\dfrac{2}{3} - 2 + 4 - \left(\dfrac{1}{3} - \dfrac{1}{2} - 2 \right)$$

$$V = -\dfrac{2}{3} - \left(- 2 \dfrac{1}{6} \right)$$

$$V = -\dfrac{2}{3} + 2 \dfrac{1}{6}$$

!!! quote ""
    $$\large{V = 1 \dfrac{1}{2}}$$


??? abstract "Oppervlaktes $I$ en $II$ los berekenen en dan min elkaar"
    We kunnen om te controleren in het voorbeeld hierboven oppervlaktes $I$ en $II$ apart berekenen en daarna min elkaar doen. Dan kunnen we controleren of we weer uitkomen op $V = 1 \frac{1}{2}$.

    We beginnen met het bepalen van de oppervlakte van $I$. We hadden deze integraal gevonden:

    $$\large{I = \int_{-1}^2 f(x) \, dx}$$

    Nu vullen we $f(x)$ in:

    $$\large{I = \int_{-1}^2 6 - x^2 \, dx}$$

    Nu kunnen we deze functie integreren:

    - De eerste term is een constante, dus om de primitieve te bepalen moeten we gewoon een $x$ toevoegen.

    - De tweede term is van de vorm $f(x) = ax^n$. Om de primitieve van deze vorm te bepalen, moeten we eerst de macht $+1$ doen, dus van een macht $2$ naar $3$. Daarna zetten we $1$ gedeeld door deze nieuwe macht ervoor, dus een factor $\frac{1}{3}$ in dit geval.

    Als we dit toepassen, dan krijgen we:

    $$\large{I = \left[ \, 6x - \dfrac{1}{3} x^3 \, \right]_{-1}^2}$$

    Nu vullen we de grenzen in:

    $$\large{I = 6 \cdot 2 - \dfrac{1}{3} \cdot 2^3 - \left( 6 \cdot -1 - \dfrac{1}{3} \cdot (-1)^3 \right)}$$

    En als we dit uitwerken, vinden we:

    $$\large{I = 12 - \dfrac{1}{3} \cdot 8 - \left( -6 - \dfrac{1}{3} \cdot -1 \right)}$$

    $$\large{I = 12 - 2 \dfrac{2}{3} - \left( -6 + \dfrac{1}{3} \right)}$$
    
    $$\large{I = 9 \dfrac{1}{3} - \left( -5 \dfrac{2}{3} \right)}$$

    $$\large{\boxed{I = 15}}$$

    <br>

    En nu kunnen we hetzelfde doen voor oppervlakte $II$. We stellen eerst weer de integraal op:

    $$\large{II = \int_{-1}^2 g(x) \, dx}$$

    $$\large{II = \int_{-1}^2 x + 4 \, dx}$$

    We hebben weer een term van de vorm $f(x) = ax^n$ een een constante. De primitieve wordt dus:

    $$\large{II = \left[ \,  \dfrac{1}{2} x^2 + 4x \, \right]_{-1}^2}$$

    Nu vullen we weer de grenzen in:

    $$\large{II = \dfrac{1}{2} \cdot 2^2 + 4 \cdot 2 - \left( \dfrac{1}{2} \cdot (-1)^2 + 4 \cdot -1 \right)}$$

    En als we dit uitwerken, vinden we:

    $$\large{II = \dfrac{1}{2} \cdot 4 + 8 - \left( \dfrac{1}{2} - 4 \right)}$$

    $$\large{II = 2 + 8 - \left( \dfrac{1}{2} - 4 \right)}$$

    $$\large{II = 10 - \left( -3 \dfrac{1}{2} \right)}$$

    $$\large{\boxed{II = 13 \dfrac{1}{2}}}$$

    En nu kunnen we uiteindelijk $V$ bepalen door deze twee oppervlaktes min elkaar te doen:

    $$\large{V = I - II}$$

    $$\large{V = 15 - 13 \dfrac{1}{2}}$$
    
    En als we dit uitwerken vinden we inderdaad wat we eerst ook gevonden hadden:

    !!! quote ""
        $$\large{V = 1\dfrac{1}{2}}$$





??? abstract "Bewijs: Twee integralen combineren"
    ### **Twee integralen combineren**

    We kunnen twee integralen met dezelfde grenzen samenvoegen tot $1$ integraal:

    $$\large{I = \int_{a}^{b} f(x) \, dx - \int_{a}^{b} g(x) \, dx}$$

    $$\large{I = \left[ \, F(x) \, \right]_{a}^{b} - \left[ \, G(x) \, \right]_{a}^{b}}$$

    $$\large{I = F(b) - F(a) - \left( G(b) - G(a) \right)}$$

    $$\large{I = F(b) - F(a) - G(b) + G(a)}$$

    $$\large{I = F(b) - G(b) - F(a) + G(a)}$$

    $$\large{I = F(b) - G(b) - \left( F(a) - G(a) \right)}$$

    $$\large{I = \left[ \, F(x) - G(x) \, \right]_{a}^{b}}$$

    $$\large{I = \int_{a}^{b} \left( f(x) - g(x) \right) \, dx }$$





## **Inhoud Bepalen**

