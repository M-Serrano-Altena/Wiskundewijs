# *Meten*

*VWO 1 · Hoofdstuk 7 · Getal & Ruimte*

<!-- TODO: korte introductie van het hoofdstuk -->

****

## **7.1 Lengte** {#p7-1}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **7.2 Oppervlakte** {#p7-2}

### **Omtrek en oppervlakte**

- De **omtrek** is de totale lengte van de rand van een figuur. Je loopt als het ware één keer helemaal om het figuur heen. Je telt alle zijden bij elkaar op. De omtrek meet je in cm, m, enzovoort.
- De **oppervlakte** is hoeveel *ruimte* een figuur op het platte vlak inneemt. Je meet dit in vierkante eenheden, zoals cm² (vierkante centimeters) of m² (vierkante meters). Een cm² is een vierkantje van $1$ cm bij $1$ cm.

Neem een rechthoek van $5$ cm lang en $3$ cm breed. Voor de omtrek loop je helemaal rond: $5 + 3 + 5 + 3 = 16$ cm. Voor de oppervlakte vul je de rechthoek met vierkantjes van $1$ cm². Er passen $3$ rijen van $5$ vierkantjes in, dus $3 \cdot 5 = 15$ cm².

### **De formules**

???+ Belangrijk
    ### **Oppervlakte van vlakke figuren**

    | Figuur         | Oppervlakte                                                           |
    | -------------- | --------------------------------------------------------------------- |
    | Rechthoek      | $\text{lengte} \cdot \text{breedte}$                                  |
    | Vierkant       | $\text{zijde} \cdot \text{zijde}$                                     |
    | Driehoek       | $\dfrac{1}{2} \cdot \text{basis} \cdot \text{hoogte}$                 |
    | Parallellogram | $\text{basis} \cdot \text{hoogte}$                                    |
    | Trapezium      | $\dfrac{1}{2} \cdot (\text{a} + \text{b}) \cdot \text{hoogte}$       |

    Bij het trapezium zijn $a$ en $b$ de twee evenwijdige zijden.

Let goed op wat de **hoogte** is. De hoogte is niet de schuine zijde! De hoogte is het stuk dat **loodrecht** op de basis staat, van de basis tot het hoogste punt.

??? note "Waarom is een driehoek de helft?"
    Als je een rechthoek schuin doormidden snijdt, krijg je twee gelijke rechthoekige driehoeken. Elke driehoek is dus de helft van de rechthoek. Daarom: $\frac{1}{2} \cdot \text{basis} \cdot \text{hoogte}$. Bij een niet-rechthoekige driehoek werkt dit net zo, want je kunt hem altijd aanvullen tot een rechthoek.

??? note "Waarom is een parallellogram basis keer hoogte?"
    Knip een driehoekje van de ene kant van een parallellogram en plak het aan de andere kant. Dan krijg je een rechthoek met dezelfde basis en dezelfde hoogte. De oppervlakte is dus niet veranderd: $\text{basis} \cdot \text{hoogte}$.

### **Voorbeelden**

??? example "Voorbeeld 1: Een rechthoek"
    **<p style="text-align: center;font-size:20px;">Een tuin is $12$ m lang en $8$ m breed. Bereken de omtrek en de oppervlakte.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    De omtrek is $2$ keer de lengte plus $2$ keer de breedte:

    $$12 + 8 + 12 + 8 = 40 \text{ m}$$

    De oppervlakte is lengte keer breedte:

    $$12 \cdot 8 = 96 \text{ m}^2$$

    !!! quote ""
        De omtrek is $40$ m en de oppervlakte is $96$ m².

??? example "Voorbeeld 2: Een driehoek"
    **<p style="text-align: center;font-size:20px;">Een driehoek heeft een basis van $10$ cm en een hoogte van $6$ cm. Bereken de oppervlakte.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We gebruiken de formule voor een driehoek:

    $$\frac{1}{2} \cdot 10 \cdot 6 = \frac{1}{2} \cdot 60 = 30$$

    !!! quote ""
        De oppervlakte is $30$ cm².

??? example "Voorbeeld 3: Een trapezium"
    **<p style="text-align: center;font-size:20px;">Een trapezium heeft evenwijdige zijden van $5$ cm en $9$ cm, en een hoogte van $4$ cm. Bereken de oppervlakte.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We vullen de formule in:

    $$\frac{1}{2} \cdot (5 + 9) \cdot 4 = \frac{1}{2} \cdot 14 \cdot 4 = 28$$

    !!! quote ""
        De oppervlakte is $28$ cm².

??? example "Voorbeeld 4: Een samengestelde figuur"
    **<p style="text-align: center;font-size:20px;">Een L-vormige kamer bestaat uit een rechthoek van $6$ bij $4$ m en een rechthoek van $3$ bij $2$ m eraan vast. Wat is de oppervlakte?</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We knippen de figuur in twee rechthoeken en tellen de oppervlaktes op:

    - Eerste rechthoek: $6 \cdot 4 = 24$ m²
    - Tweede rechthoek: $3 \cdot 2 = 6$ m²

    !!! quote ""
        De oppervlakte is $24 + 6 = 30$ m².

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **7.3 De cirkel** {#p7-3}

Een cirkel is een bijzonder figuur. Alle punten op de rand zijn even ver van het midden. Daarom heeft een cirkel een paar eigen woorden:

- De **middelpunt** is het punt in het midden.
- De **straal** ($r$) is de afstand van het middelpunt tot de rand.
- De **diameter** ($d$) is de afstand van de ene kant van de cirkel naar de andere, door het middelpunt heen.

De diameter is dus altijd twee keer de straal: $d = 2r$.

### **Het getal $\pi$**

Als je de omtrek van een cirkel deelt door zijn diameter, krijg je **altijd** hetzelfde getal. Dat getal heet **pi** en schrijf je als $\pi$. Het is ongeveer:

$$\pi \approx 3.14159\ldots$$

De cijfers achter de komma gaan oneindig door, zonder patroon. Daarom schrijven we het als $\pi$, of gebruiken we de $\pi$-knop op de rekenmachine.

???+ Belangrijk
    ### **Formules voor de cirkel**

    - Omtrek: $\large{O = \pi \cdot d = 2 \pi r}$
    - Oppervlakte: $\large{A = \pi r^2}$

Let op: bij de oppervlakte is het **de straal in het kwadraat**, niet de diameter! Dus eerst $r^2$ uitrekenen en dan pas keer $\pi$.

### **Voorbeelden**

??? example "Voorbeeld 1: De omtrek van een cirkel"
    **<p style="text-align: center;font-size:20px;">Een cirkel heeft een diameter van $10$ cm. Bereken de omtrek in één decimaal.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We gebruiken $O = \pi \cdot d$:

    $$O = \pi \cdot 10 \approx 31.4$$

    !!! quote ""
        De omtrek is ongeveer $31.4$ cm.

??? example "Voorbeeld 2: De oppervlakte van een cirkel"
    **<p style="text-align: center;font-size:20px;">Een cirkel heeft een straal van $4$ cm. Bereken de oppervlakte in één decimaal.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We gebruiken $A = \pi r^2$:

    $$A = \pi \cdot 4^2 = \pi \cdot 16 \approx 50.3$$

    !!! quote ""
        De oppervlakte is ongeveer $50.3$ cm².

??? example "Voorbeeld 3: Begin met de diameter"
    **<p style="text-align: center;font-size:20px;">Een ronde pizza heeft een diameter van $30$ cm. Hoe groot is de oppervlakte?</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben de straal nodig. De straal is de helft van de diameter: $30 : 2 = 15$ cm. Dan:

    $$A = \pi \cdot 15^2 = \pi \cdot 225 \approx 706.9$$

    !!! quote ""
        De oppervlakte is ongeveer $706.9$ cm².

??? example "Voorbeeld 4: Een halve cirkel"
    **<p style="text-align: center;font-size:20px;">Een halve cirkel heeft straal $6$ cm. Bereken de oppervlakte.</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Eerst de oppervlakte van de hele cirkel:

    $$\pi \cdot 6^2 = 36\pi$$

    Een halve cirkel is de helft hiervan:

    $$\frac{1}{2} \cdot 36\pi = 18\pi \approx 56.5$$

    !!! quote ""
        De oppervlakte is ongeveer $56.5$ cm².

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **7.4 Inhoud** {#p7-4}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">

## **7.5 Aanzichten** {#p7-5}

<!-- TODO: uitleg, belangrijke regels en voorbeelden -->

<hr style="height: 1.5px; background-color: #575757; border: none;">
