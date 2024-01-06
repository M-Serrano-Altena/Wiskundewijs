# De Afgeleide Functie

## Theorie

Een afgeleide functie geeft op elk x coördinaat de bij behorende helling/richtingscoëfficient. Dit wordt in de onderstaande voorbeelden weergegeven.

### Parabool
Een parabool heeft in het simpleste geval de vorm

$$f(x) = x^2.$$

De afgeleide van deze functie is gelijk aan 

$$f'(x) = 2x,$$ 

Waarbij $f'(x)$ aangeeft dat het gaat om de afgeleide van de functie $f(x)$ (zie dit [voorbeeld](#voorbeeld-1) voor de toelichting van het antwoord van deze afgeleide).

In het onderstaande filmpje is er te zien dat de afgeleide gelijk is aan de helling op elk punt. Ook is er te zien dat bij een top geldt dat de helling (en dus de afgeleide) gelijk is aan $0$. Dit betekent dus dat als we het x coördinaat van een top willen bepalen, we moeten stellen dat

$$f'(x) = 0.$$

???+ video
    <video controls>
    <source src="../videos/Parabola.mp4" type="video/mp4">
    </video>

    *<p style="text-align: center;">Visuele weergave van de afgeleide van de functie $f(x) = x^2$. Bij de top geldt dat de helling gelijk is aan 0. </p>*

### Exponentiele funtie 
Een exponentiele functie heeft de vorm

$f(x) = e^x$,

waar $e$ het getal van euler is. Er geldt dat $e = 2.7182818...$

???+ video
    <video controls>
    <source src="../videos/Exponential.mp4" type="video/mp4">
    </video>

???+ Belangrijk
    ### Tabel met veel voorkomende functies

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

    ### Regels

    |               | Functie                            | Afgeleide                                                                                             |
    | ------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
    | Somregel      | $\large{f(x) = g(x) + h(x)}$       | $\large{f'(x) = g'(x) + h'(x)}$                                                                       |
    | Productregel (eenvoudig)  | $\large{f(x) = a * g(x)}$ | $\large{f'(x) = a \  * \ g'(x)}$                                                    |
    | Productregel  | $\large{f(x) = g(x) * h(x)}$       | $\large{f'(x) = g'(x) \  * \ h(x) + g(x) * h'(x)}$                                                    |
    | Quotiëntregel | $\large{f(x) = \frac{g(x)}{h(x)}}$ | $\large{f'(x) = \frac{g'(x) \ * \ h(x) \ - \ g(x) \ * \ h'(x)}{h(x)^2}}$                              |
    | Kettingregel  | $\large{f(x) = g(h(x))}$           | $\large{f'(x) = \frac{\mathrm{d} \ g(h)}{\mathrm{d} h} \ * \ \frac{\mathrm{d} \ h(x)}{\mathrm{d} x}}$ |

De quotiëntregel kan je onthouden met het ezelsbruggetje: "nat - tan gedeelt door n kwadraat".

Hier staat "n" voor noemer, "t" voor teller en "a" voor afgeleide.

??? note "Opmerking"
    ### Notatie
    Een afgeleide kan op verschillende manieren worden weergegeven:
    
    $$\Large{f'(x), \ y', \ \frac{\mathrm{d} f(x)}{\mathrm{d} x}, \ \frac{\mathrm{d} y}{\mathrm{d} x}}$$

## Voorbeelden

??? example "Voorbeeld 1: f(x) = x²"
    ###Voorbeeld 1: f(x) = x²
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

    !!! quote ""
        $$\large{f'(x) = 2x}.$$


??? example "Voorbeeld 2: f(x) = 4x"
    ### Voorbeeld 2: f(x) = 4x
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 4x$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Net zoals bij het vorig voorbeeld kunnen we dit oplossen met behulp van de tweede rij van de [Tabel](#tabel-met-veel-voorkomende-functies). Maar nu hebben we ook het getal $4$ voor onze x. Als we gebruik maken van de [eenvoudige productregel](#regels) dan zien we dat de constante, in dit geval het getal $4$, niet uitmaakt voor onze afgeleide en we het gewoon ervoor kunnen laten.

    We moeten dus de afgeleide bepalen van $g(x) \equiv x$ en dan kunnen we zeggen dat $f'(x) = 4 \ g'(x)$.

    We weten dat er voor de functie

    $$\large{g(x) = x^n}$$

    geldt dat

    $$\large{g'(x) = nx^{n-1}}.$$

    Er geldt nu dat $n=1$, zodat $g(x) = x$. Onze afgeleide wordt dan:

    $$\large{g'(x) = 1*x^{1-1}}$$

    $$\large{g'(x) = x^{0}}$$

    En omdat een getal tot de macht $0$ altijd gelijk is aan $1$, wordt onze afgeleide

    $$\large{g'(x) = 1}$$

    Dit betekent dus dat

    !!! quote ""
        $$\large{f'(x) = 4}$$      


??? example "Voorbeeld 3: Somregel"
    ### Voorbeeld 3: Somregel
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = 3(\cos{(x)} + 2)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Eerst werken we de haakjes weg zodat we vinden dat

    $$\large{f(x) = 3\cos{(x)} + 6.}$$

    Daarna gebruiken we de [somregel](#regels) om dit op te splitsten in twee gedeeltes. We zeggen dat:

    $$\large{f(x) = g(x) + h(x),}$$
    
    waarbij we zeggen dat

    $$\large{g(x) = 3\cos{(x)} \ \& \ h(x) = 6.}$$

    De afgeleide van $f(x)$ wordt dan volgens de [somregel](#regels):

    $$\large{f'(x) = g'(x) + h'(x)}$$

    We kunnen dan met behulp van de eerste rij uit de [Tabel](#tabel-met-veel-voorkomende-functies) zeggen dat als

    $$\large{h(x) = 6,}$$

    wat dus een constante is die niet afhankelijk is van x, dan is de afgeleide:

    $$\large{h'(x) = 0}$$

    en dus

    $$\large{f'(x) = g'(x).}$$

    Zoals we bij het vorig voorbeeld hebben gezien, maken de constantes vóór de funtie niet uit en kunnen die ervoor blijven (zie [eenvoudige productregel](#regels)). In de [Tabel](#tabel-met-veel-voorkomende-functies) zien we dat de afgeleide van $\cos{(x)}$ gelijk is aan $-\sin{(x)}$.

    Onze afgeleide wordt dan:

    $$\large{g'(x) = -3 \sin{(x)}}$$

    en dus

    !!! quote ""
        $$\large{f'(x) = -3 \sin{(x)}}$$


??? example "Voorbeeld 4: Productregel"
    ### Voorbeeld 4: Productregel
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = xe^x$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Hier zien we dat onze functie $f(x)$ bestaat uit twee functies keer elkaar. Namelijk de functies:

    $$\large{g(x) = x \ \& \ h(x) = e^x}$$

    Dit kunnen we dus oplossen met behulp van de [productregel](#regels). Deze zegt dat:

    $$\large{f'(x) = g'(x) * h(x) + g(x) * h'(x)}$$

    Laten we eerst de $g'(x)$ en $h'(x)$ bepalen.

    Uit [Voorbeeld 2](#voorbeeld-2-fx-4x) is gebleken dat

    $$\large{g'(x) = 1.}$$

    $h'(x)$ kunnen we bepalen met de [Tabel](#tabel-met-veel-voorkomende-functies). We zien dan dat er geldt dat

    $$\large{h'(x) = h(x) = e^x.}$$

    Onze afgeleide wordt dus:

    $$\large{f'(x) = 1 * e^x + x * e^x}$$

    Dit kunnen we nog herschrijven tot

    !!! quote ""
        $$\large{f'(x) = e^x \left( 1+x \right)}$$


??? example "Voorbeeld 5: Quotiëntregel"
    ### Voorbeeld 5: Quotiëntregel

    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = \tan{(x)}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we eerst beginnen met onze $\tan$ functie op een andere manier opschrijven. In het hoofdstuk [Goniometrie](goniometrie.md#vervolg-regels-goniometrische-functies) zien we dat we een $\tan$ functie ook op de volgende manier kunnen schrijven:

    $$\large{\tan{(x)} = \frac{\sin{(x)}}{\cos{(x)}}}$$

    Nu kunnen we de [quotiëntregel](#regels) gaan toepassen. Deze zegt dat:
    
    Als:

    $$\large{f(x) = \frac{g(x)}{h(x)}}$$

    Dan: 

    $$\large{f'(x) = \frac{g'(x) \ * \ h(x) \ - \ g(x) \ * \ h'(x)}{h(x)^2}}.$$

    In ons geval geldt er dus dat

    $$\large{g(x) = \sin{(x)} \ \ \mathrm{en} \ \ h(x) = \cos{(x)}}$$

    De afgeleides zijn dan volgens de [Tabel](#tabel-met-veel-voorkomende-functies):

    $$\large{g'(x) = \cos{(x)} \ \ \mathrm{en} \ \ h'(x) = - \sin{(x)}}$$

    Nu vullen we dat in bij de quotiëntregel:

    $$\large{f'(x) = \frac{\cos{(x)} \ * \ \cos{(x)} \ - \ sin{(x)} \ * \ - \sin{(x)}}{\cos^2{(x)}}}$$

    Dit kunnen we versimplen tot:

    $$\large{f'(x) = \frac{\cos^2{(x)} + sin^2{(x)}}{\cos^2{(x)}}}$$

    We kunnen de teler nog verder versimpelen met behulp van de tweede vergelijking uit de lijst [Goniometrische Vergelijkingen](derivative.md#goniometrische-vergelijkingen). We krijgen dan als eindantwoord dat:

    !!! quote ""
        $$\large{f'(x) = \frac{1}{\cos^2{(x)}}}$$


??? example "Voorbeeld 6: Kettingregel"
    ### Voorbeeld 6: Kettingregel

    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = e^{x^2}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen maken we gebruik van de [kettingregel](#regels). Deze zegt dat voor een functie:

    $$\large{f(x) = g(h(x))}$$

    Er geldt dat:

    $$\large{f'(x) = \frac{\mathrm{d} \ g(h)}{\mathrm{d} h} \ * \ \frac{\mathrm{d} \ h(x)}{\mathrm{d} x}}$$

    Hier is $g$ een functie van $h$ en $h$ is weer een functie van $x$. In ons geval kunnen we stellen dat:

    $$\large{h(x) = x^2}$$

    Onze functie $g(h)$ wordt dan:

    $$\large{g(h) = e^h}$$

    Laten we eerst de afgeleide van $g$ naar $h$ bepalen:

    $$\large{\frac{\mathrm{d} \ g(h)}{\mathrm{d} h} = e^h,}$$
    
    want de afgeleide van een e-macht is zichzelf (zie de [Tabel](#tabel-met-veel-voorkomende-functies)). Nu bepalen we de afgeleide van $h$ naar $x$:

    $$\large{\frac{\mathrm{d} \ h(x)}{\mathrm{d} x} = 2x,}$$
    
    zie [Voorbeeld 1](#voorbeeld-1-fx-x2) voor eventuele toelichting.

    Nu kunnen we de [kettingregel](#regels) invullen:

    $$\large{f'(x) = e^h * 2x}$$

    Nu kunnen we $h$ terug substitueren:

    !!! quote ""
        $$\large{f'(x) = 2x * e^{x^2}}$$


??? example "Voorbeeld 7: Combinatie"
    ### Voorbeeld 7: Combinatie

    *<p style="text-align: left;font-size:15px;color:red "> \* Lastige opdracht</p>*
    **<p style="text-align: center;font-size:20px;">Bereken de afgeleide van de functie $f(x) = \ln{\left((x+1)^2 \right)} * \sqrt{x} + 5$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Bij zo'n soort opdracht waar je veel verschillende dingen moet doen is het erg belangrijk om echt stap voor stap te werken. Laten we beginnen met het herkenen van de functies. Er is aan het begin een functie in een functie, dus dat is iets voor de [kettingregel](#regels). Die functie wordt vermenigvuldigd met een andere functie, dus daar moeten we de [productregel](#regels) op toepassen. En dan als laatst wordt er iets opgeteld, dus dat is de [somregel](#regels).

    Laten we wat dingen definiëren:

    $$\large{g(x) \equiv \ln{\left((x+1)^2 \right)} * \sqrt{x} \ \ \mathrm{en} \ \ h(x) \equiv 5}$$

    Volgens de [somregel](#regels) weten we dat:

    $$\large{f'(x) = g'(x) + h'(x)}$$

    Er geldt dat:

    $$\large{h'(x) = 0,}$$

    zie de [Tabel](#tabel-met-veel-voorkomende-functies). En dus geldt er dat:

    $$\large{f'(x) = g'(x)}$$

    Laten we meer functies definiëren:

    $$\large{k(x) = \ln{\left((x+1)^2 \right)} \ \ \mathrm{en} \ \ l(x) = \sqrt{x},}$$

    zodat er geldt dat:

    $$\large{g(x) = k(x) * l(x).}$$

    Volgens de [productregel](#regels) geldt er dat:

    $$\large{g'(x) = k'(x) \  * \ l(x) + k(x) * l'(x)}$$

    In dit geval zijn de functies $k$ en $l$ gebruikt in plaats van $g$ en $h$. Laten we beginnen met de afgeleide van $l(x)$ bepalen. Dit doen we met behulp van de tweede rij uit de [Tabel](#tabel-met-veel-voorkomende-functies). Daar zien we dat er voor de functie:

    $$\large{f(x) = x^n}$$

    geldt dat:

    $$\large{f'(x) = nx^{n-1}}.$$

    We maken hier gebruik van het feit dat we een wortel ook op de volgende manier kunnen schrijven:

    $$\large{l(x) = \sqrt{x} \equiv x^{\frac{1}{2}}}$$

    Onze afgeleide wordt dan:

    $$\large{l'(x) = \frac{1}{2} x^{- \frac{1}{2}}.}$$

    Dit kunnen we weer versimpelen tot:

    $$\large{l'(x) = \frac{1}{2 \sqrt{x}}.}$$

    Nu bepalen we de afgeleide van $k(x)$. Hiervoor gebruiken we de [kettingregel](#regels). We definiëren:

    $$\large{k(p) = \ln{p}, \ \ p(u) = u^2 \ \ \mathrm{en} \ \ u(x) = x + 1}$$

    We moeten nu de [kettingregel](#regels) twee keer toepassen. Laten we de [kettingregel](#regels) opschrijven:

    $$\large{k'(p(u(x))) = \frac{\mathrm{d} \ k(p)}{\mathrm{d} p} \ * \ \frac{\mathrm{d} \ p(u(x))}{\mathrm{d} x}}$$

    Nu bepalen we de afgeleide van $p$ naar $x$ dit doen we weer met behulp van de [kettingregel](#regels). We krijgen dan:

    $$\large{ \frac{\mathrm{d} \ p(u(x))}{\mathrm{d} x} = \frac{\mathrm{d} \ p(u)}{\mathrm{d} u} \ * \ \frac{\mathrm{d} \ u(x)}{\mathrm{d} x}.}$$

    We kunnen deze twee vergelijkingen combineren tot:

    $$\large{k'(p(u(x))) = \frac{\mathrm{d} \ k(p)}{\mathrm{d} p} \ * \ \frac{\mathrm{d} \ p(u)}{\mathrm{d} u} \ * \ \frac{\mathrm{d} \ u(x)}{\mathrm{d} x}.}$$

    En nu berekenen we de afgeleides:

    $$\large{\frac{\mathrm{d} \ k(p)}{\mathrm{d} p} = \frac{1}{p},}$$

    zie [Tabel](#tabel-met-veel-voorkomende-functies).

    $$\large{\frac{\mathrm{d} \ p(u)}{\mathrm{d} u} = 2u,}$$

    zie [Voorbeeld 1](#voorbeeld-1-fx-x2)

    $$\large{\frac{\mathrm{d} \ u(x)}{\mathrm{d} x} = 1,}$$

    [Somregel](#regels): afgeleide van $x$ wordt $1$ en afgeleide van $1$ wordt $0$ (zie [Tabel](#tabel-met-veel-voorkomende-functies)).

    Als we dit combineren en weer terug substitueren vinden we:

    $$\large{k'(x) = \frac{2 (x + 1)}{\left( x + 1 \right)^2}}$$

    Dit versimpelt weer tot:

    $$\large{k'(x) = \frac{2}{\left( x + 1 \right)}}$$

    Als we dit weer invullen vinden we:

    $$\large{g'(x) = \frac{2}{\left( x + 1 \right)} * \sqrt{x} + \ln{\left((x+1)^2 \right)} * \frac{1}{2 \sqrt{x}}}$$

    Omdat we weten dat $f'(x) = g'(x)$ wordt ons eindantwoord (herschreven):

    !!! quote ""
        $$\large{f'(x) = \frac{2 \sqrt{x}}{\left( x + 1 \right)}  +  \frac{\ln{\left((x+1)^2 \right)}}{2 \sqrt{x}}}$$