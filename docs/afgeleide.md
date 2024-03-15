# De Afgeleide Functie

## Afgeleide bepalen

Een afgeleide functie geeft op elk x coördinaat de bijbehorende helling/richtingscoëfficient. De functie geeft dan dus niet meer het $y$-coördinaat als je $x$ invult, maar de helling van de grafiek op dat punt. Dit wordt hieronder weergegeven.

### **Parabool**
Een parabool heeft in het simpleste geval de vorm

$$f(x) = x^2.$$

De afgeleide van deze functie is gelijk aan 

$$f'(x) = 2x,$$ 

Waarbij $f'(x)$ aangeeft dat het gaat om de afgeleide van de functie $f(x)$ (zie dit [voorbeeld](#voorbeeld-1-fx-x2) voor de toelichting van het antwoord en [Notatie](#notatie) voor de notatie van de afgeleide).

In het onderstaande filmpje is er te zien dat de afgeleide gelijk is aan de helling op elk punt. Ook is er te zien dat bij een top geldt dat de helling (en dus de afgeleide) gelijk is aan $0$. Dit betekent dus dat als we het x coördinaat van een top willen bepalen, we moeten stellen dat

$$f'(x) = 0.$$

???+ video
    <video controls>
    <source src="../assets/videos/Parabola.mp4" type="video/mp4">
    </video>

    *<p style="text-align: center;">Filmpje: Visuele weergave van de afgeleide van de functie $f(x) = x^2$. Bij de top geldt dat de helling gelijk is aan 0. </p>*

### **Exponentiële funtie**
Een exponentiële functie heeft de vorm

$$f(x) = e^x,$$

waar $e$ het getal van euler is. Er geldt dat $e = 2.7182818...$

De afgeleide van $f(x) = e^x$ is:

$$f'(x) = e^x.$$

De afgeleide is dus hetzelfde als de functie zelf. Dit fenomeen is te zien in het onderstaande filmpje.

???+ video
    <video controls>
    <source src="../assets/videos/Exponential.mp4" type="video/mp4">
    </video>

    *<p style="text-align: center;">Filmpje: Visuele weergave van de afgeleide van de functie $f(x) = e^x$. Er is te zien dat op elk punt geldt dat $f(x) = f'(x)$. Dit is wat de e-macht zo bijzonder maakt. </p>*

???+ Belangrijk
    ### **Tabel met veel voorkomende functies**

    | Functie                            | Afgeleide                                    |
    | ---------------------------------- | -------------------------------------------- |
    | $\large{f(x) = a}$                 | $\large{f'(x) = 0}$                          |
    | $\large{f(x) = x^n}$               | $\large{f'(x) = nx^{n-1}}$                   |
    | $\large{f(x) = e^x}$               | $\large{f'(x) = e^x}$                        |
    | $\large{f(x) = a^x}$               | $\large{f'(x) = a^x \ * \ \ln{(x)}}$         |
    | $\large{f(x) = \ln{(x)}}$          | $\large{f'(x) = \frac{1}{x}}$                |
    | $\large{f(x) = \ ^a \! \log{(x)}}$ | $\large{f'(x) = \frac{1}{x \ * \ \ln{(a)}}}$ |
    | $\large{f(x) = \sin{(x)}}$         | $\large{f'(x) = \cos{(x)}}$                  |
    | $\large{f(x) = \cos{(x)}}$         | $\large{f'(x) = -\sin{(x)}}$                 |

    waarbij $n$ en $a$ constantes zijn die niet afhankelijk van x zijn.

    ### **Regels**

    |               | Functie                            | Afgeleide                                                                                             |
    | ------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
    | Somregel      | $\large{f(x) = g(x) + h(x)}$       | $\large{f'(x) = g'(x) + h'(x)}$                                                                       |
    | Productregel (eenvoudig)  | $\large{f(x) = a * g(x)}$ | $\large{f'(x) = a \  * \ g'(x)}$                                                    |
    | Productregel  | $\large{f(x) = g(x) * h(x)}$       | $\large{f'(x) = g'(x) \  * \ h(x) + g(x) * h'(x)}$                                                    |
    | Quotiëntregel | $\large{f(x) = \frac{g(x)}{h(x)}}$ | $\large{f'(x) = \frac{g'(x) \ * \ h(x) \ - \ g(x) \ * \ h'(x)}{h(x)^2}}$                              |
    | Kettingregel  | $\large{f(x) = f(g(x))}$           | $\large{f'(x) = \frac{\mathrm{d} \ f(g)}{\mathrm{d} g} \ * \ \frac{\mathrm{d} \ g(x)}{\mathrm{d} x}}$ |

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

    We kunnen dit oplossen met behulp van de tweede rij van de [Tabel](#tabel-met-veel-voorkomende-functies).

    Daar zien we dat er voor een functie

    $$\large{f(x) = x^n}$$

    geldt dat

    $$\large{f'(x) = nx^{n-1}}.$$

    In ons geval geldt er dat $n=2$ zodat we onze functie $f(x) = x^2$ krijgen. Onze afgeleide wordt dan:

    $$\large{f'(x) = 2x^{2-1}}$$

    $$\large{f'(x) = 2x^{1}}$$

    En omdat we kunnen zeggen dat $x^1 \equiv x$:

    !!! quote ""
        $$\large{f'(x) = 2x}.$$


??? example "Voorbeeld 2: Bereken de afgeleide van $f(x) = 4x$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 4x$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Net zoals bij het vorig voorbeeld kunnen we dit oplossen met behulp van de tweede rij van de [Tabel](#tabel-met-veel-voorkomende-functies). Maar nu hebben we ook het getal $4$ voor onze x. Als we gebruik maken van de [eenvoudige productregel](#regels) dan zien we dat een constante keer de functie niet uitmaakt voor onze afgeleide. We kunnen hier het getal $4$ er dus gewoon voor laten.

    We weten dat er voor de functie

    $$\large{f(x) = x^n}$$

    geldt dat

    $$\large{f'(x) = nx^{n-1}}.$$

    Er geldt nu dat $n=1$, zodat $f(x) = x$. Onze afgeleide wordt dan:

    $$\large{f'(x) = 4*1x^{1-1}}$$

    $$\large{f'(x) = 4x^{0}}$$

    En omdat een getal tot de macht $0$ altijd gelijk is aan $1$, wordt onze afgeleide

    !!! quote ""
        $$\large{f'(x) = 4}$$

    ??? note "Shortcut"
        Stel dat we in plaats van de $f(x)$ hierboven de functie $g(x) = 5x$ hadden, dan was onze afgeleide geworden:

        $$\large{g'(x) = 5,}$$

        volgens precies dezelfde stappen als hierboven. Er volgt dus dat voor een willekeurige constante $a$ geldt dat:

        $$\Large{f(x) = ax \Rightarrow f'(x) = a}$$       


??? example "Voorbeeld 3: Bereken de afgeleide van $f(x) = 5x^3 + 3x^2 - 15x + 100$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 5x^3 + 3x^2 - 15x + 100$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Met behulp van de [somregel](#regels) weten we dat de afgeleide van $f(x)$ de som is van de afgeleide van de individuele termen. De afgeleide wordt dan:

    $$\large{f'(x) = 5*3x^{3-1} + 3*2x^{2-1} - 15}$$

    Dit hebben we opgelost met de tweede regel uit de [tabel](#tabel-met-veel-voorkomende-functies) voor alle $x$ termen en de $+100$ term valt weg volgens de eerste regel uit de [tabel](#tabel-met-veel-voorkomende-functies). 

    We kunnen dit dan verder versimpelen naar:

    $$\large{f'(x) = 15x^2 + 6x^1 - 15}$$

    En omdat we kunnen zeggen dat $x^1 \equiv x$:

    !!! quote ""
        $$\large{f'(x) = 15x^2 + 6x - 15}$$


??? example "Voorbeeld 4: Bereken de afgeleide van $f(x) = 3(\cos{(x)} + 2)$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 3(\cos{(x)} + 2)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Eerst werken we de haakjes weg zodat we vinden dat

    $$\large{f(x) = 3\cos{(x)} + 6.}$$

    Met behulp van de [somregel](#regels) weten we dat de afgeleide van $f(x)$ de som is van de afgeleide van de individuele termen. De $+6$ term valt weg volgens regel 1 van de [tabel](#tabel-met-veel-voorkomende-functies). De afgeleide van de cosinus term kunnen we ook vinden in de [tabel](#tabel-met-veel-voorkomende-functies). 

    De afgeleide wordt dan:

    $$\large{g'(x) = 3 * - \sin{(x)}}$$

    Waarbij we dus de factor $3$ er gewoon voor mogen laten en geen extra rekening mee hoeven te houden als we de afgeleide nemen ([eenvoudige productregel](#regels)). 
    
    Ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{f'(x) = -3 \sin{(x)}}$$


??? example "Voorbeeld 5: Bereken de afgeleide van $f(x) = xe^x$"
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = xe^x$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Hier zien we dat onze functie $f(x)$ bestaat uit twee functies keer elkaar. Namelijk de functies:

    $$\large{g(x) = x \textrm{ en } h(x) = e^x}$$

    Dit kunnen we dus oplossen met behulp van de [productregel](#regels). Deze zegt dat:

    $$\large{f'(x) = g'(x) * h(x) + g(x) * h'(x)}$$

    Laten we eerst $g'(x)$ en $h'(x)$ bepalen.

    Uit [Voorbeeld 2](#voorbeeld-2-fx-4x) is gebleken dat de afgeleide van $x$ $1$ is:

    $$\large{g'(x) = 1.}$$

    $h'(x)$ kunnen we bepalen met de [Tabel](#tabel-met-veel-voorkomende-functies). We zien dan dat er geldt dat

    $$\large{h'(x) = e^x = h(x).}$$

    Als we dit invullen in de [productregel](#regels), dan vinden we dus de afgeleide:

    $$\large{f'(x) = 1 * e^x + x * e^x}$$

    Dit kunnen we herschrijven tot:

    !!! quote ""
        $$\large{f'(x) = e^x \left( 1+x \right)}$$


??? example "Voorbeeld 6: Bereken de afgeleide van $f(x) = \tan{(x)}$"

    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = \tan{(x)}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we eerst beginnen met onze $\tan$ functie op een andere manier opschrijven. In het hoofdstuk [Goniometrie](goniometrie.md#goniometrische-vergelijkingen) zien we dat we een $\tan$ functie ook op de volgende manier kunnen schrijven:

    $$\large{\tan{(x)} = \frac{\sin{(x)}}{\cos{(x)}}}$$

    Nu kunnen we de [quotiëntregel](#regels) gaan toepassen. Deze zegt dat:
    
    Als:

    $$\large{f(x) = \frac{g(x)}{h(x)}}$$

    Dan: 

    $$\large{f'(x) = \frac{g'(x) \ * \ h(x) \ - \ g(x) \ * \ h'(x)}{h(x)^2}}.$$

    In ons geval geldt er dus dat

    $$\large{g(x) = \sin{(x)} \textrm{ en } h(x) = \cos{(x)}}$$

    De afgeleides zijn dan volgens de [Tabel](#tabel-met-veel-voorkomende-functies):

    $$\large{g'(x) = \cos{(x)} \textrm{ en } h'(x) = - \sin{(x)}}$$

    Nu vullen we dat in bij de quotiëntregel:

    $$\large{f'(x) = \frac{\cos{(x)} \ * \ \cos{(x)} \ - \ sin{(x)} \ * \ - \sin{(x)}}{\cos^2{(x)}}}$$

    Dit kunnen we versimplen tot:

    $$\large{f'(x) = \frac{\cos^2{(x)} + sin^2{(x)}}{\cos^2{(x)}}}$$

    We kunnen de teller nog verder versimpelen met behulp van de tweede vergelijking uit de lijst [Goniometrische Vergelijkingen](goniometrie.md#goniometrische-vergelijkingen). We krijgen dan als eindantwoord dat:

    !!! quote ""
        $$\large{f'(x) = \frac{1}{\cos^2{(x)}}}$$


??? example "Voorbeeld 7: Bereken de afgeleide van $f(x) = e^{x^2}$"

    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = e^{x^2}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen maken we gebruik van de [kettingregel](#regels). Deze zegt dat voor een functie:

    $$\large{f(x) \equiv f(g(x))}$$

    Er geldt dat:

    $$\large{f'(x) = \frac{\mathrm{d} \ f(g)}{\mathrm{d} g} \ * \ \frac{\mathrm{d} \ g(x)}{\mathrm{d} x}}$$

    We definiëren dus een interne functie $g(x)$ binnen $f(x)$. Dus in dit geval is dit de functie:

    $$\large{g(x) = x^2}$$

    Onze functie $f(g(x))$ wordt dan:

    $$\large{f(g(x)) = e^{g(x)}}$$

    Laten we eerst de afgeleide van $f$ naar $g$ bepalen:

    $$\large{\frac{\mathrm{d} \ f(g)}{\mathrm{d} g} = e^{g},}$$
    
    want de afgeleide van een e-macht is zichzelf (zie de [Tabel](#tabel-met-veel-voorkomende-functies)). Nu bepalen we de afgeleide van $g$ naar $x$:

    $$\large{\frac{\mathrm{d} \ g(x)}{\mathrm{d} x} = 2x,}$$
    
    zie [Voorbeeld 1](#voorbeeld-1-fx-x2) voor eventuele toelichting.

    Nu kunnen we de [kettingregel](#regels) invullen:

    $$\large{f'(x) = e^{g(x)} * 2x}$$

    Nu kunnen we $g(x)$ terug substitueren:

    !!! quote ""
        $$\large{f'(x) = 2x*e^{x^2}}$$


??? example "Voorbeeld 8: Bereken de afgeleide van $f(x) = \ln{\left((x+1)^2 \right)} * \sqrt{x} + 5$"

    *<p style="text-align: left;font-size:15px;color:red "> \* Lastige opdracht</p>*
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = \ln{\left((x+1)^2 \right)} * \sqrt{x} + 5$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Bij zo'n soort opdracht waar je veel verschillende dingen moet doen is het erg belangrijk om echt stap voor stap te werken. Laten we beginnen met het herkenen van de functies. Er is aan het begin een functie in een functie, dus dat is iets voor de [kettingregel](#regels). Die functie wordt vermenigvuldigd met een andere functie, dus daar moeten we de [productregel](#regels) op toepassen. En dan als laatst wordt er iets opgeteld, dus dat is de [somregel](#regels).

    Laten we wat functies definiëren:

    $$\large{g(x) \equiv \ln{\left((x+1)^2 \right)} * \sqrt{x} \textrm{ en } h(x) \equiv 5}$$

    Volgens de [somregel](#regels) weten we dat:

    $$\large{f'(x) = g'(x) + h'(x)}$$

    Er geldt dat:

    $$\large{h'(x) = 0,}$$

    (zie evenuteel regel 1 van de [Tabel](#tabel-met-veel-voorkomende-functies)). En dus geldt er dat:

    $$\large{f'(x) = g'(x)}$$

    Deze $g(x)$ bestaat uit meerdere functies:

    $$\large{k(x) = \ln{\left((x+1)^2 \right)} \ \ \mathrm{en} \ \ l(x) = \sqrt{x},}$$

    zodat er geldt dat:

    $$\large{g(x) = k(x) * l(x).}$$

    Volgens de [productregel](#regels) geldt er dan dat:

    $$\large{g'(x) = k'(x) \  * \ l(x) + k(x) * l'(x)}.$$

    Laten we beginnen met de afgeleide van $l(x)$ bepalen. Dit doen we met behulp van de tweede rij uit de [Tabel](#tabel-met-veel-voorkomende-functies). Daar zien we dat er voor de functie:

    $$\large{f(x) = x^n}$$

    geldt dat:

    $$\large{f'(x) = nx^{n-1}}.$$

    We maken hier gebruik van het feit dat we een wortel ook op de volgende manier kunnen schrijven:

    $$\large{l(x) = \sqrt{x} \equiv x^{\frac{1}{2}}}.$$

    Dit betekent dus dat er voor ons geldt dat $n=\frac{1}{2}$. Onze afgeleide wordt dan:

    $$\large{l'(x) = \frac{1}{2} x^{\frac{1}{2} - 1}}$$

    $$\large{l'(x) = \frac{1}{2} x^{- \frac{1}{2}}.}$$

    Dit kunnen we weer versimpelen tot:

    $$\large{l'(x) = \frac{1}{2 \sqrt{x}}.}$$

    Nu bepalen we de afgeleide van $k(x)$. Hiervoor gebruiken we de [kettingregel](#regels). We definiëren:

    $$\large{k(p) = \ln{p}, \ \ p(u) = u^2 \ \ \mathrm{en} \ \ u(x) = x + 1}$$

    We moeten nu de [kettingregel](#regels) twee keer toepassen. Laten we de [kettingregel](#regels) opschrijven:

    $$\large{k'(p(u(x))) = \frac{\mathrm{d} \ k(p)}{\mathrm{d} p} \ * \ \frac{\mathrm{d} \ p(u(x))}{\mathrm{d} x}}$$

    Nu bepalen we de afgeleide van $p$ naar $x$. Dit doen we weer met behulp van de [kettingregel](#regels). We krijgen dan:

    $$\large{ \frac{\mathrm{d} \ p(u(x))}{\mathrm{d} x} = \frac{\mathrm{d} \ p(u)}{\mathrm{d} u} \ * \ \frac{\mathrm{d} \ u(x)}{\mathrm{d} x}.}$$

    We kunnen deze twee vergelijkingen combineren tot:

    $$\large{k'(p(u(x))) = \frac{\mathrm{d} \ k(p)}{\mathrm{d} p} \ * \ \frac{\mathrm{d} \ p(u)}{\mathrm{d} u} \ * \ \frac{\mathrm{d} \ u(x)}{\mathrm{d} x}.}$$

    En nu berekenen we de afgeleides. De afgeleide van $\ln(x)$ is $\frac{1}{x}$ (zie eventueel de [tabel](#tabel-met-veel-voorkomende-functies)):

    $$\large{\frac{\mathrm{d} \ k(p)}{\mathrm{d} p} = \frac{1}{p} = \frac{1}{u^2} = \frac{1}{\left( x + 1 \right)^2}, }$$

    Nu bepalen we de afgeleide van $p(u) = u^2$ naar $u$:

    $$\large{\frac{\mathrm{d} \ p(u)}{\mathrm{d} u} = 2u = 2 (x + 1),}$$

    (zie eventueel [voorbeeld 1](#voorbeeld-1-fx-x2)).

    Als laatst bepalen we de afgeleide van $u(x) = x + 1$ naar $x$:

    $$\large{\frac{\mathrm{d} \ u(x)}{\mathrm{d} x} = 1,}$$

    De afgeleide van $x$ wordt $1$ en de afgeleide van $1$ wordt $0$ (zie eventueel de [tabel](#tabel-met-veel-voorkomende-functies)).

    Als we dit combineren en invullen vinden we:

    $$\large{k'(x) = \frac{1}{\left( x + 1 \right)^2} * 2 (x + 1) * 1}$$

    Dit versimpelt weer tot:

    $$\large{k'(x) = \frac{2}{\left( x + 1 \right)}}$$

    Nu kunnen we $g'(x)$ bepalen doordat we $k(x), l(x), k'(x) \textrm{ en } l'(x)$ hebben:

    $$\large{g'(x) = \frac{2}{\left( x + 1 \right)} * \sqrt{x} + \ln{\left((x+1)^2 \right)} * \frac{1}{2 \sqrt{x}}}$$

    Omdat we weten dat $f'(x) = g'(x)$ wordt ons eindantwoord:

    !!! quote ""
        $$\large{f'(x) = \frac{2 \sqrt{x}}{\left( x + 1 \right)}  +  \frac{\ln{\left((x+1)^2 \right)}}{2 \sqrt{x}}}$$


## Extreme waardes berekenen
Zoals in we in het filmpje bij een [parabool](#parabool) kunnen zien, is de helling gelijk aan $0$ bij een top/extreme waarde. Dit komt omdat op dit punt de functie van toenemend naar afnemend wisselt, of andersom en dit betekent dus dat er op dat punt geen toename of afname is bij een kleine toename of afname in $x$. Omdat de afgeleide de helling geeft op elk punt, betekent dit dus dat als we de coördinaten willen bepalen van de extreme waarde, we moeten stellen dat de afgeleide gelijk is aan $0$:

$$\large{f'(x) = 0}$$

Laten we naar een voorbeeld kijken. We hebben de volgende functie gegeven:

$$f(x) = -x^2 + 2.$$

We willen van deze functie berekenen wat het coordinaat van de top is met behulp van de afgeleide. Hoe pakken we dit aan?

<figure markdown>
![Top van functie](assets/images/afgeleide/f(x) = -x² + 2.svg){ width="500"}
    <figcaption>Figuur 1. De grafiek $f(x) = - x^2 + 2$ geplot met de extreme waarde.</figcaption>
</figure>

We beginnen met de afgeleide bepalen van $f(x)$. Voor de $-x^2$ term kunnen we gebruik maken van de tweede regel uit de [tabel](#tabel-met-veel-voorkomende-functies). De $+2$ term valt weg, want deze is constant (eerste regel uit de [tabel](#tabel-met-veel-voorkomende-functies)). De afgeleide wordt dus:

$$f'(x) = -2x^{2-1} = -2x$$

Omdat we het coordinaat van de top willen bepalen, moeten we kijken bij welk $x$-coördinaat de afgeleide gelijk is aan $0$. Onze vergelijking wordt dus:

$$2x = 0 \Rightarrow x = 0$$

Het $x$ coördinaat van onze top is dus $0$. Om het $y$-coördinaat te bepalen moeten we ons gevonden $x$ coördinaat van de top invullen in de originele functie $f(x)$. We krijgen dan:

$$f(x=0) = -0^2 + 2 = 2$$

Het $y$-coördinaat van de top is dus bij $y=2$. De coördinaten van de top zijn dus:

!!! quote ""
    $$\large{\textrm{De top is bij } (0, 2)}$$

en dit kunnen we ook aflezen in Figuur 1.

### **Voorbeelden**

??? example "Voorbeeld 1: Bepaal de extreme waarde van $f(x) = 6x^2 - 12x + 9$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waarde van $f(x) = 6x^2 - 12x + 9$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We moeten de extreme waarde bepalen en dus moeten we stellen dat de afgeleide van onze functie gelijk is aan $0$. Laten we eerst de afgeleide bepalen van $f(x)$.

    We weten dat de afgeleide gelijk is aan de som van de individuele termen ([somregel](#regels)). De afgeleide wordt dus:

    $$\large{f'(x) = 6*2x^{2-1} - 12}$$

    $$\large{f'(x) = 12x - 12}$$

    Om de extreme waarde te bepalen stellen we dus dat dit gelijk is aan $0$ en lossen het op om het $x$-coördinaat te vinden van de extreme waarde:

    $$\large{12x - 12 = 0}$$
    
    $$\large{12x = 12}$$

    $$\large{x = 1}$$

    Het $x$-coördinaat van de top is dus bij $x = 1$. We bepalen het $y$-coördinaat door $x=1$ in te vullen in onze originele vergelijking $f(x)$:

    $$\large{f(1) = 6*1^2 - 12*1 + 9 = 3}$$

    De coördinaten van de extreme waarde zijn dus:

    !!! quote ""
        $$\large{\textrm{De top is bij } (1, 3)}$$

    Als we de functie tekenen in Figuur 2, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = 6x² - 12x + 9.svg){ width="500"}
        <figcaption>Figuur 2. De grafiek $f(x) = 6x^2 - 12x + 9$ geplot met de extreme waarde.</figcaption>
    </figure>


??? example "Voorbeeld 2: Bepaal de extreme waardes van $f(x) = -x^3 + 6x^2 - 9x + 3$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waardes van $f(x) = -x^3 + 6x^2 - 9x + 3$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We moeten de extreme waardes bepalen, en dus moeten we stellen dat de afgeleide van $f(x)$ gelijk is aan $0$. Laten we eerst de afgeleide bepalen.

    De afgeleide van een som is hetzelfde als som van de afgeleide van de individuele termen ([somregel](#regels)), en dus wordt de afgeleide:

    $$\large{f'(x) = -3x^{3-1} + 6*2x^{2-1} - 9}$$

    $$\large{f'(x) = -3x^2 + 12x - 9}$$

    Nu stellen we deze afgeleide gelijk aan $0$:

    $$\large{-3x^2 + 12x - 9 = 0}$$

    Dit is een [kwadratische vergelijking](kwadratische_vergelijkingen.md) die we gewoon kunnen oplossen. We beginnen met alle termen te delen door $-3$:

    $$\large{x^2 - 4x + 3 = 0}$$

    Dit kunnen we oplossen met door te [ontbinden in factoren](kwadratische_vergelijkingen.md#ontbinden-in-factoren). We doen dit met behulp van de product-som methode.

    Zoals altijd maken we eerst een tabel met alle factoren die samen $3$ geven en daarna berekenen we bij elke combinatie de som en kijken we of dat de $-4$ is die we zoeken.

    | Factor 1 | Factor 2 | Product |
    | -------- | -------- | ------- |
    | 1 | 3 | 3 |
    | -1 | -3 | 3 |


    | Factor 1 | Factor 2 | Som |
    | -------- | -------- | ------- |
    | 1 | 3 | 4 |
    | -1 | -3 | -4 :fontawesome-solid-check:{ .green }|

    De factoren zijn dus $-1$ en $-3$ en dus kunnen we de vergelijking schrijven als:

    $$\large{(x - 1)(x - 3) = 0}$$

    Dit geeft ons de $x$-coördinaten:

    $$\large{x = 1 \ \vee \ x = 3}$$

    Er zijn dus in dit geval twee extreme waardes. Bij elke van die extreme waardes berekenen we het bijbehorende $y$-coördinaat door het $x$-coördinaat in $f(x)$ te stoppen:

    $$\large{f(1) = -(1)^3 + 6*(1)^2 - 9*1 + 3 = -1}$$

    $$\large{f(3) = -(3)^3 + 6*(3)^2 - 9*3 + 3 = 3}$$

    De coördinaten van de twee extreme waardes zijn dus:

    !!! quote ""
        $$\large{\textrm{De toppen zijn bij } (1, -1) \textrm{ en } (3, 3)}$$

    Als we de functie tekenen in Figuur 3, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = -x³ + 6x² - 9x + 3.svg){ width="500"}
        <figcaption>Figuur 3. De grafiek $f(x) = -x^3 + 6x^2 - 9x + 3$ geplot met de extreme waardes.</figcaption>
    </figure>


??? example "Voorbeeld 3: Bepaal de extreme waarde van $f(x) = (x-2)^{7}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waarde van $f(x) = (x-2)^{7}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We willen de extreme waarde bepalen en dus stellen we dat de afgeleide van $f(x)$ gelijk is aan $0$. Om dit te doen, berekenen we eerst de afgeleide. We doen dit met behulp van de [kettingregel](#regels). 

    We definieren de volgende functie:

    $$\large{u(x) \equiv x - 2}$$

    waardoor er dus geldt dat:

    $$\large{f(u) = u^7}$$

    De [kettingregel](#regels) vertelt ons het volgende:

    $$\large{f'(x) = f'(u) * u'(x)}$$

    We berekenen eerst de afgeleide van $f(u)$ naar $u$:

    $$\large{f'(u) = 7u^{7-1} = 7u^6}$$

    Nu de afgeleide van $u(x)$ naar $x$:

    $$\large{u'(x) = 1}$$

    En dus krijgen we dat:

    $$\large{f'(x) = 7u^6 * 1}$$

    We kunnen de $u$ weer terug subsitueren voor $x - 2$ en dan krijgen we dus:

    $$\large{f'(x) = 7(x - 2)^6}$$

    Om de extreme waarde te vinden stellen we dit dus gelijk aan $0$:

    $$\large{7(x - 2)^6 = 0}$$

    Dit betekent dus dat er moet gelden dat:

    $$\large{x - 2 = 0,}$$

    want anders kan de vergelijking nooit $0$ worden. Het $x$-coördinaat van de top is dus:

    $$\large{x = 2}$$

    Als we dit in $f(x)$ invullen vinden we als $y$-coördinaat:

    $$\large{f(2) = (2 - 2)^7 = 0}$$

    De coördinaten van onze top zijn dus:

    !!! quote ""
        $$\large{\textrm{De top is bij } (2, 0)}$$

    Als we de functie tekenen in Figuur 4, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = (x - 2)⁷.svg){ width="500"}
        <figcaption>Figuur 4. De grafiek $f(x) = (x-2)^{7}$ geplot met de extreme waarde.</figcaption>
    </figure>


??? example "Voorbeeld 4: Bepaal de extreme waardes van $f(x) = 10e^x(x^2 + 4x + 0.4)$"
    **<p style="text-align: center;font-size:20px;">Bepaal de coördinaten van de extreme waardes van $f(x) = e^x(x^2 + 4x + 0.4)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We willen de extreme waardes bepalen en dus moeten we stellen dat de afgeleide gelijk is aan $0$. We berekenen de afgeleide van $f(X)$ met de [productregel](#regels) door te definieren:

    $$\large{g(x) \equiv 10e^x \textrm{ en } h(x) = x^2 + 4x + 0.4}$$

    De [productregel](#regels) vertelt ons dat:

    $$\large{f'(x) = g'(x) \  * \ h(x) + g(x) * h'(x)}$$

    Laten we dus $g'(x)$ en $h'(x)$ bepalen (zie eventueel de [tabel](#tabel-met-veel-voorkomende-functies)):

    $$\large{g'(x) = 10e^x = g(x)}$$

    $$\large{h'(x) = 2x + 4}$$

    Nu vullen we de [productregel](#regels) in:

    $$\large{f'(x) = 10e^x(x^2 + 4x + 0.4) + 10e^x(2x + 4)}$$

    Dit kunnen we versimpelen naar:

    $$\large{f'(x) = 10e^x(x^2 + 6x + 4.4)}$$

    Om de extreme waardes te bepalen stellen we deze afgeleide gelijk aan $0$:

    $$\large{10e^x(x^2 + 6x + 4.4) = 0}$$

    Dit betekent dat een van de twee termen $0$ moet zijn:

    $$\large{e^x = 0 \ \vee \ x^2 + 6x + 4.4 = 0}$$

    Maar $e^x$ wordt nooit $0$ en dus vereenvoudigt dit naar:

    $$\large{x^2 + 6x + 4.4 = 0}$$

    Ontbinden in factoren wordt hier lastig en dus gebruiken we de [*abc* formule](kwadratische_vergelijkingen.md#de-abc-formule). We hebben:

    $$\large{a = 1, \ b = 6, \ c = 4.4}$$

    De discriminant wordt dan:

    $$D = 6^2 - 4 * 1 * 4.4 = 18.4$$

    We vullen dit nu in:

    $$\large{x = \frac{-6 + \sqrt{18.4}}{2*1} \ \vee \ \frac{-6 - \sqrt{18.4}}{2*1}}$$

    $$\large{x \approx -0.86 \ \vee \ x \approx -5.14}$$

    Deze $x$-coördinaten vullen we vervolgens in $f(x)$ om de bijbehorende $y$-coördinaten te bepalen:

    $$\large{f(-0.86) = 10e^{-0.86}\left((-0.86)^2 + 4*(-0.86) + 0.4 \right) \approx -9.7}$$

    $$\large{f(-5.14) = 10e^{-5.14}\left((-5.14)^2 + 4*(-5.14) + 0.4 \right) \approx 0.37}$$

    De coördinaten van de twee extreme waardes zijn dus:

    !!! quote ""
        $$\large{\textrm{De toppen zijn bij } (-0.86, -9.7) \textrm{ en } (-5.14, 0.37)}$$

    En als we de functie tekenen in Figuur 5, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = 10eˣ(x² + 4x + 0.4).svg){ width="500"}
        <figcaption>Figuur 5. De grafiek $f(x) = 10e^x(x^2 + 4x + 0.4)$ geplot met de extreme waardes.</figcaption>
    </figure>


??? example "Voorbeeld 5: Bepaal de extreme waardes van $f(x) = \cos^2(2x)$ in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$"
    **<p style="text-align: center;font-size:18px;">Bepaal de coördinaten van de extreme waardes van $f(x) = \cos^2(2x)$ in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$</p>**
    **<p style="text-align: center;font-size:18px;">Uitwerking</p>**

    We willen de extreme waardes bepalen en dus moeten we de afgeleide gelijk aan $0$ stellen. Om de afgeleide te bepalen maken we gebruik van de [kettingregel](#regels). We herkennen drie verschillende functies binnen $f(x)$:

    $$\large{f(x) = g^2 \textrm { met } g(h) \equiv \cos(h) \textrm{ en } h(x) \equiv 2x}$$

    De afgeleides van $g(h)$ naar $h$ en $h(x)$ naar $x$ kunnen we bepalen met behulp van de [tabel](#tabel-met-veel-voorkomende-functies):

    $$\large{g'(h) = -\sin(h)}$$

    $$\large{h'(x) = 2}$$

    De afgeleide wordt dan:

    $$\large{f'(x) = 2 * g * g'(h) * h'(x)}$$

    $$\large{f'(x) = 2 * \cos(h) * -\sin(h) * 2}$$

    Als we $h$ invullen en dit verder versimpelen vinden we:

    $$\large{f'(x) = -4 \sin(2x) \cos(2x)}$$

    Dit kunnen we eventueel nog verder versimpelen met de [sinus verdubbelingsformule](goniometrie.md#goniometrische-vergelijkingen). We krijgen dan:

    $$\large{f'(x) = -2 \sin(4x)}$$

    Nu stellen we deze afgeleide gelijk aan $0$:

    $$\large{-2 \sin(4x) = 0}$$

    $$\large{\sin(4x) = 0}$$

    $$\large{\sin(4x) = \sin(0)}$$

    Dit kunnen we [uitwerken](goniometrie.md#uitwerken-sincos-vergelijkingen) om te vinden dat:

    $$\large{4x = k * 2\pi \ \vee \ 4x = \pi + k * 2\pi}$$

    Dit kunnen we ook schrijven als:

    $$\large{4x = k\pi}$$

    $$\large{x = \frac{1}{4} k\pi,}$$

    waarbij $k$ een geheel getal is. 

    We moesten alle extreme waardes geven in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$, en dus hebben we de volgende oplossingen voor $x:$

    $$\large{x = \left\{ -\frac{1}{2} \pi, -\frac{1}{4} \pi, 0, \frac{1}{4} \pi, \frac{1}{2} \pi \right\} }$$

    Als we al deze $x$-coördinaten invullen in $f(x)$, dan kunnen we de bijbehorende $y$-coördinaten berekenen:

    $$\large{y = \left\{1, 0, 1, 0, 1 \right\} }$$

    Onze coördinaten voor de toppen worden dus:

    !!! quote ""
        $$\Large{(-\frac{1}{2} \pi, 1), \ (-\frac{1}{4} \pi, 0), \ (0, 1), \ (\frac{1}{4} \pi, 0), \textrm{ en } (\frac{1}{2} \pi, 1)}$$

    En als we de functie tekenen in Figuur 6, dan zien we dat dit klopt.

    <figure markdown>
        ![Top van functie](assets/images/afgeleide/f(x) = cos²(2x).svg){ width="500"}
        <figcaption>Figuur 6. De grafiek $f(x) = \cos^2(2x)$ geplot met de extreme waardes in het domein $[-\frac{\pi}{2}, \frac{\pi}{2}]$.</figcaption>
    </figure>