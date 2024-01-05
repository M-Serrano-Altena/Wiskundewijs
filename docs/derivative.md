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

???+ note "Opmerking"
    ### Notatie
    Een afgeleide kan op verschillende manieren worden weergegeven:
    
    $$\Large{f'(x), \ y', \ \frac{\mathrm{d} f(x)}{\mathrm{d} x}, \ \frac{\mathrm{d} y}{\mathrm{d} x}}$$

## Voorbeelden

???+ example "Voorbeeld 1: f(x) = x²"
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


???+ example "Voorbeeld 2: f(x) = 4x"
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


???+ example "Voorbeeld 3: somregel"
    ### Voorbeeld 3: somregel
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


???+ example "Voorbeeld 4: productregel"
    ### Voorbeeld 4: productregel
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

