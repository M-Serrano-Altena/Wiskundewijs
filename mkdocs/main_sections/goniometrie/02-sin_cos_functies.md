## **De Sinus en Cosinus functies**
Laten we nu iets dieper ingaan op de **sinus** en **cosinus** functies. Wat deze functies bijzonder maakt, is dat het periodieke functies zijn. Dit betekent dat de functie zich herhaalt na een bepaalde tijd. In dit geval is dat elke $2 \pi$. Dus elke $2 \pi$ begint de functie weer opnieuw en herhaalt het zich weer. We zeggen dan dat deze functie een periode heeft van $2 \pi$ (zie ook Figuur 1 en Figuur 2). 

??? note "Graden vs Radialen"
    In de meetkunde gebruiken we vaak graden. Maar als we meer gaan kijken naar de goniometrische functies zelf en hun vorm, dan zijn radialen vaak handiger. 

    Radialen is een eenheid voor hoeken, net zoals graden. Radialen gaan niet van $0$ tot $360 ^{\circ}$, maar van $0$ tot $2 \pi$. We kiezen voor $2 \pi$ als eindpunt omdat dit de omtrek is van een cirkel met straal $1$. Dus als we $1$ rondje doen, hebben we $2 \pi$ afgelegd, $2$ rondjes hebben we $4 \pi$ afgelegd, $3$ rondjes $6 \pi$ enzovoort. Een half rondje is dan $\pi$ of $180 ^{\circ}$.

    We kunnen van radialen naar graden omrekenen en andersom:

    - Graden naar Radialen: $\large{\quad \theta_{grad} \cdot \Large \frac{2 \pi}{360 ^{\circ}} \large = \theta_{rad}}$
    - Radialen naar Graden: $\large{\quad \theta_{rad} \cdot \Large \frac{360 ^{\circ}}{2 \pi} \large = \theta_{grad}}$

<figure>
    <img src="/assets/images/goniometrie/Sinus.svg" 
        loading="lazy" 
        width="500" 
        alt="Sinus functie">
</figure>
<center><span><i>Figuur 1. De sinus functie over een domein van $[-3 \pi, 3 \pi]$. Je kan zien dat bij elke $2 \pi$ de functie weer begint op hetzelfde punt (stijgend bij $y=0$).</i></span></center> <br><br>

<figure>
    <img src="/assets/images/goniometrie/Cosinus.svg" 
        loading="lazy" 
        width="500" 
        alt="Cosinus functie">
</figure>
<center><span><i>Figuur 2. De cosinus functie over een domein van $[-3 \pi, 3 \pi]$. Je kan zien dat de functie zich na elke $2 \pi$ herhaald. Dus de punten $\large \frac{5}{2} \pi$ en $\large - \frac{3}{2} \pi$ zijn hetzelfde als het punt $\large \frac{1}{2} \pi$.</i></span></center> <br><br>



???+ Belangrijk
    ### **Periodiciteit van Sinus en Cosinus**
    Het feit dat de functie zich herhaald kunnen we ook terug zien in de functie zelf:

    $$\large{\sin(x + 2 \pi) = \sin(x)}$$

    $$\large{\cos(x + 2 \pi) = \cos(x)}$$

Dus dit betekent bijvoorbeeld dat:

- $\sin(\pi) = \sin(3 \pi)$
- $\cos(1 \frac{1}{2}) = \cos(- \frac{1}{2} \pi)$
- $\cos(4 \pi) = \cos(6 \pi)$
- $\sin(- \frac{1}{4} \pi) = \sin(1 \frac{3}{4} \pi)$
- <span style="font-size: 15px;">etc.</span>

Het feit dat deze functies periodiek zijn, is erg belangrijk als we er vergelijkingen mee gaan oplossen. Laten we kijken hoe dat moet.

****

### **Sinus en Cosinus vergelijkingen**

Stel we willen de volgende vergelijking oplossen:

$$\sin(x) = 0.$$

Hoe doen we dat? We willen dus kijken waar de **sinus** functie een $y$-waarde heeft van $0$. In Figuur 1 kunnen we aflezen dat dit geldt bij $x=0$, maar ook bij andere $x$-waardes. Namelijk $x = -2 \pi$, $x = -\pi$, $x = \pi$ en $x = 2 \pi$. En deze functie gaat oneindig lang door, dus dit blijft maar zo door gaan. Hoe noteren we dit wiskundig? 

We schrijven dit als volgt op:

!!! quote ""
    $$\large{x = k \cdot \pi}$$

$k$ kan hier elk geheel getal zijn. Dus $k = 0, \pm 1, \pm 2, \pm 3, ...$ 

De waardes van $k$ gaan oneindig lang door, en dat is ook wat we willen om onze oplossingen te beschrijven. Maar stel nou dat we alle oplossingen willen weten op het domein $[0, 2 \pi]$. Hoe doen we dat dan met de oplossing die we net hebben gevonden?

We moeten dan alle mogelijke waardes voor $k$ proberen die ons een $x$ geeft binnen het domein van $[0, 2\pi]$. Dus welke waardes van $k$ moeten we invullen in $x = k \cdot \pi$ om een $x$ te krijgen tussen $0$ en $2 \pi$?

Dit zijn de waardes $k = 0$, $k = 1$ en $k = 2$. Want als we $k = 3$ proberen, dan krijgen we $x = 3 \pi$ en dit is te groot. Als we aan de andere kant $k = -1$ proberen, dan krijgen we $x = -\pi$ en dit is weer te klein. Dus de oplossingen op het domein $[0, 2 \pi]$ worden:

!!! quote ""
    $$\large{x = 0 \ \vee \ x = \pi \ \vee \ x = 2 \pi}$$

Laten we naar een ander voorbeeld kijken. Stel we willen nu de volgende vergelijking oplossen:

$$\cos{(x)} = 1.$$

Hoe doen we dit? We moeten dus kijken voor welke $x$-waardes de cosinus een $y$-waarde heeft van $1$. In Figuur 2 kunnen we zien dat dit is bij $x = 0$. Maar ook bij $x = -2\pi$ en bij $x = 2\pi$. De functie herhaalt zich steeds, dus dit patroon herhaalt zich ook. Onze oplossing wordt dus:

!!! quote ""
    $$\large{x = k \cdot 2\pi}$$

$k$ kan weer elk geheel getal zijn. Dus de oplossingen op het domein $[0, 2 \pi]$ worden dan:

!!! quote ""
    $$\large{x = 0 \ \vee \ x = 2 \pi}$$

Dit is dus voor $k = 0$ of $k = 1$. Want als we andere waardes voor $k$ proberen, dan is $x$ niet meer tussen $0$ en $2 \pi$. Dus dit moeten de enige twee oplossingen zijn op het domein $[0, 2 \pi]$.

We hebben dit opgelost door de functies te schetsen, maar kunnen we het ook oplossen zonder een schets? Het antwoord is ja! Om goed te begrijpen hoe dit moet, moeten we eerst kijken naar de symmetrie in de sinus en cosinus functies. We zullen dat nodig hebben om de [algemene oplossing](#algemene-oplossing) te kunnen begrijpen.

****

### **Symmetrie**
De cosinus is gespiegeld in de $y$-as (zie eventueel Figuur 2). Dus alles links van de $y$-as is hetzelfde als rechts van de $y$-as. Links van de $y$-as is bij een negatieve $x$, rechts van de $y$-as is bij een positieve $x$. Dus met andere woorden:

$$\boxed{\cos(-x) = \cos(x)}$$

Bij de sinus is dit juist omgekeerd. Het is niet gespiegeld in de $y$-as, maar gespiegeld bij de oorsprong (zie eventueel Figuur 1). Dus alles dat rechts van de $y$-as positief is, wordt negatief links van de $y$-as. Andersom geldt dit natuurlijk ook. Dit betekent dus dat er geldt dat:

$$\boxed{\sin(-x) = - \sin(x)}$$

Apart van deze symmetrieën hebben de sinus en cosinus nog een andere symmetrie. Deze symmetrie is als je $\sin(-x)$ of $\cos(-x)$ met $\pi$ naar rechts verschuift. En ik denk dat dit makkelijker te zien is met wat filmpjes. Laten we beginnen met de symmetrie van de sinus functies.

???+ video
    **<p style="font-size: 20px;">Sinus symmetrie</p>**

    <video controls>
    <source src="/assets/videos/Sin.mp4" type="video/mp4">
    </video>


    *<p style="text-align: center;">Filmpje: Een sinus functie wordt aangepast om te bewijzen dat $\sin(x) = \sin(\pi - x)$. Eerst wordt de transformatie $\sin(x) \rightarrow \sin(-x)$ toegepast. Vervolgens wordt deze functie naar rechts verschoven met $\pi$. Deze nieuwe functie wordt beschreven door $\sin(\pi - x)$ en we zien dat dit precies hetzelfde is als onze oude functie $\sin(x)$.</p>*

We zien dus dat we een $\sin(x)$ functie op zo'n manier kunnen aanpassen dat we de functie $\sin(\pi - x)$ krijgen. En deze functie is weer precies dezelfde functie als de $\sin(x)$ die we eerst hadden. Dit betekent dus dat we de volgende symmetrie hebben:

$$\boxed{\sin(\pi - x) = \sin(x)}$$

Voor consinus functies hebben we een soort gelijke symmetrie.

???+ video
    **<p style="font-size: 20px;">Cosinus symmetrie</p>**

    <video controls>
    <source src="/assets/videos/Cos.mp4" type="video/mp4">
    </video>


    *<p style="text-align: center;">Filmpje: Een cosinus functie wordt aangepast om te bewijzen dat $-\cos(x) = \cos(\pi - x)$. Eerst verandert de $\cos(x)$ naar $-\cos(x)$ en tegelijkertijd wordt laten zien dat $\cos(x) = \cos(-x)$. Daarna wordt de $\cos(-x)$ functie naar rechts verschoven met $\pi$. Deze verplaatste functie wordt beschreven door $\cos(\pi - x)$ en dit is precies hetzelfde als $- \cos(x)$.</p>*

We zien dus dat als we een $\cos(-x)$ functie met $\pi$ naar rechts verschuiven, dat we dezelfde functie krijgen als $- \cos(x)$. Voor cosinus functies hebben we dus de volgende symmetrie:

$$\boxed{\cos(\pi - x) = -\cos(x)}$$

We zetten hieronder nog even alle symmetrieën op een rijtje.

???+ Belangrijk
    ### **Symmetrieformules**
    
    1. $$\large{\sin(-x) = - \sin(x)}$$

    2. $$\large{\cos(-x) = \cos(x)}$$

    3. $$\large{\sin(\pi - x) = \sin(x)}$$

    4. $$\large{\cos(\pi - x) = - \cos(x)}$$
    
Met deze kennis kunnen we nu sinus en cosinus vergelijking gaan oplossen. We hebben daarvoor de [symmetrieformules](#symmetrieformules) en de [periodiciteit](#periodiciteit-van-sinus-en-cosinus) van de functies nodig. Laten we eerst kijken naar een sinus vergelijking.

****

**<p style="font-size: 20px;">Sinus vergelijking oplossen</p>**

Laten we [weer](#sinus-en-cosinus-vergelijkingen) kijken naar de volgende vergelijking:

$$\sin(x) = 0.$$

Om dit op te lossen willen we eerst aan beide kanten een $\sin$ functie hebben. We moeten dus de $0$ schrijven als $\sin(a)$. We willen er dus achter komen van welk getal we de sinus moeten nemen om $0$ te krijgen. Om dit te doen kunnen we de $\arcsin$ van $0$ nemen (later zullen we de [eenheidscirkel](#de-eenheidscirkel) gebruiken). 

We krijgen dan dus $a = \arcsin(0)$. Als we dit invullen, dan vinden we $a = 0$. Dit betekent dus dat we de $0$ ook kunnen schrijven als $\sin(0)$. Onze vergelijking wordt dan dus:

$$\sin(x) = \sin(0)$$

Nu kunnen we aan beide kanten de sinus weghalen om te vinden:

$$x = 0$$

Dit is dus $1$ oplossing, maar we moeten nog rekening houden met de [periodiciteit](#periodiciteit-van-sinus-en-cosinus) en [symmetrie](#symmetrieformules). We weten dus dat de functie periodiek is en dat het elke $2\pi$ zich herhaalt. Dit betekent dus dat $x = 2\pi$, $x = 4\pi$, $x=6\pi$, etc. ook oplossingen zijn. Dus om hier rekening mee te houden schrijven we:

$$x = 0 + k \cdot 2\pi$$

$$x = k \cdot 2\pi$$

$k$ kan hier dus alle gehele getallen zijn. Maar we hebben ook nog de symmetrie die we in de [symmetrieformules](#symmetrieformules) hebben gezien. Dus we weten dat:

$$\sin(x) = \sin(\pi - x)$$

Dit betekent dus dat er moet gelden dat:

$$\sin(0) = \sin(\pi - 0)$$

Om hier rekening mee te houden moeten we nog een set oplossingen toevoegen:

$$x = k \cdot 2 \pi \ \vee \ x = \pi - 0 + k \cdot 2 \pi$$

$$x = k \cdot 2 \pi \ \vee \ x = \pi + k \cdot 2 \pi$$

In dit geval kunnen we deze twee verschillende sets combineren. Want we krijgen bij de linker de oplossingen $x = 0, 2\pi, 4\pi, ...$ en bij de rechter de oplossingen $x = \pi, 3 \pi, 5 \pi, ...$. Dus samen zijn onze oplossingen $x = 0, \pi, 2 \pi, 3\pi, 4\pi, 5\pi, ...$. Dit kunnen we opschrijven als:

!!! quote ""
    $$\large{x = k \cdot \pi}$$

En dat is ook wat we [eerder](#sinus-en-cosinus-vergelijkingen) gevonden hadden. In het algemeen hebben we dus voor een vergelijking van de vorm:

$$\large{\sin(x) = \sin(a)}$$

de volgende oplossingen:

$$\large{x = a + k \cdot 2\pi \ \vee \ x = \pi - a + k \cdot 2\pi}$$

****

**<p style="font-size: 20px;">Cosinus vergelijking oplossen</p>**

We kijken nu [weer](#sinus-en-cosinus-vergelijkingen) naar de volgende cosinus vergelijking:

$$\cos(x) = 1$$

We willen hier ook weer aan beide kanten dezelfde functie hebben, dus aan beide kanten een cosinus. We moeten dus de $1$ gaan schrijven als een cosinus. Dus welke getal moet $a$ zijn zodat $\cos(a) = 1$? Als we de $\arccos$ nemen, dan vinden we $a = \arccos(1) = 0$.

We weten nu dus dat $1 = \cos(0)$. De vergelijking kunnen we dan dus schrijven als:

$$\cos(x) = \cos(0)$$

Als we aan beide kanten de $\cos$ weg halen, dan vinden we dus dat $1$ van onze oplossingen is:

$$x = 0$$

Maar we moeten weer rekening houden met de [periodiciteit](#periodiciteit-van-sinus-en-cosinus) en de [symmetrie](#symmetrieformules) van de cosinus. Net zoals bij de sinus herhaalt de cosinus zich elke $2 \pi$, dus onze oplossingen herhaling zich ook op dezelfde manier:

$$x = 0 + k \cdot 2 \pi$$

$$x = k \cdot 2 \pi$$

Bij de cosinus hebben we een andere symmetrie dan bij de sinus. Bij de cosinus hebben we:

$$\cos(x) = \cos(-x)$$

Dus om hier rekening mee te houden moeten we nog een set oplossingen toevoegen:

$$x = k \cdot 2 \pi \ \vee \ x = -0 + k \cdot 2 \pi$$

$$x = k \cdot 2 \pi \ \vee \ x =  k \cdot 2 \pi$$

Maar in dit geval geldt er dat $0 = -0$, dus dit kunnen we gewoon weer versimpelen naar wat we eerst hadden:

!!! quote ""
    $$\large{x = k \cdot 2 \pi}$$

En dat is ook wat we [eerder](#sinus-en-cosinus-vergelijkingen) gevonden hadden. In het algemeen hebben we dus voor een vergelijking van de vorm:

$$\large{\cos(x) = \cos(a)}$$

de volgende oplossingen:

$$\large{x = a + k \cdot 2 \pi \ \vee \ x = -a + k \cdot 2 \pi}$$

We hebben nu dus de algemene oplossingen gevonden voor sinus en cosinus vergelijkingen!

???+ Belangrijk
    ### **Algemene Oplossing**

    <br>
    **<p style="font-size: 17px;">Sinus</p>**

    Een vergelijking van de vorm:

    $$\Large{\sin(x) = \sin(a)}$$

    heeft de volgende oplossingen:

    $$\Large{x = a + k \cdot 2 \pi \ \vee \ x = \pi - a + k \cdot 2 \pi}$$

    $k$ kan hier elk geheel getal zijn, dus $k = 0, \pm 1, \pm 2, \pm 3, ...$

    <br>
    **<p style="font-size: 17px;">Cosinus</p>**

    Een vergelijking van de vorm:

    $$\Large{\cos(x) = \cos(a)}$$

    heeft de volgende oplossingen:

    $$\Large{x = a + k \cdot 2 \pi \ \vee \  x = - a + k \cdot 2 \pi}$$

    $k$ kan hier weer elk geheel getal zijn, dus $k = 0, \pm 1, \pm 2, \pm 3, ...$

****

**<p style="font-size: 20px;">Sinus en Cosinus naar elkaar omschrijven</p>**

De sinus en de cosinus functies lijken best veel op elkaar: ze hebben dezelfde vorm, herhalen elke $2 \pi$ en gaan beide van $-1$ tot $1$. Het enige verschil is dat ze op andere punten beginnen. De sinus begint bij $y=0$ en de cosinus bij $y=1$. Dat is het enige verschil tussen de twee functies.

Dus als we de sinus functie een klein beetje kunnen verschuiven zodat het bij $y=1$ begint, dan hebben we een cosinus gemaakt. Het blijkt dat we $\sin(x)$ met $\dfrac{1}{2} \pi$ naar links moeten verschuiven om dit te bereiken. De verschoven sinus krijgt de vorm $\sin(x + \frac{1}{2} \pi)$ en dit is dus hetzelfde als $\cos(x)$:

$$\boxed{\sin(x + \frac{1}{2} \pi) = \cos(x)}$$

???+ video
    <video controls>
    <source src="/assets/videos/SinToCos.mp4" type="video/mp4">
    </video>

We kunnen natuurlijk ook de cosinus naar rechts verschuiven met $\frac{1}{2} \pi$ in plaats van de sinus naar links te verschuiven. De verschoven cosinus krijgt dan de vorm $\cos(x - \frac{1}{2} \pi)$ en dit is dan gelijk aan $\sin(x)$:

$$\boxed{\cos(x - \frac{1}{2} \pi) = \sin(x)}$$

???+ video
    <video controls>
    <source src="/assets/videos/CosToSin.mp4" type="video/mp4">
    </video>

<br>

???+ Belangrijk
    ### **Sinus en Cosinus omschrijven**

    $$\large{\cos(x) = \sin(x + \frac{1}{2} \pi)}$$

    $$\large{\sin(x) = \cos(x - \frac{1}{2} \pi)}$$

    ??? note "Andere manier van omschrijven"
        Als je niet wilt onthouden bij welke functie je $+ \frac{1}{2} \pi$ doet en bij welke $- \frac{1}{2} \pi$, dan kun je het ook als volgt omschrijven:

        $$\large{\cos(x) = \sin(\frac{1}{2} \pi - x)}$$

        $$\large{\sin(x) = \cos(\frac{1}{2} \pi - x)}$$

        En dit verband werkt ook altijd.

        ??? abstract "Bewijs"
            Dit kunnen we zelf bewijzen met behulp van de [Symmetrieformules](#symmetrieformules). 
            
            Om van een cosinus naar een sinus te gaan, kunnen de volgende symmetrie gebruiken:

            $$\large{\sin(x) = \sin(\pi - x)}$$

            Als we dit toepassen op $\sin(x + \frac{1}{2} \pi)$, dan vinden we:

            $$\large{\sin(x + \frac{1}{2} \pi) = \sin(\pi - (x + \frac{1}{2} \pi))}$$

            Als we dit uitwerken, dan vinden we:

            $$\large{\sin(x + \frac{1}{2} \pi) = \sin(\pi - x - \frac{1}{2} \pi)}$$

            $$\large{\sin(x + \frac{1}{2} \pi) = \sin(\frac{1}{2} \pi - x)}$$

            Het verband $\cos(x) = \sin(x + \frac{1}{2} \pi)$ wordt dan dus:

            $$\large{\boxed{\cos(x) = \sin(\frac{1}{2} \pi - x)}}$$

            <br>

            Om van een sinus naar een cosinus te gaan, kunnen we de volgende symmetrie gebruiken:
            
            $$\large{\cos(x) = \cos(-x)}$$

            Als we dit toepassen op $\cos(x - \frac{1}{2} \pi)$, dan vinden we:

            $$\large{\cos(x - \frac{1}{2} \pi) = \cos(-(x - \frac{1}{2} \pi))}$$

            Als we de haakjes uitwerken, vinden we:

            $$\large{\cos(x - \frac{1}{2} \pi) = \cos(\frac{1}{2} \pi - x)}$$

            Het verband $\sin(x) = \cos(x - \frac{1}{2} \pi)$ wordt dan dus:

            $$\large{\boxed{\sin(x) = \cos(\frac{1}{2} \pi - x)}}$$


### **Voorbeelden**
??? example "Voorbeeld 1: $\cos(2x) = 0$"
    **<p style="text-align: center;font-size:20px;">Los op: $\cos(2x) = 0$</p>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Om dit op te lossen willen we eerst aan beide kanten een cosinus hebben. We moeten dus kijken hoe we de $0$ als cosinus schrijven. Als we de $\arccos$ van $0$ nemen, dan vinden we $\frac{1}{2} \pi$. Met andere woorden, als we de cosinus van $\frac{1}{2} \pi$ nemen, krijgen we weer de $0$ terug. En omdat dus $\cos(\frac{1}{2} \pi) = 0$, kunnen we dit invullen in de vergelijking:

    $$\large{\cos(2x) = \cos(\frac{1}{2} \pi)}$$

    Nu kunnen we de [algemene oplossing](#algemene-oplossing) gebruiken voor een cosinus:

    $$\large{2x = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 2x = - \frac{1}{2} \pi + k \cdot 2 \pi}$$

    Nu kunnen we alles door $2$ delen om als eindantwoord te vinden:

    !!! quote ""
        $$\large{x = \frac{1}{4} \pi + k \cdot \pi \ \vee \ x = - \frac{1}{4} \pi + k \cdot \pi}$$

    <br>
    In dit geval kunnen we eventueel deze oplossingen ook combineren:

    - **Linker set:** $x = -\frac{3}{4} \pi, \frac{1}{4} \pi, 1 \frac{1}{4} \pi, 2 \frac{1}{4} \pi, ...$ *
    - **Rechter set:** $x = - \frac{1}{4} \pi, \frac{3}{4} \pi, 1 \frac{3}{4} \pi, ...$ *
    - **Gecombineerd:** $x = - \frac{3}{4} \pi, - \frac{1}{4} \pi, \frac{3}{4} \pi, 1 \frac{1}{4} \pi, 1 \frac{3}{4} \pi, ...$ *

    Deze combinatie kunnen we beschrijven op de volgende manier:

    !!! quote ""
        $$\large{x = \frac{1}{4} \pi + k \cdot \frac{1}{2} \pi}$$

    **De oplossingen gaan ook door in het negatieve, maar die zijn hier weg gelaten om het overzichtelijk te houden.*

??? example "Voorbeeld 2: $\sin(3x) = \cos(-x)$"
    **<p style="text-align: center;font-size:20px;">Los op: $\sin(3x) = \cos(-x)$</p>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    Als eerst kunnen met de [symmetrieformule](#symmetrieformules) $\cos(x) = \cos(-x)$ dit ook schrijven als:

    $$\large{\sin(3x) = \cos(x),}$$

    Om dit op te lossen, moeten we óf van beide functies een sinus maken óf van beide functies een cosinus. We kiezen er hier voor om van beide functies een sinus te maken. We moeten dan dus de $\cos(x)$ [omschrijven](#sinus-en-cosinus-omschrijven) naar $\sin(x + \frac{1}{2} \pi)$:

    $$\large{\sin(3x) = \sin(x + \frac{1}{2} \pi).}$$

    Nu kunnen we dit oplossen volgens de [algemene oplossing](#algemene-oplossing):

    $$\large{3x = x + \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 3x = \pi - (x + \frac{1}{2} \pi) + k \cdot 2 \pi}$$

    $$\large{3x = x + \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 3x = \frac{1}{2} \pi - x + k \cdot 2 \pi}$$

    Nu doen we alle termen met $x$ naar de linkerkant:

    $$\large{2x = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 4x = \frac{1}{2} \pi + k \cdot 2 \pi}$$

    Nu delen we bij de linker oplossing alles door $2$ en bij de rechter oplossing alles door $4$:
    
    !!! quote ""
        $$\large{x = \frac{1}{4} \pi + k \cdot \pi \ \vee \ x = \frac{1}{8} \pi + k \cdot \frac{1}{2} \pi}$$


??? example "Voorbeeld 3: $\cos(3x + \pi) = \cos(x + \frac{1}{2} \pi)$ op het domein $[-\pi, \pi]$"
    **<p style="text-align: center;font-size:20px;">Los op: $\cos(3x + \pi) = \cos(x + \frac{1}{2} \pi)$ op het domein $[-\pi, \pi]$</p>**

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben hier aan beide kanten al een cosinus staan, dus we kunnen dit meteen gaan [uitwerken](#algemene-oplossing):

    $$\large{3x + \pi = x + \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 3x + \pi = - (x + \frac{1}{2} \pi) + k \cdot 2 \pi}$$

    $$\large{3x + \pi = x + \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 3x + \pi = - x - \frac{1}{2} \pi + k \cdot 2 \pi}$$

    Nu doen we eerst alle termen met $x$ naar de linkerkant:
    
    $$\large{2x + \pi = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 4x + \pi = - \frac{1}{2} \pi + k \cdot 2 \pi}$$
    
    En nu doen we alle getallen rechts:

    $$\large{2x = - \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 4x = - 1 \frac{1}{2} \pi + k \cdot 2 \pi}$$

    Als laatst delen we nu bij de linker oplossing alles door $2$ en bij de rechter oplossing alles door $4$. Als we dit doen, dan vinden we alle oplossingen:

    $$\large{\boxed{x = - \frac{1}{4} \pi + k \cdot \pi \ \vee \ x = - \frac{3}{8} \pi + k \cdot \frac{1}{2} \pi}}$$

    Maar let op! We willen alleen de oplossingen hebben op het domein $[-\pi, \pi]$. Dus we moeten voor $k$ alle gehele getallen invullen die ons een oplossing geeft tussen $-\pi$ en $\pi$. Laten we eerst bij de linker oplossing wat waardes voor $k$ proberen:

    - $k = 0 \quad \Longrightarrow \quad x = - \frac{1}{4} \pi$
    - $k = 1 \quad \Longrightarrow \quad x = \frac{3}{4} \pi$

    En dit zijn de enige waardes van $k$ die ons een $x$ tussen $-\pi$ en $\pi$ geeft. $k = -1$ geeft ons $x = -1 \frac{1}{2} \pi$ en $k = 2$ geeft ons $x = 1 \frac{3}{4} \pi$ en dit ligt allebei niet tussen $-\pi$ en $\pi$.

    Nu kijken we naar de rechter oplossing:

    - $k = -1 \quad \Longrightarrow \quad x = -\frac{7}{8} \pi$
    - $k = 0 \quad \Longrightarrow \quad x = -\frac{3}{8} \pi$
    - $k = 1 \quad \Longrightarrow \quad x = \frac{1}{8} \pi$
    - $k = 2 \quad \Longrightarrow \quad x = \frac{5}{8} \pi$

    Dit zijn alle oplossingen bij de rechter vergelijking op het domein $[-\pi, \pi]$. Want voor $k = -2$ krijgen we $x = -1 \frac{3}{8} \pi$ en voor $k = 3$ krijgen we $x = 1 \frac{1}{8} \pi$.
    
    Alle oplossingen op het domein $[-\pi, \pi]$ zijn dus:

    !!! quote ""
        $\large{x = -\dfrac{7}{8} \pi \ \vee \ x = -\dfrac{3}{8} \pi \ \vee \ x = - \dfrac{1}{4} \pi \ \vee \ x = \dfrac{1}{8} \pi \ \vee \ x = \dfrac{3}{4} \pi \ \vee \ x = \dfrac{5}{8} \pi}$

<hr style="height: 1.5px; background-color: #575757; border: none;">