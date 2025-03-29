## **Oppervlakte wentelen om de x-as**

We hebben [net](#oppervlakte-onder-een-grafiek) gezien dat we de oppervlakte onder een grafiek kunnen bepalen met een integraal. We plotten weer een grafiek met daaronder een oppervlakte $V$.

<figure>
    <img src="/assets/images/primitieven/Oppervlakte onder de grafiek - herhaling.svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 1. Functie geplot met oppervlakte $V$ onder de grafiek.</i></span></center> <br><br>

Apart van een oppervlakte onder de grafiek kunnen we ook een inhoud maken. Om dit te doen, *wentelen* we de oppervlakte $V$ *om de $x$-as*. Dus met andere woorden, we draaien met de hele oppervlakte een rondje om de $x$-as zodat we een inhoud krijgen. Hieronder kunnen we zien hoe dit eruit ziet: 

<center>
    <a href="/assets/interactive_images/Grafiek wentelen om de x-as.html" target="_blank">
        <img src="/assets/images/primitieven/Grafiek wentelen om de x-as.png" 
             alt="Omwentelingslichaam L" 
             width="500" 
             height="400" 
             loading="lazy">
    </a>
    <br>
    *<span>Figuur 2. Oppervlakte $V$ gewenteld om de $x$-as zodat er een lichaam $L$ ontstaat met een bepaalde inhoud. (Klik voor <a href="/assets/interactive_images/Grafiek wentelen om de x-as.html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
</center>

Om de inhoud van dit lichaam $L$ te bepalen, gebruiken we dezelfde methode als bij een [oppervlakte](#oppervlakte-onder-een-grafiek). Bij een oppervlakte telden we oneindig dunne rechthoekjes allemaal bij elkaar op: 

<figure>
    <img src="/assets/images/primitieven/Oppervlakte onder de grafiek - herhaling (met 100 rechthoeken).svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 3. Functie geplot met $100$ rechthoeken onder de grafiek.</i></span></center> <br><br>

Want als we de rechthoekjes klein genoeg maken, dan is dat gelijk aan de oppervlakte $V$. We noteerden dit dan als een integraal:

$$V = \int_a^b f(x) \, dx$$

<br>

Bij een inhoud doen we eigenlijk precies hetzelfde. Het enige verschil is dat we nu geen rechthoeken bij elkaar optellen, maar cilinders. Laten we dus als eerst de inhoud van $L$ proberen te benaderen met $10$ cilinders:

<center>
    <a href="/assets/interactive_images/Grafiek wentelen om de x-as (10 cilinders).html" target="_blank">
        <img src="/assets/images/primitieven/Grafiek wentelen om de x-as (10 cilinders).png" 
             alt="Omwentelingslichaam L" 
             width="500" 
             height="400" 
             loading="lazy">
    </a>
    <br>
    *<span>Figuur 4. Oppervlakte $V$ gewenteld om de $x$-as met $10$ cilinders onder de grafiek. (Klik voor <a href="/assets/interactive_images/Grafiek wentelen om de x-as (10 cilinders).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
</center>

De inhoud van $1$ cilinder kunnen we bepalen met de formule:

$$I(\text{cilinder}) = \pi r^2 \cdot \Delta x$$

In dit geval is de straal ($r$) de hoogte tot de functie, dus $f(x)$. In ons geval geldt dus voor $1$ cilinder: 

$$I(\text{cilinder}) = \pi \left(f(x)\right)^2 \cdot \Delta x$$

Verder is $\Delta x$ de breedte van de cilinder. Dus net zoals bij de rechthoeken is $\Delta x$ voor alle cilinders hetzelfde en wordt steeds kleiner als we meer cilinders toevoegen. 

Als we de oppervlakte van alle cilinders bij elkaar doen, dan kunnen we het net zoals bij de [oppervlakte](#oppervlakte-onder-een-grafiek) schrijven als:

$$I(\text{cilinders}) = \sum_{i=1}^{10} \pi \left(f(x_i)\right)^2 \cdot \Delta x$$

waarbij we weer een sommatieteken $\sum$ gebruiken om aan te geven dat we de oppervlaktes van alle 10 cilinders bij elkaar op tellen.

Maar als we naar Figuur 4 kijken, dan zien we dat we stukjes van $L$ overhouden. De cilinders zijn nu dus nog alleen maar een benadering. En om deze benadering te verbeteren, kunnen we meer cilinders toevoegen:

<center>
    <a href="/assets/interactive_images/Grafiek wentelen om de x-as (50 cilinders).html" target="_blank">
        <img src="/assets/images/primitieven/Grafiek wentelen om de x-as (50 cilinders).png" 
             alt="Omwentelingslichaam L" 
             width="500" 
             height="400" 
             loading="lazy">
    </a>
    <br>
    *<span>Figuur 5. Oppervlakte $V$ gewenteld om de $x$-as met $50$ cilinders onder de grafiek. (Klik voor <a href="/assets/interactive_images/Grafiek wentelen om de x-as (50 cilinders).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
</center>

In Figuur 5 kunnen we zien dat het met $50$ cilinders al een stuk meer op lichaam $L$ lijkt. Maar als je inzoomt, dan zie je dat het nog steeds niet precies hetzelfde is. Daarom kunnen we net zoals bij een [oppervlakte](#oppervlakte-onder-een-grafiek) oneindig veel cilinders gebruiken die allemaal oneindig dun zijn.

Om dit te doen, laten we $\Delta x$ weer naar $0$ gaan zodat de cilinders oneindig dun worden. De inhoud van de cilinders wordt dan gelijk aan de inhoud van $L$:

$$I(L) = \lim_{\Delta x \, \to \, 0} \ \sum_{i=1}^{\infty} \pi \left(f(x_i)\right)^2 \cdot \Delta x$$

En dit kunnen we weer opschrijven als een integraal:

$$I(L) = \int_a^b \pi \left(f(x)\right)^2 \, dx$$

en omdat $\pi$ een constante is, kunnen we die ook buiten de integraal halen. De algemene vorm om een oppervlakte om de $x$-as te wentelen wordt dan dus:

$$\boxed{I(L) = \pi \int_a^b \left(f(x)\right)^2 \, dx}$$

<br>

???+ Belangrijk
    ### **Algemene Integraal Wentelen x-as**

    Om de inhoud te bepalen van een oppervlakte die gewenteld wordt om de $x$-as, moeten we de volgende integraal berekenen:

    $$\large{\boxed{I(L) = \pi \int_a^b \left(f(x)\right)^2 \, dx}}$$

    waarbij $a$ en $b$ weer de grenzen van de integraal zijn. 
    
    Om deze integraal op te lossen moet je dus eerst het kwadraat uitwerken, en daarna pas integreren.

<br>

Laten we naar een voorbeeld kijken om dit wat duidelijker te maken. Stel we hebben de volgende functie:

$$f(x) = 2x^2$$

met een oppervlakte $V$ dat ingesloten wordt door de functie $f(x)$, de $x$-as, de $y$-as en de lijn $x=2$. 

Nu willen we de inhoud bepalen van het lichaam $L$ dat ontstaat als we $V$ om de $x$-as wentelen. Hoe pakken we dit aan?

Laten we als eerst een schets maken van de situatie zodat we het beter kunnen begrijpen:

<center>
    <a href="/assets/interactive_images/f(x) = 2x^2 (3D).html" target="_blank">
        <img src="/assets/images/primitieven/f(x) = 2x^2 (3D).png" 
                alt="Omwentelingslichaam L" 
                width="500" 
                height="400" 
                loading="lazy">
    </a>
    <br>
    *<span>Figuur 6. Oppervlakte $V$ wentelt om de $x$-as om lichaam $L$ te maken. (Klik voor <a href="/assets/interactive_images/f(x) = 2x^2 (3D).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
</center>

Om de inhoud van dit lichaam $L$ te bepalen, kunnen we de [algemene vorm](#algemene-integraal-wentelen-x-as) gebruiken:

$$I(L) = \pi \int_a^b \left(f(x)\right)^2 \, dx$$

De oppervlakte $V$ ligt boven de $x$-as en wordt ingesloten door de $y$-as en $x=2$. Dit betekent dat de grenzen dus $x=0$ en $x=2$ zijn:

$$I(L) = \pi \int_0^2 \left(2x^2\right)^2 \, dx$$

En nu kunnen we nog het kwadraat uitwerken:

$$I(L) = \pi \int_0^2 4x^4 \, dx$$

En nu dat het kwadraat is uitgewerkt, kunnen we dit gaan integreren. Deze functie is van de vorm $f(x) = ax^n$, dus voor de primitieve moeten we de macht $+1$ doen en dan $1$ gedeeld door deze nieuwe macht ervoor zetten:

$$I(L) = \pi \left[ \, \dfrac{1}{5} \cdot 4x^5 \, \right]_0^2$$

En als we dit versimpelen:

$$I(L) = \pi \left[ \, \dfrac{4}{5} x^5 \, \right]_0^2$$

Nu kunnen we de grenzen invullen:

$$I(L) = \pi \left( \dfrac{4}{5} \cdot 2^5 - \dfrac{4}{5} \cdot 0^5 \right)$$

En als we dit uitwerken, dan krijgen we:

$$I(L) = \pi \left( \dfrac{4}{5} \cdot 32 \right)$$

Ons eindantwoord wordt dan:

!!! quote ""
    $$\large{I(L) = 25 \dfrac{3}{5} \pi}$$

### **Voorbeelden**

??? example "Voorbeeld 1: Bereken exact de inhoud van het omwentelingslichaam onder de functie $f(x) = 4 - x^2$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = 4 - x^2$ en de $x$-as. Oppervlakte $V$ wordt om de $x$-as gewenteld om lichaam $L$ te maken.</p>*

    <br>

    **<span style="font-size: 17px;">Bereken exact de inhoud van omwentelingslichaam $L$.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om de situatie te begrijpen maken we eerst een plaatje van de situatie:

    <center>
        <a href="/assets/interactive_images/f(x) = 4 - x^2 (3D).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = 4 - x^2 (3D).png" 
                 alt="Omwentelingslichaam L" 
                 width="500" 
                 height="400" 
                 loading="lazy">
        </a>
        <br>
        *<span>Figuur 1. Oppervlakte $V$ gewenteld om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = 4 - x^2 (3D).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>
    
    Om de inhoud van het omwentelingslichaam $L$ te berekenen, moeten we eerst de grenzen bepalen. Vlakdeel $V$ wordt ingesloten door de $x$-as, dus de grenzen zijn de snijpunten met de $x$-as.

    Om de snijpunten met de $x$-as te kunnen bepalen moeten we de functie $f(x)$ gelijk aan $0$ stellen:

    $$\large{4 - x^2 = 0}$$

    Om dit op te lossen halen we de $4$ naar de andere kant en doen beide kanten keer $-1$:

    $$\large{-x^2 = -4}$$

    $$\large{x^2 = 4}$$

    Dit is een vergelijking van de vorm [$x^2 = c$](/kwadratische_vergelijkingen/#oplossen-vorm-x2-c), dus we moeten aan beide kanten de wortel nemen:

    $$\large{x = -2 \, \vee \, x = 2}$$

    De grenzen zijn dus $x=-2$ en $x=2$. Hiermee kunnen we de integraal opstellen. De [algemene vorm](#algemene-integraal-wentelen-x-as) voor een omwentelingslichaam om de $x$-as was:

    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 \, dx}$$

    Nu kunnen we de grenzen en $f(x)$ invullen:

    $$\large{I(L) = \pi \int_{-2}^{2} \left( 4 - x^2 \right)^2 \, dx}$$

    Als we de [haakjes uitwerken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken), krijgen we:

    $$\large{I(L) = \pi \int_{-2}^{2} \left( 4 - x^2 \right)\left( 4 - x^2 \right) \, dx}$$

    $$\large{I(L) = \pi \int_{-2}^{2} 4^2 - 2 \cdot 4x^2 + \left(x^2\right)^2 \, dx}$$

    $$\large{I(L) = \pi \int_{-2}^{2} 16 - 8x^2 + x^4 \, dx}$$

    Laten we nog even de volgorde omdraaien:

    $$\large{I(L) = \pi \int_{-2}^{2} x^4 - 8x^2 + 16 \, dx}$$

    Nu kunnen we deze functie gaan integreren. 
    
    - Bij de eerste twee termen doen we de macht $+1$ en dan $1$ gedeeld door deze nieuwe macht ervoor. <br><br>
    
    - De laatste term is een constante (getal zonder $x$), dus bij de primitieve plakken we er gewoon een $x$ aan vast. 
    
    We krijgen dus:

    $$\large{I(L) = \pi \left[ \, \dfrac{1}{5}x^5 - \dfrac{1}{3} \cdot 8x^3 + 16x \, \right]_{-2}^{2}}$$

    $$\large{I(L) = \pi \left[ \, \dfrac{1}{5}x^5 - 2 \dfrac{2}{3} x^3 + 16x \, \right]_{-2}^{2}}$$

    En nu kunnen we de grenzen invullen en min elkaar doen:

    $$\large{I(L) = \pi \left( \dfrac{1}{5} \cdot 2^5 - 2 \dfrac{2}{3} \cdot 2^3 + 16 \cdot 2 \right) - \pi \left( \dfrac{1}{5} \cdot (-2)^5 - 2 \dfrac{2}{3} \cdot (-2)^3 + 16 \cdot -2 \right)}$$

    Als we dit uitwerken, dan krijgen we:

    $$\large{I(L) = \pi \left( \dfrac{1}{5} \cdot 32 - 2 \dfrac{2}{3} \cdot 8 + 32 \right) - \pi \left( \dfrac{1}{5} \cdot -32 - 2 \dfrac{2}{3} \cdot -8 - 32 \right)}$$

    $$\large{I(L) = \pi \left( 6 \dfrac{2}{5} - 21 \dfrac{1}{3} + 32 \right) - \pi \left( -6 \dfrac{2}{5} + 21 \dfrac{1}{3} - 32 \right)}$$

    $$\large{I(L) =  17 \dfrac{1}{15} \pi - - 17 \dfrac{1}{15} \pi}$$

    Ons eindantwoord wordt dan dus:

    !!! quote ""
        $$\large{I(L) =  34 \dfrac{2}{15} \pi}$$


??? example "Voorbeeld 2: Bereken exact de inhoud van het omwentelingslichaam onder de functie $f(x) = \sin(x) + \cos(x)$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \sin(x) + \cos(x)$, de $y$-as en de $x$-as. Vervolgens wordt oppervlakte $V$ om de $x$-as gewenteld om lichaam $L$ te maken.</p>*

    <br>

    **<span style="font-size: 17px;">Bereken exact de inhoud van omwentelingslichaam $L$.</span>**

    *<span style="font-size: 17px;">\* Hint: Gebruik de [goniometrische vergelijkingen](/goniometrie/#goniometrische-vergelijkingen).</span>*

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Laten we eerst een plaatje maken om de situatie een beetje te kunnen begrijpen:

    <center>
        <a href="/assets/interactive_images/f(x) = sin(x) + cos(x) (3D).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = sin(x) + cos(x) (3D).png" 
                 alt="Omwentelingslichaam L" 
                 width="500" 
                 height="400" 
                 loading="lazy">
        </a>
        <br>
        *<span>Figuur 2. Oppervlakte $V$ gewenteld om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = sin(x) + cos(x) (3D).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>


    Om de inhoud van $L$ te bepalen, hebben we eerst de grenzen nodig. We weten dat de linkergrens de $y$-as is, dus $x=0$. De rechtergrens is het eerste positieve snijpunt met de $x$-as. En om die te bepalen, moeten we de functie gelijk aan $0$ stellen:

    $$\large{\sin(x) + \cos(x) = 0}$$

    Om dit op te lossen, doen we aan beide kanten $-\sin(x)$:

    $$\large{\cos(x) = -\sin(x)}$$

    Met de [symmetrieformules](/goniometrie/#symmetrieformules) weten we dat we de $-$ in de sinus kunnen zetten:

    $$\large{\cos(x) = \sin(-x)}$$

    Nu kunnen we de cosinus [omschrijven](/goniometrie/#sinus-en-cosinus-omschrijven) naar een sinus:

    $$\large{\sin(x + \dfrac{1}{2} \pi) = \sin(-x)}$$

    Nu kunnen we deze vergelijking oplossen met de [algemene oplossing](/goniometrie/#algemene-oplossing):

    $$\large{x + \dfrac{1}{2} \pi = -x + k \cdot 2\pi \, \vee \, x + \dfrac{1}{2} \pi = \pi - \left( -x \right) + k \cdot 2\pi}$$

    $$\large{x + \dfrac{1}{2} \pi = -x + k \cdot 2\pi \, \vee \, x + \dfrac{1}{2} \pi = x + \pi + k \cdot 2\pi}$$

    En als we alle getallen naar links halen en alle $x$ termen naar rechts:

    $$\large{2x = -\dfrac{1}{2} \pi + k \cdot 2\pi \, \vee \, 0 = \dfrac{1}{2} \pi + k \cdot 2\pi}$$

    Bij de rechter oplossing is de $x$ term weggevallen, dus daar hebben we niks meer aan. We houden dus alleen over:

    $$\large{2x = -\dfrac{1}{2} \pi + k \cdot 2\pi}$$

    Nu kunnen we beide kanten door $2$ delen om te vinden:

    $$\large{x = -\dfrac{1}{4} \pi + k \cdot \pi}$$

    De eerste positieve oplossing is bij $k=1$, dus bij:

    $$\large{x = -\dfrac{1}{4}\pi + \pi = \dfrac{3}{4} \pi}$$

    De grenzen van oppervlakte $V$ zijn dus $x=0$ en $x=\frac{3}{4}\pi$. Nu kunnen we de integraal opstellen van de inhoud van omwentelingslichaam $L$:

    $$\large{I(L) = \pi \int_0^{\frac{3}{4}\pi} \left( \sin(x) + \cos(x) \right)^2 \, dx}$$

    Als we de [haakjes uitwerken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken), dan vinden we:

    $$\large{I(L) = \pi \int_0^{\frac{3}{4}\pi} \left( \sin(x) + \cos(x) \right)\left( \sin(x) + \cos(x) \right) \, dx}$$

    $$\large{I(L) = \pi \int_0^{\frac{3}{4}\pi} \sin^2(x) + 2\sin(x)\cos(x) + \cos^2(x) \, dx}$$

    Nu kunnen we twee verschillende [goniometrische vergelijkingen](/goniometrie/#goniometrische-vergelijkingen) gebruiken. Daarvoor veranderen we eerst de volgorde van de termen:
    
    $$\large{I(L) = \pi \int_0^{\frac{3}{4}\pi} \sin^2(x) + \cos^2(x) + 2\sin(x)\cos(x) \, dx}$$
    
    Nu herkennen we als eerst de term $\sin^2(x) + \cos^2(x)$. Deze term is voor alle $x$ gelijk aan $1:$

    $$\large{I(L) = \pi \int_0^{\frac{3}{4}\pi} 1 + 2\sin(x)\cos(x) \, dx}$$

    We hebben nu nog de $2\sin(x)\cos(x)$ term. Met een van de verdubbelingsformules kunnen we dit herschrijven als $\sin(2x):$

    $$\large{I(L) = \pi \int_0^{\frac{3}{4}\pi} 1 + \sin(2x) \, dx}$$

    Nu kunnen we deze functie integreren. 
    
    - Als eerst hebben we een constante (los getal zonder $x$), dus bij de primitieve plakken we er gewoon een $x$ aan vast. We krijgen dus als primitieve: $\quad \underline{1 \longrightarrow x}$ <br><br>
    
    - In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van $\sin(x)$ gelijk is aan $-\cos(x)$. Wij hebben $2x$, dus we moeten nog rekening houden met de [kettingregel](#regels). Bij de afgeleide zouden we de functie keer $2$ doen, dus om dit te compenseren moeten we het nu keer $\dfrac{1}{2}$ doen. We krijgen dus als primitieve: $\quad \underline{\sin(2x) \longrightarrow -\dfrac{1}{2} \cos(2x)}$

    Als we dit combineren, dan vinden we:

    $$\large{I(L) = \pi \left[\, x - \dfrac{1}{2} \cos(2x) \, \right]_0^{\frac{3}{4}\pi}}$$

    Nu kunnen we de grenzen invullen en min elkaar doen:

    $$\large{I(L) = \pi \left(\dfrac{3}{4} \pi - \dfrac{1}{2} \cos(2 \cdot \dfrac{3}{4} \pi) \right) - \pi \left(0 - \dfrac{1}{2} \cdot \cos(2 \cdot 0) \right)}$$

    En als we dit uitwerken, dan vinden we:

    $$\large{I(L) = \pi \left(\dfrac{3}{4} \pi - \dfrac{1}{2} \cos(1 \dfrac{1}{2} \pi) \right) - \pi \left(- \dfrac{1}{2} \cdot 1 \right)}$$

    $$\large{I(L) = \pi \left(\dfrac{3}{4} \pi - \dfrac{1}{2} \cdot 0 \right) - \pi \left(- \dfrac{1}{2} \right)}$$

    $$\large{I(L) = \pi \left(\dfrac{3}{4} \pi - 0 \right) - - \dfrac{1}{2} \pi}$$

    Ons eindantwoord wordt dan dus:

    !!! quote ""
        $$\large{I(L) = \dfrac{3}{4} \pi^2 + \dfrac{1}{2} \pi}$$



??? example "Voorbeeld 3: Bereken exact de inhoud van het omwentelingslichaam onder de functie $f(x) = \sqrt{2x - 8}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $\sqrt{2x - 8}$, de $x$-as en de lijn $x=10$. Vlakdeel $V$ wordt gewenteld om de $x$-as om lichaam $L$ te maken.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken exact de inhoud van omwentelingslichaam $L$.</span>**

    **<span style="font-size: 17px;">b) De lijn $x=p$ verdeelt $V$ in vlakdelen $V_1$ en $V_2$ die allebei wentelen om de $x$-as. De omwentelingslichamen van $V_1$ en $V_2$ noemen we $L_1$ en $L_2$. Bereken exact voor welke $p$ de inhoud van $L_1$ gelijk is aan de inhoud van $L_2$.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Om een beetje de situatie te kunnen begrijpen, schetsen we eerst de situatie:

    <center>
        <a href="/assets/interactive_images/f(x) = sqrt(2x - 8) (3D).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = sqrt(2x - 8) (3D).png" 
                 alt="Omwentelingslichaam L" 
                 width="500" 
                 height="400" 
                 loading="lazy">
        </a>
        <br>
        *<span>Figuur 3. Oppervlakte $V$ gewenteld om de $x$-as om lichaam $L$ te maken. (Klik voor <a href="/assets/interactive_images/f(x) = sqrt(2x - 8) (3D).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>


    Om de inhoud van $L$ te bepalen, hebben we de grenzen nodig. We weten al dat de rechter grens gelijk is aan $x=10$, we moeten alleen nog de linker grens bepalen. Als we in Figuur 3 kijken, dan zien we dat dit gebeurt bij het begin $f(x)$. We hebben hier te maken met een wortel functie, dus het begin punt is bij de $x$ waar de wortel gelijk is aan $0$. Want als we onze $x$ nog kleiner zouden maken, dan zouden we een negatieve wortel krijgen en dit mag niet. 

    Om het punt te bepalen waar de wortel gelijk aan $0$ is, moeten we bepalen bij welke $x$ de gedeelte in de wortel gelijk is aan $0$:

    $$\large{2x - 8 = 0}$$

    Als we dit oplossen door aan beide kanten $+8$ te doen en dan beide kanten te delen door $2$, dan vinden we:

    $$\large{2x = 8}$$

    $$\large{x = 4}$$

    Onze grenzen zijn dus $x=4$ en $x=10$. Nu kunnen we de [algemene integraal] voor een omwentelingslichaam opstellen:

    $$\large{I(L) = \pi \int_a^b \left( f(x) \right)^2 \, dx}$$

    Nu kunnen we de grenzen en $f(x)$ invullen:

    $$\large{I(L) = \pi \int_4^{10} \left( \sqrt{2x - 8} \right)^2 \, dx}$$

    Nu kunnen we de haakjes uitwerken. We weten dat een kwadraat en een wortel [tegen elkaar wegvallen](/basisvaardigheden/#regels-met-wortels), dus we houden over:

    $$\large{I(L) = \pi \int_4^{10} 2x - 8 \, dx}$$

    Nu kunnen we dit gaan integreren. 
    
    - De eerste term is van de vorm $f(x) = ax^n$, dus om de primitieve te bepalen moeten we de macht $+1$ doen. Daarna doen we $1$ gedeeld door deze nieuwe macht ervoor. Dus in ons geval krijgen we: $\quad \underline{2x \longrightarrow \dfrac{1}{2} \cdot 2x^2 = x^2}$ <br><br>

    - De tweede term is een constante (een los getal zonder $x$), dus om de primitieve te bepalen plakken we er gewoon een $x$ aan vast: $\quad \underline{-8 \longrightarrow -8x}$

    We krijgen dus:

    $$\large{I(L) = \pi \left[ \, x^2 - 8x \, \vphantom{\frac{1}{2}} \right]_4^{10}}$$

    Nu vullen we de grenzen in en doen die min elkaar:

    $$\large{I(L) = \pi \left( 10^2 - 8 \cdot 10 \right) - \pi \left( 4^2 - 8 \cdot 4 \right)}$$
    
    En als we dit uitwerken, vinden we:

    $$\large{I(L) = \pi \left( 100 - 80 \right) - \pi \left( 16 - 32 \right)}$$

    $$\large{I(L) = 20 \pi - - 16 \pi}$$

    Ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{I(L) = 36 \pi}$$

    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We moeten bepalen voor welke $p$ het omwentelingslichaam van $L$ verdeeld wordt in $2$ gelijke inhouden. Samen moeten de twee inhouden gelijk zijn aan de $36 \pi$ die we bij a) hebben gevonden, dus de inhoud van $L_1$ en $L_2$ moet allebei $18 \pi$ zijn. Laten we de integraal voor $L_1$ opstellen:

    $$\large{I(L_1) = \pi \int_4^p \left( \sqrt{2x - 8} \right)^2 \, dx}$$

    We hebben dus eigenlijk dezelfde integraal als bij a), alleen dan weten we nu de rechter grens niet. We weten dus ook dat dit gelijk moet zijn aan $18 \pi$:

    $$\large{\pi \int_4^p \left( \sqrt{2x - 8} \right)^2 \, dx = 18 \pi}$$
    
    Omdat het dezelfde integraal is als bij a), kunnen we meteen de primitieve opschrijven:

    $$\large{\pi \left[ \, x^2 - 8x \, \vphantom{\frac{1}{2}} \right]_4^{p} = 18 \pi}$$

    Nu kunnen we de grenzen invullen:

    $$\large{\pi \left( p^2 - 8p \right) - \pi \left( 4^2 - 8 \cdot 4 \right) = 18 \pi}$$

    $$\large{\pi \left( p^2 - 8p \right) - \pi \left( 16 - 32 \right) = 18 \pi}$$

    $$\large{\pi \left( p^2 - 8p \right) - -16 \pi = 18 \pi}$$

    $$\large{\pi \left( p^2 - 8p + 16 \right) = 18 \pi}$$

    Nu kunnen we deze vergelijking oplossen om $p$ te vinden. We hebben aan beide kanten iets met $\pi$, dus we kunnen aan beide kanten gedeeld door $\pi$ doen:

    $$\large{p^2 - 8p + 16 = 18}$$

    We hebben hier een $p^2$ term, een $p$ term en getallen, dus het is een vergelijking van de vorm [x^2 + bx + c = 0](/kwadratische_vergelijkingen/#oplossen-vorm-x2-bx-c-0). Laten we het dus eerst in de juiste vorm schrijven om het te kunnen oplossen. We doen aan beide kanten $-18$:

    $$\large{p^2 - 8p - 2 = 0}$$

    We kunnen dit proberen te [ontbinden in factoren](/kwadratische_vergelijkingen/#ontbinden-in-factoren), maar we zien al snel dat dit niet makkelijk is. We gebruiken daarom de [*abc* formule](/kwadratische_vergelijkingen/#de-abc-formule).

    We schrijven als eerst de $a$, de $b$ en de $c$ op:

    $$\large{a = 1, \ b = - 8 \ \mathrm{en} \ c = -2}$$

    De discriminant wordt dan:

    $$\large{D = b^2 - 4ac}$$

    $$\large{D = (-8)^2 - 4 \cdot 1 \cdot -2}$$

    $$\large{D = 64 - -8 = 72}$$

    Nu kunnen we $p$ bepalen:

    $$\large{p = \dfrac{-b \pm \sqrt{D}}{2a}}$$

    $$\large{p = \dfrac{- -8 \pm \sqrt{72}}{2 \cdot 1}}$$

    $$\large{p = \dfrac{8 + \sqrt{72}}{2} \, \vee \, p = \dfrac{8 - \sqrt{72}}{2}}$$

    $$\large{p = 4 + \dfrac{1}{2}\sqrt{72} \, \vee \, p = 4 - \dfrac{1}{2}\sqrt{72}}$$

    We kunnen nu nog de $\sqrt{72}$ versimpelen door het te schrijven als $\sqrt{36} \cdot \sqrt{2}$. We kunnen namelijk de $\sqrt{36}$ gewoon uitwerken. We krijgen dan:

    $$\large{p = 4 + \dfrac{1}{2} \cdot 6\sqrt{2} \, \vee \, p = 4 - \dfrac{1}{2} \cdot 6\sqrt{2}}$$

    En dit wordt weer:

    $$\large{p = 4 + 3\sqrt{2} \, \vee \, p = 4 - 3\sqrt{2}}$$

    Nu hebben we twee waardes van $p$ gevonden, maar welke is de juiste waarde? We weten dat $p$ het lichaam $p$ verdeelt in tweeën, dus het moet een waarde tussen $4$ en $x=10$. Het moet namelijk wel binnen de grenzen van lichaam $L$ liggen.

    Als we kijken naar de waarde $4 - 3\sqrt{2}$, dan zien we al dat dit een waarde kleiner dan $4$ is ( want we doen $4$ min een positief getal). Oftewel dat kan niet de waarde voor $p$ zijn, en dus is ons eindantwoord:

    !!! quote ""
        $$\large{p = 4 + 3\sqrt{2}}$$






??? example "Voorbeeld 4: Bereken exact de inhoud van het omwentelingslichaam onder de functie $f(x) = \dfrac{x + 1}{x}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \dfrac{x + 1}{x}$, de lijnen $y=1$, $x=1$ en $x=4$. $L$ is het omwentelingslichaam van vlakdeel $V$</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken exact de inhoud van $L$ als $V$ om de $x$-as gewenteld wordt.</span>**

    <br>

    **<span style="font-size: 17px;">b) Bereken exact de inhoud van $L$ als $V$ om de lijn $y = 1$ gewenteld wordt.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Om de situatie te begrijpen maken we eerst een plaatje van de situatie:

    <center>
        <a href="/assets/interactive_images/f(x) = (x+1) !divide! x (3D).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = (x+1) !divide! x (3D).png" 
                 alt="Omwentelingslichaam L" 
                 width="500" 
                 height="400" 
                 loading="lazy">
        </a>
        <br>
        *<span>Figuur 4. Oppervlakte $V$ gewenteld om de $x$-as om lichaam $L$ te maken. (Klik voor <a href="/assets/interactive_images/f(x) = (x+1) !divide! x (3D).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    We hebben $y=1$ als grens, dus als we de inhoud wentelen om de $x$-as krijgen we een deels hol omwentelingslichaam. Hoe kunnen we de inhoud van dit omwentelingslichaam $L$ bepalen?

    Het makkelijkste is om eerst de inhoud van het lichaam zonder gat te berekenen ($I(L_{\text{vol}})$ ), en dan min de inhoud van het gat te doen ($I(\text{gat})$ ). Op deze manier is de inhoud alleen nog van het lichaam $L$ dat we in Figuur 4 zien.

    We weten dat de grenzen $x=1$ en $x=4$ zijn, dus de inhoud van het lichaam zonder gat wordt:

    $$\large{I(L_{\text{vol}}) = \pi \int_1^4 \left(\dfrac{x+1}{x}\right)^3 \, dx}$$

    We beginnen als eerst door de teller en noemer apart in het kwadraat te doen:

    $$\large{I(L_{\text{vol}}) = \pi \int_1^4 \dfrac{\left(x+1\right)^2}{x^2} \, dx}$$

    Nu kunnen we de [haakjes uitwerken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken):

    $$\large{I(L_{\text{vol}}) = \pi \int_1^4 \dfrac{x^2 + 2x + 1}{x^2} \, dx}$$

    En om dit te integreren, moeten we de breuk opdelen in drie kleine breuken. We kunnen namelijk de termen in de teller apart door $x^2$ delen:

    $$\large{I(L_{\text{vol}}) = \pi \int_1^4 1 + \dfrac{2}{x} + \dfrac{1}{x^2} \, dx}$$

    Nu kunnen we dit integreren.

    - De eerste term is een constante (getal zonder $x$), dus bij de primitieve plakken we daar gewoon een $x$ aan vast: $\quad \underline{1 \longrightarrow 1x = 1}$ <br><br>

    - De tweede term is van de vorm $f(x) = \frac{1}{x}$. De primitieve hiervan kunnen vinden bij de tabel: $\quad \underline{\frac{2}{x} \longrightarrow 2\ln|x|}$ <br><br>

    - De derde term is van de vorm $f(x) = ax^n$. We moeten het alleen nog eerst in die vorm zetten door de breuk te vervangen met een `$-$' in de macht: $\quad \frac{1}{x^2} \rightarrow x^{-2}$. Om dit te primitiveren moeten we de macht $+1$ doen en dan $1$ gedeeld door deze nieuwe macht ervoor zetten: $\quad \underline{x^{-2} \longrightarrow \frac{1}{-1} x^{-1} = -\frac{1}{x}}$

    We krijgen dus:

    $$\large{I(L_{\text{vol}}) = \pi \left[ \, x + 2\ln|x| - \dfrac{1}{x} \, \right]_1^4}$$

    Nu kunnen we de grenzen invullen:

    $$\large{I(L_{\text{vol}}) = \pi \left( 4 + 2\ln(4) - \dfrac{1}{4} \right) - \pi \left( 1 + 2\ln(1) - \dfrac{1}{1} \right)}$$

    En als we dit versimpelen, dan vinden we:

    $$\large{I(L_{\text{vol}}) =  \pi \left( 3\dfrac{3}{4} + 2\ln(4) \right) - \pi \left( 2\ln(1) \right)}$$

    We weten dat $\ln(1) = 0$ (want $e^0 = 1$ ), dus de inhoud zonder het gat wordt dus:

    $$\large{\boxed{I(L_{\text{vol}}) =  3\dfrac{3}{4} \pi + 2\ln(4) \pi}}$$

    Nu moeten we de inhoud bepalen van het gat. Dit is gewoon een cilinder met straal $1$, dus daarvan kunnen we de inhoud makkelijk bepalen. De formule voor de inhoud van een cilinder is:

    $$\large{I(\text{cilinder}) = \pi r^2 \cdot h}$$

    Dus in ons geval hebben we een straal van $1$ (want het gat gaat tot $y=1$) en een hoogte van $4-1 = 3$

    $$\large{I(\text{gat}) = \pi \cdot 1^2 \cdot 3 = 3\pi}$$

    De inhoud van $L$ wordt dus:

    $$\large{I(L) = 3\dfrac{3}{4} \pi + 2\ln(4) \pi - 3\pi}$$

    En als we dit uitwerken (en $\pi$ buiten haakjes halen), dan vinden we als eindantwoord:

    !!! quote ""
        $$\large{I(L) = \left( \dfrac{3}{4} + 2\ln(4) \right)\pi}$$

    <br>

    **<span style="font-size: 17px;">b)</span>**

    We moeten dus de inhoud berekenen van $V$ gewenteld om de lijn $y=1$. Laten we eerst weer een schets maken van ons nieuwe omwentelingslichaam $L_2:$

    <center>
        <a href="/assets/interactive_images/f(x) = (x+1) !divide! x (3D - om y=1).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = (x+1) !divide! x (3D - om y=1).png" 
                 alt="Omwentelingslichaam L" 
                 width="500" 
                 height="400" 
                 loading="lazy">
        </a>
        <br>
        *<span>Figuur 5. Oppervlakte $V$ gewenteld om de lijn $y=1$ om lichaam $L_2$ te maken. (Klik voor <a href="/assets/interactive_images/f(x) = (x+1) !divide! x (3D - om y=1).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    Om de inhoud van $L_2$ te bepalen, kunnen we de het hele omwentelingslichaam met $1$ omlaag schuiven:

    <center>
        <a href="/assets/interactive_images/f(x) = 1 !divide! x (3D).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = 1 !divide! x (3D).png" 
                 alt="Omwentelingslichaam L" 
                 width="500" 
                 height="400" 
                 loading="lazy">
        </a>
        <br>
        *<span>Figuur 6. Omwentelingslichaam $L_2$ met $1$ omlaag verschoven. (Klik voor <a href="/assets/interactive_images/f(x) = (x+1) !divide! x (3D - om y=1).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    We zien in Figuur 6 dat als we het $L_2$ met $1$ naar beneden verschuiven, dat dan vanzelf $f(x)$ ook met $1$ mee naar beneden moet verschuiven. Onze nieuwe functie (aangegeven als $\widetilde{f}(x)$ ) wordt dus:

    $$\large{\widetilde{f}(x) = \dfrac{x + 1}{x} - 1}$$

    En dit kunnen we herschrijven als:

    $$\large{\widetilde{f}(x) = \dfrac{x + 1}{x} - \dfrac{x}{x}}$$

    $$\large{\widetilde{f}(x) = \dfrac{x + 1 - x}{x}}$$
    
    $$\large{\widetilde{f}(x) = \dfrac{1}{x}}$$

    Oftewel de inhoud van $V$ gewenteld om de lijn $y=1$ is dus hetzelfde als de inhoud van de functie $\widetilde{f}(x) = \frac{1}{x}$. Laten we deze inhoud bepalen:

    $$\large{I(L_2) = I(\widetilde{L_2}) = \pi \int_1^4 \left(\dfrac{1}{x}\right)^2 \, dx}$$

    $$\large{I(L_2) = I(\widetilde{L_2}) = \pi \int_1^4 \dfrac{1}{x^2} \, dx}$$

    We hebben bij a) gezien dat de primitieve van $\dfrac{1}{x^2}$ gelijk is aan $-\frac{1}{x}:$

    $$\large{I(L_2) = \pi \left[\,  -\frac{1}{x} \, \right]_1^4}$$

    Als we de grenzen invullen en min elkaar doen, dan vinden we:

    $$\large{I(L_2) = \pi \left(-\frac{1}{4} -- \frac{1}{1} \right)}$$

    $$\large{I(L_2) =  -\frac{1}{4}\pi + \pi }$$

    Ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{I(L_2) =  \frac{3}{4}\pi}$$

    

<hr style="height: 1.5px; background-color: #575757; border: none;">