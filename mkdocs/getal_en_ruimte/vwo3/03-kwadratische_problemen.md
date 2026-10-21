# *Kwadratische problemen*

*VWO 3 · Hoofdstuk 3 · Getal & Ruimte*

<!-- TODO: korte introductie van het hoofdstuk -->

****

## **3.1 Kwadratische vergelijkingen** {#p3-1}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **3.2 Kwadratische functies** {#p3-2}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **3.3 De functie $f(x) = a(x-d)(x-e)$** {#p3-3}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **3.4 De functie $f(x) = a(x-p)^2 + q$** {#p3-4}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **3.5 De abc-formule** {#p3-5}

Sommige kwadratische vergelijkingen kun je niet makkelijk oplossen door te ontbinden in factoren. Neem bijvoorbeeld:

$$x^2 + 3x - 5 = 0$$

Wij zoeken twee getallen die keer elkaar $-5$ zijn en bij elkaar opgeteld $3$. Dat lukt hier niet met mooie getallen. Gelukkig is er een formule die **altijd** werkt: de abc-formule.

Een kwadratische vergelijking kunnen we altijd in deze vorm schrijven:

$$ax^2 + bx + c = 0$$

Hierbij zijn $a$, $b$ en $c$ gewoon losse getallen. In ons voorbeeld is $a = 1$, $b = 3$ en $c = -5$. Let op: het minteken hoort bij het getal!

???+ Belangrijk
    ### **De abc-formule**

    De oplossingen van $ax^2 + bx + c = 0$ zijn:

    $$\large{x = \dfrac{-b + \sqrt{D}}{2a} \quad \text{of} \quad x = \dfrac{-b - \sqrt{D}}{2a}}$$

    waarbij $D$ de **discriminant** is:

    $$\large{D = b^2 - 4ac}$$

Je rekent dus eerst $D$ uit, en daarna vul je dit in de formule in. Je rekent de formule twee keer uit: één keer met een plus voor de wortel en één keer met een min. Zo vind je twee oplossingen.

### **Hoeveel oplossingen zijn er?**

De discriminant $D$ vertelt je meteen hoeveel oplossingen er zijn. Dat komt doordat je een wortel van $D$ moet nemen, en dat kan niet altijd:

- Is $D > 0$? Dan is $\sqrt{D}$ een positief getal, dus plus en min geven twee verschillende antwoorden. Er zijn **twee** oplossingen.
- Is $D = 0$? Dan is $\sqrt{D} = 0$, dus plus en min geven hetzelfde antwoord. Er is **één** oplossing.
- Is $D < 0$? Dan kun je geen wortel nemen van een negatief getal. Er zijn **geen** oplossingen.

### **Stappenplan**

1. Zorg dat de vergelijking van de vorm $ax^2 + bx + c = 0$ is. Er moet dus $0$ aan een kant staan.
2. Lees $a$, $b$ en $c$ af.
3. Reken $D = b^2 - 4ac$ uit.
4. Vul alles in de formule in.

### **Voorbeelden**

??? example "Voorbeeld 1: Los op $x^2 + 3x - 5 = 0$"
    **<p style="text-align: center;font-size:20px;">Los op: $x^2 + 3x - 5 = 0$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    De vergelijking heeft al de vorm $ax^2 + bx + c = 0$. We lezen af dat $a = 1$, $b = 3$ en $c = -5$. Nu rekenen we de discriminant uit:

    $$D = 3^2 - 4 \cdot 1 \cdot (-5) = 9 + 20 = 29$$

    $D$ is groter dan $0$, dus er zijn twee oplossingen. We vullen ze in de formule in:

    $$x = \dfrac{-3 + \sqrt{29}}{2} \qquad \text{of} \qquad x = \dfrac{-3 - \sqrt{29}}{2}$$

    Op de rekenmachine vinden we de afgeronde antwoorden:

    !!! quote ""
        $$\large{x \approx 1.19 \quad \text{of} \quad x \approx -4.19}$$


??? example "Voorbeeld 2: Los op $2x^2 - 8x + 8 = 0$"
    **<p style="text-align: center;font-size:20px;">Los op: $2x^2 - 8x + 8 = 0$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Hier is $a = 2$, $b = -8$ en $c = 8$. De discriminant is:

    $$D = (-8)^2 - 4 \cdot 2 \cdot 8 = 64 - 64 = 0$$

    $D = 0$, dus er is maar één oplossing:

    $$x = \dfrac{-(-8)}{2 \cdot 2} = \dfrac{8}{4}$$

    !!! quote ""
        $$\large{x = 2}$$


??? example "Voorbeeld 3: Los op $x^2 + 2x + 5 = 0$"
    **<p style="text-align: center;font-size:20px;">Los op: $x^2 + 2x + 5 = 0$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Hier is $a = 1$, $b = 2$ en $c = 5$. De discriminant is:

    $$D = 2^2 - 4 \cdot 1 \cdot 5 = 4 - 20 = -16$$

    $D$ is kleiner dan $0$. We kunnen geen wortel nemen van $-16$, dus:

    !!! quote ""
        Er zijn geen oplossingen.


??? example "Voorbeeld 4: Los op $x^2 = 4x + 1$"
    **<p style="text-align: center;font-size:20px;">Los op: $x^2 = 4x + 1$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Hier staat nog geen $0$ aan een kant. Dus eerst trekken we $4x$ en $1$ af aan beide kanten:

    $$x^2 - 4x - 1 = 0$$

    Nu is $a = 1$, $b = -4$ en $c = -1$. De discriminant is:

    $$D = (-4)^2 - 4 \cdot 1 \cdot (-1) = 16 + 4 = 20$$

    En dus krijgen we de oplossingen:

    $$x = \dfrac{4 + \sqrt{20}}{2} \qquad \text{of} \qquad x = \dfrac{4 - \sqrt{20}}{2}$$

    !!! quote ""
        $$\large{x \approx 4.24 \quad \text{of} \quad x \approx -0.24}$$

Meer over kwadratische vergelijkingen en andere manieren om ze op te lossen vind je op de pagina [Kwadratische Vergelijkingen](/kwadratische_vergelijkingen/).

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **3.6 Verschillende oplosmethoden** {#p3-6}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">
