# *Differentiaalrekening*

*VWO Wiskunde B · Hoofdstuk 6 · Getal & Ruimte*

<!-- TODO: korte introductie van het hoofdstuk -->

****

## **6.1 Toppen en buigpunten** {#p6-1}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **6.2 De afgeleide van machtsfuncties** {#p6-2}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **6.3 De kettingregel** {#p6-3}

Tot nu toe kunnen we functies als $f(x) = x^3$ of $f(x) = 5x^2$ afleiden. Maar wat doen we met een functie als:

$$f(x) = (3x + 1)^4$$

Hier zit een functie *in* een andere functie. Binnen de haakjes staat $3x + 1$, en dat wordt daarna tot de macht $4$ gedaan. Je zou de haakjes kunnen uitwerken, maar dat is bij een hoge macht veel werk. Met de **kettingregel** kan het veel sneller.

Zie het als een keten van twee stappen. Eerst doe je $x$ keer $3$ en plus $1$. Dat noemen we de **binnenfunctie**. Daarna doe je het resultaat tot de macht $4$. Dat noemen we de **buitenfunctie**.

???+ Belangrijk
    ### **De kettingregel**

    Als $f(x) = g(h(x))$, dan is

    $$\large{f'(x) = g'(h(x)) \cdot h'(x)}$$

    In woorden: **leid de buitenkant af (en laat de binnenkant staan), en vermenigvuldig dit met de afgeleide van de binnenkant.**

Dat klinkt misschien ingewikkeld. Laten we het stap voor stap doen met $f(x) = (3x + 1)^4$:

- De buitenkant is "iets tot de macht $4$". De afgeleide hiervan is "$4 \cdot$ dat iets tot de macht $3$". De binnenkant blijft staan: $4(3x + 1)^3$.
- De binnenkant is $3x + 1$. De afgeleide hiervan is $3$.

Als we dit met elkaar vermenigvuldigen, krijgen we:

$$f'(x) = 4(3x + 1)^3 \cdot 3 = 12(3x + 1)^3$$

??? note "Waarom moet je keer de afgeleide van de binnenkant doen?"
    Stel $x$ wordt een klein beetje groter. Dan wordt $3x + 1$ drie keer zo veel groter, want de binnenkant heeft helling $3$. En die verandering wordt daarna nog eens versterkt door de buitenkant. De totale verandering is dus de verandering van de buitenkant *keer* de verandering van de binnenkant. Daarom vermenigvuldigen we die twee afgeleiden met elkaar.

### **Stappenplan**

1. Bepaal wat de binnenfunctie en wat de buitenfunctie is.
2. Leid de buitenfunctie af, en laat de binnenfunctie staan.
3. Leid de binnenfunctie af.
4. Vermenigvuldig deze twee met elkaar.
5. Schrijf het netjes op (zet getallen vooraan).

### **Voorbeelden**

??? example "Voorbeeld 1: Leid af $f(x) = (2x - 5)^3$"
    **<p style="text-align: center;font-size:20px;">Bepaal de afgeleide van $f(x) = (2x - 5)^3$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    De binnenfunctie is $2x - 5$ en de buitenfunctie is "iets tot de macht $3$". De afgeleide van de buitenkant is $3 \cdot (2x - 5)^2$. De afgeleide van de binnenkant is $2$. Dus:

    $$f'(x) = 3(2x - 5)^2 \cdot 2$$

    !!! quote ""
        $$\large{f'(x) = 6(2x - 5)^2}$$


??? example "Voorbeeld 2: Leid af $f(x) = \sqrt{x^2 + 1}$"
    **<p style="text-align: center;font-size:20px;">Bepaal de afgeleide van $f(x) = \sqrt{x^2 + 1}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    De binnenfunctie is $x^2 + 1$. De buitenfunctie is de wortel. Een wortel kunnen we schrijven als macht $\frac{1}{2}$, dus:

    $$f(x) = (x^2 + 1)^{\frac{1}{2}}$$

    De afgeleide van de buitenkant is $\frac{1}{2}(x^2 + 1)^{-\frac{1}{2}}$ en de afgeleide van de binnenkant is $2x$. Dus:

    $$f'(x) = \frac{1}{2}(x^2 + 1)^{-\frac{1}{2}} \cdot 2x = x \cdot (x^2 + 1)^{-\frac{1}{2}}$$

    Een macht van $-\frac{1}{2}$ schrijven we weer als wortel in de noemer:

    !!! quote ""
        $$\large{f'(x) = \dfrac{x}{\sqrt{x^2 + 1}}}$$


??? example "Voorbeeld 3: Hellingen en raaklijnen"
    **<p style="text-align: center;font-size:20px;">Bepaal de helling van de grafiek van $f(x) = (3x - 2)^2$ in het punt waar $x = 1$.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We leiden eerst af met de kettingregel. De buitenkant geeft $2(3x - 2)$ en de binnenkant geeft $3$:

    $$f'(x) = 2(3x - 2) \cdot 3 = 6(3x - 2)$$

    Nu vullen we $x = 1$ in:

    $$f'(1) = 6 \cdot (3 \cdot 1 - 2) = 6 \cdot 1 = 6$$

    !!! quote ""
        De helling in het punt waar $x = 1$ is $6$.

Meer over de kettingregel, ook voor functies zoals $\sin$ en $e^x$, vind je op de pagina [De Afgeleide Functie](/afgeleide/#regels).

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **6.4 Raaklijnen, toppen, rakende en loodrecht snijdende grafieken** {#p6-4}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">
