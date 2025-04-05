## **De Eenheidscirkel**
De eenheidscirkel is eigenlijk gewoon een cirkel met een straal van lengte $1$. We kunnen het gebruiken om verschillende waardes van sinus en cosinus te bepalen bij verschillende hoeken.

???+ video
    <video controls>
    <source src="/assets/videos/UnitCircle.mp4" type="video/mp4">
    </video>

    *<p style="text-align: center;">Filmpje: Een schets van de eenheidscirkel. Het $x$-coördinaat van een punt op de cirkel is de cosinus van de bijbehorende hoek. Het $y$-coördinaat van dat punt is de sinus van die bijbehorende hoek.</p>*

<figure>
    <img src="/assets/images/goniometrie/Unit_Circle.svg" 
        loading="lazy" 
        width="1000" 
        alt="Eenheidscirkel">
</figure>
<center><span><i>Figuur 1. De eenheidscirkel met de hoeken in het blauw weergegeven.</i></span></center> <br><br>

We kunnen met de eenheidscirkel kijken wat de cosinus en sinus van een bepaalde hoek zijn. We kijken dan naar het $x$- en $y$-coördinaat van het punt op de cirkel dat hoort bij die hoek. Het $x$-coördinaat bij die hoek is hetzelfde als de cosinus van die hoek. En het $y$-coördinaat bij de hoek is hetzelfde als de sinus van die hoek. Hieronder kunnen zien we waarom dit het geval is.

??? abstract "Bewijs"
    We hebben hieronder de eenheidscirkel getekend met een willekeurige hoek $\theta$. Bij deze hoek hebben we een driehoek getekent met de straal als schuine zijde. Deze zijde heeft een lengte $1$, want de straal van een eenheidscirkel is altijd $1$.

    <figure>
        <img src="/assets/images/goniometrie/Unit_Circle_triangle.svg" 
            loading="lazy" 
            width="300" 
            alt="Eenheidscirkel met driehoek">
    </figure>
    <center><span><i>Figuur 2. De eenheidscirkel met daarin een driehoek getekend met een bepaalde hoek $\theta$. $x$ en $y$ zijn het $x$- en $y$-coördinaat van het punt.</i></span></center> <br><br>


    Zijde $b$ is hier de overstaande zijde en zijde $a$ is de aanliggende zijde (zie eventueel de opmerking bij [goniometrische functies](#goniometrische-functies)). Bij de [goniometrische functies](#goniometrische-functies) hebben de volgende verbanden gezien:

    $$\large{\sin(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Schuin}}}$$

    $$\large{\cos(\theta) = \frac{\mathrm{Aanliggend}}{\mathrm{Schuin}}}$$

    We hebben net gezien dat onze schuine zijde een lengte $1$ heeft. Als we dit invullen, dan delen we door $1$ en houden we dus alleen de teller over:

    $$\large{\sin(\theta) = \mathrm{Overstaand}}$$

    $$\large{\cos(\theta) = \mathrm{Aanliggend}}$$

    We hebben net ook gezien dat zijde $b$ onze overstaande zijde is en zijde $a$ de aanliggende. Dit kunnen we dus gaan invullen:

    $$\large{\sin{(\theta)} = b}$$

    $$\large{\cos{(\theta)} = a}$$

    Maar de lengte van $a$ is precies hetzelfde als het $x$-coördinaat van het punt. Want de zijde begint bij de oorsprong en eindigt bij $x$. En dus als we bij $0$ beginnen en een afstand $a$ afleggen om bij $x$ te komen, dan moet $x$ gelijk zijn aan de lengte $a$.
    
    We kunnen hetzelfde argument gebruiken voor $b$. We beginnen bij $y=0$ en gaan dan tot het $y$-coördinaat van het punt. Als we een afstand $b$ af moeten leggen om daar te komen, dan is het $y$-coördinaat hetzelfde als de lengte $b$. 
    
    Als we dit invullen in de sinus en cosinus formules die we net gevonden hebben, dan krijgen we dus: 

    !!! quote ""
        $$\large{\sin(\theta) = x\textrm{-coordinaat}}$$

        $$\large{\cos(\theta) = y\textrm{-coordinaat}}$$

<br>
Stel dus dat we er bijvoorbeeld achter willen komen wat $\sin(\frac{1}{3} \pi)$ is. We kunnen dan op de eenheidscirkel zoeken naar de hoek $\frac{1}{3} \pi$. We willen de sinus weten van deze hoek, dus moeten we kijken naar het $y$-coordinaat van het punt bij deze hoek. In Figuur 1 kunnen we aflezen dat dit $\frac{\sqrt{3}}{2}$ is. Er geldt dus dat:

$$\large{\sin(\frac{1}{3} \pi) = \frac{\sqrt{3}}{2}}$$

Als we $\cos(\frac{1}{3} \pi)$ wilden weten, dan moeten we naar het $x$-coördinaat van dat punt kijken. We zien dat dit $\frac{1}{2}$ is, dus er geldt dat:

$$\large{\cos(\frac{1}{3} \pi) = \frac{1}{2}}$$

Maar we hebben niet altijd de eenheidscirkel bij de hand, bijvoorbeeld bij toetsen niet. Dus is het handig om de eenheidscirkel te onthouden. Maar dit kan wel een beetje een gedoe zijn. Dus om niet alles te hoeven onthouden, kan het volgende trucje handig zijn.

****

### **Trucje voor het Onthouden**
Met deze methode hoef je alleen de vorm van de eenheidscirkel te onthouden en $3$ hoeken en $3$ waardes. Met de vorm van de cirkel bedoelen we dat bij $\theta = 0$ we rechts op de cirkel zitten. En met elke $\frac{1}{2} \pi$ (dus $90 ^{\circ}$) gaan we een kwart rondje tegen de klok in.

Als je dit onthoudt, samen met de volgende hoeken en waardes kun je de hele eenheidscirkel zelf opstellen.

???+ Belangrijk
    #### **<p style="font-size: 18px;">Om te onthouden<p>**

    Hoeken:

    $$\Large{\boxed{\frac{1}{6} \pi < \frac{1}{4} \pi <\frac{1}{3} \pi}}$$

    Waardes:

    $$\Large{\boxed{\frac{1}{2} < \frac{1}{2} \sqrt{2} < \frac{1}{2} \sqrt{3}}}$$

Om te kijken hoe we dit moeten toepassen, kijken we weer naar $\sin(\frac{1}{3} \pi)$.

We delen de eenheidscirkel op in $4$ kwartjes. We beginnen bij het kwart rechtsboven en dan tellen we tegen de klok in verder. Elk kwart cirkel heeft zijn eigen start- en eindhoek. Bij het eerste kwart is dit een starthoek van $0$ en een eindhoek van $\frac{1}{2} \pi$, bij het tweede kwart een starthoek van $\frac{1}{2} \pi$ en een eindhoek van $\pi$, enzovoort. 

We hebben de hoek $\frac{1}{3} \pi$ en dit is tussen $0$ en $\frac{1}{2} \pi$. We zitten dus in het eerste kwart van de cirkel, dus het kwart rechtsboven. Als we dat weten, dan kijken we naar de voortgang om van het begin- naar het eindpunt te gaan. Hoe groter de hoek, hoe meer voortgang. Dus $\frac{1}{3} \pi$ is de grootste hoek van [de $3$ hoeken](#om-te-onthouden), dus we hebben de meeste voortgang gemaakt tussen het begin- en eindpunt. 

Het beginpunt is bij $(1,0)$ en het eindpunt is bij $(0,1)$. We nemen de sinus, dus we zijn alleen geïnteresseerd in het $y$-coördinaat. En we moeten dus kijken welke van [de $3$ waardes](#om-te-onthouden) ons de meeste voortgang geeft om van $y=0$ naar $y=1$ te gaan. De meeste voortgang hier is dus de waarde $y = \frac{1}{2}\sqrt{3}$. Dit is namelijk de grootste waarde tussen $0$ en $1$ van [de $3$ waardes](#om-te-onthouden). Onze sinus wordt dan dus:

$$\sin(\frac{1}{3} \pi) = \frac{1}{2}\sqrt{3}$$

En die $y$-waarde zien we ook als we de eenheidscirkel tekenen.

<figure>
    <img src="/assets/images/goniometrie/Unit_Circle_Triangle_1_3_Pi.svg" 
        loading="lazy" 
        width="650" 
        alt="Eenheidscirkel met driehoek voor sin(1/3 pi)">
</figure>
<center><span><i>Figuur 3. De eenheidscirkel met de driehoek van de hoek $\frac{1}{3} \pi$. We willen de sinus van de hoek weten, dus kijken we naar het $y$-coördinaat. We kunnen aflezen dat het $y$ coördinaat gelijk is aan $\frac{1}{2}\sqrt{3}$.</i></span></center> <br><br>


Laten we nu kijken naar een voorbeeld waar we niet in het eerste kwart van de cirkel zitten. Dus stel we willen bepalen wat $\cos(\frac{5}{6} \pi)$ is. Hoe pakken we dit dan aan?

We hebben dus de hoek $\theta = \frac{5}{6} \pi$ en deze hoek zit tussen de starthoek $\frac{1}{2} \pi$ en de eindhoek $\pi$. Deze hoek zit dus in het tweede kwart van de cirkel, dus linksboven. Om met [dezelfde $3$ hoeken](#om-te-onthouden) te kunnen werken moeten we onze hoek min de starthoek doen:

$$\theta' = \frac{5}{6} \pi - \frac{1}{2} \pi$$

$$\theta' = \frac{1}{3} \pi$$

Hiermee kunnen we dezelfde stappen als net toepassen. Dit is de grootste hoek uit [de $3$ hoeken](#om-te-onthouden), dus er is de meeste voortgang gemaakt tussen ons begin- en eindpunt. Ons beginpunt is nu bij $(0, 1)$ en ons eindpunt is bij $(-1, 0)$. We nemen de consinus, dus we zijn alleen geïnteresseerd in het $x$-coördinaat. De meeste voortgang om van $x = 0$ naar $x = -1$ te gaan uit [de $3$ waardes](#om-te-onthouden) is bij $x = -\frac{1}{2} \sqrt{3}$. De cosinus wordt dan dus:

$$\large{\cos(\frac{5}{6} \pi) = - \frac{1}{2}\sqrt{3}}$$

En dit $x$-coördinaat kunnen we ook zien als we de eenheidscirkel tekenen.

<figure>
    <img src="/assets/images/goniometrie/Unit_Circle_Triangle_5_6_Pi.svg" 
        loading="lazy" 
        width="650" 
        alt="Eenheidscirkel met driehoek voor cos(5/6 pi)">
</figure>
<center><span><i>Figuur 4. De eenheidscirkel met de driehoek van de hoek $\frac{5}{6} \pi$. We willen de cosinus van de hoek weten, dus kijken we naar het $x$-coördinaat. We kunnen aflezen dat het $x$-coördinaat gelijk is aan $-\frac{1}{2}\sqrt{3}$.</i></span></center> <br><br>


Als dit misschien nog niet helemaal duidelijk was, staan hieronder nog een paar andere voorbeelden om ermee te oefenen.

#### **<p style="font-size: 20px;">Voorbeelden<p>**

??? example "Voorbeeld 1: $\cos(\frac{3}{4} \pi)$"
    **<p style="text-align: center;font-size:20px;">Bepaal: $\cos(\frac{3}{4} \pi)$</p>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben hier een hoek van $\theta = \frac{3}{4} \pi$ en dat zit tussen de starthoek $\frac{1}{2} \pi$ en de eindhoek $\pi$. We nemen de cosinus, dus we zijn alleen geïnteresseerd in het $x$-coördinaat. Om dit te bepalen, moeten we eerst onze hoek min de starthoek doen:
    
    $$\large{\theta' = \frac{3}{4} \pi - \frac{1}{2} \pi}$$

    $$\large{\theta' = \frac{1}{4} \pi}$$

    Dit is de middelste hoek uit [de $3$ hoeken](#om-te-onthouden). Dus onze voorgang om van het begin- naar het eindpunt te gaan zit in het midden. Ons startpunt is bij $(0, 1)$ en ons eindpunt is bij $(-1, 0)$. 
    
    We kijken dus alleen naar het $x$-coördinaat, dus we moeten kijken naar de voortgang om van $x=0$ naar $x=-1$ te gaan. De middelste waarde tussen $0$ en $-1$ uit [de $3$ waardes](#om-te-onthouden) is $x = -\frac{1}{2}\sqrt{2}$. De cosinus wordt dus: 

    !!! quote ""
        $$\large{\cos(\frac{3}{4} \pi) = -\frac{1}{2} \sqrt{2}}$$

    En dit $x$-coördinaat zien we ook als we de eenheidscirkel tekenen.

    <figure>
        <img src="/assets/images/goniometrie/Unit_Circle_Triangle_3_4_Pi.svg" 
            loading="lazy" 
            width="550" 
            alt="Eenheidscirkel met driehoek voor cos(3/4 pi)">
    </figure>
    <center><span><i>Figuur 1. De eenheidscirkel met de driehoek van de hoek $\frac{3}{4} \pi$. We willen de cosinus van de hoek weten, dus kijken we naar het $x$-coördinaat. We kunnen aflezen dat het $x$-coördinaat gelijk is aan $-\frac{1}{2}\sqrt{2}$.</i></span></center> <br><br>




??? example "Voorbeeld 2: $\sin(1 \frac{1}{6} \pi)$"
    **<p style="text-align: center;font-size:20px;">Bepaal: $\sin(1 \frac{1}{6} \pi)$</p>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben hier een hoek van $\theta = 1 \frac{1}{6}$ en dit zit tussen de starthoek $\pi$ en de eindhoek $1 \frac{1}{2} \pi$. We nemen de sinus, dus we zijn alleen geïnteresseerd in het $y$-coördinaat. Om dit te bepalen doen we onze hoek min de starthoek:

    $$\large{\theta' = 1 \frac{1}{6} \pi - \pi}$$

    $$\large{\theta' = \frac{1}{6} \pi}$$
    
    Deze hoek is de kleinste hoek uit [de $3$ hoeken](#om-te-onthouden), dus we hebben de minste voortgang gemaakt tussen ons begin- en eindpunt. Ons beginpunt is bij $(-1,0)$ en ons eindpunt is bij $(0, -1)$. Dus we moeten kijken welke [waarde](#om-te-onthouden) van de $3$ de minste voortgang geeft om van $y=0$ naar $y=-1$ te gaan. Dit is bij $y = -\frac{1}{2}$. De sinus wordt dan dus: 
    
    !!! quote ""
        $$\large{\sin(1 \frac{1}{6} \pi) = - \frac{1}{2}}$$
    
    Deze $y$-waarde zien we ook als de eenheidscirkel tekenen.

    <figure>
        <img src="/assets/images/goniometrie/Unit_Circle_Triangle_1_1_6_Pi.svg" 
            loading="lazy" 
            width="550" 
            alt="Eenheidscirkel met driehoek voor sin(1 1/6 pi)">
    </figure>
    <center><span><i>Figuur 2. De eenheidscirkel met de driehoek van de hoek $1 \frac{1}{6} \pi$. We willen de sinus van de hoek weten, dus kijken we naar het $y$-coördinaat. We kunnen aflezen dat het $y$-coördinaat gelijk is aan $-\frac{1}{2}$.</i></span></center> <br><br>



??? example "Voorbeeld 3: $\cos(1 \frac{2}{3} \pi)$"
    **<p style="text-align: center;font-size:20px;">Bepaal: $\cos(1 \frac{2}{3} \pi)$</p>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben hier een hoek van $\theta = 1 \frac{2}{3}$ dat tussen de starthoek $\theta = 1 \frac{1}{2} \pi$ en de eindhoek $2 \pi$ zit. Als eerst doen we onze hoek min de starthoek: 
    
    $$\large{\theta' = 1 \frac{2}{3} \pi - 1 \frac{1}{2} \pi}$$

    $$\large{\theta' = \frac{1}{6} \pi}$$
    
    Deze hoek is de kleinste uit [de $3$ hoeken](#om-te-onthouden) en dus is er de minste voortgang gemaakt tussen ons start- en eindpunt. 
    
    Ons startpunt is $(0, -1)$ en ons eindpunt is $(1, 0)$. We nemen de cosinus en we zijn dus alleen geïntereseerd in het $x$-coördinaat. De minste voortgang om van $x = 0$ naar $x = 1$ te gaan is bij $x = \frac{1}{2}$. De cosinus van $1 \frac{2}{3} \pi$ is dus:

    !!! quote ""
        $$\large{\cos(1 \frac{2}{3} \pi) = \frac{1}{2}}$$

    En dit $x$-coördinaat kunnen we ook zien als we het tekenen.

    <figure>
        <img src="/assets/images/goniometrie/Unit_Circle_Triangle_1_2_3_Pi.svg" 
            loading="lazy" 
            width="550" 
            alt="Eenheidscirkel met driehoek voor cos(1 2/3 pi)">
    </figure>
    <center><span><i>Figuur 3. De eenheidscirkel met de driehoek van de hoek $1 \frac{2}{3} \pi$. We willen de cosinus van de hoek weten, dus kijken we naar het $x$-coördinaat. We kunnen aflezen dat het $x$-coördinaat gelijk is aan $\frac{1}{2}$.</i></span></center> <br><br>


Maar je bent natuurlijk niet verplicht om dit trucje te gebruiken. Als je het handiger vindt om gewoon de eenheidscirkel helemaal uit je hoofd te leren, doe dat vooral!

<hr style="height: 1.5px; background-color: #575757; border: none;">
