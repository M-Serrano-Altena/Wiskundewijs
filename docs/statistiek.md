# Statistiek
We gebruiken statistiek om gegevens beter te kunnen begrijpen. Dit kunnen we doen door het op een begrijpelijke manier weer te geven. Bijvoorbeeld in een staafdiagram, histogram of een cirkeldiagram. Maar we kunnen ook bepaalde gegevens berekenen die ons meer informatie geven, zoals bijvoorbeeld het gemiddelde, de mediaan of de modus. Hiermee krijgen we beter grip op de data. 

## Data weergeven
We kunnen informatie handig weergeven in grafieken en in diagrammen. We kijken naar een paar verschillende type diagrammen en bekijken hoe je ze af moet lezen en zelf maken. 

### Staafdiagrammen
We beginnen met staafdiagrammen. Stel we willen bijvoorbeeld kijken naar het aantal fietsen dat een fietsenwinkel verkoopt in $1$ week. We krijgen de volgende data:

| Maandag   | Dinsdag   | Woensdag  | Donderdag | Vrijdag   | Zaterdag  | Zondag    |
| --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| 8         | 5         | 9         | 4         | 15        | 24        | 11        |

We willen nu dit op een handige en duidelijke manier weergeven in een grafiek, zodat we de dagen goed met elkaar kunnen vergelijking. We kunnen dit doen door middel van een **staafdiagram**. In Figuur 1 is er een staafdiagram weergegeven van deze data. 

<figure markdown>
![Staafdiagram](assets/images/statistiek/Aantal verkochte fietsen in 1 week - sdg.svg){ width="500"}
    <figcaption>Figuur 1. Staafdiagram van het aantal verkochte fietsen in 1 week.</figcaption>
</figure>

Hiermee kunnen we precies zien hoeveel fietsen er op elke dag zijn verkocht en zien we ook meteen wat de dag is waar er de meeste fietsen verkocht is en welke dag de minste fietsen. 

Namelijk op zaterdag waren er de meeste fietsen verkocht: $24$ fietsen, en op donderdag de minste fietsen: $4$ fietsen. 

???+ belangrijk
    We gebruiken vooral staafdiagrammen bij data waar we verschillende type categorieën of groepen met elkaar vergelijken. 
    
    Dus in dit geval zijn de verschillende groepen de verschillende dagen van de week.

### Histogrammen
Laten we nu kijken naar een klas die een wiskunde toets heeft gemaakt. Daarbij hebben de leerlingen verschillende cijfers gehaald, en die zijn weergegeven met een **histogram** in Figuur 2.

<figure markdown>
![Histogram](assets/images/statistiek/Behaalde cijfers wiskunde toets - hg.svg){ width="500"}
    <figcaption>Figuur 2. Histogram van de behaalde cijfers voor een wiskunde toets.</figcaption>
</figure>

We kunnen hier aflezen hoeveel leerlingen een bepaald cijfer hebben gehaald. Dus $4$ leerlingen hebben een $4$ gehaald, $8$ leerlingen een $7$ en $3$ leerlingen een $7$.

???+ belangrijk
    We gebruiken een histogram wanneer we continue data willen weergeven en het meer gaat om de absolute waardes van de dataverdeling. 
    
    Dus in dit geval gaat de cijferverdeling van een $4$ naar een $9$ en zien we hoeveel leerlingen een bepaald cijfer hebben gehaald.


### Cirkeldiagrammen
We kunnen het voorbeeld van net over de cijfers van een wiskunde toets ook weergeven in een **cirkeldiagram**.

<figure markdown>
![Cirkeldiagram](assets/images/statistiek/Behaalde cijfers wiskunde toets - cdg.svg){ width="500"}
    <figcaption>Figuur 3. Cirkeldiagram van de behaalde cijfers voor een wiskunde toets.</figcaption>
</figure>

In Figuur 3 kunnen aflezen welk percentage van de leerlingen een bepaald cijfer heeft gehaald. Dus $26.7 \%$ heeft een $7$ gehaald, $20 \%$ een $8$, $10 \%$ een 9, etc.

???+ belangrijk
    We gebruiken cirkeldiagrammen als we een kleine hoeveelheid verschillende groepen willen weergeven. En dan met name de relatieve grootte van de groepen, en niet zozeer de absolute hoeveelheden. 
    
    Dus in dit geval om te laten zien welk percentage van de leerlingen welk cijfer heeft gehaald en niet per se dat bijvoorbeeld het $8$ leerlingen waren die een $7$ hebben gehaald. 


### Lijndiagrammen
De laatste manier om data weer te geven is met een **lijndiagram**. We kijken nu naar de temperatuur in de maand Juli. 

<figure markdown>
![Lijndiagram](assets/images/statistiek/Temperatuur in de maand Juli - ldg.svg){ width="500"}
    <figcaption>Figuur 4. Lijndiagram van de temperatuur in de maand Juli. De maximum temperatuur op een dag is aangegeven in het blauw, en de minimum temperatuur op een dag is aangegeven in het groen.</figcaption>
</figure>

We kunnen in Figuur 4 precies aflezen wat de minimum en maximum temperatuur is op elke dag van de maand Juli. Dus op 10 Juli was de minimum temperatuur ongeveer $23 \ ^{\circ} \textrm C$ en de maximum temperatuur ongeveer $29 \ ^{\circ} \textrm C$.

???+ belangrijk
    We gebruiken lijndiagrammen als we een relatie tussen twee waardes willen weergeven. Het is vooral nuttig om de groei of afname van een bepaalde waarde te laten zien. Bij lijndiagrammen kun je ook meerdere datasets vergelijken.

    In dit geval kijken we naar de relatie tussen de temperatuur en de tijd. We kunnen dan precies zijn hoe de temperatuur verandert in de tijd. We vergelijken ook twee datasets, namelijk die van de maximum temperatuur en die van de minimum temperatuur.  


## Gemiddelde
Het gemiddelde is handig om een uitspraak te kunnen doen over de hele dataset. Je kunt over het algemeen ermee kijken waar de meeste data zich bevindt en het maakt het vergelijken van verschillende datasets makkelijker. 

Laten we bijvoorbeeld naar twee verschillende klassen kijken: klas A en klas B. De twee verschillende klassen hebben net een toets gemaakt en de leerlingen hebben verschillende cijfers gehaald. De cijfers van beide klassen is weergegeven met een histogram in Figuur 5.  

<figure markdown>
![Histogram](assets/images/statistiek/Cijfers van klas A en klas B - hg.svg){ width="500"}
    <figcaption>Figuur 5. Histogram van de behaalde cijfers voor een wiskunde toets.</figcaption>
</figure>

We zien hier dat de cijfers van klas A over het algemeen hoger zijn dan die van klas B. Een gemiddelde kan heel handig zijn om te bekijken hoe de leerlingen het over het algemeen of gemiddeld hebben gedaan. 

We berekenen een gemiddelde op de volgende manier:

???+ Belangrijk
    Een gemiddelde bereken je als volgt:

    - Tel alle getallen bij elkaar op
    - Deel het door het aantal getallen
    

    Dus voor de getallen $\large{2, 4, 6, 8}$ kunnen we het gemiddelde als volgt berekenen:

    - We tellen alle getallen bij elkaar op:

    $$\large{2 + 4 + 6 + 8 = 20}$$

    - Dan delen we het door het aantal getallen:

    $$\large{\frac{20}{4} = 5}$$

    Het gemiddelde van deze reeks getallen is dus $5$.


## Mediaan en Modus

