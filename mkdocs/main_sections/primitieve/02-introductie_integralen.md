## **Introductie Integralen**
We kunnen *integralen* gebruiken om een oppervlakte onder een grafiek te bepalen. Maar hoe werkt het en hoe lossen we zo'n integraal op?

### **Oppervlakte onder een grafiek**

Stel we willen de oppervlakte $V$ bepalen onder deze grafiek, hoe doen we dat?

<figure>
    <img src="/assets/images/primitieven/Oppervlakte onder de grafiek.svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 1. Functie geplot met oppervlakte $V$ onder de grafiek.</i></span></center> <br><br>

Deze oppervlakte heeft een lastige vorm, dus we kunnen het niet zomaar bepalen door lengte keer breedte te gebruiken... Of toch wel? 

Als we deze oppervlakte $V$ indelen in allemaal kleine rechthoeken, dan kunnen we de oppervlaktes van alle rechthoekjes bij elkaar optellen. En deze totale oppervlakte is dan hetzelfde als de oppervlakte $V$.

<figure>
    <img src="/assets/images/primitieven/Oppervlakte onder de grafiek (met 10 rechthoeken).svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 2. Functie geplot met $10$ rechthoeken onder de grafiek. De breedte van de rechthoeken is $\Delta x$. De hoogte is de waarde van de functie bij de $x$ waar de rechthoek begint.</i></span></center> <br><br>

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

<figure>
    <img src="/assets/images/primitieven/Oppervlakte onder de grafiek (met 100 rechthoeken).svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 3. Functie geplot met $100$ rechthoeken onder de grafiek.</i></span></center> <br><br>

Dit is bijvoorbeeld al een stuk beter. Het is nog steeds niet precies hetzelfde als oppervlakte $V$, maar we komen steeds meer in de buurt. We hebben nu dus:

$$\textrm{Opp alle rechthoeken} = \sum_{i=1}^{100} f(x_i) \cdot \Delta x$$

Als we meer rechthoekjes gebruiken, wordt de breedte van elke rechthoek ($\Delta x$) ook steeds kleiner. Dus als we deze breedte oneindig klein zouden kunnen maken, dan wordt onze benadering zó goed, dat het eigenlijk geen benadering meer is. 

We kunnen dus de oppervlakte van $V$ bepalen door oneindig veel rechthoeken te gebruiken. Om dit te doen, laten we de breedte $\Delta x$ naar $0$ gaan:

$$V = \lim_{\Delta x \ \to \ 0} \ \sum_{i=1}^{\infty} f(x_i) \cdot \Delta x$$

En dit kunnen we ook noteren als:

$$V = \int_a^b f(x) \, dx$$

We schrijven $dx$ in plaats van $\Delta x$ om aan te geven dat het om een oneindig kleine afstand gaat. $a$ en $b$ zijn hier de grenzen van het oppervlak. Dus $a$ is het $x$-coördinaat van het begin van de oppervlakte, $b$ het $x$-coördinaat van het einde van de oppervlakte. Voor oppervlakte $V$ van Figuur 1 zou dus gelden: $a=9$ en $b=13$.

Deze notatie noemen we een *integraal*. En het mooie van zo'n integraal is dat we nu niet meer de oppervlakte van elke rechthoek apart bij elkaar op hoeven te tellen. Met oneindig veel rechthoeken zou je namelijk een tijdje bezig zijn... 

****

### **Integralen Uitwerken**

We kunnen een *integraal* uitwerken door de primitieve te gebruiken. Laten we hiernaar kijken met behulp van een voorbeeld. Stel we hebben bijvoorbeeld de volgende functie:

$$f(x) = 6x^2$$

In Figuur 1 is deze functie geschetst met een oppervlakte $V$ onder deze grafiek. 

<figure>
    <img src="/assets/images/primitieven/f(x) = 6x^2.svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 4. De grafiek $f(x) = 6x^2$ geplot met oppervlakte $V$. Deze oppervlakte onder de functie $f(x)$ gaat van $x=0$ tot $x=1$.</i></span></center> <br><br>

Zoals we bij de sectie [Oppervlakte onder een grafiek](#oppervlakte-onder-een-grafiek) hebben gezien, kunnen we de oppervlakte $V$ bepalen met een integraal. Een integraal heeft de volgende vorm:

$$V = \int_a^b f(x) \, dx,$$

waarbij $a$ en $b$ de grenzen zijn van de oppervlakte. Dus in ons geval start de oppervlakte van $V$ bij $x=0$ en eindigt bij $x=1$:

$$V = \int_0^1 f(x) \, dx$$

Nu vullen we $f(x)$ ook in:

$$V = \int_0^1 6x^2 \, dx$$

Nu moeten we de functie *integreren*. Dit is eigenlijk hetzelfde als primitiveren, alleen dan moeten we daarna nog de grenzen invullen:

$$V = \int_a^b f(x) \, dx = \left[ \, F(x) \, \vphantom{\frac{1}{2}} \right]_a^b = F(b) - F(a)$$

Laten we dus eerst de functie primitiveren. 

We hebben $6x^2$ als functie en dit is van de vorm $f(x) = ax^n$. Om deze vorm te primitiveren, moeten we de macht $+1$ doen en dan $1$ gedeeld door deze nieuwe macht ervoor zetten. 

We hadden een macht van $2$, dus dat wordt nu een $3$. En we zetten dan een factor $\frac{1}{3}$ ervoor:

$$F(x) = \dfrac{1}{3} \cdot 6 x^{3} + c$$

Als we dit versimpelen, krijgen we:

$$F(x) = 2 x^{3} + c$$

Onze integraal wordt dus:

$$V = \left[ \, 2x^3 + c \, \vphantom{\frac{1}{2}} \right]_0^1$$

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

$$V = \left[ \, 2x^3 \, \vphantom{\frac{1}{2}}\right]_0^1 = 2 \cdot 1^3 - 2 \cdot 0^3 = 2$$


???+ Belangrijk

    #### **<span style="font-size: 18px;">Algemene Vorm</span>**

    Een integraal los je op door de primitieve te bepalen en daarna de grenzen in te vullen: 

    $$\large{V = \int_a^b f(x) \, dx = \left[ \, F(x) \, \vphantom{\frac{1}{2}}\right]_a^b = F(b) - F(a)}$$

    Hier zijn $a$ en $b$ de grenzen van de integraal. Dus bij een oppervlakte is $a$ de linkergrens van de oppervlakte, en $b$ de rechtergrens.


??? note "Bepaalde en Onbepaalde Integralen"
    We hebben net gekeken naar *bepaalde* integralen. Dit zijn integralen met grenzen, dus van de vorm:

    $$\large{V = \int_a^b f(x) \, dx = \left[\, F(x) \, \vphantom{\frac{1}{2}} \right]_a^b = F(b) - F(a)}$$

    <br>

    We hebben ook *onbepaalde* integralen. Dit zijn integralen zonder grenzen. Dit lijkt misschien ingewikkeld, maar eigenlijk is het gewoon een andere manier om een primitieve op te schijven:

    $$\large{\int f(x) \, dx = F(x)}$$

****

### **Oppervlaktes onder de x-as**

Als een oppervlakte onder de $x$-as ligt, geeft dit een negatieve bijdrage aan een integraal. In het voorbeeld hierboven hebben we gezien dat de oppervlakte $V$ van Figuur 4 gelijk is aan $2$:

$$V = \int_0^1 6x^2 \, dx = 2$$

Maar stel dat we nu $-6x$ gebruiken in plaats van $6x$. Wat komt er dan uit de integraal?

$$V_2 = \int_0^1 -6x^2 \, dx$$

$$V_2 = \left[ \, -2x^3 \, \vphantom{\frac{1}{2}} \right]_0^1$$

$$V_2 = -2 \cdot 1^3 - -2 \cdot 0^3$$

$$V_2 = -2$$

Dus zoals we hier kunnen zien krijgen we precies dezelfde oppervlakte als bij $6x$, alleen dan nu negatief. En als we deze functie tekenen, dan zien we ook dat het dezelfde oppervlakte is als bij Figuur 4. Alleen dan nu is de oppervlakte onder de $x$-as:

<figure>
    <img src="/assets/images/primitieven/f(x) = -6x^2.svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 5. De grafiek $f(x) = -6x^2$ geplot met oppervlakte $V$. Deze oppervlakte onder de functie $f(x)$ gaat van $x=0$ tot $x=1$.</i></span></center> <br><br>


Maar omdat een oppervlakte niet negatief kan zijn, voegen we een '$-$' toe bij de integraal:

$$V_2 = - \int_0^1 -6x^2 \, dx$$

Dit zorgt ervoor dat de minnen tegen elkaar wegvallen zodat de oppervlakte weer positief wordt.

???+ Belangrijk
    **<span style="font-size: 18px;">Algemene vorm onder de x-as</span>**

    Als we een oppervlakte onder de $x$-as hebben, moeten we een '$-$' toevoegen aan de integraal:

    $$\large{V = - \int_a^b f(x) \, dx}$$

    Anders krijgen we namelijk een negatieve oppervlakte.

****

### **Deel boven en deel onder de x-as**

Als zowel een deel van een oppervlakte boven de $x$-as is als onder de $x$-as, moeten we goed opletten. Want alleen het gedeelte onder de $x$-as krijgt een extra '$-$'. Dit betekent dat we de hele oppervlakte moeten splitsen in het deel boven de $x$-as en het deel onder de $x$-as.

Laten we kijken naar de volgende functie:

$$f(x) = \sin(x)$$

Stel dat we de totale oppervlakte willen bepalen van vlakdeel $V$ dat tussen $x=-\pi$ en $x=\pi$ ligt. Dit heeft een deel onder de $x$-as ( $I$ ) en een deel boven de $x$-as ( $II$ ):

<figure>
    <img src="/assets/images/primitieven/f(x) = sin(x).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 6. De grafiek $f(x) = \sin(x)$ geplot met oppervlakte $I$ en $II$. Samen gaan deze oppervlaktes van $x=-\pi$ tot $x=\pi$. Oppervlakte $I$ ligt onder de $x$-as en oppervlakte $II$ ligt boven de $x$-as.</i></span></center> <br><br>


Als we de totale oppervlakte willen berekenen, dan moeten we oppervlakte $I$ en oppervlakte $II$ apart berekenen. Want als we het als geheel proberen te integreren, dan krijgen we uit de integraal dat de totale oppervlakte $0$ is. En dit klopt natuurlijk niet. 

??? abstract "Bewijs dat $\int_{-\pi}^{\pi} \sin(x) \, dx$ uitkomt op $0$"
    We kunnen dit zelf ook gewoon berekenen met de kennis die we nu hebben. De oppervlakte onder $f(x) = \sin(x)$ gaat van $-\pi$ tot $\pi$. Onze integraal wordt dus:

    $$\large{V = \int_{-\pi}^{\pi} \sin(x) \, dx}$$

    We kunnen in de [tabel](#tabel-met-veel-voorkomende-functies) zien dat de primitieve van $\sin(x)$ is $-\cos(x)$:

    $$\large{V = \left[ \, -\cos(x) \, \vphantom{\frac{1}{2}}\right]_{-\pi}^{\pi}}$$

    Nu vullen we de grenzen in en doen ze min elkaar:

    $$\large{V = -\cos(\pi) - -\cos(-\pi)}$$

    $$\large{V = -\cos(\pi) + \cos(-\pi)}$$

    We weten dat zowel $\cos(\pi)$ als $\cos(-\pi)$ is $-1$, dus:

    $$\large{V = - -1 + -1}$$

    $$\large{V = 1 - 1}$$

    !!! quote ""
        $$\large{V = 0}$$

<br>

We beginnen eerst met de oppervlakte van $I$ te bepalen. Deze oppervlakte gaat van $x=-\pi$ tot $x=0$ en is onder de $x$-as. Onze integraal wordt dan dus:

$$I = - \int_{-\pi}^{0} \sin(x) \, dx$$

Nu kunnen we de primitieve nemen. In de [tabel](#tabel-met-veel-voorkomende-functies) zien we dat de primitieve van $\sin(x)$ gelijk is aan $-\cos(x)$:

$$I = -\left[ \, -\cos(x) \, \vphantom{\frac{1}{2}} \right]_{-\pi}^{0}$$

Nu vullen we de grenzen in en doen ze min elkaar:

$$I = -\left( -\cos(0) - -\cos(-\pi) \right)$$

$$I = -\left( -\cos(0) + \cos(-\pi) \right)$$

$$I = \cos(0) - \cos(-\pi)$$

Als we dit uitwerken, vinden we:

$$I = 1 - -1$$

$$\boxed{I = 2}$$

En nu kunnen we hetzelfde doen voor oppervlakte $II$. Deze oppervlakte gaat van $x=0$ tot $x=\pi$ en is boven de $x$-as. We krijgen dan:

$$II = \int_{0}^{\pi} \sin(x) \, dx$$

$$II = \left[ \, -\cos(x) \, \vphantom{\frac{1}{2}} \right]_{0}^{\pi}$$

$$II = -\cos(\pi) - -\cos(0)$$

$$II = -\cos(\pi) + \cos(0)$$

En als we dit uitwerken, krijgen we:

$$II = --1 + 1$$

$$\boxed{II = 2}$$

En nu kunnen we uiteindelijk de totale oppervlakte $V$ bepalen door $I$ en $II$ bij elkaar op te tellen:

$$V = I + II$$

$$V = 2 + 2$$

!!! quote ""
    $$\large{V = 4}$$


???+ Belangrijk
    #### **<span style="font-size: 18px;">Algemeen deel boven deel onder x-as</span>**

    Als een gedeelte van de oppervlakte boven de $x$-as is en een gedeelte onder de $x$-as, moeten we de integraal opsplitsen. We berekenen beide oppervlaktes apart en tellen ze daarna pas bij elkaar op:

    $$\large{V = \int_a^b f(x) \, dx \qquad \Longrightarrow \qquad V = \int_a^c f(x) \, dx \, + \int_c^b -f(x) \, dx}$$

    waarbij $c$ dus het snijpunt met de $x$-as tussen $a$ en $b$ is. We krijgen bij de tweede integraal een '$-$' omdat het [onder de $x$-as](#oppervlaktes-onder-de-x-as) ligt.

    <figure>
        <img src="/assets/images/primitieven/Functie met deel boven en deel onder de x-as.svg" 
             loading="lazy" 
             width="450" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 7. Voorbeeld van een functie met een deel boven de $x$-as en een deel onder de $x$-as.</i></span></center> <br><br>


### **Voorbeelden**

??? example "Voorbeeld 1: Los op $I = \int_1^4 3x \, dx$"
    **<p style="text-align: center;font-size:20px;">Los op $I = \int_1^4 3x \, dx$</p>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we eerst de functie $3x$ primitiveren. Deze functie is van de vorm $f(x) = ax^n$. Om de primitieve van deze vorm te bepalen, doen we de macht $+1$ en zetten $1$ gedeeld door deze nieuwe macht ervoor. We gaan dus van een macht $1$ naar een $2$ en zetten een factor $\frac{1}{2}$ ervoor:

    $$\large{I = \left[ \, \dfrac{1}{2} \cdot 3x^2 \, \right]_1^4}$$

    De integratieconstante $c$ mogen we weglaten omdat het toch wegvalt als we de grenzen invullen. Als we dit verder versimpelen, krijgen we:

    $$\large{I = \left[ \, 1 \dfrac{1}{2} x^2 \, \right]_1^4}$$

    Nu kunnen we de grenzen gaan invullen en min elkaar doen:

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

    Nu vullen we de grenzen in en doen ze min elkaar:

    $$\large{I = \left( \dfrac{1}{2} \cdot 2^4  - 2 \cdot 2^3 + \dfrac{1}{2} \cdot 2^2 - 3 \cdot 2 \right) - \left( \dfrac{1}{2} \cdot (-2)^4 - 2 \cdot (-2)^3 + \dfrac{1}{2} \cdot (-2)^2 - 3 \cdot -2 \right)}$$

    En als we dit uitwerken, krijgen we:

    $$\large{I = \left( \dfrac{1}{2} \cdot 16 - 2 \cdot 8 + \dfrac{1}{2} \cdot 4 - 6 \right) - \left( \dfrac{1}{2} \cdot 16 - 2 \cdot -8 + \dfrac{1}{2} \cdot 4 + 6 \right)}$$

    $$\large{I = \left( 8 - 16 + 2 - 6 \right)- \left( 8 + 16 + 2 + 6 \right)}$$

    $$\large{I = \left( -12 \right) - \left( 32 \right)}$$

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

    <figure>
        <img src="/assets/images/primitieven/f(x) = -x^2 + 2x + 3.svg" 
             loading="lazy" 
             width="450" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 1. De grafiek $f(x) = -x^2 + 2x + 3$ geplot met vlakdeel $V$. Vlakdeel $V$ wordt ingesloten door $f(x)$, de $x$-as en de $y$-as.</i></span></center> <br><br>

    Om de oppervlakte $V$ te bepalen, schrijven we eerst de [algemene vorm](#algemene-vorm) van een integraal op:

    $$\large{V = \int_a^b f(x) \, dx}$$

    Om dit op te lossen moeten we eerst de grenzen bepalen. We weten dat $V$ begint bij de $y$-as, dus bij $x=0.$ Vlakdeel $V$ eindigt bij het rechter snijpunt met de $x$-as, dus die moeten we eerst bepalen.

    De [snijpunten met de $x$-as](/kwadratische_vergelijkingen/#snijpunten-met-de-x-as) bepalen we door de volgende vergelijking op te lossen:

    $$\large{f(x) = 0}$$

    Dus als we $f(x)$ invullen:

    $$\large{-x^2 + 2x + 3 = 0}$$

    Om dit op te lossen, doen we eerst alles keer $-1$:

    $$\large{x^2 - 2x - 3 = 0}$$

    We kunnen dit nu oplossen door het te [ontbinden in factoren](/kwadratische_vergelijkingen/#ontbinden-in-factoren). We moeten dus twee getallen verzinnen die keer elkaar $-3$ zijn en plus elkaar $-2$. 
    
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

    $$\large{V = \left( -\dfrac{1}{3} \cdot 3^3 + 3^2 + 3 \cdot 3 \right) - \left( -\dfrac{1}{3} \cdot 0^3 + 0^2 + 3 \cdot 0 \right)}$$

    Als we dit versimpelen, vinden we:

    $$\large{V = \left( -\dfrac{1}{3} \cdot 27 + 9 + 9 \right) - (0)}$$

    $$\large{V = -9 + 18}$$

    !!! quote ""
        $$\large{V = 9}$$

    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We weten dat de lijn $x=p$ het vlakdeel $V$ verdeelt in twee gelijke oppervlaktes. Laten we dit weer schetsen zodat we de situatie beter kunnen begrijpen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = -x^2 + 2x + 3 (gesplitst).svg" 
             loading="lazy" 
             width="500" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 2. De grafiek $f(x) = -x^2 + 2x + 3$ geplot met vlakdeel $V$ verdeelt in $2$ gelijke delen. De twee delen worden gesplitst door de lijn $x=p$.</i></span></center> <br><br>

    We weten uit vraag a) dat de totale oppervlakte $V=9$ is, dus de oppervlakte van $I$ en $II$ zijn beide $4 \frac{1}{2}$:

    $$\large{I = 4\dfrac{1}{2} = II}$$

    We kunnen oppervlakte $I$ ook schrijven als integraal:

    $$\large{I = \int_0^p -x^2 + 2x + 3 \, dx}$$

    Oppervlakte $I$ gaat van $0$ tot $p$, dus vandaar dat dat ook de grenzen in de integraal zijn. We gebruiken hier oppervlakte $I$ om $p$ te bepalen, maar we hadden ook oppervlakte $II$ kunnen gebruiken. Het enige verschil is dat de grenzen dan niet van $0$ tot $p$ zouden gaan, maar van $p$ tot $3$. 
    
    Omdat we net gezegd hebben dat $I = 4 \dfrac{1}{2}$, krijgen we de volgende vergelijking:

    $$\large{\int_0^p -x^2 + 2x + 3 \, dx = 4 \dfrac{1}{2}}$$

    We kunnen nu de functie integreren (zie eventueel weer vraag a) ):

    $$\large{\left[ \, -\dfrac{1}{3} x^3 + x^2 + 3x \, \right]_0^p = 4 \dfrac{1}{2}}$$

    Nu vullen we de grenzen in en doen ze min elkaar:

    $$\large{\left( -\dfrac{1}{3} p^3 + p^2 + 3p \right) - \left( -\dfrac{1}{3} 0^3 + 0^2 + 30 \right) = 4 \dfrac{1}{2}}$$

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


??? example "Voorbeeld 4: Bereken exact de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \sqrt{x}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \sqrt{x}$, de $x$-as en de lijn $x = p$, met $p > 1$. Vlakdeel $W$ wordt ingesloten door de grafiek van $f(x)$, de $x$-as, de lijn $x=2$ en de lijn $x = 2p$</p>*

    <br>

    **<span style="font-size: 17px;"> Bereken exact de oppervlakte van vlakdeel $V$ als vlakdeel $W$ een factor $\sqrt{2}$ groter is dan $V$.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    Als eerst is het handig om een schets te maken, zodat we beter kunnen begrijpen wat we moeten doen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = sqrt(x).svg" 
             loading="lazy" 
             width="500" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 3. De grafiek $f(x) = \sqrt{x}$ geplot met vlakdeel $V$ en $W$. Vlakdeel $W$ is $\sqrt{2}$ keer groter dan vlakdeel $V$.</i></span></center> <br><br>

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


??? example "Voorbeeld 5: Bereken de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \dfrac{2}{x}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \dfrac{2}{x}$, de $x$-as, de lijn $x=-1$ en de lijn $x=p$, met $p < -1$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$ met $p = 1000$.</span>**

    **<span style="font-size: 17px;">b) Bepaal de factor waarmee $p$ moet toenemen om de oppervlakte van $V$ te verdubbelen.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Laten we als eerst een schets maken om de situatie beter te kunnen begrijpen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = 2 !divide! x.svg" 
             loading="lazy" 
             width="500" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 4. De grafiek $f(x) = \dfrac{1}{x}$ geplot met vlakdeel $V$. Het vlakdeel $V$ gaat van $x = -1000$ (te groot om weer te geven in de schets) tot $x = -1$.</i></span></center> <br><br>

    We zien in Figuur 4 dat deze oppervlakte [onder de $x$-as](#oppervlaktes-onder-de-x-as) ligt. Dit betekent dat we een '$-$' moeten toevoegen aan onze integraal. We hebben de grenzen al gekregen, dus onze integraal wordt:

    $$\large{V = - \int_{-1000}^{-1} \dfrac{2}{x} \, dx}$$
    
    In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van $\dfrac{1}{x}$ gelijk is aan $\ln|x|$. Nu hebben we nog een extra factor $2$, maar die kunnen we er gewoon voor laten staan:

    $$\large{V = - \left[ \, 2\ln|x| \, \vphantom{\frac{1}{2}}\right]_{-1000}^{-1}}$$

    Als we de grenzen invullen en min elkaar doen, krijgen we:

    $$\large{V = -\left( \,  2\ln|\! - \! 1| \ - \ 2\ln|\! - \! 1000| \, \right)}$$

    $$\large{V = -2\ln|\! - \! 1| \ + \ 2\ln|\! - \! 1000|}$$

    En nu zien we waarom de absolute waarde nemen hier zo belangrijk is. Want een logaritme van een negatief getal bestaat niet. Maar gelukkig maakt de absolute waarde het weer positief:

    $$\large{V = -2\ln(1) + 2\ln(1000)}$$

    Het logaritme van $1$ is altijd $0$ (want $e^0$ is $1$), dus we kunnen dit versimpelen naar:

    $$\large{V = 2\ln(1000)}$$

    We kunnen eventueel de $1000$ nog schrijven als $10^3$ en dan de derde macht uit de $\ln$ halen:

    $$\large{V = 3\cdot 2\ln(10)}$$

    !!! quote ""
        $$\large{V = 6\ln(10)}$$

    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We willen dat de oppervlakte van $V$ verdubbelt, dus onze nieuwe oppervlakte wordt dan:

    $$\large{V = 2 \cdot 6\ln(10)}$$

    $$\large{V = 12\ln(10)}$$

    We willen dus bepalen bij welke $p$ een grens van $x=p$ een oppervlakte geeft van $V = 12\ln(10)$.
    
    We hebben de integraal bij a) al berekend, alleen laten we de $p$ nu staan in plaats van $-1000$ in te vullen bij de grenzen:

    $$\large{V = -\int_{p}^{-1} \dfrac{2}{x} \, dx}$$

    $$\large{V = -\left[ \, 2\ln|x| \, \vphantom{\frac{1}{2}} \right]_{p}^{-1}}$$

    Nu vullen we deze grenzen in en doen het min elkaar:

    $$\large{V = -\left( \, 2\ln|\! - \! 1| \ - \ 2\ln|p| \, \right)}$$

    $$\large{V = -2\ln|\! - \! 1| \ + \ 2\ln|p|}$$

    We weten dat $\ln(1)$ is $0$, dus dit kunnen we versimpelen naar:

    $$\large{V = 2\ln|p|}$$

    En nu kunnen we zeggen dit gelijk moet zijn aan de $12\ln(10)$ die we net hebben berekend:

    $$\large{2\ln|p| = 12\ln(10)}$$

    En deze vergelijking kunnen we gaan oplossen om $p$ te bepalen. We beginnen met aan beide kanten te delen door $2$:

    $$\large{\ln|p| = 6\ln(10)}$$

    Om de logaritmes weg te werken, stoppen we de $6$ eerst in de logaritme als macht:

    $$\large{\ln|p| = \ln(10^6)}$$

    Nu kunnen we de logaritme aan beide kanten weghalen:
    
    $$\large{|p| = 10^6}$$

    We hebben nu dat $|p|$ gelijk is aan $10^6$, dus dit betekent dat er twee opties zijn:

    $$\large{p = 10^6 \ \vee \ p = -10^6}$$

    We hebben in de vraag gekregen dat $p < -1$, dus de juiste oplossing is:

    $$\large{p = -10^6 = -1 \, 000 \, 000}$$

    We moesten in de vraag bepalen met welke factor $p$ groter werd. $p$ is van $-1000$ naar $-1 \, 000 \, 000$ gegaan, dus het is toegenomen met een $1000$:

    !!! quote ""
        $$\large{\textrm{Toename met een factor } 1000}$$ 


??? example "Voorbeeld 6: Bereken de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$, de $x$-as en de buitenste twee snijpunten met de $x$-as.</p>*

    <br>

    **<span style="font-size: 17px;">Bereken de oppervlakte van $V$ op $2$ decimalen nauwkeurig.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Laten we eerst beginnen met het maken van een schets, zodat we de situatie een beetje kunnen begrijpen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = (4x-7)^3 -10x + 18.svg" 
             loading="lazy" 
             width="500" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 5. De grafiek $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$ geplot met vlakdeel $V$. Vlakdeel $V$ ligt tussen de buitenste twee snijpunten met de $x$-as.</i></span></center> <br><br>


    We zien hier dat de oppervlakte $V$ bestaat uit [een deel boven en een deel onder de $x$-as](#deel-boven-en-deel-onder-de-x-as). We willen $V$ dus opsplitsen in het deel boven en het deel onder de $x$-as:

    <figure>
        <img src="/assets/images/primitieven/f(x) = (4x-7)^3 -10x + 18 (gesplitst).svg" 
             loading="lazy" 
             width="500" 
             alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 6. De grafiek $f(x) = \left( 4x - 7 \right)^3 - 10x + 18$ geplot met vlakdeel $I$ en vlakdeel $II$. Vlakdeel $I$ ligt tussen het linker en middelste snijpunt met de $x$-as. Vlakdeel $II$ ligt tussen het middelste en rechter snijpunt met de $x$-as.</i></span></center> <br><br>


    Om de oppervlakte van $V$ te kunnen bepalen, moeten we eerst de grenzen weten. We moeten dus de [snijpunten met de $x$-as](/kwadratische_vergelijkingen/#snijpunten-met-de-x-as) bepalen. Om dit te doen, moeten we $f(x)$ gelijk aan $0$ stellen:

    $$\large{f(x) = 0}$$

    $$\large{\left( 4x - 7 \right)^3 - 10x + 18 = 0}$$

    In de vraag staat geen algebraïsch of exact, dus we mogen onze grafische rekenmachine gebruiken om dit op te lossen.

    We voeren in:

    $$\large{\left\{ \begin{array}{ l l } y_1 = \left( 4x - 7 \right)^3 - 10x + 18  \\ y_2 = 0 \end{array} \right.}$$

    De optie intersect geeft:

    $$\large{\left\{ \begin{array}{ l l l } x_1 \approx 1.33175  \\ x_2 \approx 1.80084 \\ x_3 \approx 2.11740 \end{array} \right.}$$

    Laten we eerst de integraal opstellen voor $I$. We zeiden net dat die het linker en middelste snijpunt als grenzen heeft:

    $$\large{I = \int_{1.33175}^{1.80084} \left( 4x - 7 \right)^3 - 10x + 18 \, dx}$$ 

    Nu moeten we deze functie primitiveren. 
    
    - De eerste twee termen zijn van de vorm $f(x) = ax^n$. Om de primitieve te bepalen van deze vorm, moeten we de macht $+1$ doen en $1$ gedeeld door deze nieuwe macht ervoor zetten. 
    
    - De laatste term is gewoon een constante (getal zonder $x$), dus daar plakken we gewoon een $x$ aan vast.

    We krijgen dus:

    $$\large{\widetilde{I} = \left[ \, \dfrac{1}{4} \left( 4x - 7 \right)^4 - \dfrac{1}{2} \cdot 10x^2 + 18x \, \right]_{1.33175}^{1.80084}}$$ 

    Maar als we de eerste term zouden afleiden, dan krijgen we door de [kettingregel](/afgeleide/#regels) een extra factor $4$. Omdat we die factor niet willen hebben, moeten we bij de primitieve deze weg compenseren door een extra factor $\frac{1}{4}$ toe te voegen:

    $$\large{\widetilde{I} = \left[ \, \dfrac{1}{4} \cdot \dfrac{1}{4} \left( 4x - 7 \right)^4 - \dfrac{1}{2} \cdot 10x^2 + 18x \, \right]_{1.33175}^{1.80084}}$$

    Dit kunnen we nog iets versimpelen:

    $$\large{I = \left[ \, \dfrac{1}{16} \left( 4x + 7 \right)^4 - 5x^2 + 18x \, \right]_{1.33175}^{1.80084}}$$

    Nu moeten we de grenzen invullen en min elkaar doen:

    $$\large{I = \dfrac{1}{16} \left( 4 \cdot 1.80084 - 7 \right)^4 - 5 \cdot 1.80084^2 + 18 \cdot 1.80084 - \left( \dfrac{1}{16} \left( 4 \cdot 1.33175 - 7 \right)^4 - 5 \cdot 1.33175^2 + 18 \cdot 1.33175 \right)}$$

    En als we dit uitrekenen met een rekenmachine, dan vinden we:

    $$\large{\boxed{I = 0.606768454058562...}}$$

    Nu kunnen we hetzelfde doen voor $II$. We zagen eerder dat deze oppervlakte tussen het middelste snijpunt ($x \approx 1.80084$) en het rechter snijpunt ($x \approx 2.11740$) zit. Verder is deze oppervlakte [onder de $x$-as](#oppervlaktes-onder-de-x-as), dus we moeten nog een '$-$' toevoegen bij de integraal:

    $$\large{II = - \int_{1.80084}^{2.11740} \left( 4x - 7 \right)^3 - 10x + 18 \, dx}$$ 

    We hebben net al de primitieve bepaald:

    $$\large{II = - \left[ \, \dfrac{1}{16} \left( 4x + 7 \right)^4 - 5x^2 + 18x \, \right]_{1.80084}^{2.11740}}$$

    En nu vullen we de grenzen in:

    $$\large{II = - \left( \, \dfrac{1}{16} \left( 4 \cdot 2.11740 - 7 \right)^4 - 5 \cdot 2.11740^2 + 18 \cdot 2.11740 - \left( \dfrac{1}{16} \left( 4 \cdot 1.80084 - 7 \right)^4 - 5 \cdot 1.80084^2 + 18 \cdot 1.80084 \right) \, \right)}$$

    En als we dit uitrekenen met een rekenmachine, dan vinden we:

    $$\large{\boxed{II = 0.212291635293138...}}$$

    En nu kunnen we $V$ bepalen door $I$ en $II$ bij elkaar op te tellen:

    $$\large{V = 0.606768454058562... \ + \ 0.212291635293138...}$$

    $$\large{V = 0.8190600893517...}$$

    We moesten dit op twee decimalen nauwkeurig schrijven, dus ons eindantwoord wordt:

    !!! quote ""
        $$\large{V \approx 0.82}$$


??? example "Voorbeeld 7: Bereken exact de oppervlakte van vlakdeel $V$ onder de functie $f(x) = \cos(x)$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \cos(x)$, de lijn $x = \frac{1}{6} \pi$ en de lijn $x = p$, met $\frac{1}{6} \pi < p < \pi$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$ voor $p = \frac{2}{3} \pi$.</span>**

    **<span style="font-size: 17px;">b) Bepaal $p$ als $V$ precies $1$ is.</span>**

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Als eerst maken we een schets om de situatie beter te kunnen begrijpen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = cos(x).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 7. De grafiek $f(x) = \cos(x)$ geplot met vlakdeel $V$. Het vlakdeel $V$ gaat van $x = \frac{1}{6} \pi$ tot $x = \frac{2}{3} \pi$.</i></span></center> <br><br>


    We zien hier dat we een [deel boven en een deel onder de $x$-as](#deel-boven-en-deel-onder-de-x-as) hebben. Om de oppervlakte van $V$ te berekenen, moeten we dit dus opsplitsen in twee oppervlaktes. 

    <figure>
        <img src="/assets/images/primitieven/f(x) = cos(x) (gesplitst).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 8. De grafiek $f(x) = \cos(x)$ geplot met vlakdeel $I$ en vlakdeel $II$. Vlakdeel $I$ is het gedeelte van $V$ boven de $x$-as, vlakdeel $II$ het gedeelte onder de $x$-as.</i></span></center> <br><br>


    Nu dat we $V$ gesplitst hebben in een deel boven de $x$-as en een deel onder de $x$-as, moeten we berekenen waar ze worden gesplitst. Dan weten we namelijk de grenzen van beide oppervlaktes. 
    
    We weten dat $I$ overgaat in $II$ bij de $x$-as. We moeten dus het snijpunt bepalen met de $x$-as dat binnen de grenzen van $V$ ligt ($x=\frac{1}{6} \pi$ en $x=\frac{2}{3}$). Dit doen we door $f(x)$ gelijk aan $0$ te stellen:

    $$\large{\cos(x) = 0}$$

    Om dit op te lossen moeten we eerst de $0$ schrijven als een cosinus. Op de [eenheidscirkel](/goniometrie/#de-eenheidscirkel) kunnen we aflezen dat $\cos(\frac{1}{2} \pi) = 0$. We kunnen dit dus ook schrijven als:

    $$\large{\cos(x) = \cos(\frac{1}{2} \pi)}$$

    En nu kunnen we deze [cosinus vergelijking uitwerken](/goniometrie/#algemene-oplossing):

    $$\large{x = \frac{1}{2} \pi + k \cdot 2\pi \ \vee \ x = -\frac{1}{2} + k \cdot 2\pi}$$

    We wilden het snijpunt bepalen dat tussen $x=\frac{1}{6} \pi$ en $x=\frac{2}{3} \pi$ ligt. We vinden dan alleen maar $1$ oplossing:

    $$\large{\boxed{x = \frac{1}{2} \pi}}$$

    Nu weten we dus de grenzen van zowel $I$ als $II$, want de grenzen van $V$ wisten we al. Dus $I$ begint bij $x=\frac{1}{6} \pi$ en eindigt bij $x=\frac{1}{2} \pi$ en $II$ begint juist bij $x=\frac{1}{2} \pi$ en eindigt bij $x=\frac{2}{3} \pi$. $V$ is deze twee vlakdelen plus elkaar, dus we krijgen: 

    $$\large{V = \int_{\frac{1}{6} \pi}^{\frac{1}{2} \pi} \cos(x) \, dx \, + \int_{\frac{1}{2} \pi}^{\frac{2}{3} \pi} -\cos(x) \, dx}$$

    De tweede integraal krijgt dus een '$-$' omdat vlakdeel $II$ [onder de $x$-as](#oppervlaktes-onder-de-x-as) ligt.

    In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van $\cos(x)$ gelijk is aan $\sin(x)$:

    $$\large{V = \left[ \, \sin(x) \, \vphantom{\frac{1}{2}} \right]_{\frac{1}{6} \pi}^{\frac{1}{2} \pi} + \left[ \, -\sin(x) \, \vphantom{\frac{1}{2}} \right]_{\frac{1}{2} \pi}^{\frac{2}{3} \pi}}$$ 

    Nu vullen we de grenzen in:

    $$\large{V = \left( \sin(\frac{1}{2} \pi) - \sin(\frac{1}{6} \pi) \right) + \left( -\sin(\frac{2}{3} \pi) - -\sin(\frac{1}{2} \pi) \right)}$$ 

    $$\large{V = \left( \sin(\frac{1}{2} \pi) - \sin(\frac{1}{6} \pi) \right) + \left( -\sin(\frac{2}{3} \pi) + \sin(\frac{1}{2} \pi) \right)}$$ 

    En als we dit uitwerken, vinden we:

    $$\large{V = \left( 1 - \frac{1}{2} \right) + \left( -\dfrac{1}{2} \sqrt{3} + 1\right)}$$ 

    !!! quote ""
        $$\large{V = 1\dfrac{1}{2} - \dfrac{1}{2} \sqrt{3}}$$


    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    Nu willen we $p$ weten wanneer er geldt dat $V=1$. De oppervlakte die we bij a) hebben berekend is kleiner dan $1$ (want $V = 1\frac{1}{2} - \frac{1}{2} \sqrt{3} \approx 0.63$). Dit betekent dus dat we verwachten dat $p$ groter is dan de $\frac{2}{3} \pi$ van net. Laten we een nieuwe schets maken:

    <figure>
        <img src="/assets/images/primitieven/f(x) = cos(x) (p onbekend).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 9. De grafiek $f(x) = \cos(x)$ geplot met vlakdeel $I$ en vlakdeel $II$. Vlakdeel $I$ is het gedeelte van $V$ boven de $x$-as, vlakdeel $II$ het gedeelte onder de $x$-as.</i></span></center> <br><br>

    
    Laten we net zoals bij a) de vergelijking voor $V$ opstellen. Alleen nu laten we de grens $x=p$ staan in plaats van $\frac{2}{3} \pi$ in te vullen:

    $$\large{V = \int_{\frac{1}{6} \pi}^{\frac{1}{2} \pi} \cos(x) \, dx \, + \int_{\frac{1}{2} \pi}^{p} -\cos(x) \, dx}$$

    $$\large{V = \left[ \, \sin(x) \, \vphantom{\frac{1}{2}} \right]_{\frac{1}{6} \pi}^{\frac{1}{2} \pi} + \left[ \, -\sin(x) \, \vphantom{\frac{1}{2}} \right]_{\frac{1}{2} \pi}^{p}}$$ 

    Nu vullen we de grenzen in:

    $$\large{V = \left( \sin(\frac{1}{2} \pi) - \sin(\frac{1}{6} \pi) \right) + \left( -\sin(p) - -\sin(\frac{1}{2} \pi) \right)}$$ 

    $$\large{V = \left( \sin(\frac{1}{2} \pi) - \sin(\frac{1}{6} \pi) \right) + \left( -\sin(p) + \sin(\frac{1}{2} \pi) \right)}$$ 

    En als we dit uitwerken, vinden we:

    $$\large{V = \left( 1 - \frac{1}{2} \right) + \left( -\sin(p) + 1\right)}$$ 

    $$\large{V = -\sin(p) + 1\dfrac{1}{2}}$$ 

    We wilden $p$ weten voor $V = 1$:

    $$\large{-\sin(p) + 1\frac{1}{2} = 1}$$

    Nu kunnen we deze vergelijking oplossen om $p$ te vinden. We halen eerst alle getallen naar rechts door aan beide kanten $-1\frac{1}{2}$ te doen:

    $$\large{-\sin(p) = -\dfrac{1}{2}}$$

    En nu doen we nog beide kanten keer $-1$:

    $$\large{\sin(p) = \dfrac{1}{2}}$$

    Om dit op te lossen moeten we eerst aan beide kanten een sinus hebben. We kunnen op de [eenheidscirkel](/goniometrie/#de-eenheidscirkel) aflezen dat $\sin(\frac{1}{6} \pi) = \frac{1}{2}$, dus we kunnen dit ook schrijven als:

    $$\large{\sin(p) = \sin(\frac{1}{6} \pi)}$$

    Nu kunnen we de [algemene oplossing](/goniometrie/#algemene-oplossing) gebruiken voor een sinus:

    $$\large{p = \frac{1}{6} \pi + k \cdot 2 \pi \ \vee \ p = \pi - \frac{1}{6} \pi + k \cdot 2 \pi}$$

    $$\large{p = \frac{1}{6} \pi + k \cdot 2 \pi \ \vee \ p = \frac{5}{6} \pi + k \cdot 2 \pi}$$

    We hadden in de vraag gegeven gekregen dat $p$ tussen $\frac{1}{6} \pi$ en $\pi$ ligt. Maar het kan niet $p=\frac{1}{6} \pi$ zijn, want daar begint de oppervlakte. Er blijft dan maar $1$ mogelijke oplossing over:

    !!! quote ""
        $$\large{p = \frac{5}{6} \pi}$$ 

<hr style="height: 1.5px; background-color: #575757; border: none;">