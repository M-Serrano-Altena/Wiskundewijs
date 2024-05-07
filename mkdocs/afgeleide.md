# *De Afgeleide Functie*

## **Introductie Afgeleide**

De afgeleide van een functie geeft je op elk $x$-coördinaat de bijbehorende *richtingscoëfficient*.* De functie geeft dan dus niet meer het $y$-coördinaat als je $x$ invult, maar de helling van de grafiek op dat punt. Laten we naar een paar verschillende functies kijken.

*<div> * Richtingscoëfficient is een ander woord voor helling.</div>*

### **Parabool**
Een parabool heeft in het simpleste geval de vorm

$$f(x) = x^2.$$

[Straks](#voorbeelden) zullen we zien dat de afgeleide van deze functie is:

$$f'(x) = 2x.$$ 

$f'(x)$ geeft hier dus aan dat het gaat om de afgeleide van de functie $f(x)$. Er zijn veel verschillende manieren om afgeleides weer te geven. Bij de opmerking over de [notatie](#notatie) zie je de meest gebruikte notaties.

In het onderstaande filmpje kun je zien dat de afgeleide gelijk is aan de helling op elk punt. 

???+ video
    <video controls>
    <source src="../assets/videos/Parabola.mp4" type="video/mp4">
    </video>

    *<p style="text-align: center;">Filmpje: Visuele weergave van de afgeleide van de functie $f(x) = x^2$. Bij de top is de helling gelijk aan $0$. </p>*

In het filmpje kunnen we iets interessants zien. Bij de top van de functie kunnen we zien dat de helling $0$ is. Dit betekent dus ook dat de afgeleide gelijk is $0$. En dit blijkt altijd het geval te zijn voor alle toppen. Dus als we de coördinaten van een top willen bepalen, moeten we de afgeleide gelijk stellen aan $0$:

$$f'(x) = 0.$$

Als we deze vergelijking dus oplossen, vinden we het $x$-coördinaat van de top. En als we deze $x$-waarde in $f(x)$ stoppen, krijgen we ook het $y$-coördinaat. Bij [Extreme waardes bepalen](#extreme-waardes-berekenen) kijken we hier meer uitgebreid naar.

### **Exponentiële funtie**
Een exponentiële functie heeft de vorm

$$f(x) = e^x.$$

Deze $e$ is het getal van euler. Het is een constante met de volgende waarde: $e = 2.7182818...$

Het bijzondere van dit getal is dat de afgeleide van $e^x$ ook $e^x$ is. De afgeleide van deze functie is dus zichzelf!

Dus als:

$$f(x) = e^x$$

Dan geldt er dat:

$$f'(x) = e^x.$$

In het onderstaande filmpje kunnen we goed zien hoe dit eruit ziet.

???+ video
    <video controls>
    <source src="../assets/videos/Exponential.mp4" type="video/mp4">
    </video>

    *<p style="text-align: center;">Filmpje: Visuele weergave van de afgeleide van de functie $f(x) = e^x$. Er is te zien dat op elk punt geldt dat $f(x) = f'(x)$. Dit is wat de e-macht zo bijzonder maakt. </p>*

De helling op elk punt is dus hetzelfde als het $y$-coördinaat op dat punt. De functie blijft dus maar steeds sneller stijgen als $y$ toeneemt. Als iets op deze manier steeds sneller blijft toenemen, noemen we dat *exponentieel*.

## **Afgeleides Bepalen**
Om een afgeleide te bepalen, kunnen we de onderstaande [tabel](#tabel-met-veel-voorkomende-functies) gebruiken. Daarin staan de meest voorkomende afgeleides van verschillende functies. En hier vind je de [regels](#regels) voor functies die bestaan uit andere kleinere functies.

???+ Belangrijk
    ### **Tabel met veel voorkomende functies**

    | Functie                            | Afgeleide                                    |
    | ---------------------------------- | -------------------------------------------- |
    | $\large{f(x) = a}$                 | $\large{f'(x) = 0}$                          |
    | $\large{f(x) = ax}$                 | $\large{f'(x) = a}$                          |
    | $\large{f(x) = ax^n}$              | $\large{f'(x) = n \cdot ax^{n-1}}$           |
    | $\large{f(x) = e^x}$               | $\large{f'(x) = e^x}$                        |
    | $\large{f(x) = a^x}$               | $\large{f'(x) = a^x \cdot \ln(x)}$         |
    | $\large{f(x) = \ln{(x)}}$          | $\large{f'(x) = \Large \frac{1}{x}}$                |
    | $\large{f(x) = \ ^a \! \log{(x)}}$ | $\large{f'(x) = \Large \frac{1}{x \ \cdot \ \ln{(a)}}}$ |
    | $\large{f(x) = \sin(x)}$         | $\large{f'(x) = \cos(x)}$                  |
    | $\large{f(x) = \cos(x)}$         | $\large{f'(x) = -\sin(x)}$                 |

    waarbij $n$ en $a$ constantes zijn. Dus gewoon getallen die niet afhankelijk zijn van $x$.

    ### **Regels**

    |               | Functie                            | Afgeleide                                                                                             |
    | ------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
    | Somregel      | $\large{f(x) = g(x) + h(x)}$       | $\large{f'(x) = g'(x) + h'(x)}$                                                                       |                                                 |
    | Productregel  | $\large{f(x) = g(x) \cdot h(x)}$       | $\large{f'(x) = g'(x) \cdot h(x) + g(x) \cdot h'(x)}$                                                    |
    | Quotiëntregel | $\large{f(x) = \Large \frac{g(x)}{h(x)}}$ | $\large f'(x) = \Large \frac{g'(x) \ \cdot \ h(x) \ - \ g(x) \ \cdot \ h'(x)}{h(x)^2}$                              |
    | Kettingregel  | $\large{f(x) = f(u(x))}$           | $\large f'(x) = \Large \frac{\mathrm{d} \textit{f} }{\mathrm{d} u} \cdot \frac{\mathrm{d} u}{\mathrm{d} x}$ |

De quotiëntregel kan je onthouden met het ezelsbruggetje: "nat - tan gedeelt door n kwadraat".

Hier staat "n" voor noemer, "t" voor teller en "a" voor afgeleide.

??? note "Opmerking Notatie"
    ### **Notatie**
    Een afgeleide kan op verschillende manieren worden weergegeven:
    
    $$\Large{f'(x), \ y', \ \frac{\mathrm{d} f(x)}{\mathrm{d} x}, \ \frac{\mathrm{d} y}{\mathrm{d} x}, \frac{\mathrm{d}}{\mathrm{d} x} y, \frac{\mathrm{d}}{\mathrm{d} x} f(x)} $$

### **Voorbeelden**

??? example "Voorbeeld 1: Bereken de afgeleide van $f(x) = x^2$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = x^2$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We kunnen dit oplossen met behulp van de derde rij van de [tabel](#tabel-met-veel-voorkomende-functies). We zien dat er voor een functie van de vorm:

    $$\large{f(x) = ax^n}$$

    de afgeleide gelijk is aan:

    $$\large{f'(x) = n \cdot ax^{n-1}}.$$

    In ons geval is $a$ gelijk aan $1$ en de macht $n$ is gelijk aan $2$. Onze afgeleide wordt dan dus:

    $$\large{f'(x) = 2 \cdot x^{2-1}}$$

    $$\large{f'(x) = 2x^{1}}$$

    Iets tot de macht $1$ is gewoon zichzelf, dus ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{f'(x) = 2x}.$$


??? example "Voorbeeld 2: Bereken de afgeleide van $f(x) = 4x$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 4x$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Dit kunnen we oplossen met de tweede rij van de [tabel](#tabel-met-veel-voorkomende-functies). Dus voor de functie:

    $$\large{f(x) = ax}$$

    is de afgeleide:

    $$\large{f'(x) = a}.$$

    We hebben hier een $4$ voor de $x$ staan, dus dat is onze $a$. Onze afgeleide wordt dan dus:

    !!! quote ""
        $$\large{f'(x) = 4}$$

??? example "Voorbeeld 3: Bereken de afgeleide van $f(x) = 3x^2 + 2x + 6$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 3x^2 + 2x + 6$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben hier eigenlijk een som van verschillende kleine functies. We willen dus de afgeleide bepalen van de hele functie, maar hoe doen we dat? 
    
    Met de [somregel](#regels) kunnen we zien dat we dan de afgeleides van de losse termen kunnen nemen. Dus als:

    De afgeleide van de eerste term kunnen we bepalen met de derde rij uit de [tabel](#tabel-met-veel-voorkomende-functies). Dus als:

    $$g(x) = 3x^2,$$

    dan is de afgeleide:

    $$g'(x) = 2 \cdot 3x^{2-1}$$
    
    $$g'(x) = 6x^1.$$

    Iets tot de macht $1$ is zichzelf, dus dit wordt:

    $$g'(x) = 6x.$$

    Nu bepalen we de afgeleide van de tweede term, $h(x) = 2x$. Met de tweede rij van de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat onze $a$ $2$ moet zijn. Dus:

    $$h'(x) = 2$$ 

    Als laatst bepalen we de afgeleide van de derde term, $k(x) = 6$. In de eerste rij van de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de afgeleide van een constante $0$ is. Dus:
    
    $$k'(x) = 0$$

    Nu combineren we al deze resultaten om te vinden:

    $$f'(x) = 6x + 2 + 0$$

    Ons eindantwoord wordt dus:
    !!! quote ""
        $$f'(x) = 6x + 2$$


??? example "Voorbeeld 4: Bereken de afgeleide van $f(x) = 5x^3 + 3x^2 - 15x + 100$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 5x^3 + 3x^2 - 15x + 100$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Met behulp van de [somregel](#regels) weten we dat we de afgeleide van de individuele termen kunnen nemen. De afgeleide wordt dan:

    $$\large{f'(x) = 3 \cdot 5x^{3-1} + 2 \cdot 3x^{2-1} - 15 + 0}$$

    We hebben hier de eerste drie regels uit de [tabel](#tabel-met-veel-voorkomende-functies) gebruikt: 
    
    - Voor de $5x^3$ en de $3x^2$ term hebben we regel $3$ gebruikt. 
    - De $-15x$ term wordt gewoon $-15$ volgens regel $2$.
    - De $+100$ term wordt $0$ volgens regel $1$. 

    We kunnen dit dan verder versimpelen naar:

    $$\large{f'(x) = 15x^2 + 6x^1 - 15}$$

    Iets tot de macht $1$ is zichzelf, dus $x^1$ wordt gewoon $x$:

    !!! quote ""
        $$\large{f'(x) = 15x^2 + 6x - 15}$$


??? example "Voorbeeld 5: Bereken de afgeleide van $f(x) = 3(\cos{(x)} + 2)$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 3(\cos{(x)} + 2)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Eerst werken we de haakjes uit. Als we dit doen, vinden we:

    $$\large{f(x) = 3\cos{(x)} + 6.}$$

    Met de [somregel](#regels) weten we dat we hier de afgeleide kunnen nemen van de individuele termen: 
    
    - De afgeleide van $\cos(x)$ kunnen we vinden in de [tabel](#tabel-met-veel-voorkomende-functies). Dit is $-\sin(x)$.
    - De afgeleide van de $+6$ term is $0$ (regel $1$).

    Bij een afggeleide blijven de constantes keer de functie gewoon ervoor. Dus die kunnen we gewoon lekker laten staan en hoeven we dus niks mee te doen. De afgeleide wordt dus:

    $$\large{g'(x) = 3 \cdot - \sin{(x)} + 0}$$

    Waarbij we dus de factor $3$ er gewoon voor mogen laten. 
    
    Ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{f'(x) = -3 \sin{(x)}}$$


??? example "Voorbeeld 6: Bereken de afgeleide van $f(x) = xe^x$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = xe^x$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Hier zien we dat onze functie $f(x)$ bestaat uit twee functies keer elkaar. Namelijk de functies:

    $$\large{g(x) = x}$$

    <p style="text-align: center;font-size:14px;">en</p>

    $$\large{h(x) = e^x}$$

    Dit kunnen we dus oplossen met behulp van de [productregel](#regels). Deze zegt dat:

    $$\large{f'(x) = g'(x) \cdot h(x) + g(x) \cdot h'(x)}$$

    Laten we eerst de afgeleides van $g(x)$ en $h(x)$ bepalen.

    We kunnen de afgeleide van $x$ bepalen met regel $2$ uit de [tabel](#tabel-met-veel-voorkomende-functies). In dit geval is onze $a$ in $f(x) = ax$ gelijk aan $1$, dus is de afgeleide van $x$ is $1$:

    $$\large{g'(x) = 1.}$$

    De afgeleide van $e^x$ kunnen we bepalen met de [tabel](#tabel-met-veel-voorkomende-functies). We zien dat de afgeleide van $e^x$ zichzelf is, dus ook $e^x$:

    $$\large{h'(x) = e^x = h(x).}$$

    Als we dit invullen in de [productregel](#regels), dan vinden we dus:

    $$\large{f'(x) = 1 \cdot e^x + x \cdot e^x}$$

    $$\large{f'(x) = xe^x + e^x}$$

    We kunnen hier nog de $e^x$ buiten haakjes halen:

    !!! quote ""
        $$\large{f'(x) = e^x \left( 1+x \right)}$$


??? example "Voorbeeld 7: Bereken de afgeleide van $f(x) = \tan{(x)}$"

    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = \tan{(x)}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we onze $\tan$ functie anders opschrijven. In het hoofdstuk [Goniometrie](goniometrie.md#goniometrische-vergelijkingen) zien we dat een $\tan$ functie ook geschreven kan worden als:

    $$\large{\tan{(x)} = \frac{\sin{(x)}}{\cos{(x)}}}$$

    Nu kunnen we de [quotiëntregel](#regels) toepassen. Deze zegt dat voor een functie van de vorm:

    $$\large{f(x) = \frac{g(x)}{h(x)}}$$

    de afgeleide gelijk is aan: 

    $$\large{f'(x) = \frac{g'(x) \ \cdot \ h(x) \ - \ g(x) \ \cdot \ h'(x)}{h(x)^2}}.$$

    In ons geval geldt er dat:

    $$\large{g(x) = \sin{(x)}}$$
    
    <p style="text-align: center;font-size:14px;">en</p>

    $$\large{h(x) = \cos{(x)}}$$

    De afgeleides van deze twee functies kunnen we vinden in de [tabel](#tabel-met-veel-voorkomende-functies):

    $$\large{g'(x) = \cos{(x)}}$$
    
    <p style="text-align: center;font-size:14px;">en</p>
    
    $$\large{h'(x) = - \sin{(x)}}$$

    Nu vullen we dat in bij de quotiëntregel:

    $$\large{f'(x) = \frac{\cos{(x)} \ \cdot \ \cos{(x)} \ - \ \sin{(x)} \ \cdot \ - \sin{(x)}}{\cos^2{(x)}}}$$

    Dit kunnen we versimplen tot:

    $$\large{f'(x) = \frac{\cos^2{(x)} + \sin^2{(x)}}{\cos^2{(x)}}}$$

    We kunnen de teller nog verder versimpelen met de tweede vergelijking van de [Goniometrische Vergelijkingen](goniometrie.md#goniometrische-vergelijkingen). Daar zien we dat $\cos^2(x) + \sin^2(x) = 1$. Ons eindantwoord wordt dan dus:

    !!! quote ""
        $$\large{f'(x) = \frac{1}{\cos^2{(x)}}}$$


??? example "Voorbeeld 8: Bereken de afgeleide van $f(x) = e^{x^2}$"

    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = e^{x^2}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen, gebruiken we de [kettingregel](#regels). Deze zegt dat voor een functie in een functie, dus:

    $$\large{f(x) \equiv f(u(x))}$$

    de afgeleide gelijk is aan:

    $$\large{f'(x) = \frac{\mathrm{d} f}{\mathrm{d} u} \cdot \frac{\mathrm{d} u}{\mathrm{d} x}}.$$

    Dus we moeten eerst de buitenste en de binnenste functie bepalen. Dus in dit geval hebben we als binnenste functie:

    $$\large{u(x) = x^2}$$

    en als buitenste functie:

    $$\large{f(u) = e^{u}}$$

    Laten we eerst de afgeleide van $f$ naar $u$ bepalen:

    $$\large{\frac{\mathrm{d} f}{\mathrm{d} u} = e^{u},}$$
    
    want de afgeleide van een e-macht is gewoon zichzelf (zie eventueel de [Tabel](#tabel-met-veel-voorkomende-functies)). Nu bepalen we de afgeleide van $u$ naar $x$:

    $$\large{\frac{\mathrm{d} u}{\mathrm{d} x} = 2x,}$$
    
    (zie voorbeeld 1 voor eventuele toelichting). Nu kunnen we de [kettingregel](#regels) toepassen:

    $$\large{f'(x) = e^{u} \cdot 2x}$$

    Nu kunnen we $u$ weer terug *substitueren* (dit betekent gewoon invullen):

    !!! quote ""
        $$\large{f'(x) = 2x \cdot e^{x^2}}$$


??? example "Voorbeeld 9: Bereken de afgeleide van $f(x) = \ln{\left((x+1)^2 \right)} \cdot \sqrt{x} + 5$"

    *<p style="text-align: left;font-size:15px;color: #FA3D3D; "> \* Lastige opdracht</p>*
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = \ln{\left((x+1)^2 \right)} \cdot \sqrt{x} + 5$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Bij een lastige opdracht is het belangrijk om echt stap voor stap te werken. Deze functie is een combinatie van een aantal andere functies. We herkennen hier de volgende functies:
    
    - $\large{\boxed{u(x) = \left(x + 1\right)^2}}$
    - $\large{\boxed{g(u) = \ln(u)}}$
    - $\large{\boxed{h(x) = \sqrt{x}}}$

    De vergelijking wordt dan:

    $$\large{f(x) = g(u) \cdot h(x) + 5}$$

    Als we dingen optellen, mogen we de afgeleides nemen van de losse termen. Dus laten we de afgeleide van de $+5$ term bepalen. Dit is gelijk aan $0$, want $5$ is een constante (zie regel $1$ van de [tabel](#tabel-met-veel-voorkomende-functies)). Dus die term voegt niks toe aan onze afgeleide.

    We moeten nu dus de afgeleide bepalen van $g(u) \cdot h(x)$. Dit zijn twee functies keer elkaar, dus moeten we de [productregel](#regels) gebruiken:

    $$\large{\boxed{f'(x) = \frac{\mathrm{d} g}{\mathrm{d} x} \cdot h(x) + g(u) \cdot \frac{\mathrm{d} h}{\mathrm{d} x}}}$$

    (Zie eventueel de [notatie](#notatie) van afgeleides). Laten we beginnen met $\large{\frac{\mathrm{d} h}{\mathrm{d} x}}$ bepalen:

    We kunnen $\sqrt{x}$ ook schrijven als $x^{\frac{1}{2}}$, dus:

    $$\large{h(x) = x^{\frac{1}{2}}}$$

    Nu kunnen we de afgeleide bepalen met regel $2$ van de [tabel](#tabel-met-veel-voorkomende-functies). We krijgen dan:

    $$\large{\frac{\mathrm{d} h}{\mathrm{d} x} = \frac{1}{2}x^{\frac{1}{2} - 1}}$$

    $$\large{\frac{\mathrm{d} h}{\mathrm{d} x} = \frac{1}{2}x^{-\frac{1}{2}}}$$

    En dit kunnen we ook schrijven als:

    $$\large{\boxed{\frac{\mathrm{d} h}{\mathrm{d} x} = \frac{1}{2 \sqrt{x}}}}$$

    Oké, dat was de afgeleide van de eerste functie! Nu moeten we $\large{\frac{\mathrm{d} g}{\mathrm{d} x}}$ bepalen. $g$ bestaat uit de functie $u$ en die bestaat weer uit $x$. We moeten dus de [kettingregel](#regels) gebruiken:

    $$\large{\frac{\mathrm{d} g}{\mathrm{d} x} = \frac{\mathrm{d} g}{\mathrm{d} u} \cdot \frac{\mathrm{d} u}{\mathrm{d} x}}$$

    Laten we beginnen met $\large{\frac{\mathrm{d} g}{\mathrm{d} u}}$ bepalen. We hebben:

    $$\large{g(u) = \ln(u).}$$

    In de [tabel](#tabel-met-veel-voorkomende-functies) zien we dat de afgeleide van $\ln(x)$ is $\frac{1}{x}$. Dus:

    $$\large{\frac{\mathrm{d} g}{\mathrm{d} u} = \frac{1}{u}}$$

    Nu bepalen we $\large{\frac{\mathrm{d} u}{\mathrm{d} x}}$. We hebben:

    $$\large{u(x) = \left(x + 1 \right)^2}$$

    Dit is ook weer een functie in een functie! Dus moeten weer de [kettingregel](#regels) gebruiken. We hebben namelijk de functie $\large{k(x) = x + 1}$. We krijgen dan dus dat $u$ is:

    $$\large{u(k) = k^2}$$

    De afgeleide van $u$ wordt dan:

    $$\large{\frac{\mathrm{d} u}{\mathrm{d} x} = \frac{\mathrm{d} u}{\mathrm{d} k} \cdot \frac{\mathrm{d} k}{\mathrm{d} x}}$$

    De afgeleide van $u$ naar $k$ is hetzelfde als dat we bij voorbeeld $1$ hadden gedaan:

    $$\large{\frac{\mathrm{d} u}{\mathrm{d} k} = 2k}$$

    De afgeleide van $k = x + 1$ naar $x$ kunnen we bepalen met regel $1$ en $2$ van de [tabel](#tabel-met-veel-voorkomende-functies). Daarmee vinden we dat de afgeleide van $x$ is $1$ en de afgeleide van $1$ is $0$. Dus:

    $$\large{\frac{\mathrm{d} k}{\mathrm{d} x} = 1}$$

    De afgeleide van $u$ naar $x$ is dus:

    $$\large{\frac{\mathrm{d} u}{\mathrm{d} x} = 2k}$$

    Als we dit opschrijven in termen van $x$:

    $$\large{\frac{\mathrm{d} u}{\mathrm{d} x} = 2(x + 1)}$$

    Nu kunnen we $\large{\frac{\mathrm{d} g}{\mathrm{d} x}}$ bepalen:

    $$\large{\frac{\mathrm{d} g}{\mathrm{d} x} = \frac{\mathrm{d} g}{\mathrm{d} u} \cdot \frac{\mathrm{d} u}{\mathrm{d} x}}$$

    $$\large{\frac{\mathrm{d} g}{\mathrm{d} x} = \frac{1}{u} \cdot 2\left(x + 1\right)}$$

    Als we $u$ schrijven in termen van $x$:

    $$\large{\frac{\mathrm{d} g}{\mathrm{d} x} = \frac{1}{\left(x + 1\right)^2} \cdot 2(x + 1)}$$

    Dit kunnen we weer versimpelen naar:

    $$\large{\boxed{\frac{\mathrm{d} g}{\mathrm{d} x} = \frac{2}{\left(x + 1\right)}}}$$

    Nu kunnen we uiteindelijk de afgeleide van $f(x)$ bepalen! Dit is wat we allemaal hebben gevonden:

    - $\large{f'(x) = \frac{\mathrm{d} g}{\mathrm{d} x} \cdot h(x) + g(x) \cdot \frac{\mathrm{d} h}{\mathrm{d} x}}$
    - $\large{\frac{\mathrm{d} g}{\mathrm{d} x} = \frac{2}{\left(x + 1\right)}}$
    - $\large{h(x) = \sqrt{x}}$
    - <span style="line-height: 5;"> $\large{\left. \begin{array}{ l l } g(u) = \ln(u)  \\ u(x) = \left(x + 1\right)^2 \end{array} \right\} \Longrightarrow g(x) = \ln\left((x + 1)^2 \right)}$ </span>
    - $\large{\frac{\mathrm{d} h}{\mathrm{d} x} = \frac{1}{2\sqrt{x}}}$ 

    Laten we de vergelijking gaan invullen:

    $$\large{f'(x) = \frac{2}{\left(x + 1\right)} \cdot \sqrt{x} + \ln\left((x + 1)^2 \right) \cdot \frac{1}{2\sqrt{x}}}$$

    Dit kunnen we nog verder versimpelen:

    $$\large{\frac{2\sqrt{x}}{\left(x + 1\right)} + \frac{\ln\left((x + 1)^2 \right)}{2\sqrt{x}}}$$

    We kunnen met de [Regels van Logaritmes](basisvaardigheden.md#regels-met-logaritmes) het kwadraat uit de $\ln$ halen:
    
    $$\large{\frac{2\sqrt{x}}{\left(x + 1\right)} + \frac{2\ln(x + 1)}{2\sqrt{x}}}$$

    De $2$ in de teller en de noemer vallen dan tegen elkaar weg. Ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{\frac{2\sqrt{x}}{\left(x + 1\right)} + \frac{\ln(x + 1)}{\sqrt{x}}}$$


## **Extreme waardes bepalen**
Zoals we zagen bij het filmpje van een [parabool](#parabool), is de helling $0$ bij een top. Dit komt omdat op dit punt de functie van toenemend naar afnemend wisselt, of andersom. Dit betekent dus dat er op dat punt geen toename/afname is als $x$ toeneemt/afneemt. Dus als we de coördinaten van de top willen weten, moeten we kijken waar de helling (en dus de afgeleide) $0$ is. Hier hoort de volgende vergelijking bij:

$$\large{f'(x) = 0}$$

Laten we naar een voorbeeld kijken. Stel we hebben de volgende functie:

$$f(x) = -x^2 + 2.$$

En we willen van deze functie de coördinaten van de top weten. Hoe pakken we dit aan?

<figure markdown>
![Top van functie](assets/images/afgeleide/f(x) = -x² + 2.svg){ width="500"}
    <figcaption>Figuur 1. De grafiek $f(x) = - x^2 + 2$ geplot met de extreme waarde (ander woord voor de top).</figcaption>
</figure>

We beginnen dus met de afgeleide bepalen van $f(x)$. Voor de $-x^2$ term kunnen we regel $2$ gebruiken van de [tabel](#tabel-met-veel-voorkomende-functies). De afgeleide van de $+2$ term wordt $0$, want dit is een constante (regel $1$ uit de [tabel](#tabel-met-veel-voorkomende-functies)). De afgeleide wordt dus:

$$f'(x) = -2x^{2-1} + 0$$

$$f'(x) = -2x$$

We willen de top bepalen, dus moeten we de afgeleide gelijk stellen aan $0$:

$$f'(x) = 0$$

Als we dit invullen, vinden we:

$$2x = 0$$

$$\boxed{x = 0}$$

Het $x$-coördinaat van onze top is dus $0$. Om het $y$-coördinaat van de top te bepalen, moeten we dit invullen in de originele functie $f(x)$. We krijgen dan:

$$f(0) = -0^2 + 2$$

$$\boxed{f(0) = 2}$$

Het $y$-coördinaat van de top is dus bij $y=2$. De coördinaten van de top zijn dus:

!!! quote ""
    $$\large{(0, 2)}$$

en dit kunnen we ook aflezen in Figuur 1.

### **Voorbeelden**

??? example "Voorbeeld 1: Bepaal de extreme waarde van $f(x) = 6x^2 - 12x + 9$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waarde van $f(x) = 6x^2 - 12x + 9$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We moeten de extreme waarde bepalen van $f(x)$, dus de top. Dus we moeten de afgeleide van $f(x)$ gelijk stellen aan $0$. Laten we eerst de afgeleide van $f(x)$ bepalen.

    We weten dat we de afgeleide kunnen nemen van de individuele termen ([somregel](#regels)). De afgeleide wordt dus:

    $$\large{f'(x) = 2 \cdot 6x^{2-1} - 12}$$

    $$\large{f'(x) = 12x - 12}$$

    Om de extreme waarde te bepalen stellen we dit dus gelijk aan $0$:

    $$\large{12x - 12 = 0}$$
    
    $$\large{12x = 12}$$

    $$\large{\boxed{x = 1}}$$

    Het $x$-coördinaat van de top is dus bij $x = 1$. Het $y$-coördinaat bepalen we door $x=1$ in te vullen in $f(x)$:

    $$\large{f(1) = 6 \cdot 1^2 - 12 \cdot 1 + 9}$$

    $$\large{\boxed{f(1) = 3}}$$

    De coördinaten van de top zijn dus:

    !!! quote ""
        $$\large{(1, 3)}$$

    En als we de functie tekenen, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = 6x² - 12x + 9.svg){ width="500"}
        <figcaption>Figuur 2. De grafiek $f(x) = 6x^2 - 12x + 9$ geplot met de extreme waarde.</figcaption>
    </figure>


??? example "Voorbeeld 2: Bepaal de extreme waardes van $f(x) = -x^3 + 6x^2 - 9x + 3$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waardes van $f(x) = -x^3 + 6x^2 - 9x + 3$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We moeten weer de extreme waardes bepalen. Dus dit betekent dat we de afgeleide gelijk aan $0$ moeten stellen. Laten we weer eerst de afgeleide bepalen.

    De afgeleide is de afgeleide van de individuele termen ([somregel](#regels)):

    $$\large{f'(x) = -3x^{3-1} + 6 \cdot 2x^{2-1} - 9}$$

    $$\large{f'(x) = -3x^2 + 12x - 9}$$

    Nu stellen we deze afgeleide gelijk aan $0$:

    $$\large{-3x^2 + 12x - 9 = 0}$$

    Dit is een [kwadratische vergelijking](kwadratische_vergelijkingen.md) die we gewoon kunnen oplossen. We beginnen met alle termen te delen door $-3$:

    $$\large{x^2 - 4x + 3 = 0}$$

    Dit kunnen we oplossen met door te [ontbinden in factoren](kwadratische_vergelijkingen.md#ontbinden-in-factoren). We doen dit met behulp van de [product-som methode](kwadratische_vergelijkingen.md#product-som-methode).

    We maken eers een tabel met alle factoren die samen $3$ geven.

    | Factor 1 | Factor 2 | Product |
    | -------- | -------- | ------- |
    | 1 | 3 | 3 |
    | -1 | -3 | 3 |

    Nu maken we de bijbehorende som tabel om te kijken welke factoren samen $-4$ zijn.

    | Factor 1 | Factor 2 | Som |
    | -------- | -------- | ------- |
    | 1 | 3 | 4 |
    | -1 | -3 | -4 :fontawesome-solid-check:{ .green }|

    De factoren zijn dus $-1$ en $-3$. De vergelijking wordt dus:

    $$\large{(x - 1)(x - 3) = 0}$$

    $$\large{x - 1 = 0 \ \vee \ x - 3 = 0}$$

    Dit geeft ons de $x$-coördinaten:

    $$\large{\boxed{x = 1 \ \vee \ x = 3}}$$

    In dit geval zijn er dus twee extreme waardes. We berekenen bij beide extreme waardes de bijbehorende $y$-coördinaten. Dit doen we door elk $x$-coördinaat in $f(x)$ te stoppen:

    $$\large{f(1) = -(1)^3 + 6 \cdot (1)^2 - 9 \cdot 1 + 3}$$

    $$\large{\boxed{f(1) = -1}}$$

    $$\large{f(3) = -(3)^3 + 6 \cdot (3)^2 - 9 \cdot 3 + 3}$$

    $$\large{\boxed{f(3) = 3}}$$

    De coördinaten van de twee extreme waardes zijn dus:

    !!! quote ""
        $$\large{(1, -1) \textrm{ en } (3, 3)}$$

    Als we de functie tekenen, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = -x³ + 6x² - 9x + 3.svg){ width="500"}
        <figcaption>Figuur 3. De grafiek $f(x) = -x^3 + 6x^2 - 9x + 3$ geplot met de extreme waardes.</figcaption>
    </figure>


??? example "Voorbeeld 3: Bepaal de extreme waarde van $f(x) = (x-2)^{7}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waarde van $f(x) = (x-2)^{7}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om de extreme waarde te bepalen, stellen we de afgeleide van $f(x)$ gelijk aan $0$. We beginnen dus met het bepalen van de afgeleide:

    We zien dat deze functie bestaat uit een functie in een functie. We hebben namelijk:

    - $\large{u(x) = x - 2}$
    - $\large{f(u) = u^7}$

    Om de afgeleide te bepalen, moeten we de [kettingregel](#regels) toepassen:

    $$\large{f'(x) = \frac{\mathrm{d}f}{\mathrm{d} u} \ \cdot \ \frac{\mathrm{d} u}{\mathrm{d} x}}$$

    We berekenen eerst de afgeleide van $f$ naar $u$. Dit doen we met regel $3$ van de [tabel](#tabel-met-veel-voorkomende-functies):

    $$\large{f(u) = u^7}$$

    $$\large{\frac{\mathrm{d}f}{\mathrm{d} u} = 7 \cdot u^{7-1}}$$

    $$\large{\frac{\mathrm{d}f}{\mathrm{d} u} = 7u^6}$$

    Nu bepalen we de afgeleide van $u$ naar $x$:

    $$\large{u(x) = x - 2}$$

    $$\large{\frac{\mathrm{d} u}{\mathrm{d} x} = 1 + 0 = 1}$$

    Want de afgeleide van $x$ is $1$ ([regel $2$](#tabel-met-veel-voorkomende-functies)) en de afgeleide van $-2$ is $0$ ([regel $1$](#tabel-met-veel-voorkomende-functies)). Als we dit combineren, dan krijgen we:

    $$\large{f'(x) = 7u^6 \cdot 1}$$

    Als we $u$ weer schrijven in termen van $x$ krijgen we als afgeleide:

    $$\large{f'(x) = 7(x - 2)^6}$$

    Om de extreme waarde te bepalen, moeten we de afgeleide dus gelijk aan $0$ stellen:

    $$\large{f'(x) = 0}$$

    $$\large{7(x - 2)^6 = 0}$$

    Dit kan alleen $0$ zijn als:

    $$\large{x - 2 = 0,}$$

    Als we dit oplossen, vinden we:

    $$\large{x = 2}$$

    Het $x$-coördinaat van de top is dus $2$. Als we dit in $f(x)$ invullen, vinden we als $y$-coördinaat:

    $$\large{f(2) = (2 - 2)^7 = 0}$$

    De coördinaten van onze top zijn dus:

    !!! quote ""
        $$\large{(2, 0)}$$

    Als we de functie tekenen, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = (x - 2)⁷.svg){ width="500"}
        <figcaption>Figuur 4. De grafiek $f(x) = (x-2)^{7}$ geplot met de extreme waarde.</figcaption>
    </figure>


??? example "Voorbeeld 4: Bepaal de extreme waardes van $f(x) = 10e^x(x^2 + 4x + 0.4)$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waardes van $f(x) = e^x(x^2 + 4x + 0.4)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om de extreme waardes te bepalen moeten we stellen dat de afgeleide gelijk is aan $0$. Dus als eerst berekenen we de afgeleide van $f(x)$.

    Dit zijn twee functies keer elkaar, dus moeten we de [productregel](#regels) gebruiken. We hebben de volgende twee functies:

    - $\large{g(x) = 10e^x}$
    - $\large{h(x) = x^2 + 4x + 0.4}$

    De [productregel](#regels) vertelt ons dat:

    $$\large{f'(x) = g'(x) \cdot h(x) + g(x) \cdot h'(x)}$$

    Laten we dus $g'(x)$ en $h'(x)$ bepalen:

    $g(x)$ is een $e$-macht, dus de afgeleide is weer zichzelf (zie eventueel de [tabel](#tabel-met-veel-voorkomende-functies)):

    $$\large{g'(x) = 10e^x}$$

    De afgeleide van $h(x)$ kunnen we bepalen met de eerste drie regels van de [tabel](#tabel-met-veel-voorkomende-functies):

    $$\large{h'(x) = 2x + 4}$$

    Nu vullen we passen we de productregel toe:

    $$\large{f'(x) = 10e^x \cdot (x^2 + 4x + 0.4) + 10e^x \cdot (2x + 4)}$$

    Dit kunnen we versimpelen naar:

    $$\large{f'(x) = 10e^x(x^2 + 6x + 4.4)}$$

    Om de extreme waardes te bepalen stellen we deze afgeleide gelijk aan $0$:

    $$\large{10e^x(x^2 + 6x + 4.4) = 0}$$

    We zien hier dat deze twee factoren keer elkaar $0$ zijn. Dit kan alleen als een van de twee factoren $0$ is:

    $$\large{10e^x = 0 \ \vee \ x^2 + 6x + 4.4 = 0}$$

    Maar $e^x$ wordt nooit $0$, ongeacht welke $x$ je invult. Dit betekent dus dat de rechter vergelijking $0$ moet zijn:

    $$\large{x^2 + 6x + 4.4 = 0}$$

    Ontbinden in factoren wordt hier lastig en dus gebruiken we de [*abc* formule](kwadratische_vergelijkingen.md#de-abc-formule). We hebben:

    $$\large{a = 1, \ b = 6, \ c = 4.4}$$

    De discriminant wordt dan:

    $$D = 6^2 - 4 \cdot 1 \cdot 4.4 = 18.4$$

    Nu kunnen we $x$ bepalen:

    $$\large{x = \frac{-6 + \sqrt{18.4}}{2 \cdot 1} \ \vee \ \frac{-6 - \sqrt{18.4}}{2 \cdot 1}}$$

    We kunnen dit met een rekenmachine berekenen:

    $$\large{x \approx -0.86 \ \vee \ x \approx -5.14}$$

    De bijbehorende $y$-coördinaten kunnen we bepalen door dit in te vullen in $f(x)$:

    $$\large{f(-0.86) = 10e^{-0.86}\left((-0.86)^2 + 4 \cdot (-0.86) + 0.4 \right)}$$

    $$\large{f(-0.86) \approx -9.7}$$

    $$\large{f(-5.14) = 10e^{-5.14}\left((-5.14)^2 + 4 \cdot (-5.14) + 0.4 \right)}$$

    $$\large{f(-5.14) \approx 0.37}$$

    De coördinaten van de twee extreme waardes zijn dus:

    !!! quote ""
        $$\large{(-0.86, -9.7) \textrm{ en } (-5.14, 0.37)}$$

    En als we de functie tekenen, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = 10eˣ(x² + 4x + 0.4).svg){ width="500"}
        <figcaption>Figuur 5. De grafiek $f(x) = 10e^x(x^2 + 4x + 0.4)$ geplot met de extreme waardes.</figcaption>
    </figure>


??? example "Voorbeeld 5: Bepaal de extreme waardes van $f(x) = \cos^2(2x)$ in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$"
    **<p style="text-align: center;font-size:18px;">Bepaal de coördinaten van de extreme waardes van $f(x) = \cos^2(2x)$ in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$</p>**
    **<p style="text-align: center;font-size:18px;">Uitwerking</p>**

    Om de extreme waardes te bepalen, moeten we de afgeleide gelijk aan $0$ stellen. We beginnen dus met de afgeleide van $f(x)$ te bepalen. Deze functie bestaat uit meerdere functies in elkaar:

    - $\large{u(x) = \cos(2x)}$
    - $\large{f(u) = u^2}$

    De [kettingregel](#regels) vertelt ons:

    $$\large{f'(x) = \frac{\mathrm{d}f}{\mathrm{d} u} \ \cdot \ \frac{\mathrm{d} u}{\mathrm{d} x}}$$

    We beginnen met $\large{\frac{\mathrm{d}f}{\mathrm{d} u}}$ bepalen:

    $$\large{\frac{\mathrm{d}f}{\mathrm{d} u} = 2 \cdot u^{2-1}}$$

    $$\large{\frac{\mathrm{d}f}{\mathrm{d} u} = 2u}$$

    Als we dit schrijven in termen van $x$:

    $$\large{\boxed{\frac{\mathrm{d}f}{\mathrm{d} u} = 2 \cos(2x)}}$$

    Nu bepalen we $\large{\frac{\mathrm{d}u}{\mathrm{d} x}}$. Maar let op! Deze functie bestaat ook uit meerdere functies in elkaar:

    - $\large{g(x) = 2x}$
    - $\large{u(g) = \cos(g)}$

    Dus we kunnen $\large{\frac{\mathrm{d}u}{\mathrm{d} x}}$ bepalen door weer de kettingregel te gebruiken:

    $$\large{\frac{\mathrm{d}u}{\mathrm{d} x} = \frac{\mathrm{d}u}{\mathrm{d} g} \cdot \frac{\mathrm{d}g}{\mathrm{d} x}}$$

    De afgeleide van $g$ naar $x$ is:

    $$\large{\frac{\mathrm{d}g}{\mathrm{d} x} = 2}$$

    En de afgeleide van $u$ naar $g$ kunnen we in de [tabel](#tabel-met-veel-voorkomende-functies) opzoeken:

    $$\large{\frac{\mathrm{d}u}{\mathrm{d} g} = -\sin(g)}$$

    De afgeleide van $u$ naar $x$ wordt dan dus:

    $$\large{\frac{\mathrm{d}u}{\mathrm{d} x} = -\sin(g) \cdot 2}$$

    En als we $g$ weer in termen van $x$ doen:

    $$\large{\boxed{\frac{\mathrm{d}u}{\mathrm{d} x} = -2 \sin(2x)}}$$

    De afgeleide van $f$ naar $x$ wordt dan dus:

    $$\large{f'(x) = \frac{\mathrm{d}f}{\mathrm{d} u} \cdot \frac{\mathrm{d}u}{\mathrm{d} x}}$$

    Als we dit nu invullen, vinden we:

    $$\large{f'(x) = 2 \cos(2x) \cdot -2 \sin(2x)}$$

    $$\large{f'(x) = -4 \sin(2x) \cos(2x)}$$

    Dit kunnen we eventueel nog verder versimpelen met de [sinus verdubbelingsformule](goniometrie.md#goniometrische-vergelijkingen). We krijgen dan:

    $$\large{f'(x) = -2 \sin(4x)}$$

    Nu kunnen we deze afgeleide gelijk aan $0$ stellen om de extreme waardes te bepalen:

    $$\large{-2 \sin(4x) = 0}$$

    $$\large{\sin(4x) = 0}$$

    $$\large{\sin(4x) = \sin(0)}$$

    Als we dit [oplossen](goniometrie.md#uitwerken-sincos-vergelijkingen) dan vinden we:

    $$\large{4x = k \cdot 2\pi \ \vee \ 4x = \pi + k \cdot 2\pi}$$

    Dit kunnen we ook schrijven als:

    $$\large{4x = k \cdot \pi}$$

    Als we aan beide kanten door $4$ delen:

    $$\large{x = \frac{1}{4} k \cdot \pi,}$$

    waarbij $k$ een geheel getal is. 

    We moesten alle extreme waardes geven in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$. Dus dan krijgen we de volgende oplossingen:

    $$\large{x = -\frac{1}{2} \pi \ \vee \ x = -\frac{1}{4} \pi \ \vee \ x = 0 \ \vee \ x = \frac{1}{4} \pi \ \vee \ x = \frac{1}{2} \pi}$$

    Als we al deze $x$-coördinaten invullen in $f(x)$, dan kunnen we de bijbehorende $y$-coördinaten berekenen:

    $$\large{y = \left\{ \begin{array}{ c c c c c } f(- \frac{1}{2} \pi) = 1  \\ f(- \frac{1}{4} \pi) = 0 \\ f(0) = 1 \\ f(\frac{1}{4} \pi) = 0 \\ f(\frac{1}{2} \pi) = 1 \\ \end{array} \right. }$$

    Onze coördinaten voor de toppen worden dus:

    !!! quote ""
        $$\large{(-\frac{1}{2} \pi, 1), \ (-\frac{1}{4} \pi, 0), \ (0, 1), \ (\frac{1}{4} \pi, 0) \textrm{ en } (\frac{1}{2} \pi, 1)}$$

    En als we de functie tekenen, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = cos²(2x).svg){ width="500"}
        <figcaption>Figuur 6. De grafiek $f(x) = \cos^2(2x)$ geplot met de extreme waardes in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$.</figcaption>
    </figure>