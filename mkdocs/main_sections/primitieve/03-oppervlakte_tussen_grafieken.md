## **Oppervlakte tussen twee grafieken**

We hebben net gezien hoe we de oppervlakte onder een grafiek kunnen berekenen door te integreren. Maar kunnen we ook de oppervlakte berekenen van een vlakdeel dat tussen twee grafieken in ligt? 

Laten we kijken naar de volgende functies:

$$\large{\left\{ \begin{array}{ l l } f(x) =  6 - x^2  \\ g(x) = x + 4 \end{array} \right.}$$

Stel dat we de oppervlakte tussen deze twee functies willen bepalen. Hoe pakken we dat aan?

In Figuur 1 hebben we de twee functies geplot met het vlakdeel $V$ dat tussen de twee functies in ligt:

<figure>
    <img src="/assets/images/primitieven/f(x) = 6 - x^2; g(x) = x + 4.svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 1. Grafiek geplot met de functies $f(x) = 6 - x^2$ en $g(x) = x + 4$. Vlakdeel $V$ ligt tussen de twee functies in.</i></span></center> <br><br>


De oppervlakte van $V$ kunnen we bepalen door de oppervlakte onder $f(x)$ en de oppervlakte onder $g(x)$ te gebruiken. Laten we naar deze twee oppervlaktes kijken:

<figure>
    <img src="/assets/images/primitieven/f(x) = 6 - x^2; g(x) = x + 4 (Opp I).svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
    <img src="/assets/images/primitieven/f(x) = 6 - x^2; g(x) = x + 4 (Opp II).svg" 
         loading="lazy" 
         width="500" 
         alt="Functie met oppervlakte V onder de grafiek">
</figure>
<center><span><i>Figuur 2. Grafiek geplot met de functies $f(x) = 6 - x^2$ en $g(x) = x + 4$. Vlakdeel $I$ is de oppervlakte onder $f(x)$, vlakdeel $II$ is de oppervlakte onder $g(x)$.</i></span></center> <br><br>

In Figuur 2 kunnen we zien dat vlakdeel $I$ heel erg lijkt op vlakdeel $II$. Het enige verschil is dat vlakdeel $I$ het stuk tussen $f(x)$ en $g(x)$ extra heeft. 

Het gedeelte dat vlakdeel $I$ dus groter maakt dan vlakdeel $II$, is de oppervlakte tussen $f(x)$ en $g(x)$. En dat is precies het vlakdeel $V$ dat we willen berekenen.

Dus als we $V$ willen bepalen, moeten we kijken naar het verschil tussen $I$ en $II$. We moeten dus de oppervlaktes min elkaar doen:

$$V = I - II$$

En deze oppervlaktes kunnen we gewoon bepalen door te integreren. We zien in Figuur 2 dat beide oppervlaktes dezelfde grenzen hebben, namelijk de snijpunten tussen de twee functies. We kunnen aflezen dat dit de punten $x=-2$ en $x=1$ zijn. De integralen worden dan dus:

$$I = \int_{-2}^1 f(x) \, dx$$

$$II = \int_{-2}^1 g(x) \, dx$$

Nu kunnen we een vergelijking voor $V$ opstellen door $I$ en $II$ in te vullen:

$$V = \int_{-2}^1 f(x) \, dx - \int_{-2}^1 g(x) \, dx$$

En omdat deze twee integralen dezelfde grenzen hebben, kunnen we het [schrijven als $1$ integraal](#integralen-samenvoegen):

$$\boxed{V = \int_{-2}^1 \left( f(x) - g(x) \right) \, dx}$$

Dit is dus de integraal om een oppervlakte tussen twee functies te bepalen. 

Laten we nu $f(x)$ en $g(x)$ invullen:

$$V = \int_{-2}^1 \left( 6 - x^2 - \left( x+4 \right) \right) \, dx$$

En als we dit versimpelen:

$$V = \int_{-2}^1 \left( 6 - x^2 - x - 4 \right) \, dx$$

$$V = \int_{-2}^1 \left(- x^2 - x + 2 \right) \, dx$$

Nu kunnen we deze functie gaan integreren:

- De eerste twee termen zijn van de vorm $f(x) = ax^n$ (want we kunnen de $x$ term schrijven als $x^1$). Om deze vorm te primitiveren, moeten we de macht $+1$ doen. Daarna zetten we een factor van $1$ gedeeld door deze nieuwe macht vóór de term.

- De laatste term is een constante (een los getal zonder $x$). Om een constante te primitiveren, moeten we er gewoon een $x$ aan vast plakken.

We krijgen dus:

$$V = \left[\, - \dfrac{1}{3}x^3 - \dfrac{1}{2} x^2 + 2x \, \right]_{-2}^1$$

Nu vullen we de grenzen in en doen het min elkaar:

$$V = \left( - \dfrac{1}{3} \cdot 1^3 - \dfrac{1}{2} \cdot 1^2 + 2 \cdot 1 \right) - \left(- \dfrac{1}{3} \cdot (-2)^3 - \dfrac{1}{2} \cdot (-2)^2 + 2 \cdot -2 \right)$$

En als we dit uitwerken, dan krijgen we:

$$V = \left(- \dfrac{1}{3} \cdot 1 - \dfrac{1}{2} \cdot 1 + 2 \right) - \left(- \dfrac{1}{3} \cdot -8 - \dfrac{1}{2} \cdot 4 - 4 \right)$$

$$V = \left( - \dfrac{1}{3} - \dfrac{1}{2} + 2\right) - \left(2 \dfrac{2}{3} - 2 - 4 \right)$$

$$V = \left(1 \dfrac{1}{6} \right) - \left(- 3 \dfrac{1}{3} \right)$$

$$V = 1 \dfrac{1}{6} + 3 \dfrac{1}{3}$$

!!! quote ""
    $$\large{V = 4 \dfrac{1}{2}}$$


??? abstract "Oppervlaktes $I$ en $II$ los berekenen en dan min elkaar"
    We kunnen om het voorbeeld hierboven te controleren, de oppervlaktes $I$ en $II$ apart berekenen en daarna pas min elkaar doen. We verwachten dan dat we weer uitkomen op de $V = 4 \frac{1}{2}$ die we net hebben berekend.

    We beginnen met het bepalen van de oppervlakte van $I$. We hadden deze integraal gevonden:

    $$\large{I = \int_{-2}^1 f(x) \, dx}$$

    Nu vullen we $f(x)$ in:

    $$\large{I = \int_{-2}^1 6 - x^2 \, dx}$$

    Nu kunnen we deze functie integreren:

    - De eerste term is een constante, dus om de primitieve te bepalen moeten we gewoon een $x$ toevoegen.

    - De tweede term is van de vorm $f(x) = ax^n$. Om de primitieve van deze vorm te bepalen, moeten we eerst de macht $+1$ doen, dus van een macht $2$ naar $3$. Daarna zetten we $1$ gedeeld door deze nieuwe macht ervoor, dus in dit geval zetten we er een factor $\frac{1}{3}$ voor.

    Als we dit toepassen, dan krijgen we:

    $$\large{I = \left[ \, 6x - \dfrac{1}{3} x^3 \, \right]_{-2}^1}$$

    Nu vullen we de grenzen in en doen ze min elkaar:

    $$\large{I = \left( 6 \cdot 1 - \dfrac{1}{3} \cdot 1^3 \right) - \left( 6 \cdot -2 - \dfrac{1}{3} \cdot (-2)^3 \right)}$$

    En als we dit uitwerken, vinden we:

    $$\large{I = \left( 6 - \dfrac{1}{3} \cdot 1 \right) - \left( -12 - \dfrac{1}{3} \cdot -8 \right)}$$

    $$\large{I = \left( 6 - \dfrac{1}{3} \right) - \left( -12 + 2 \dfrac{2}{3} \right)}$$
    
    $$\large{I = \left( 5 \dfrac{2}{3} \right) - \left( -9 \dfrac{1}{3} \right)}$$

    $$\large{I = 5 \dfrac{2}{3} + 9 \dfrac{1}{3}}$$

    $$\large{\boxed{I = 15}}$$

    <br>

    En nu kunnen we hetzelfde doen voor oppervlakte $II$. We stellen eerst weer de integraal op:

    $$\large{II = \int_{-2}^1 g(x) \, dx}$$

    $$\large{II = \int_{-2}^1 x + 4 \, dx}$$

    We hebben weer een term van de vorm $f(x) = ax^n$ een een constante. De primitieve wordt dus:

    $$\large{II = \left[ \,  \dfrac{1}{2} x^2 + 4x \, \right]_{-2}^1}$$

    Nu vullen we weer de grenzen in:

    $$\large{II = \left( \dfrac{1}{2} \cdot 1^2 + 4 \cdot 1 \right) - \left( \dfrac{1}{2} \cdot (-2)^2 + 4 \cdot -2 \right)}$$

    En als we dit uitwerken, vinden we:

    $$\large{II = \left( \dfrac{1}{2} + 4 \right) - \left( \dfrac{1}{2} \cdot 4 - 8 \right)}$$

    $$\large{II = \left( 4 \dfrac{1}{2} \right) - \left( 2 - 8 \right)}$$

    $$\large{II = 4 \dfrac{1}{2} - \left( -6 \right)}$$

    $$\large{\boxed{II = 10 \dfrac{1}{2}}}$$

    En nu kunnen we uiteindelijk $V$ bepalen door deze twee oppervlaktes min elkaar te doen:

    $$\large{V = I - II}$$

    $$\large{V = 15 - 10 \dfrac{1}{2}}$$
    
    En als we dit uitwerken, vinden we inderdaad wat we eerst ook gevonden hadden:

    !!! quote ""
        $$\large{V = 4 \dfrac{1}{2}}$$

<br>

???+ Belangrijk
    ### **Integralen samenvoegen**

    We kunnen de som van twee integralen met dezelfde grenzen samenvoegen tot $1$ integraal:
    
    $$\large{\int_{a}^{b} f(x) \, dx \ + \int_{a}^{b} g(x) \, dx \ \iff \ \int_{a}^{b} \left( \, f(x) + g(x) \, \right) \, dx}$$

    <br>

    En we kunnen hetzelfde doen voor twee integralen die min elkaar zijn:

    $$\large{\int_{a}^{b} f(x) \, dx \ - \int_{a}^{b} g(x) \, dx \ \iff \ \int_{a}^{b} \left( \, f(x) - g(x) \, \right) \, dx}$$


??? abstract "Bewijs: Integralen samenvoegen" 
    
    **<span style="font-size: 18px;">Twee integralen plus elkaar</span>**

    Om te bewijzen dat we twee integralen kunnen samenvoegen, moeten we eerst de integralen uitwerken. We beginnen met twee integralen plus elkaar:

    $$\large{I = \int_{a}^{b} f(x) \, dx \, + \int_{a}^{b} g(x) \, dx}$$

    $$\large{I = \left[ \, F(x) \, \vphantom{\frac{1}{2}} \right]_{a}^{b} + \left[ \, G(x) \vphantom{\frac{1}{2}} \, \right]_{a}^{b}}$$

    En nu vullen we de grenzen in:

    $$\large{I = \left( \, F(b) - F(a) \, \right) + \left( \, G(b) - G(a) \, \right)}$$

    $$\large{I = F(b) - F(a) + G(b) - G(a)}$$

    We kunnen nu de volgorde veranderen van de functies:

    $$\large{I = F(b) + G(b) - F(a) - G(a)}$$

    Als we het opschrijven met haakjes, krijgen we:

    $$\large{I = \left( \, F(b) + G(b) \, \right) - \left( \,  F(a) + G(a) \, \right)}$$

    En deze vorm kunnen we nu terug schrijven als $1$ integraal:

    $$\large{I = \left[ \, F(x) + G(x) \, \vphantom{\frac{1}{2}} \right]_{a}^{b}}$$

    !!! quote ""
        $$\large{I = \int_{a}^{b} \left( \, f(x) + g(x) \, \right) \, dx }$$
    
    <br>

    **<span style="font-size: 18px;">Twee integralen min elkaar</span>**

    We kunnen ook precies hetzelfde bewijzen voor twee integralen min elkaar.

    $$\large{I = \int_{a}^{b} f(x) \, dx \, - \int_{a}^{b} g(x) \, dx}$$

    $$\large{I = \left[ \, F(x) \, \vphantom{\frac{1}{2}} \right]_{a}^{b} - \left[ \, G(x) \, \vphantom{\frac{1}{2}} \right]_{a}^{b}}$$

    Als we de grenzen invullen:

    $$\large{I = \left( \, F(b) - F(a) \, \right) - \left( \, G(b) - G(a) \, \right)}$$

    $$\large{I = F(b) - F(a) - G(b) + G(a)}$$

    Nu kunnen we weer de volgorde veranderen van de functies en er haakjes omheen doen:

    $$\large{I = F(b) - G(b) - F(a) + G(a)}$$

    $$\large{I = \left( \, F(b) - G(b) \, \right) - \left( \,  F(a) - G(a) \, \right)}$$

    En deze vorm kunnen we nu terug schrijven als $1$ integraal:

    $$\large{I = \left[ \, F(x) - G(x) \, \vphantom{\frac{1}{2}} \right]_{a}^{b}}$$

    !!! quote ""
        $$\large{I = \int_{a}^{b} \left( \, f(x) - g(x) \, \right) \, dx }$$

<br>

En hiermee kunnen we ook gelijk de algemene integraal opschrijven om de oppervlakte tussen twee functies te bepalen.

???+ Belangrijk
    ### **Algemene Integraal**

    We kunnen de oppervlakte tussen twee functies bepalen door de oppervlakte onder de bovenste functie min de oppervlakte onder de onderste functie te doen:

    $$\large{V = \int_a^b f(x) \, dx - \int_a^b g(x) \, dx}$$

    Dit kunnen we [samenvoegen](#integralen-samenvoegen) en schrijven als $1$ integraal:

    $$\large{\boxed{V = \int_a^b \left( \, f(x) - g(x) \, \right) \, dx}}$$

    Hierbij is $f(x)$ de bovenste functie en $g(x)$ de onderste functie.
    
    (Buiten het gebied van de oppervlakte kan $g(x)$ boven $f(x)$ liggen, maar dat maakt voor de integraal niet uit.)


??? note "Terugblik: Oppervlaktes onder de $x$-as"
    We hebben [eerder](#oppervlaktes-onder-de-x-as) gezien dat we bij een oppervlakte onder de $x$-as een '$-$' moeten toevoegen aan de integraal. 
    
    Dit is eigenlijk een specifieke vorm van een oppervlakte tussen twee grafieken. Het is namelijk een oppervlakte tussen $f(x)$ en de lijn $y=0$. 
    
    En omdat de functie onder de $x$-as ligt, is de lijn $y=0$ de bovenste functie en $f(x)$ de onderste. En we doen altijd de bovenste functie min de onderste functie, dus we krijgen:

    $$\large{V = \int_a^b 0 - f(x) \, dx}$$

    En hier kunnen we de $0$ gewoon weglaten:

    $$\large{V = \int_a^b - f(x) \, dx}$$

    En als we de '$-$' uit de integraal halen, dan krijgen we weer wat we eerder ook hadden:

    $$\large{\boxed{V = - \int_a^b f(x) \, dx}}$$


??? note "Oppervlaktes *tussen twee grafieken* onder de $x$-as"
    Als we een oppervlakte hebben **tussen twee grafieken** dat (deels) onder de $x$-as ligt, dan verandert dat niks aan de integraal. Kijk maar naar het volgende vlakdeel $V$ dat deels onder de $x$-as ligt:

    <figure>
        <img src="/assets/images/primitieven/Oppervlakte tussen twee functies onder de x-as.svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 3. Twee functies geplot met vlakdeel $V$ tussen de twee functies. Vlakdeel $V$ ligt deels onder de $x$-as.</i></span></center> <br><br>


    We kunnen deze oppervlakte omhoog verschuiven door beide functies omhoog te verschuiven met een bepaalde constante $c$:

    <figure>
        <img src="/assets/images/primitieven/Oppervlakte tussen twee functies onder de x-as (verschoven).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 4. De twee functies omhoog verschoven met een bepaalde constante $c$. Vlakdeel $V$ tussen de twee functies ligt nu volledig boven de $x$-as.</i></span></center> <br><br>


    We kunnen zien dat de oppervlakte $V$ is verschoven, maar het is nog steeds even groot gebleven. Het maakt dus niet uit waar de oppervlakte zich bevindt ten opzichte van de $x$-as. De integraal voor een oppervlakte $V$ tussen twee functies [blijft](#algemene-integraal):

    $$\large{\boxed{V = \int_a^b \left( \, f(x) - g(x) \, \right) \, dx}}$$

    waarbij $f(x)$ de bovenste functie is en $g(x)$ de onderste functie.
    
    <br>
    
    We kunnen het ook bewijzen met formules in plaats van het met een tekening:

    ??? abstract "Bewijs oppervlakte hetzelfde blijft na een verschuiving"
        In Figuur 3 hebben we de twee functies $f(x)$ en $g(x)$. De algemene vorm voor een oppervlakte tussen twee functies is:
        
        $$\large{V = \int_a^b \left( \, f(x) - g(x) \, \right) \, dx}$$

        In Figuur 4 verschuiven we de twee functies omhoog met een constante $c$. Stel we gaan er nu niet vanuit dat de verschoven functies dezelfde oppervlakte omsluiten. Laten we deze nieuwe oppervlakte $W$ noemen en dan kijken of dit hetzelfde is als de oppervlakte $V$.
        
        Onze nieuwe functies worden dus $f(x) + c \,$ en $\, g(x) + c:$

        $$\large{W = \int_a^b \left( \, (f(x) + c) - (g(x) + c) \, \right) \, dx}$$

        Als we de haakjes uitwerken, dan zien we eigenlijk gelijk al dat we op dezelfde integraal uitkomen als die we bij $V$ hadden:

        $$\large{W = \int_a^b \left( \, f(x) + c - g(x) - c \, \right) \, dx}$$

        !!! quote ""
            $$\large{W = \int_a^b \left( \, f(x) - g(x) \, \right) \, dx = V}$$

        En dus heeft het verschuiven van beide functies geen invloed op de oppervlakte tussen de functies.



### **Voorbeelden**

??? example "Voorbeeld 1: Bereken de oppervlakte tussen de functies $f(x) = x^2 - 4x + 6$ en $g(x) = -x^2 + 4x$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = x^2 - 4x + 6$ en de functie $g(x) = -x^2 + 4x$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$.</span>**

    **<span style="font-size: 17px;">b) De lijn $x=p$ verdeelt $V$ in de oppervlaktes $I$ en $II$. Bepaal de waarde voor $p$ waar $I$ twee keer zo groot is als $II$. Geef je antwoord op $3$ decimalen nauwkeurig.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    **<span style="font-size: 17px;">a)</span>**

    Om de situatie een beetje te kunnen begrijpen, maken we eerst een schets:

    <figure>
        <img src="/assets/images/primitieven/f(x) = x^2 - 4x + 6; g(x) = -x^2 + 4x.svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 1. Grafiek geplot met de functies $f(x) = x^2 - 4x + 6$ en $g(x) = -x^2 + 4x$. Vlakdeel $V$ ligt tussen de twee functies in.</i></span></center> <br><br>

    Om de oppervlakte $V$ te bepalen, hebben we eerst de grenzen nodig. In dit geval zijn dat de [snijpunten tussen de twee functies](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken). Om deze te bepalen moeten we $f(x)$ gelijk stellen aan $g(x)$ en de vergelijking oplossen:

    $$\large{f(x) = g(x)}$$ 

    $$\large{x^2 - 4x + 6 = -x^2 + 4x}$$

    Om dit op te lossen halen we eerst alles naar de linkerkant:

    $$\large{2x^2 - 8x + 6 = 0}$$

    Nu kunnen we alles nog delen door $2$:

    $$\large{x^2 - 4x + 3 = 0}$$

    Nu kunnen we het [ontbinden in factoren](/kwadratische_vergelijkingen/#ontbinden-in-factoren). We zoeken twee factoren die keer elkaar $3$ zijn en plus elkaar $-4$.
    
    De factoren die hieraan voldoen zijn $-3$ en $-1$:

    $$\large{(x - 3)(x - 1) = 0}$$

    Hieruit volgt:

    $$\large{x - 3 = 0 \ \vee \ x - 1 = 0}$$

    $$\large{\boxed{x = 3 \ \vee \ x = 1}}$$

    De grenzen zijn dus $x=1$ en $x=3$. Nu kunnen we de oppervlakte van $V$ gaan bepalen.

    De oppervlakte van $V$ is ingesloten door de functies $f(x)$ en $g(x)$, dus $V$ ligt [tussen de twee grafieken](#oppervlakte-tussen-twee-grafieken). We moeten dus een integraal nemen van de bovenste functie min de onderste functie. 
    
    In Figuur 1 zien we dat $g(x)$ de bovenste functie is en $f(x)$ de onderste functie:

    $$\large{V = \int_1^3 \left( \, g(x) - f(x) \, \right) \, dx}$$

    $$\large{V = \int_1^3 \left( \, \left( -x^2 + 4x \right) - \left( x^2 - 4x + 6 \right) \, \right) \, dx}$$

    $$\large{V = \int_1^3 \left( \, -2x^2 + 8x - 6 \, \right) \, dx}$$

    Nu moeten we de primitieve nemen:

    - De eerste twee termen zijn van de vorm $f(x) = ax^n$ (want we kunnen $8x$ schrijven als $8x^1$). Om de primitieve van deze vorm te nemen, moeten we eerst de macht $+1$ doen. Daarna zetten we een factor van $1$ gedeeld door deze nieuwe macht ervoor.

    - De laatste term is een constante (een los getal zonder $x$), dus dan plakken we bij de primitieve er gewoon een $x$ aan vast.

    We krijgen dus:

    $$\large{V = \left[ \, \dfrac{1}{3} \cdot -2x^3 + \dfrac{1}{2} \cdot 8x^2 - 6x \, \right]_1^3}$$

    En als we dit nog versimpelen:

    $$\large{V = \left[ \, -\dfrac{2}{3} x^3 + 4x^2 - 6x \,\right]_1^3}$$

    Nu kunnen we de grenzen invullen en die min elkaar doen:

    $$\large{V = \left( -\dfrac{2}{3} \cdot 3^3 + 4 \cdot 3^2 - 6 \cdot 3 \right) - \left( -\dfrac{2}{3} \cdot 1^3 + 4 \cdot 1^2 - 6 \cdot 1 \right)}$$

    En als we dit uitwerken, krijgen we:

    $$\large{V = \left( -\dfrac{2}{3} \cdot 27 + 4 \cdot 9 - 18 \right) - \left( -\dfrac{2}{3} + 4  - 6 \right)}$$

    $$\large{V = \left( -18 + 36 - 18 \right) - \left( -2\dfrac{2}{3} \right)}$$

    $$\large{V = \left( \, 0 \, \right) + 2\dfrac{2}{3} }$$

    !!! quote ""
        $$\large{V = 2\dfrac{2}{3}}$$


    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We weten dat de lijn $x=p$ het vlakdeel $V$ zo verdeelt dat vlakdeel $I$ twee keer zo groot is als vlakdeel $II$. Laten we weer een schets maken zodat we de situatie beter kunnen begrijpen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = x^2 - 4x + 6; g(x) = -x^2 + 4x (gesplitst).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 2. Grafiek geplot met de functies $f(x) = x^2 - 4x + 6$ en $g(x) = -x^2 + 4x$. Vlakdeel $V$ wordt verdeeld in de vlakdelen $I$ en $II$ zodat $I$ twee keer zo groot is als $II$.</i></span></center> <br><br>

    Om dit op te lossen, moeten we oppervlakte $I$ en $II$ apart berekenen. We beginnen met oppervlakte $I$.

    Het is eigenlijk precies dezelfde integraal als bij a), alleen dan is de rechter grens nu $x=p$ in plaats van het rechter snijpunt:

    $$\large{I = \int_1^p \left( \, g(x) - f(x) \, \right) \, dx}$$

    $$\large{I = \int_1^p \left( \, -2x^2 + 8x - 6 \, \right) \, dx}$$

    We hebben de primitieve ook al bij a) bepaald:

    $$\large{I = \left[ \, -\dfrac{2}{3} x^3 + 4x^2 - 6x \, \right]_1^p}$$

    En nu vullen we deze nieuwe grenzen in:

    $$\large{I = \left( -\dfrac{2}{3} p^3 + 4p^2 - 6p \right) - \left( -\dfrac{2}{3} \cdot 1^3 + 4 \cdot 1^2 - 6 \cdot 1 \right)}$$

    $$\large{I = -\dfrac{2}{3} p^3 + 4p^2 - 6p - \left( -\dfrac{2}{3} + 4 - 6 \right)}$$

    $$\large{I = -\dfrac{2}{3} p^3 + 4p^2 - 6p - \left( -2\dfrac{2}{3} \right)}$$

    $$\large{\boxed{I = -\dfrac{2}{3} p^3 + 4p^2 - 6p  + 2\dfrac{2}{3}}}$$

    En nu doen we hetzelfde maar dan voor $II$. Het vlakdeel $II$ begint juist bij $x=p$ en eindigt bij $x=3$. Behalve de grenzen blijft de rest weer precies hetzelfde, dus we kunnen meteen al de primitieve opschrijven:

    $$\large{II = \left[ \, -\dfrac{2}{3} x^3 + 4x^2 - 6x \, \right]_p^3}$$

    En nu vullen we deze grenzen in:

    $$\large{II = \left( -\dfrac{2}{3} \cdot 3^3 + 4 \cdot 3^2 - 6 \cdot 3 \right) - \left( -\dfrac{2}{3} p^3 + 4p^2 - 6p \right)}$$

    $$\large{II = \left( -\dfrac{2}{3} \cdot 27 + 4 \cdot 9 - 18 \right) + \dfrac{2}{3} p^3 - 4p^2 + 6p}$$

    $$\large{II = \left( -18 + 36 - 18 \right) + \dfrac{2}{3} p^3 - 4p^2 + 6p}$$

    $$\large{II = \left( \, 0 \, \right) + \dfrac{2}{3} p^3 - 4p^2 + 6p}$$

    $$\large{\boxed{II = \dfrac{2}{3} p^3 - 4p^2 + 6p}}$$

    We weten dat $I$ twee keer zo groot is als $II$, dus we kunnen de volgende vergelijking opstellen:

    $$\large{I = 2 \cdot II}$$

    En nu vullen we de vergelijkingen voor $I$ en $II$ die we net hebben gevonden:

    $$\large{-\dfrac{2}{3} p^3 + 4p^2 - 6p  + 2\dfrac{2}{3} = 2 \cdot \left( \dfrac{2}{3} p^3 - 4p^2 + 6p \right)}$$

    $$\large{-\dfrac{2}{3} p^3 + 4p^2 - 6p  + 2\dfrac{2}{3} = \dfrac{4}{3} p^3 - 8p^2 + 12p}$$

    En nu kunnen we alle termen naar de linkerkant halen:

    $$\large{-2p^3 + 12p^2 - 18p  + 2\dfrac{2}{3} = 0}$$

    We hebben hier een term met een derdemacht, dus dit wordt een lastige vergelijking om met de hand op te lossen. Maar er stond gelukkig geen algebraïsch of exact in de vraag, dus we mogen onze grafische rekenmachine gebruiken.

    We voeren in:

    $$\large{\left\{ \begin{array}{ l l } y_1 = -2x^3 + 12x^2 - 18x  + 2\dfrac{2}{3}  \\ y_2 = 0 \end{array} \right.}$$

    De optie intersect geeft:

    $$\large{\left\{ \begin{array}{ l l l } x_1 = 0.16601...  \\ x_2 = 2.22607... \\ x_3 = 3.60791... \end{array} \right.}$$

    We hebben hier $3$ oplossingen gevonden, dus hoe moeten we nu weten welke $p$ is? 

    De grenzen van vlakdeel $V$ zijn $x=1$ en $x=3$, en de lijn $x=p$ ligt binnen dit vlakdeel. Oftewel, $p$ moet dus ook tussen $1$ en $3$ liggen. De enige mogelijkheid is dan dus $x_2$. Als we dit op $3$ decimalen nauwkeurig schrijven, dan krijgen we als eindantwoord:

    !!! quote ""
        $$\large{p \approx 2.226}$$ 


??? example "Voorbeeld 2: Bereken de oppervlakte tussen de functies $f(x) = \sqrt{x}$ en $g(x) = x^2$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \sqrt{x}$ en de functie $g(x) = x^2$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken exact de oppervlakte van vlakdeel $V$.</span>**

    **<span style="font-size: 17px;">b) De lijn $k$ gaat door de oorsprong en verdeelt $V$ in twee even grote oppervlaktes. Vlakdeel $W$ is de oppervlakte onder deze lijn met de twee snijpunten als grenzen. Bepaal exact hoeveel keer groter de oppervlakte van $W$ is ten opzichte van de oppervlakte van $V$.</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    **<span style="font-size: 17px;">a)</span>**

    Laten we een schets maken zodat we de situatie een beetje kunnen begrijpen:

    <figure>
        <img src="/assets/images/primitieven/f(x) = sqrt(x); g(x) = x^2.svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 3. Grafiek geplot met de functies $f(x) = \sqrt{x}$ en $g(x) = x^2$. Vlakdeel $V$ ligt tussen de twee functies in.</i></span></center> <br><br>


    Om de oppervlakte $V$ te kunnen bepalen, hebben we eerst de grenzen nodig. Dit zijn de [snijpunten tussen de twee functies](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken), dus laten we die bepalen. We stellen de twee functies gelijk aan elkaar:

    $$\large{f(x) = g(x)}$$

    $$\large{\sqrt{x} = x^2}$$

    Om de wortel weg te werken, kunnen we beide kanten kwadrateren:

    $$\large{x = x^4}$$

    Nu kunnen we de $x^4$ ook naar de linkerkant halen:

    $$\large{x - x^4 = 0}$$

    En als we alles nog keer $-1$ doen:

    $$\large{x^4 - x = 0}$$

    Beide termen hebben een $x$, dus dit kunnen we op dezelfde manier [oplossen](/kwadratische_vergelijkingen/#oplossen-vorm-x2-bx-0) als een vergelijking van de vorm $x^2 + bx = 0:$

    $$\large{x \left( x^3 - 1 \right) = 0}$$
    
    Hieruit volgt:

    $$\large{x = 0 \ \vee \ x^3 - 1 = 0}$$

    $$\large{x = 0 \ \vee \ x^3 = 1}$$

    En nu nemen we aan beide kanten de derdemachtswortel:
    
    $$\large{x = 0 \ \vee \ x = \sqrt[3]{1}}$$

    $$\large{\boxed{x = 0 \ \vee \ x = 1}}$$

    De snijpunten (en dus de grenzen) liggen bij $x = 0$ en $x = 1$.

    Nu kunnen we de oppervlakte van $V$ gaan bepalen. Dit is een [oppervlakte tussen twee grafieken](#oppervlakte-tussen-twee-grafieken), dus we moeten de bovenste min de onderste functie doen. In Figuur 3 kunnen we zien dat $f(x)$ boven $g(x)$ ligt bij de oppervlakte. Onze integraal wordt dus:

    $$\large{V = \int_0^1 \left( f(x) - g(x) \right) \, dx}$$

    $$\large{V = \int_0^1 \left( \sqrt{x} - x^2 \right) \, dx}$$

    Om de primitieve te bepalen, schrijven we de wortel als een macht $\frac{1}{2}$: 
    
    $$\large{V = \int_0^1 \left( x^{\frac{1}{2}} - x^2 \right) \, dx}$$

    Laten we nu de primitieve gaan bepalen.

    Beide termen zijn van de vorm $f(x) = ax^n$. Bij deze vorm doen we de macht $+1$ en daarna doen we het keer een factor van $1$ gedeeld door deze nieuwe macht. We krijgen dus:

    $$\large{V = \left[ \, \dfrac{1}{1\frac{1}{2}} \cdot x^{1\frac{1}{2}} - \dfrac{1}{3} x^3 \, \right]_0^1}$$

    En als we dit nog iets versimpelen:

    $$\large{V = \left[ \, \dfrac{2}{3} x^{1\frac{1}{2}} - \dfrac{1}{3} x^3 \, \right]_0^1}$$

    En nu vullen we de grenzen in en doen het min elkaar:

    $$\large{V = \left( \, \dfrac{2}{3} \cdot 1^{1\frac{1}{2}} - \dfrac{1}{3} \cdot 1^3 \, \right) - \left( \, \dfrac{2}{3} \cdot 0^{1\frac{1}{2}} - \dfrac{1}{3} \cdot 0^3 \, \right)}$$

    En als we dit uitwerken:

    $$\large{V = \left( \, \dfrac{2}{3} - \dfrac{1}{3} \, \right) - \left( \, 0 \, \right)}$$

    !!! quote ""
        $$\large{V = \dfrac{1}{3}}$$


    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    Om dit op te lossen, moeten we als eerst de lijn $k$ opstellen. De algemene vorm van een lijn is:

    $$\large{k \! : y = ax + b}$$

    We weten dat lijn $k$ door de oorsprong gaat, dus door het punt $(0, 0)$. Laten we dit punt invullen:

    $$\large{0 = a \cdot 0 + b}$$

    Hieruit volgt dus dat:

    $$\large{b = 0}$$

    De lijn $k$ kunnen we dus versimpelen naar:

    $$\large{k \! : y = ax}$$

    We weten dat lijn $k$ de oppervlakte $V$ in twee gelijke delen verdeelt. In Figuur 4 hieronder zien we het onderste deel, die we vlakdeel $I$ noemen:
    
    <figure>
        <img src="/assets/images/primitieven/f(x) = sqrt(x); g(x) = x^2 (met lijn k; opp I).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 4. Grafiek geplot met de functies $f(x) = x^2$, $g(x) = \sqrt{x}$ en de lijn $k$. Vlakdeel $I$ is de oppervlakte tussen lijn $k$ en $g(x)$.</i></span></center> <br><br>
    
    De oppervlakte van vlakdeel $I$ is dus de helft van $V$, dus $I = \dfrac{1}{6}$. We kunnen hiermee lijn $k$ bepalen, door de oppervlakte van $I$ ook uit te rekenen met een integraal. 
    
    Lijn $k$ is de bovenste functie en $g(x)$ de onderste, dus we krijgen:

    $$\large{I = \int_0^1 \left( \, ax - x^2 \, \right) \, dx}$$

    Beide termen zijn van de vorm $f(x) = ax^n$ (want $ax$ kunnen we schrijven als $ax^1$). Om dit te primitiveren doen we eerst de macht $+1$. Daarna moeten we een $1$ gedeeld door de nieuwe macht ervoor zetten.

    We krijgen dus:

    $$\large{I = \left[ \, \frac{1}{2} ax^2 - \dfrac{1}{3} x^2 \, \right]_0^1}$$

    En als we de grenzen invullen, vinden we:

    $$\large{I = \left( \frac{1}{2} a \cdot 1^2 - \dfrac{1}{3} \cdot 1^2 \right) - \left( \frac{1}{2} a \cdot 0^2 - \dfrac{1}{3} \cdot 0^2 \right)}$$

    $$\large{I = \frac{1}{2} a - \dfrac{1}{3}}$$

    En dit is dus gelijk aan $\dfrac{1}{6}$:

    $$\large{\frac{1}{2} a - \dfrac{1}{3} = \dfrac{1}{6}}$$

    $$\large{\frac{1}{2} a = \dfrac{1}{2}}$$

    We vinden dus:

    $$\large{a = 1}$$

    En lijn $k$ wordt dus:

    $$\large{\boxed{k \! : y = x}}$$

    We weten dat vlakdeel $W$ de oppervlakte onder lijn $k$ is met de twee snijpunten als grenzen. Laten we nog een schets maken:

    <figure>
        <img src="/assets/images/primitieven/f(x) = sqrt(x); g(x) = x^2 (met lijn k; opp W).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 5. Grafiek geplot met de functies $f(x) = x^2$, $g(x) = \sqrt{x}$ en de lijn $k$. Vlakdeel $W$ is de oppervlakte onder lijn $k$.</i></span></center> <br><br>

    Nu kunnen we oppervlakte $W$ bepalen. We stellen eerst de integraal op:

    $$\large{W = \int_0^1 x \, dx}$$

    Als we dit integreren, dan vinden we:

    $$\large{W = \left[ \, \dfrac{1}{2} x^2 \, \right]_0^1}$$

    En nu vullen we de grenzen in:

    $$\large{W = \dfrac{1}{2} \cdot 1^2 - \dfrac{1}{2} \cdot 0^2}$$

    $$\large{\boxed{W = \dfrac{1}{2}}}$$

    We moesten bepalen hoeveel keer groter deze oppervlakte was ten opzichte van $V$. Bij a) hadden we berekend dat $V = \dfrac{1}{3}$, dus de verhouding tussen de twee oppervlaktes wordt:

    $$\large{\dfrac{W}{V} =  \dfrac{\frac{1}{2}}{\frac{1}{3}}}$$

    $$\large{\dfrac{W}{V} =  1 \dfrac{1}{2}}$$

    En hieruit volgt dus dat:

    !!! quote ""
        $$\large{W = 1\dfrac{1}{2} V}$$


??? example "Voorbeeld 3: Bereken de oppervlakte tussen de functies $f(x) =  e^{x - 4} - 2$ en $g(x) = \ln(x)$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) =  e^{x - 4} - 2$ en de functie $g(x) = \ln(x)$.</p>*

    <br>

    **<span style="font-size: 17px;">a) Bereken de oppervlakte van vlakdeel $V$ in $3$ decimalen nauwkeurig.</span>**

    **<span style="font-size: 17px;">b) De lijn $k$ gaat door de twee snijpunten van de functies. Bepaal de oppervlakte van het vlakdeel $W$ dat tussen $g(x)$ en lijn $k$ ligt. Rond af op $2$ decimalen</span>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    **<span style="font-size: 17px;">a)</span>**

    Om de situatie een beetje te kunnen begrijpen, maken we eerst een schets:

    <figure>
        <img src="/assets/images/primitieven/f(x) = e^(x - 4) - 2; g(x) = ln(x).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 6. Grafiek geplot met de functies $f(x) = e^{x - 4} - 2$ en $g(x) = \ln(x)$. Vlakdeel $V$ ligt tussen de twee functies in.</i></span></center> <br><br>

    We moeten de oppervlakte van $V$ bepalen, dus laten we eerst de grenzen bepalen. In dit geval liggen de grenzen bij de [snijpunten van de twee functies](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken). Om de snijpunten te bepalen, stellen we de twee functies gelijk aan elkaar:

    $$\large{f(x) = g(x)}$$

    $$\large{e^{x - 4} - 2 = \ln(x)}$$

    Er staat geen algebraïsch of exact in de vraag, dus we mogen onze grafische rekenmachine gebruiken om dit op te lossen. 
    
    We voeren in:

    $$\large{\left\{ \begin{array}{ l l } y_1 = e^{x - 4} - 2 \\ y_2 = \ln(x) \end{array} \right.}$$

    De optie intersect geeft:

    $$\large{\left\{ \begin{array}{ l l } x_1 = 0.13821...  \\ x_2 = 5.29954... \end{array} \right.}$$

    De grenzen van $V$ zijn dus $x \approx 0.13821$ en $x \approx 5.29954$. 
    
    Nu kunnen we de integraal opstellen. $V$ ligt [tussen twee grafieken](#oppervlakte-tussen-twee-grafieken) in, dus we moeten de bovenste functie min de onderste functie doen. In Figuur 6 zien we dat tussen de grenzen $g(x)$ boven $f(x)$ ligt, dus we krijgen:

    $$\large{V = \int_{0.13821}^{5.29954} \left( \, g(x) - f(x) \, \right) \, dx}$$

    Nu vullen we $f(x)$ en $g(x)$ in:

    $$\large{V = \int_{0.13821}^{5.29954} \left( \ln(x) - \left( e^{x-4} - 2 \right) \right) \, dx}$$

    $$\large{V = \int_{0.13821}^{5.29954} \left( \ln(x) - e^{x-4} + 2 \right) \, dx}$$

    Nu kunnen we de primitieve gaan bepalen.

    - De eerste term is $\ln(x)$. In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve hiervan gelijk is aan: $\underline{x\ln(x) - x}$ 

    - De tweede term is een $e$ macht. We weten dat, net zoals bij een afgeleide, de primitieve van een $e$ macht zichzelf is. De primitieve van $-e^{x - 4}$ is dus gewoon weer: $\underline{-e^{x - 4}}$

    - De laatste term is een constante (een los getal zonder $x$). Om de primitieve van een constante te bepalen, moeten we er gewoon een $x$ aan vast plakken. De primitieve van $2$ is dus: $\underline{2x}$ 

    We krijgen dus:

    $$\large{V = \left[ \, x\ln(x) - x - e^{x-4} + 2x \vphantom{\frac{1}{2}} \, \right]_{0.13821}^{5.29954}}$$

    We kunnen nu nog de $-x$ en de $2x$ samenvoegen:

    $$\large{V = \left[ \, x\ln(x) - e^{x-4} + x \, \vphantom{\frac{1}{2}} \right]_{0.13821}^{5.29954}}$$

    Nu kunnen we de grenzen invullen:

    $$\large{V = \left( 5.29954 \cdot \ln(5.29954) - e^{5.29954-4} + 5.29954 \right) - \left( 0.13821 \cdot \ln(0.13821) - e^{0.13821-4} + 0.13821 \right)}$$

    Als we dit invullen op onze rekenmachine, dan vinden we:

    $$\large{V = 10.6258851315957...}$$

    We moesten afronden op $3$ decimalen, dus als eindantwoord krijgen we:

    !!! quote ""
        $$\large{V = 10.626}$$


    <br><br>

    **<span style="font-size: 17px;">b)</span>**

    We weten dat lijn $k$ door de twee snijpunten gaat, dus laten we hier een schets van maken:

    <figure>
        <img src="/assets/images/primitieven/f(x) = e^(x - 4) - 2; g(x) = ln(x) (met lijn k).svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 7. Grafiek geplot met de functies $f(x) = e^{x - 4} - 2$, $g(x) = \ln(x)$ en de lijn $k$. Vlakdeel $W$ ligt tussen $g(x)$ en lijn $k$.</i></span></center> <br><br>

    Om oppervlakte $W$ te bepalen, moeten we eerst lijn $k$ opstellen:
    
    $$\large{k \! : y = ax + b}$$

    We hebben twee punten gegeven gekregen waar de lijn doorheen gaat. We hebben de $x$-coördinaten bij a) al berekend, namelijk $x_1 \approx 0.13821$ en $x_2 \approx 5.29954$. Laten we ook de bijbehorende $y$-coördinaten berekenen. We kunnen het in beide functies invullen, maar we kiezen hier voor $g(x)$:
        
    $$\large{\left\{ \begin{array}{ l l } y_1 = \ln( 0.13821...) \approx -1.97897 \\ y_2 = \ln(5.29954...) \approx 1.66761 \end{array} \right.}$$

    We hebben dus de snijpunten $(0.13821, -1.97897)$ en $(5.29954, 1.66761)$. Hiermee kunnen we de richtingscoëfficient ( $a$ ) van lijn $k$ bepalen:

    $$\large{a = \dfrac{\Delta y}{\Delta x} = \dfrac{1.66761 - - \! 1.97897}{5.29954 - 0.13821}}$$

    En als we dit uitrekenen, dan vinden we:

    $$\large{a \approx 0.70652}$$

    De lijn $k$ wordt dus:

    $$\large{k \! : y = 0.70652x + b}$$

    Om $b$ te bepalen moeten we $1$ van de twee snijpunten invullen. Wij kiezen hier voor het punt $(5.29954, 1.66761)$ (maar het ander snijpunt mag dus ook):

    $$\large{1.66761 = 0.70652 \cdot 5.29954 + b}$$

    $$\large{1.66761 = 3.74423 + b}$$

    Als we beide kanten $-3.74423$ doen, dan vinden we:

    $$\large{b = −2.07662}$$

    De lijn $k$ is dus:

    $$\large{\boxed{k \! : y = 0.70652x − 2.07662}}$$

    Nu kunnen we oppervlakte $W$ bepalen. We weten dat deze oppervlakte tussen lijn $k$ en $g(x)$ ligt en we zien in Figuur 7 dat $g(x)$ boven de lijn $k$ ligt. We krijgen dus $g(x)$ min lijn $k$ in de integraal:

    $$\large{W = \int_{0.13821}^{5.29954} \left( \, \ln(x) - \left( 0.70652x − 2.07662 \right) \, \right) \, dx}$$

    $$\large{W = \int_{0.13821}^{5.29954} \left( \, \ln(x) -  0.70652x + 2.07662 \, \right) \, dx}$$

    Nu kunnen we de primitieve bepalen:

    - We hebben bij a) al gezien dat de primitieve van $\ln(x)$ gelijk is aan: $\underline{x \ln(x) - x}$

    - De tweede term is van de vorm $f(x) = ax^n$. We moeten dus de macht $+1$ doen en dan een factor van $1$ gedeeld door deze macht keer de term doen. We krijgen dus: $\frac{1}{2} \cdot -0.70652 x^2 = \underline{-0.35326 x^2}$
    
    - De laatste term is een constante, dus daar plakken we gewoon een $x$ aan vast. We krijgen dus: $\underline{2.07662 x}$

    De primitieve wordt dus:

    $$\large{W = \left[ \, x \ln(x) - x - 0.35326 x^2 + 2.07662 x \, \vphantom{\frac{1}{2}} \right]_{0.13821}^{5.29954}}$$

    En nu kunnen we nog de $-x$ en de $2.07662 x$ bij elkaar optellen:

    $$\large{W = \left[ \, x \ln(x) - 0.35326 x^2 + 1.07662 x \, \vphantom{\frac{1}{2}} \right]_{0.13821}^{5.29954}}$$

    Nu kunnen we de grenzen invullen:

    $$\large{W = \left( \, 5.29954 \cdot \ln(5.29954) - 0.35326 \cdot 5.29954^2 + 1.07662 \cdot 5.29954 \, \right) - \left( \, 0.13821 \cdot \ln(0.13821) - 0.35326 \cdot 0.13821^2 + 1.07662 \cdot 0.13821 \, \right)}$$

    Als we dit invullen in een rekenmachine, dan vinden we:

    $$\large{W = 4.75332208894266...}$$

    We moesten afronden op $2$ decimalen, dus als eindantwoord krijgen we:

    !!! quote ""
        $$\large{W = 4.75}$$


??? example "Voorbeeld 4: Bereken algebraïsch de oppervlakte tussen de functies $f(x) = \sin(3x) + 2$ en $g(x) = \cos(3x) + 2$"
    *<p style="text-align: center;font-size:20px;">Vlakdeel $V$ wordt ingesloten door de functie $f(x) = \sin(3x) + 2$ en de functie $g(x) = \cos(3x) + 2$ binnen een bepaald domein (zie Figuur 8).</p>*

    <figure>
        <img src="/assets/images/primitieven/f(x) = sin(3x) + 2; g(x) = cos(3x) + 2.svg" 
            loading="lazy" 
            width="500" 
            alt="Functie met oppervlakte V onder de grafiek">
    </figure>
    <center><span><i>Figuur 8. Grafiek geplot met de functies $f(x) = \sin(3x) + 2$ en $g(x) = \cos(3x) + 2$. Vlakdeel $V$ ligt tussen deze twee functies. De grenzen van $V$ zijn het eerste positieve snijpunt en de lijn $x = p$.</i></span></center> <br><br>

    <br>

    **<span style="font-size: 17px;">Bereken algebraïsch de oppervlakte van vlakdeel $V$ als $p = \frac{2}{3} \pi$. Rond af op $3$ decimalen.</span>**


    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen moeten we eerst de grenzen bepalen. Om dit te doen, hebben we de eerste twee positieve snijpunten nodig. De meest rechter grens hebben we namelijk al gegeven gekregen, want dat is de lijn $x=\frac{2}{3} \pi$.

    Om de [snijpunten te bepalen](/kwadratische_vergelijkingen/#snijpunten-met-andere-grafieken) tussen $f(x)$ en $g(x)$ moeten we de twee functies aan elkaar gelijk stellen:

    $$\large{f(x) = g(x)}$$

    $$\large{\sin(3x) + 2 = \cos(3x) + 2}$$

    Om dit op te lossen beginnen we met aan beide kanten $-2$ te doen:

    $$\large{\sin(3x) = \cos(3x)}$$

    Nu hebben we óf aan beide kanten een sinus nodig óf aan beide kanten een cosinus. Wij schrijven de [cosinus om naar een sinus](/goniometrie/#sinus-en-cosinus-omschrijven) (maar andersom mag ook):

    $$\large{\sin(3x) = \sin(3x + \dfrac{1}{2} \pi)}$$

    Nu kunnen we de [algemene oplossing](/goniometrie/#algemene-oplossing) voor een sinus vergelijking gebruiken:

    $$\large{3x = 3x + \dfrac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 3x = \pi - \left( 3x + \dfrac{1}{2} \pi \right) + k \cdot 2 \pi}$$

    $$\large{3x = 3x + \dfrac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 3x = -3x + \dfrac{1}{2} \pi + k \cdot 2 \pi}$$

    Nu halen we alle $x$ termen naar de linkerkant:

    $$\large{0 = \dfrac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 6x = \dfrac{1}{2} \pi + k \cdot 2 \pi}$$

    De $x$'en zijn bij de linker vergelijking weggevallen, dus daar hebben we niks meer aan. We gaan verder met de rechter vergelijking:

    $$\large{6x = \dfrac{1}{2} \pi + k \cdot 2 \pi}$$

    Nu delen we beide kanten door $6$ om te vinden:

    $$\large{x = \dfrac{1}{12} \pi + k \cdot \dfrac{1}{3} \pi}$$

    We moesten de eerste twee positieve snijpunten bepalen, dus onze oplossingen worden:

    $$\large{x = \dfrac{1}{12} \pi \ \vee \ x = \dfrac{5}{12} \pi}$$

    Het linker snijpunt is dus bij $x=\dfrac{1}{12} \pi$ en het middelste snijpunt bij $x = \dfrac{5}{12} \pi$.

    Nu dat we de grenzen van vlakdeel $V$ hebben, kunnen we de oppervlakte gaan bepalen. De oppervlakte zit [tussen twee grafieken in](#oppervlakte-tussen-twee-grafieken), dus we moeten de bovenste min de onderste functie doen.


    ***<p style="text-align: left;font-size:17px;">Maar let op!</p>***
    Bij het eerste gedeelte van de oppervlakte is $f(x)$ boven $g(x)$, maar bij het tweede gedeelte is juist andersom; $g(x)$ is boven $f(x)$. We moeten dan net zoals bij [een deel boven en een deel onder de $x$-as](#deel-boven-en-deel-onder-de-x-as) de oppervlakte in tweeën delen.

    We weten dat het eerste gedeelte over gaat in het tweede gedeelte bij het tweede snijpunt. En dit snijpunt hebben we net hebben bepaald (namelijk $x = \frac{5}{12} \pi$ ). 
    
    De grenzen van het eerste oppervlakte zijn dus $x=\frac{1}{12} \pi$ en $x = \frac{5}{12} \pi$. Van het tweede oppervlakte zijn de grenzen juist $x = \frac{5}{12} \pi$ en $x = \frac{2}{3} \pi$. We kunnen de oppervlakte van $V$ dus als volgt bepalen:

    $$\large{V = \int_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \left( \, f(x) - g(x)  \, \right) \, dx \, + \int_{\frac{5}{12} \pi}^{\frac{2}{3} \pi} \left( \, g(x) - f(x)  \, \right) \, dx}$$

    En nu vullen we $f(x)$ en $g(x)$ in:

    $$\large{V = \int_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \left( \, (\sin(3x) + 2) - (\cos(3x) + 2)  \, \right) \, dx \, + \int_{\frac{5}{12} \pi}^{\frac{2}{3} \pi} \left( \, (\cos(3x) + 2) - (\sin(3x) + 2)  \, \right) \, dx}$$

    En als we dit versimpelen:

    $$\large{V = \int_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \left( \, \sin(3x) - \cos(3x)  \, \right) \, dx \, + \int_{\frac{5}{12} \pi}^{\frac{2}{3} \pi} \left( \, \cos(3x) - \sin(3x) \, \right) \, dx}$$

    We kunnen ook nog een '$-$' buiten de tweede integraal halen:

    $$\large{V = \int_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \left( \, \sin(3x) - \cos(3x)  \, \right) \, dx \, - \int_{\frac{5}{12} \pi}^{\frac{2}{3} \pi} \left( \, -\cos(3x) + \sin(3x) \, \right) \, dx}$$

    $$\large{V = \int_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \left( \, \sin(3x) - \cos(3x)  \, \right) \, dx \, - \int_{\frac{5}{12} \pi}^{\frac{2}{3} \pi} \left( \, \sin(3x) - \cos(3x) \, \right) \, dx}$$

    Nu kunnen we namelijk twee keer hetzelfde integreren en gewoon andere grenzen invullen. Laten we dit integreren:

    - De eerste term is $\sin(3x)$. In de [tabel](#tabel-met-veel-voorkomende-functies) kunnen we zien dat de primitieve van $\sin(x)$ gelijk is aan $-\cos(x)$. Alleen wij hebben nog een $3$ binnen de sinus, dus om rekening te houden met de [kettingregel](/afgeleide/#regels) moeten wij een factor $\frac{1}{3}$ toevoegen. We krijgen dus als primitieve: $\underline{-\dfrac{1}{3} \cos(3x)}$

    - De tweede term is $\cos(3x)$, dus heel vergelijkbaar aan de eerste term. In de [tabel](#tabel-met-veel-voorkomende-functies) zien we dat de primitieve van $\cos(x)$ gelijk is aan $\sin(x)$. Maar we moeten wel weer rekening houden met de [kettingregel](/afgeleide/#regels), dus we krijgen als primitieve: $\underline{\dfrac{1}{3} \sin(3x)}$. 

    We krijgen dus:
    
    $$\large{V = \left[ \, -\dfrac{1}{3} \cos(3x) - \dfrac{1}{3} \sin(3x) \, \right]_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \ - \ \left[ \, -\dfrac{1}{3} \cos(3x) - \dfrac{1}{3} \sin(3x) \, \right]_{\frac{5}{12} \pi}^{\frac{2}{3} \pi}}$$

    We kunnen nu nog de factor $-\dfrac{1}{3}$ buiten de haakjes zetten:

    $$\large{V = -\dfrac{1}{3} \left[ \, \cos(3x) + \sin(3x) \, \vphantom{\frac{1}{2}} \right]_{\frac{1}{12} \pi}^{\frac{5}{12} \pi} \ + \ \dfrac{1}{3} \left[ \, \cos(3x) + \sin(3x) \, \vphantom{\frac{1}{2}} \right]_{\frac{5}{12} \pi}^{\frac{2}{3} \pi}}$$

    En nu kunnen we de grenzen invullen:

    $$\large{V = -\dfrac{1}{3} \left( \cos(3 \cdot \frac{5}{12} \pi) + \sin(3 \cdot \frac{5}{12} \pi) \right) - - \dfrac{1}{3} \left( \cos(3 \cdot \frac{1}{12} \pi) + \sin(3 \cdot \frac{1}{12} \pi) \right) \ + \ \dfrac{1}{3} \left( \cos(3 \cdot \frac{2}{3} \pi) + \sin(3 \cdot \frac{2}{3} \pi) \right) - \dfrac{1}{3} \left( \cos(3 \cdot \frac{5}{12} \pi) + \sin(3 \cdot \frac{5}{12} \pi) \right)}$$

    Deze hele vergelijking kunnen we nu gewoon in een rekenmachine stoppen. We vinden dan:

    $$\large{V = 1.7475468957064...}$$

    We moesten afronden op $3$ decimalen, dus we krijgen als eindantwoord:

    !!! quote ""
        $$\large{V = 1.748}$$

<hr style="height: 1.5px; background-color: #575757; border: none;">