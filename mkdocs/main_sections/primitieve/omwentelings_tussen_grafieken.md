## **Omwentelingslichaam tussen twee grafieken**

We zagen [eerder](#oppervlakte-tussen-twee-grafieken) dat we een oppervlakte tussen twee functies kunnen bereken door te integreren. Maar kunnen we deze oppervlakte tussen functies dan ook wentelen om de $x$-as om een inhoud te krijgen?

(Goed nieuws: het lijkt verdacht veel op hoe we [oppervlaktes tussen grafieken](#oppervlakte-tussen-twee-grafieken) hebben bepaald.)

<br>

Laten we kijken naar de volgende twee functies:

$$\large{\left\{ \begin{array}{ l l } f(x) = 3 - x^2  \\ g(x) = x^2 + 1 \end{array} \right.}$$

Stel we hebben de oppervlakte $V$ tussen $f(x)$ en $g(x)$ die we willen wentelen om de $x$-as. Hoe doen we dat?

Laten we eerst een schets maken om de situatie beter te begrijpen:

<figure>
    <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as (2D).svg" 
         loading="lazy" 
         width="400" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 1. De grafieken $f(x) = 3 - x^2$ en $g(x) = x^2 + 1$ geplot met oppervlakte $V$ tussen de twee functies. Dit is de oppervlakte die we gaan wentelen om de $x$-as.</i></span></center> <br><br>


<center>
    <a href="/assets/interactive_images/Opp tussen twee functies wentelen om x-as.html" target="_blank">
        <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as.png" 
                alt="Omwentelingslichaam L" 
                width="500" 
                height="400" 
                loading="lazy">
    </a>
    <br>
    *<span>Figuur 2. Omwentelingslichaam $L$ dat ontstaat als we $V$ om de $x$-as wentelen. (Klik voor <a href="/assets/interactive_images/Opp tussen twee functies wentelen om x-as.html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
</center>

We nemen dus de oppervlakte $V$ tussen de twee grafieken (Figuur 1) en dan wentelen we die oppervlakte om de $x$-as (Figuur 2). Hierdoor ontstaat omwentelingslichaam $L$.

En we zien dat we dan een soort bolachtige inhoud krijgen met een gat erin (misschien beter te zien in de interactieve afbeelding).

Laten we nu net zoals bij de [oppervlaktes tussen grafieken](#oppervlakte-tussen-twee-grafieken) kijken naar de twee oppervlaktes onder $f(x)$ en onder $g(x)$:

<figure>
    <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as (2D - opp I).svg" 
         loading="lazy" 
         width="450" 
         alt="Functie met oppervlakte V onder de grafiek">
    <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as (2D - opp II).svg" 
         loading="lazy" 
         width="450" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 3. De grafieken $f(x) = 3 - x^2$ en $g(x) = x^2 + 1$ geplot met de twee oppervlaktes onder de twee grafieken. De bovenste plot is de oppervlakte onder $f(x)$, de onderste is de oppervlakte onder $g(x)$</i></span></center> <br><br>

Laten we nu allebei deze oppervlaktes gaan wentelen om de $x$-as:

<center>
    <a href="/assets/interactive_images/Opp tussen twee functies wentelen om x-as (Inhoud 1).html" target="_blank">
        <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as (Inhoud 1).png" 
                alt="Omwentelingslichaam L" 
                width="500" 
                height="400" 
                loading="lazy">
    </a>
    <a href="/assets/interactive_images/Opp tussen twee functies wentelen om x-as (Inhoud 2).html" target="_blank">
        <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as (Inhoud 2).png" 
                alt="Omwentelingslichaam L" 
                width="500" 
                height="400" 
                loading="lazy">
    </a>
    <br>
    <br>
    *<span>Figuur 4. Omwentelingslichamen $L_1$ en $L_2$ die ontstaan als we $I$ en $II$ respectievelijk om de $x$-as wentelen. (Klik op de afbeelding voor interactieve weergave)</span>* <br><br>
</center>

In Figuur 4 kunnen we zien dat $L_1$ eigenlijk hetzelfde is als omwentelingslichaam $L$ uit Figuur 2, maar dan zonder gat. En zoals je misschien ondertussen wel kan raden, is de inhoud van $L_2$ nou net precies de inhoud die we missen in $L$ door het gat. 

Met andere woorden de inhoud van $L$ is de inhoud van het geheel ($L_1$) min de inhoud van het gat ($L_2$):

$$I(L) = I(L_1) - I(L_2)$$

En de inhouden van $L_1$ en $L_2$ kunnen we gewoon bepalen door met de [algemene formule](#algemene-integraal-wentelen-x-as):

$$I(L_1) = \pi \int_a^b \left( f(x) \right)^2 \, dx$$

$$I(L_2) = \pi \int_a^b \left( g(x) \right)^2 \, dx$$

Als we dit nu invullen bij onze formule voor $I(L)$ dan vinden we:

$$I(L) = \pi \int_a^b \left( f(x) \right)^2 \, dx - \pi \int_a^b \left( g(x) \right)^2 \, dx$$

En weer net zoals bij [oppervlaktes tussen twee grafieken](#algemene-integraal), kunnen we de twee [integralen samenvoegen](#integralen-samenvoegen):

$$\boxed{I(L) = \pi \int_a^b \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$

En dit is gelijk ook de algemene formule om een vlakdeel tussen twee functies te wentelen om de $x$-as. Hier zijn $a$ en $b$ zoals altijd gewoon weer de onder- en bovengrenzen.

<br>

Laten we dit nu uitwerken voor ons voorbeeld. We vullen als eerst $f(x)$ en $g(x)$ in de formule:

$$I(L) = \pi \int_a^b \left( 3 - x^2 \right)^2 - \left( x^2 + 1 \right)^2 \, dx$$

Nu kunnen we dit versimpelen door de [haakjes weg te werken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken):

$$I(L) = \pi \int_a^b \left(9 - 6x^2 + x^4 \right) - \left(x^4 + 2x^2 + 1 \right) \, dx$$

En nu kunnen we nog eventjes de volgorde binnen de linker haakjes aanpassen voor gemak:

$$I(L) = \pi \int_a^b \left(x^4 - 6x^2 + 9 \right) - \left(x^4 + 2x^2 + 1 \right) \, dx$$

Nu kunnen we als laatste nog de rechter haakjes keer $-1$ doen om die haakjes weg te werken:

$$I(L) = \pi \int_a^b x^4 - 6x^2 + 9 - x^4 - 2x^2 - 1 \, dx$$

En als we het nog versimpelen:

$$I(L) = \pi \int_a^b - 8x^2 + 8 \, dx$$

Nu dat we dit hebben, moeten we alleen nog de grenzen weten. We wentelen de volledige oppervlakte tussen de twee functies, dus we hebben de [snijpunten](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken) van $f(x)$ en $g(x)$ nodig:

$$f(x) = g(x)$$

$$3 - x^2 = x^2 + 1$$

$$2x^2 = 2$$

$$x^2 = 1$$

$$x = 1 \, \vee \, x = -1$$

(Zie eventueel het hoofdstuk [Kwadratische Vergelijkingen](/kwadratische_vergelijkingen/) voor meer uitleg)

Hieruit volgt dus dat de ondergrens $a=-1$ en de bovengrens $b=1$:

$$I(L) = \pi \int_{-1}^{1} - 8x^2 + 8 \, dx$$

Nu kunnen we dit gaan primitiveren:

- De eerste term is van de vorm $ax^n$, dus daar doen we de macht $+1$ en dan $1$ gedeeld door deze nieuwe macht ervoor: $\ \underline{-8x^2 \longrightarrow \frac{1}{3} \cdot -8x^3}$. En dit kunnen we weer versimpelen tot $\underline{-2\frac{2}{3} x^3}$

- De tweede term is een constante, dus daar plakken we gewoon een $x$ aan vast: $\ \underline{8 \longrightarrow 8x}$.

We krijgen dus:

$$I(L) = \pi \left[ \, -2\frac{2}{3} x^3 + 8x \, \right]_{-1}^{1}$$

En als we de grenzen invullen, dan vinden we:

$$I(L) = \pi \left(\left( -2\frac{2}{3} \cdot 1^3 + 8 \cdot 1 \right) - \left( -2\frac{2}{3} \cdot (-1)^3 + 8 \cdot -1 \right)\right)$$

En als we het versimpelen, krijgen we:

$$I(L) = \pi \left(\left( -2\frac{2}{3} + 8 \right) - \left( 2\frac{2}{3} - 8  \right)\right)$$

$$I(L) = \pi \left( -2\frac{2}{3} + 8  -2\frac{2}{3} + 8\right)$$

$$I(L) = \pi \left( -5\frac{1}{3} + 16\right)$$

Ons eindantwoord wordt dan uiteindelijk dus:

!!! quote ""
    $$\large{I(L) = 10\frac{2}{3}\pi}$$

<br><br>

???+ Belangrijk
    ### **Algemene Integraal Wentelen x-as tussen grafieken**

    Stel $L$ is een omwentelingslichaam van een oppervlakte tussen twee functies (boven de $x$-as):
    
    Dan kunnen we de inhoud van $L$ bepalen door de inhoud$^*$ onder de bovenste functie ( $I(L_1)$ ) min de inhoud onder de onderste functie ( $I(L_2)$ ) te doen:

    $$\large{I(L) = I(L_1) - I(L_2)}$$
    
    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 \, dx - \pi \int_{a}^{b} \left( g(x) \right)^2 \, dx}$$
    
    (zie eventueel [oppervlakte wentelen om de $x$-as](#algemene-integraal-wentelen-x-as) voor uitleg over hoe we deze integralen krijgen.)

    Deze integralen kunnen we nu nog [samenvoegen](#integralen-samenvoegen) voor de algemene integraal:

    $$\large{\boxed{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}}$$

    waarbij $a$ en $b$ zoals altijd de onder- en bovengrens van de inhoud zijn. 
    
    Maar in tegenstelling tot [oppervlaktes tussen twee functies](#algemene-integraal), is $f(x)$ niet *altijd* de bovenste functie. Het is beter om $f(x)$ als de 'buitenste' functie te zien en $g(x)$ als de 'binnenste' functie:
    
    - **Boven de $x$-as** is de buitenste functie ( $f(x)$ ) gewoon de bovenste functie en is $g(x)$ de onderste functie.  
    - Maar **onder de $x$-as** is de buitenste functie ( $f(x)$ ) juist de onderste functie, omdat die verder van de $x$-as ligt. De binnenste functie ( $g(x)$ ) is dan juist de bovenste functie. 

    <br>

    *<span>\* Met inhoud bedoelen we dus de inhoud die ontstaat als we de oppervlakte onder de grafiek wentelen om de $x$-as.</span>*


??? note "Oppervlaktes onder de $x$-as wentelen om de $x$-as"
    Hierboven staat dat we in de algemene formule:
    
    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$
    
    onder de $x$-as $f(x)$ juist als de onderste functie nemen in plaats van de bovenste functie. Waarom is dit?

    Laten we weer kijken naar hetzelfde voorbeeld als hierboven met de functies:

    $$\large{\left\{ \begin{array}{ l l } f(x) = 3 - x^2  \\ g(x) = x^2 + 1 \end{array} \right.}$$

    De oppervlakte tussen de twee functies was:

    <figure>
        <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as (2D).svg" 
            loading="lazy" 
            width="400" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 1 (opnieuw). De grafieken $f(x) = 3 - x^2$ en $g(x) = x^2 + 1$ geplot met oppervlakte $V$ tussen de twee functies.</i></span></center> <br><br>

    En het omwentelingslichaam was:

    <center>
        <a href="/assets/interactive_images/Opp tussen twee functies wentelen om x-as.html" target="_blank">
            <img src="/assets/images/primitieven/Opp tussen twee functies wentelen om x-as.png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 2 (opnieuw). Omwentelingslichaam $L$ dat ontstaan als we $V$ om de $x$-as wentelen. (Klik voor <a href="/assets/interactive_images/Opp tussen twee functies wentelen om x-as.html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    Laten we nu we beide functies keer $-1$ doen om ze onder de $x$-as te zetten:

    $$\large{\left\{ \begin{array}{ l l } f(x) = -3 + x^2  \\ g(x) = -x^2 - 1 \end{array} \right.}$$

    <figure>
        <img src="/assets/images/primitieven/f(x)= x^2 - 3; g(x) = -x^2 - 1.svg" 
            loading="lazy" 
            width="400" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 5. De zelfde functies als bij Figuur $1$ geplot maar dan onder de $x$-as.</i></span></center> <br><br>

    We zien in Figuur 5 dat $f(x)$ vanzelf van de bovenste functie naar de onderste functie is gegaan.

    Laten we ook kijken wat er gebeurt als we deze nieuwe oppervlakte wentelen om de $x$-as:

    <center>
        <a href="/assets/interactive_images/f(x)= x^2 - 3; g(x) = -x^2 - 1 (Inhoud).html" target="_blank">
            <img src="/assets/images/primitieven/f(x)= x^2 - 3; g(x) = -x^2 - 1 (Inhoud).png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 2. Omwentelingslichaam $L_2$ dat ontstaan als we $V_2$ om de $x$-as wentelen. (Klik voor <a href="/assets/interactive_images/f(x)= x^2 - 3; g(x) = -x^2 - 1 (Inhoud).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    En als we goed kijken, dan zien we dat dit precies hetzelfde omwentelingslichaam is als bij Figuur 2! Oftewel waar $f(x)$ **boven de $x$-as** de bovenste functie was, is dat **onder de $x$-as** de onderste functie. En voor $g(x)$ is dit precies andersom.
    
    Daarom is het dus makkelijker om erover na te denken als de buitenste functie min de binnenste functie. 

    Want zowel boven als onder de $x$-as is $f(x)$ de buitenste functie. En op dezelfde manier is $g(x)$ de binnenste functie zowel boven als onder de $x$-as.

    <br>

    **PS.**

    *<span>Als je $f(x)$ en $g(x)$ per ongeluk omdraait, is er niet super veel aan de hand. Het antwoord uit de integraal is dan precies hetzelfde alleen dan wel negatief.</span>*
    
    *<span>En omdat je weet dat een inhoud niet negatief kan zijn, betekent dat gewoon dat je $f(x)$ en $g(x)$ moet omdraaien in de [algemene integraal](#algemene-integraal-wentelen-x-as-tussen-grafieken).</span>*


<br>

### **Voorbeelden**

??? example "Voorbeeld 1: Bereken de inhoud van het omwentelingslichaam van de oppervlakte tussen de functies $f(x) = x + 3$ en $g(x) = x^2 + 1$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functies $f(x) = x + 3$ en $g(x) = x^2 + 1$.</p>*

    <br>

    **<span style="font-size: 17px;">Bereken exact de inhoud van het lichaam $L$ dat ontstaat als $V$ wentelt om de $x$-as.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Laten we als eerst een schets maken om de situatie beter te kunnen begrijpen:

    <center>
        <a href="/assets/interactive_images/f(x) = x + 3; g(x) = x^2 + 1.html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = x + 3; g(x) = x^2 + 1.png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 1. Omwentelingslichaam $L$ dat ontstaat als we de oppervlakte tussen $f(x) = x + 3$ en $g(x) = x^2 + 1$ wentelen om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = x + 3; g(x) = x^2 + 1.html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>


    Om de inhoud van lichaam $L$ te bepalen hebben we de [algemene formule](#algemene-integraal-wentelen-x-as-tussen-grafieken) nodig:

    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$

    waarbij $f(x)$ de buitenste functie is en $g(x)$ de binnenste. En dat is hier ook zo bij ons (zie eventueel Figuur 1), dus we kunnen het gewoon invullen:

    $$\large{I(L) = \pi \int_{a}^{b} \left( x + 3 \right)^2 - \left( x^2 + 1 \right)^2 \, dx}$$

    En als we de [haakjes uitwerken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken):

    $$\large{I(L) = \pi \int_{a}^{b} x^2 + 6x + 9 - \left( x^4 + 2x^2 + 1 \right) \, dx}$$

    En nu werken we de rechter haakjes weg door alles er binnen keer $-1$ te doen:

    $$\large{I(L) = \pi \int_{a}^{b} x^2 + 6x + 9 - x^4 - 2x^2 - 1 \, dx}$$

    En als we dit versimpelen:

    $$\large{I(L) = \pi \int_{a}^{b} -x^4 - x^2 + 6x + 8 \, dx}$$

    Om dit op te lossen, moeten we eerst nog de grenzen bepalen. Het gaat om de hele oppervlakte dat tussen de functies ligt, dus hebben we de [snijpunten](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken) van $f(x)$ en $g(x)$ nodig:

    $$\large{f(x) = g(x)}$$

    En als we nu $f(x)$ en $g(x)$ invullen:

    $$\large{x + 3 = x^2 + 1}$$

    Om dit op te lossen halen we eerst alles naar de linkerkant:

    $$\large{-x^2 + x + 2 = 0}$$

    En nog alles keer $-1$ om $x^2$ positief te maken:

    $$\large{x^2 - x - 2 = 0}$$

    Dit kunnen we oplossen door te [ontbinden in factoren](/kwadratische_vergelijkingen/#ontbinden-in-factoren). We zijn dus opzoek naar twee getallen die plus elkaar $-1$ zijn en keer elkaar $-2$. 

    <br>

    De getallen die daaraan voldoen zijn $-2$ en $+1$. We kunnen de formule dus ontbinden naar de vorm:

    $$\large{\left( x - 2 \right) \left( x + 1 \right) = 0}$$

    Hieruit volgt dat:

    $$\large{x - 2 = 0 \, \vee \, x + 1 = 0}$$

    Oftewel:

    $$\large{x = 2 \, \vee \, x = -1}$$

    De grenzen zijn dus $a=-1$ en $b=2$:

    $$\large{I(L) = \pi \int_{-1}^{2} -x^4 - x^2 + 6x + 8 \, dx}$$

    Nu kunnen we dit gaan primitiveren:

    - De eerste $3$ termen zijn allemaal van de vorm $ax^n$. Om dit te primitiveren, doen we de macht $+1$ en dan zetten we $1$ gedeeld door de nieuwe macht ervoor.
    - De laatste term is een constante (getal zonder $x$), dus daar plakken we gewoon een $x$ aan vast.

    We krijgen dus:

    $$\large{I(L) = \pi \left[ \, \frac{1}{5} \cdot -x^5 - \frac{1}{3} \cdot x^3 + \frac{1}{2} \cdot 6x^2 + 8x \, \right]_{-1}^{2}}$$

    En als we dit nog versimpelen:

    $$\large{I(L) = \pi \left[ \, -\frac{1}{5} x^5 - \frac{1}{3} x^3 + 3x^2 + 8x \, \right]_{-1}^{2}}$$

    Nu kunnen we de grenzen gaan invullen:

    $$\large{I(L) = \pi \left(\left( -\frac{1}{5} \cdot 2^5 - \frac{1}{3} \cdot 2^3 + 3 \cdot 2^2 + 8 \cdot 2 \right) - \left( -\frac{1}{5} \cdot (-1)^5 - \frac{1}{3} \cdot (-1)^3 + 3 \cdot (-1)^2 + 8 \cdot -1 \right) \right)}$$

    Nu kunnen we dit gaan versimpelen:

    $$\large{I(L) = \pi \left(\left( -\frac{1}{5} \cdot 32 - \frac{1}{3} \cdot 8 + 3 \cdot 4 + 16 \right) - \left( -\frac{1}{5} \cdot -1 - \frac{1}{3} \cdot -1 + 3 \cdot 1 - 8 \right) \right)}$$

    $$\large{I(L) = \pi \left(\left( -6 \frac{2}{5} - 2 \frac{2}{3} + 12 + 16 \right) - \left( \frac{1}{5} + \frac{1}{3} + 3 - 8 \right) \right)}$$

    $$\large{I(L) = \pi \left(\left( -9 \frac{1}{15} + 28 \right) - \left( \frac{8}{15} -5 \right) \right)}$$

    $$\large{I(L) = \pi \left(\left( 18 \frac{14}{15} \right) - \left( -4 \frac{7}{15}  \right) \right)}$$

    $$\large{I(L) = \pi \left( 18 \frac{14}{15} + 4 \frac{7}{15} \right)}$$

    $$\large{I(L) = 23 \frac{6}{15} \pi = 23 \frac{2}{5} \pi}$$

    Het eindantwoord wordt dus:

    !!! quote ""
        $$\large{I(L) = 23 \frac{2}{5} \pi}$$
    



??? example "Voorbeeld 2: Bereken de inhoud van het omwentelingslichaam van de oppervlakte tussen de functies $f(x) = e^{x-5}$ en $g(x) = \sqrt{2x}$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functies $f(x) = e^{x-5}$, $g(x) = \sqrt{2x}$ de lijn $x=1$ en de lijn $x=5$.</p>*

    <br>

    **<span style="font-size: 17px;">Bereken algebraïsch de inhoud van het lichaam $L$ dat ontstaat als $V$ wentelt om de $x$-as. Rond af op $2$ decimalen.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Laten we eerst een schets maken van de situatie:

    <center>
        <a href="/assets/interactive_images/f(x) = e^(x - 5); g(x) = sqrt(2x).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = e^(x - 5); g(x) = sqrt(2x).png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 2. Omwentelingslichaam $L$ dat ontstaat als we de oppervlakte tussen $f(x) = e^{x-5}$, $g(x) = \sqrt{2x}$, de lijn $x=1$ en de lijn $x=5$ wentelen om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = e^(x - 5); g(x) = sqrt(2x).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    We willen de inhoud weten van lichaam $L$ dat ontstaat als we de oppervlakte $V$ tussen $f(x)$ en $g(x)$ wentelen om de $x$-as. Om dit te berekenen gebruiken we de [algemene integraal](#algemene-integraal-wentelen-x-as-tussen-grafieken):

    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$

    waarbij de buitenste functie $f(x)$ is en de binnenste functie $g(x)$. Maar bij ons is $g(x)$ de buitenste functie, en $f(x)$ is de binnenste functie, dus moeten we het andersom opschrijven:

    $$\large{I(L) = \pi \int_{a}^{b} \left( g(x) \right)^2 - \left( f(x) \right)^2 \, dx}$$

    Nu kunnen we $g(x)$ en $f(x)$ invullen:

    $$\large{I(L) = \pi \int_{a}^{b} \left( \sqrt{2x} \right)^2 - \left( e^{x - 5} \right)^2 \, dx}$$

    Nu kunnen we nog de haakjes wegwerken:
    
    - De wortel in $\sqrt{2x}$ valt weg tegen het kwadraat dus dat wordt gewoon $2x$
    - Het kwadraat kunnen we in de $e$-macht stoppen door de machten keer elkaar te doen. We krijgen dus $e^{2 \cdot \left(x - 5\right)}$, oftewel $e^{2x - 10}$

    De integraal wordt dus:

    $$\large{I(L) = \pi \int_{a}^{b} 2x - e^{2x - 10} \, dx}$$

    Verder hebben gegeven gekregen dat de oppervlakte ingesloten wordt door $x=1$ en $x=5$, dus de grenzen zijn $a=1$ en $b=5$:

    $$\large{I(L) = \pi \int_{1}^{5} 2x - e^{2x - 10} \, dx}$$

    Nu kunnen we dit gaan primitiveren:

    - De eerste term is van de vorm $ax^n$. Dus daar moeten we gewoon de macht $+1$ doen en dan $1$ gedeeld door deze nieuwe macht ervoor zetten $\ \underline{2x \longrightarrow \frac{1}{2} \cdot 2x^2 = x^2}$
    - De tweede term is een $e$-macht, dus de primitieve ervan blijft over het algemeen hetzelfde. Alleen als we $e^{2x - 2}$ afleiden, krijgen we door de [kettingregel](/afgeleide/#regels) er een extra $2$ voor door de $2x$ in de macht. Om deze $2$ op te heffen bij de afgeleide, moeten wij een $\frac{1}{2}$ toevoegen bij de de primitieve. Dus $\ \underline{e^{2x - 5} \longrightarrow \frac{1}{2} e^{2x - 5}}$

    We krijgen dus:

    $$\large{I(L) = \pi \left[ \, x^2 - \frac{1}{2} e^{2x - 10} \, \right]_{1}^{5}}$$

    Nu kunnen we de grenzen invullen:

    $$\large{I(L) = \pi \left( \left(5^2 - \frac{1}{2} e^{2 \cdot 5 - 10} \right) - \left( 1^2 - \frac{1}{2} e^{2 \cdot 1 - 10} \right) \right)}$$

    En nu kunnen we dit gaan versimpelen:

    $$\large{I(L) = \pi \left( \left(25 - \frac{1}{2} e^{10 - 10} \right) - \left( 1 - \frac{1}{2} e^{2 - 10} \right) \right)}$$

    $$\large{I(L) = \pi \left( \left(25 - \frac{1}{2} e^{0} \right) - \left( 1 - \frac{1}{2} e^{-8} \right) \right)}$$

    Nu kunnen we de rechter haakjes wegwerken door alles er binnen keer $-1$ te doen. Verder weten we ook nog dat $e^0 = 1$:

    $$\large{I(L) = \pi \left( 25 - \frac{1}{2}  - 1 + \frac{1}{2} e^{-8} \right)}$$

    $$\large{I(L) = \pi \left( 23 \frac{1}{2} + \frac{1}{2} e^{-8} \right)}$$

    Dit kunnen we niet verder versimpelen. We moesten het antwoord geven in $2$ decimalen, dus dit kunnen we nu gewoon in onze rekenmachine invullen. We vinden dan:

    !!! quote ""
        $$\large{I(L) \approx 73.83}$$








??? example "Voorbeeld 3: Bereken de inhoud van het omwentelingslichaam van de oppervlakte tussen de functies $f(x) = -\cos(x) - 2$ en $g(x) = \cos(x) - 2$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functies $f(x) = -\cos(x) - 2$ en $g(x) = \cos(x) - 2$ (zie Figuur 3).</p>*

    <figure>
        <img src="/assets/images/primitieven/f(x) = -cos(x) - 2; g(x) = cos(x) - 2.svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 3. De grafieken $f(x) = -\cos(x) - 2$ en $g(x) = \cos(x) - 2$ geplot met oppervlakte $V$ tussen de twee functies. Deze oppervlakte wordt gewenteld om de $x$-as om lichaam $L$ te maken.</i></span></center> <br><br>

    <br>

    **<span style="font-size: 17px;">Bereken exact de inhoud van het lichaam $L$ dat ontstaat als $V$ wentelt om de $x$-as.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Laten we als eerst een schets maken van de wenteling om de $x$-as:

    <center>
        <a href="/assets/interactive_images/f(x) = -cos(x) - 2; g(x) = cos(x) - 2.html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = -cos(x) - 2; g(x) = cos(x) - 2.png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 4. Omwentelingslichaam $L$ dat ontstaat als we oppervlakte $V$ wentelen om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = -cos(x) - 2; g(x) = cos(x) - 2.html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>


    Om de inhoud van $L$ te bepalen, moeten we de [algemene integraal](#algemene-integraal-wentelen-x-as-tussen-grafieken) gebruiken:

    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$

    waarbij $f(x)$ de buitenste formule is en $g(x)$ de binnenste formule. Maar in Figuur 4 zien we dat $g(x)$ juist de buitenste functie is en $f(x)$ de binnenste functie is. Oftewel we moeten de $f(x)$ en $g(x)$ in de formule omwisselen:

    $$\large{I(L) = \pi \int_{a}^{b} \left( g(x) \right)^2 - \left( f(x) \right)^2 \, dx}$$

    Nu kunnen we $g(x)$ en $f(x)$ invullen:

    $$\large{I(L) = \pi \int_{a}^{b} \left( \cos(x) - 2 \right)^2 - \left( -\cos(x) - 2 \right)^2 \, dx}$$

    Laten we nu de [haakjes wegwerken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken):

    $$\large{I(L) = \pi \int_{a}^{b} \left( \cos^2(x) - 4\cos(x) + 4 \right) - \left( \cos^2(x) + 4\cos(x) + 4 \right) \, dx}$$

    Nu kunnen we nog de rechter haakjes wegwerken door alles er binnen keer $-1$ te doen:

    $$\large{I(L) = \pi \int_{a}^{b} \cos^2(x) - 4\cos(x) + 4  - \cos^2(x) - 4\cos(x) - 4 \, dx}$$

    En als we dit versimpelen, krijgen we:

    $$\large{I(L) = \pi \int_{a}^{b} -8\cos(x) \, dx}$$

    Nu hebben we nog de grenzen nodig van deze integraal. Oppervlakte $V$ zit volledig tussen $f(x)$ en $g(x)$, dus we hebben de [snijpunten](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken) nodig:

    $$\large{f(x) = g(x)}$$

    $$\large{-\cos(x) - 2 = \cos(x) - 2}$$

    Nu kunnen we beide kanten $-\cos(x)$ en $+2$ doen om alles naar de linkerkant te halen:

    $$\large{-2\cos(x) = 0}$$

    Nu kunnen we nog beide kanten delen door $-2$:

    $$\large{\cos(x) = 0}$$

    Om dit op te lossen, moeten we er eerst beide kanten een cosinus maken. Oftewel we moeten dus de $0$ schrijven als een cosinus.

    Op de [eenheidscirkel](/goniometrie/#de-eenheidscirkel) kunnen we aflezen welke hoek we moeten gebruiken. Het is $\cos$, dus we willen weten bij welke hoek het **$x$-coördinaat** gelijk is aan $0$. Dit is helemaal bovenaan de cirkel, oftewel bij een hoek van $\frac{1}{2} \pi$:

    $$\large{\cos(x) = \cos(\frac{1}{2} \pi)}$$

    Deze vergelijking kunnen we nu oplossen met de [algemene oplossing](/goniometrie/#algemene-oplossing) voor een cosinus:

    $$\large{x = \frac{1}{2} \pi + k \cdot 2 \pi \, \vee \, x = -\frac{1}{2} \pi + k \cdot 2 \pi}$$

    In Figuur 3 die we gegeven hadden, zien we dat $V$ ingesloten wordt door de eerste twee positieve snijpunten. Onze grenzen zijn dus de eerste twee positieve oplossingen. 
    
    En als we verschillende gehele getallen invullen voor $k$, dan zien we dat de eerste twee oplossingen zijn:

    $$\large{x = \frac{1}{2} \pi \, \vee \, 1 \frac{1}{2} \pi}$$

    Onze grenzen zijn dus $a = \dfrac{1}{2} \pi$ en $b = 1 \dfrac{1}{2} \pi$. Onze integraal wordt dan dus:

    $$\large{I(L) = \pi \int_{\frac{1}{2} \pi}^{1 \frac{1}{2} \pi} -8\cos(x) \, dx}$$

    Nu kunnen we dit gaan primitiveren.

    We hebben een $\cos(x)$ functie, en in de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien we dat de primitieve hiervan $\sin(x)$ is. Dus $\ \underline{\cos(x) \longrightarrow \sin(x)}$

    We krijgen dus:

    $$\large{I(L) = \pi \left[ \, -8\sin(x) \, \vphantom{\frac{1}{2}}\right]_{\frac{1}{2} \pi}^{1 \frac{1}{2} \pi}}$$

    Nu kunnen we de grenzen invullen:

    $$\large{I(L) = \pi \left( -8\sin(1 \frac{1}{2} \pi) - -8\sin(\frac{1}{2} \pi) \right)}$$

    $$\large{I(L) = \pi \left( -8\sin(1 \frac{1}{2} \pi) + 8\sin(\frac{1}{2} \pi) \right)}$$

    We weten ([eenheidscirkel](/goniometrie/#de-eenheidscirkel) of rekenmachine) dat $\sin(1 \frac{1}{2} \pi) = -1$ en $\sin(\frac{1}{2} \pi) = 1$, dus we krijgen:

    $$\large{I(L) = \pi \left( -8 \cdot -1 + 8 \cdot 1 \right)}$$

    $$\large{I(L) = \pi \left( 8 + 8 \right)}$$

    Ons eindantwoord wordt dus:

    !!! quote ""
        $$\large{I(L) = 16 \pi}$$




??? example "Voorbeeld 4: Bereken de inhoud van het omwentelingslichaam van de oppervlakte tussen de functies $f(x) = -x^3 + 6x$ en $g(x) = 2x$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functies $f(x) = -x^3 + 6x$ en $g(x) = 2x$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken algebraïsch de inhoud van het lichaam $L$ dat ontstaat als $V$ wentelt om de $x$-as. Rond af op $1$ decimaal.</span>**

    <br>

    **<span style="font-size: 17px;">b) De lijn $x=p$ verdeelt de oppervlakte $V$ in de twee oppervlaktes $I$ en $II$. Allebei deze oppervlaktes wentelen vervolgens om de $x$-as om lichamen $L_1$ en $L_2$ te maken. Bereken in $2$ decimalen nauwkeurig voor welke $p$ de inhoud van $L_1$ gelijk is aan de inhoud van $L_2$.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    <br>

    **<span style="font-size: 17px;">a)</span>**

    Laten we eerst de situatie schetsen:

    <center>
        <a href="/assets/interactive_images/f(x) = 6x - x^3; g(x) = 2x.html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = 6x - x^3; g(x) = 2x.png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 5. Omwentelingslichaam $L$ dat ontstaat als we de oppervlakte tussen $f(x) = -x^3 + 6x$ en $g(x) = 2x$ wentelen om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = 6x - x^3; g(x) = 2x.html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>


    Om de inhoud van $L$ te bepalen, moeten we [algemene integraal](#algemene-integraal-wentelen-x-as-tussen-grafieken) gebruiken:

    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$

    waarbij $f(x)$ de buitenste functie is en $g(x)$ de binnenste functie. In ons geval is dit ook zo, dus we kunnen gelijk $f(x)$ en $g(x)$ in de formule stoppen:

    $$\large{I(L) = \pi \int_{a}^{b} \left( -x^3 + 6x \right)^2 - \left( 2x \right)^2 \, dx}$$

    Nu kunnen we nog de [haakjes uitwerken](/basisvaardigheden/#kwadratisch-haakjes-wegwerken):

    $$\large{I(L) = \pi \int_{a}^{b} \left(x^6 - 12x^4 + 36x^2 \right)  -  \left(4x^2\right) \, dx}$$

    En als we dit versimpelen:

    $$\large{I(L) = \pi \int_{a}^{b} x^6 - 12x^4 + 36x^2  -  4x^2 \, dx}$$

    $$\large{I(L) = \pi \int_{a}^{b} x^6 - 12x^4 + 32x^2 \, dx}$$

    Nu moeten we nog de grenzen $a$ en $b$ bepalen. De oppervlakte zit volledig tussen de twee functies in, dus we moeten de [snijpunten](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken) van $f(x)$ en $g(x)$ bepalen:

    $$\large{f(x) = g(x)}$$

    En als we $f(x)$ en $g(x)$ invullen:

    $$\large{-x^3 + 6x = 2x}$$

    Om dit op te lossen, halen we eerst alles naar de linkerkant:

    $$\large{-x^3 + 4x = 0}$$

    Nu kunnen we nog alles keer $-1$ doen om $x^3$ positief te maken:

    $$\large{x^3 - 4x = 0}$$

    We zien dat beide termen een $x$ hebben, dus die kunnen we buiten haakjes halen:

    $$\large{x \left(x^2 - 4 \right) = 0}$$

    De twee termen keer elkaar zijn gelijk aan $0$, dus dat betekent dat één van de twee gelijk moet zijn aan $0$:

    $$\large{x = 0 \, \vee \, x^2 - 4 = 0}$$

    Nu kunnen we nog de rechter vergelijking oplossen door de $4$ naar de andere kant te halen:

    $$\large{x = 0 \, \vee \, x^2 = 4 }$$

    De oplossingen hiervan zijn:

    $$\large{x = 0 \, \vee \, x = 2 \, \vee \, x = -2 }$$

    (zie eventueel [oplossen vorm $x^2 = c$](/kwadratische_vergelijkingen/#oplossen-vorm-x2-c))

    De oplossingen op volgorde van klein naar groot zijn dus:
    
    $$\large{x = -2, \, x=0, \, x=2}$$

    En als we naar Figuur 5 kijken, dan zien we dat $V$ ingesloten wordt door de oorsprong en het snijpunt rechts daarvan. Oftewel door het punt $x=0$ en het punt $x=2$.

    Onze grenzen zijn dus $a=0$ en $b=2$:

    $$\large{I(L) = \pi \int_{0}^{2} x^6 - 12x^4 + 32x^2 \, dx}$$

    Nu kunnen we dit gaan primitiveren.

    Alle termen zijn van de vorm $ax^n$. Oftewel om de primitieve te nemen, moeten we de macht $+1$ doen en dan $1$ gedeeld door deze nieuwe macht ervoor doen.

    We krijgen dus:

    $$\large{I(L) = \pi \left[ \, \frac{1}{7} x^7 - \frac{1}{5} \cdot 12x^5 + \frac{1}{3} \cdot 32x^3 \, \right]_{0}^{2}}$$

    En als we dit verder versimpelen, krijgen we:

    $$\large{I(L) = \pi \left[ \, \frac{1}{7} x^7 - 2 \frac{2}{5} x^5 + 10 \frac{2}{3} x^3 \, \right]_{0}^{2}}$$

    Nu kunnen we de grenzen gaan invullen:

    $$\large{I(L) = \pi \left( \left( \frac{1}{7} \cdot 2^7 - 2 \frac{2}{5} \cdot 2^5 + 10 \frac{2}{3} \cdot 2^3 \right) - \left( \frac{1}{7} \cdot 0^7 - 2 \frac{2}{5} \cdot 0^5 + 10 \frac{2}{3} \cdot 0^3 \right) \right)}$$


    En als we dit versimpelen, dan krijgen we:

    $$\large{I(L) = \pi \left( \left( \frac{1}{7} \cdot 128 - 2 \frac{2}{5} \cdot 32 + 10 \frac{2}{3} \cdot 8 \right) - \left( 0 \right) \right)}$$

    $$\large{I(L) = \pi \left(18 \frac{2}{7} - 76 \frac{4}{5} + 85 \frac{1}{3} \right)}$$

    En als we dit uitrekenen, dan vinden we:

    $$\large{I(L) = 84.254...}$$

    We moesten afronden op $1$ decimaal, dus ons eindantwoord wordt:

    !!! quote ""
        $$\large{I(L) \approx 84.3}$$


    <br>

    **<span style="font-size: 17px;">b)</span>**

    We moeten dus bepalen voor welke waarde van $p$ de lijn $x=p$ het lichaam $L$ verdeelt in twee gelijke inhouden $L_1$ en $L_2$. Laten we zoals altijd eerst een schets maken van de situatie:

    <figure>
        <img src="/assets/images/primitieven/f(x) = 6x - x^3; g(x) = 2x (gesplitst - 2D).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 6. De oppervlakte $V$ tussen $f(x)$ en $g(x)$ opgedeeld in de oppervlaktes $I$ en $II$. Deze twee oppervlaktes wentelen we om de $x$-as om de lichamen $L_1$ en $L_2$ te maken.</i></span></center> <br><br>

    Deze oppervlaktes $I$ en $II$ wentelen we vervolgens allebei om de $x$-as om lichamen $L_1$ en $L_2$ te krijgen:

    <center>
        <a href="/assets/interactive_images/f(x) = 6x - x^3; g(x) = 2x (gesplitst - 3D).html" target="_blank">
            <img src="/assets/images/primitieven/f(x) = 6x - x^3; g(x) = 2x (gesplitst - 3D).png" 
                    alt="Omwentelingslichaam L" 
                    width="500" 
                    height="400" 
                    loading="lazy">
        </a>
        <br>
        *<span>Figuur 7. Omwentelingslichamen $L_1$ en $L_2$ die ontstaan als we oppervlaktes $I$ en $II$ allebei wentelen om de $x$-as. (Klik voor <a href="/assets/interactive_images/f(x) = 6x - x^3; g(x) = 2x (gesplitst - 3D).html" target="_blank">interactieve afbeelding</a>)</span>* <br><br>
    </center>

    Laten we als eerst weer de [algemene integraal](#algemene-integraal-wentelen-x-as-tussen-grafieken) opschrijven om een oppervlakte tussen grafieken te wentelen om de $x$-as:

    $$\large{I(L) = \pi \int_{a}^{b} \left( f(x) \right)^2 - \left( g(x) \right)^2 \, dx}$$

    We hebben in vraag a) al bepaald wat we krijgen als we $f(x)$ en $g(x)$ invullen, dus laten we dat er weer bij pakken:

    $$\large{I(L) = \pi \int_{a}^{b} x^6 - 12x^4 + 32x^2 \, dx}$$

    Het enige wat we nu nog moeten bepalen zijn de grenzen. In a) zagen we dat de grenzen voor het hele ding $a=0$ en $b=2$ zijn. En omdat de lijn $x=p$ tussen de twee lichamen in ligt, kunnen we ook de grenzen van $L_1$ en $L_2$ bepalen.

    Want $L_1$ begint ook bij $x=0$, maar eindigt bij $x=p$. Oftewel:

    $$\large{I(L_1) = \pi \int_{0}^{p} x^6 - 12x^4 + 32x^2 \, dx}$$

    En $L_2$ begint juist bij $x=p$ en eindigt bij $x=2$, dus voor $L_2$ geldt:

    $$\large{I(L_2) = \pi \int_{p}^{2} x^6 - 12x^4 + 32x^2 \, dx}$$

    En nu kunnen we de primitieve bepalen. Het is dezelfde formule als bij a), dus die kunnen we er ook gewoon weer bij pakken:

    $$\large{I(L) = \pi \left[ \, \frac{1}{7} x^7 - 2 \frac{2}{5} x^5 + 10 \frac{2}{3} x^3 \, \right]_{0}^{2}}$$

    En dus voor $L_1$ en $L_2$ krijgen we:

    $$\large{I(L_1) = \pi \left[ \, \frac{1}{7} x^7 - 2 \frac{2}{5} x^5 + 10 \frac{2}{3} x^3 \, \right]_{0}^{p}}$$

    $$\large{I(L_2) = \pi \left[ \, \frac{1}{7} x^7 - 2 \frac{2}{5} x^5 + 10 \frac{2}{3} x^3 \, \right]_{p}^{2}}$$

    Laten we eerst de grenzen invullen voor $L_1$:

    $$\large{I(L_1) = \pi \left( \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right) - \left(\frac{1}{7} \cdot 0^7 - 2 \frac{2}{5} \cdot 0^5 + 10 \frac{2}{3} \cdot 0^3 \right) \right)}$$

    Alles bij de rechter haakjes is $0$, dus we krijgen voor de inhoud van $L_1$ de formule:

    $$\large{I(L_1) = \pi \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right)}$$

    Nu kunnen we de grenzen invullen voor $L_2$:

    $$\large{I(L_2) = \pi \left( \left(\frac{1}{7} \cdot 2^7 - 2 \frac{2}{5} \cdot 2^5 + 10 \frac{2}{3} \cdot 2^3 \right) - \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right) \right)}$$

    En als we de linker haakjes versimpelen:

    $$\large{I(L_2) = \pi \left( \left(\frac{1}{7} \cdot 128 - 2 \frac{2}{5} \cdot 32 + 10 \frac{2}{3} \cdot 8 \right) - \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right) \right)}$$

    $$\large{I(L_2) = \pi \left( \left(18 \frac{2}{7} - 76 \frac{4}{5} + 85 \frac{1}{3} \right) - \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right) \right)}$$

    En als we de linker haakjes nu uitrekenen, dan vinden we:

    $$\large{I(L_2) = \pi \left( 26.82 - \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right) \right)}$$

    Nu kunnen we nog alles in de rechter haakjes keer $-1$ doen om de haakjes weg te werken:

    $$\large{I(L_2) = \pi \left( 26.82 - \frac{1}{7} p^7 + 2 \frac{2}{5} p^5 - 10 \frac{2}{3} p^3 \right)}$$

    En als we nog de volgorde omdraaien, vinden we onze formule voor de inhoud van $L_2$:

    $$\large{I(L_2) = \pi \left( -\frac{1}{7} p^7 + 2 \frac{2}{5} p^5 - 10 \frac{2}{3} p^3 + 26.82 \right)}$$

    En nu moeten we bepalen voor welke waarde van $p$ de inhouden van $L_1$ en $L_2$ hetzelfde zijn. Oftewel we moeten de volgende vergelijking oplossen:

    $$\large{I(L_1) = I(L_2)}$$

    En als we $I(L_1)$ en $I(L_2)$ invullen:

    $$\large{ \pi \left( \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 \right) = \pi \left( -\frac{1}{7} p^7 + 2 \frac{2}{5} p^5 - 10 \frac{2}{3} p^3 + 26.82 \right)}$$

    Beide kanten hebben de $\pi$, dus die kunnen we gewoon weg delen:

    $$\large{ \frac{1}{7} p^7 - 2 \frac{2}{5} p^5 + 10 \frac{2}{3} p^3 = -\frac{1}{7} p^7 + 2 \frac{2}{5} p^5 - 10 \frac{2}{3} p^3 + 26.82}$$

    Deze vergelijking is best lastig om met de hand op te lossen, maar gelukkig stond er in de vraag geen *exact* of *algebraïsch*. We mogen dus onze grafische rekenmachine gebruiken. 
    
    We vullen in:

    $$\large{y_1 = \frac{1}{7} x^7 - 2 \frac{2}{5} x^5 + 10 \frac{2}{3} x^3}$$

    $$\large{y_2 = -\frac{1}{7} x^7 + 2 \frac{2}{5} x^5 - 10 \frac{2}{3} x^3 + 26.82}$$

    En de optie *intersect* geeft:

    $$\large{x \approx 1.22}$$

    Oftewel als eindantwoord krijgen we dus:

    !!! quote ""
        $$\large{p \approx 1.22}$$


<hr style="height: 1.5px; background-color: #575757; border: none;">