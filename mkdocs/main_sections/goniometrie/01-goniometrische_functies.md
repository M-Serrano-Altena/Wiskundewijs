## **De Goniometrische Functies**

Goniometrie gaat vooral over driehoeken en wat we daar allemaal mee kunnen berekenen. We kunnen de goniometrische functies gebruiken om hiermee te helpen. We gebruiken ze als we een hoek en een zijde hebben van een rechthoekige driehoek. We kunnen dan de andere twee zijdes berekenen met de goede goniometrische functie. Dit is erg handig, want met [Pythagoras](/pythagoras/) kunnen we dit niet doen. 

Er zijn drie soorten goniometrische functies die we vaak gebruiken. De **sinus**, de **cosinus** en de **tangens**. Welke functie we gebruiken is afhankelijk van wat we hebben en wat we willen berekenen. Hieronder zie je het verband tussen de functies en de zijdes van een rechthoekige driehoek.

???+ Belangrijk
    ### **Goniometrische Functies**
    $$\large{\sin(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Schuin}}}$$

    $$\large{\cos(\theta) = \frac{\mathrm{Aanliggend}}{\mathrm{Schuin}}}$$

    $$\large{\tan(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}}}$$

Dit kan je onthouden met het ezelsbruggetje: "SOS CAS TOA". Dit kun je als volgt begrijpen:

- SOS: <u>S</u>inus is <u>O</u>verstaand gedeeld door <u>S</u>chuin.
- CAS: <u>C</u>osinus is <u>A</u>anliggend gedeeld door <u>S</u>chuin.
- TOA: <u>T</u>angens is <u>O</u>verstaand gedeeld door <u>A</u>anliggend.

??? note "Overstaand, Aanliggend en Schuin"
    <span style="font-size: 14px;">*Overstaand*, *Aanliggend* en *Schuin* gaan over de verschillende zijdes van een rechthoekige driehoek. Dit is altijd bepaald ten opzichte van de hoek waar je naar kijkt. Dus in Figuur 1 kijken we ten opzichte van de hoek $\theta$. </span>
    
    <span style="font-size: 14px;">Vanuit deze hoek $\theta$ bepalen we welke de overstaande zijde is en welke de aanliggende. De schuine zijde is altijd hetzelfde voor een rechthoekige driehoek. Dus dan maakt het niet uit vanaf welke hoek je kijkt.</span>

    <figure>
        <img src="/assets/images/goniometrie/Right_Triangle_Sides.svg" 
            loading="lazy" 
            width="250" 
            alt="Rechthoekige driehoek">
    </figure>
    <center><span><i>Figuur 1. Een rechthoekige driehoek met de overstaande, aanliggende en schuine zijdes aangegeven.</i></span></center> <br><br>

    <span style="font-size: 14px;">De kenmerken van de verschillende soorten zijdes:</span>
    
    - <span style="font-size: 15px;">**Schuine zijde:** De zijde tegenover de hoek van $90 ^{\circ}$. Het is ook de langste zijde van de rechthoekige driehoek.</span>
    - <span style="font-size: 15px;">**Aanliggende zijde:** De andere zijde die samen met de schuine zijde de hoek $\theta$ maakt.</span>
    - <span style="font-size: 15px;">**Overstaande zijde:** De zijde tegenover de hoek $\theta$.</span>

****

### **Zijdes Bepalen**

Laten we naar een voorbeeld kijken. In Figuur 2 hieronder hebben we een rechthoekige driehoek gegeven gekregen. 

<figure>
    <img src="/assets/images/goniometrie/Right_Triangle_Gonio.svg" 
        loading="lazy" 
        width="300" 
        alt="Rechthoekige driehoek">
</figure>
<center><span><i>Figuur 2. Een rechthoekige driehoek met de hoek $\theta$ en de punten $A$, $B$ en $C$.</i></span></center> <br><br>

Stel we willen zijde $BC$ bepalen en we weten dat $\theta = 60 ^{\circ}$ en $AB = 2$. Hoe pakken we dit dan aan?

Zoals we eerder zagen, kunnen we dit probleem niet oplossen met [Pythagoras](/pythagoras/). Hiervoor hebben we de goniometrische funties nodig. Maar welke moeten we gebruiken, de sinus, cosinus of de tangens? 

We hebben de hoek $\theta$ en de zijde $AB$. Dit is de aanliggende zijde, want het maakt samen met de schuine zijde de hoek $\theta$. Verder willen we zijde $BC$ weten. Dit is de overstaande zijde, want het is de zijde tegenover hoek $\theta$.

We zoeken dus een functie die iets met een overstaande en aanliggende zijde heeft. We kunnen bij de [goniometrische functies](#goniometrische-functies) zien dat we dan de **tangens** moeten gebruiken. Deze functie heeft namelijk beide zijdes die we willen. Laten we als eerst de tangens opschrijven:

$$\tan(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}}$$

De overstaande zijde is dus $BC$ en de aanliggende is $AB$:

$$\tan{(\theta)} = \frac{BC}{AB}.$$

Nu kunnen we dit [omschrijven](/basisvaardigheden/#formules-omschrijven) om $BC$ vrij te maken:

$$BC = AB \cdot \tan{(\theta)}.$$

Laten we nu de gegevens invullen die we hebben:

$$BC = 2 \cdot \tan{(60 ^{\circ})}.$$

Als we dit in een rekenmachine stoppen, dan vinden we:

!!! quote ""
    $$\large{BC \approx 3.46}$$


We kunnen in Figuur 2 controleren dat dit antwoord best zou kunnen kloppen.

****

### **Hoeken Bepalen**
We kunnen de [goniometrische functies](#goniometrische-functies) ook gebruiken om een hoek te bepalen. We hebben daarvoor $2$ zijdes van de rechthoekige driehoek nodig. 

We gebruiken dan de inverse van de goniometrische functie. Dit noteren we dan met een *arc* of met een macht $-1$. 

???+ Belangrijk
    $$\large{\sin(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Schuin}} \iff \theta = \arcsin \! \left(\frac{\mathrm{Overstaand}}{\mathrm{Schuin}}\right)}$$

    $$\large{\cos(\theta) = \frac{\mathrm{Aanliggend}}{\mathrm{Schuin}} \iff \theta = \arccos \! \left(\frac{\mathrm{Aanliggend}}{\mathrm{Schuin}}\right)}$$

    $$\large{\tan(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}} \iff \theta = \arctan \! \left(\frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}}\right)}$$

??? note "Notatie van de inverse goniometrische functies"
    Op een rekenmachine worden de inverse functies aangegeven met een $^{-1}$. Dus:
    
    - $\large{\sin^{-1}(x)}$
    - $\large{\cos^{-1}(x)}$
    - $\large{\tan^{-1}(x).}$
    
    Maar we raden het af om het zo op te schrijven, omdat dit verwarring kan opleveren. Want
    
    $$\large{\sin^{-1}(x) \neq \frac{1}{\sin(x)}}$$
    
    De inverse betekent hier dus <u>**niet**</u> dat we $1$ gedeeld door de functie moeten doen. Maar bij $x^{-1}$ is dit juist wel het geval. Dit kan verwarrend zijn, dus om dit te vermijden schrijven wij de inverse van $\sin(x)$ als $\arcsin(x)$ op.

<br>

Laten we naar een voorbeeld kijken om te zien hoe dit werkt. In Figuur 3 hebben we een rechthoekige driehoek met zijdes $BC = 2$ en $AB = 2$. 

<figure>
    <img src="/assets/images/goniometrie/Right_Triangle_Angle.svg" 
        loading="lazy" 
        width="250" 
        alt="Rechthoekige driehoek met zijdes BC en AB">
</figure>
<center><span><i>Figuur 3. Een rechthoekige driehoek met zijdes $BC = 2$ en $AB = 2$.</i></span></center> <br> <br>

We willen nu de hoek $\theta$ bepalen. Om dit te doen, kijken we als eerst naar welke zijdes we hebben. 

We hebben de zijde $BC$ als overstaande zijde. Dit kunnen we herkennen aan het feit dat de zijde niet is verbonden met de hoek $\theta$. We hebben ook zijde $AB$ als aanliggende zijde. Dit weten we omdat het samen met de schuine zijde de hoek $\theta$ maakt. En $AB$ is niet de schuine zijde, want de schuine zijde is de zijde tegenover de $90 ^{\circ}$ hoek. 

We hebben dus de overstaande en de aanliggende zijde. Dit betekent dus dat we de **tangens** moeten gebruiken:

$$\tan(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}}$$

$$\tan(\theta) = \frac{BC}{AB}$$

Als we nu $BC = 2$ en $AB = 2$ invullen:

$$\tan(\theta) = \frac{2}{2}$$

$$\tan(\theta) = 1$$

Dus we weten dat de tangens van $\theta$ gelijk is aan $1$. We kunnen nu $\theta$ bepalen door de $\arctan$ te nemen:

$$\theta = \arctan(1)$$

Als we dit in onze rekenmachine stoppen (dus $\tan^{-1}(1)$), dan vinden we:

$$\theta = 45 ^{\circ}$$

En als we kijken in Figuur 3, dan kunnen we controleren dat dit een logisch antwoord is. Het ziet er namelijk ook uit als de helft van een rechte ($90 ^{\circ}$) hoek.

### **Voorbeelden**
??? example "Voorbeeld 1: Bereken zijde $BC$"
    **<p style="text-align: center;font-size:20px;">Bereken zijde $BC$ in de onderstaande rechthoekige driehoek.</p>**

    <figure>
        <img src="/assets/images/goniometrie/Right_Triangle_Ex1.svg" 
            loading="lazy" 
            width="300" 
            alt="Rechthoekige driehoek met hoek $\theta = 30^\circ$ en zijde AC">
    </figure>
    <center><span><i>Figuur 1. Een rechthoekige driehoek met een hoek $\theta = 30^{\circ}$ en een zijde $AC = 4$.</i></span></center> <br><br>

    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We hebben dus de hoek $\theta=30 ^{\circ}$ en een zijde $AC = 4$. Zijde $AC$ is de schuine zijde, want het is de zijde tegenover de hoek van $90 ^{\circ}$. We willen zijde $BC$ bepalen en dat is de overstaande zijde. $BC$ is namelijk de zijde tegenover $\theta$.

    Dus onze functie moet iets met een schuine zijde hebben en iets met een overstaande zijde. Als we bij de [goniometrische functies](#goniometrische-functies) kijken, dan zien we dat we de **sinus** moeten gebruiken. Laten we deze opschrijven:

    $$\large{\sin(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Schuin}}}$$

    We weten dus dat $AC$ de schuine zijde is en $BC$ de overstaande:

    $$\large{\sin(\theta) = \frac{BC}{AC}}$$

    We willen $BC$ bepalen, dus laten we die vrij maken. We moeten dus de formule gaan [omschrijven](/basisvaardigheden/#formules-omschrijven):

    $$\large{BC = AC \cdot \sin(\theta)}$$

    Als we nu $AC = 4$ en $\theta = 30 ^{\circ}$ invullen, krijgen we:

    $$\large{BC = 4 \cdot \sin(30 ^{\circ})}$$

    En als we dit in een rekenmachine stoppen, dan vinden we:

    !!! quote ""
        $$\large{BC = 2}$$

    En als we dit controleren in Figuur 1, dan kunnen we zien dat dit een logisch antwoord is.


??? example "Voorbeeld 2: Bepaal de hoek $\theta$"
    **<p style="text-align: center;font-size:20px;">Bepaal de hoek $\theta$ in de onderstaande rechthoekige driehoek.</p>**

    <figure>
        <img src="/assets/images/goniometrie/Right_Triangle_Ex2.svg" 
            loading="lazy" 
            width="300" 
            alt="Rechthoekige driehoek met zijdes AC = 4 en AB = 3">
    </figure>
    <center><span><i>Figuur 2. Een rechthoekige driehoek met zijdes $AC = 4$ en $AB = 3$.</i></span></center> <br><br>

    <br><br><br><br><br>


    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We moeten de hoek $\theta$ bepalen, dus laten we eerst kijken naar welke zijdes we hebben. Zijde $AC$ is de schuine zijde, want het is de zijde tegenover de rechte hoek. Dat betekent dat $AB$ de aanliggende zijde is, want samen met de schuine zijde $AC$ maken ze $\theta$. 

    Dus we hebben de schuine en aanliggende zijde. Dit betekent dat we de **cosinus** moeten gebruiken:

    $$\large{\cos(\theta) = \frac{\mathrm{Aanliggend}}{\mathrm{Schuin}}}$$

    We vullen dus $AB$ in als aanliggende zijde en $AC$ als schuine zijde:

    $$\large{\cos(\theta) = \frac{AB}{AC}}$$

    We weten dat $AB = 3$ en $AC = 4$:

    $$\large{\cos(\theta) = \frac{3}{4}}$$

    Om de hoek te bepalen, nemen we de $\arccos$:

    $$\large{\theta = \arccos(\frac{3}{4})}$$

    Als we dit invullen op onze rekenmachine (dus $\cos^{-1}(\frac{3}{4})$), dan vinden we:

    $$\large{\theta = 41.41... ^{\circ}}$$

    Graden ronden we af op $1$ decimaal, dus ons eindantwoord wordt dan:

    !!! quote ""
        $$\large{\theta \approx 41.4 ^{\circ}}$$

    En bij VMBO ronden we af op gehele getallen:
    
    !!! quote ""
        $$\large{\theta \approx 41 ^{\circ}}$$


??? example "Voorbeeld 3: Bepaal de hoek $\theta$ en zijde $AB$"
    **<p style="text-align: center;font-size:20px;">Bepaal de hoek $\theta$ in de onderstaande rechthoekige driehoek.</p>**

    <figure>
        <img src="/assets/images/goniometrie/Right_Triangle_Ex3.svg" 
            loading="lazy" 
            width="300" 
            alt="Rechthoekige driehoek met zijdes AC = 8 en BC = 6">
    </figure>
    <center><span><i>Figuur 3. Een rechthoekige driehoek met zijdes $AC = 8$ en $BC = 6$.</i></span></center> <br><br>


    <br><br><br><br><br>

    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We willen de hoek $\theta$ en de zijde $AB$ bepalen, dus laten we als eerst beginnen met $\theta$.

    We hebben de zijdes $BC$ en de zijdes $AC$ gegeven. Zijde $BC$ is de overstaande zijde, want het is de zijde tegenover de hoek $\theta$. 

    Om te bepalen welke zijde $AC$ is, moeten we goed opletten. De zijde tegenover de rechte hoek is de schuine zijde. In dit geval is dat zijde $AB$. Dit betekent dus dat zijde $AC$ de aanliggende zijde is, want samen met de schuine zijde maken ze $\theta$.

    We hebben dus de overstaande en de aanliggende zijde, dus moeten we de **tangens** gebruiken:

    $$\tan(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}}$$

    We weten dus dat de overstaande zijde $BC$ is en de aanliggende $AC$:

    $$\tan(\theta) = \frac{BC}{AC}$$

    Nu kunnen we $BC = 6$ en $AC = 8$ invullen:

    $$\tan(\theta) = \frac{6}{8} = \frac{3}{4}$$

    Om $\theta$ te bepalen, kunnen we de $\arctan$ nemen:

    $$\large{\theta = \arctan(\frac{3}{4})}$$

    Als we dit invullen in onze rekenmachine (dus $\tan^{-1}(\frac{3}{4})$), dan vinden we:

    $$\large{\theta = 36.869...}$$

    Graden ronden we af op $1$ decimaal, dus ons eindantwoord wordt:

    !!! quote ""
        $$\large{\theta = 36.9 ^{\circ}}$$

    En bij VMBO ronden we af op gehele getallen:

    !!! quote ""
        $$\large{\theta = 37 ^{\circ}}$$

    <br>

    Nu willen we zijde $AB$ bepalen. We kunnen dit op meerdere manieren doen. We kunnen dit berekenen met de **sinus**, met de **cosinus** of met [Pythagoras](/pythagoras/). Wij kiezen er hier voor om het met de **sinus** te berekenen. Maar voel je vrij om de andere methodes te proberen om te kijken of je het beheerst!

    Voor de sinus hebben we iets met de overstaande en de schuine zijde:

    $$\large{\sin(\theta) = \frac{\mathrm{Overstaand}}{\mathrm{Schuin}}}$$

    We hebben net gezien dat de overstaande zijde $BC$ is en $AB$ de schuine zijde:

    $$\large{\sin(\theta) = \frac{BC}{AB}}$$

    We moeten nu deze formule [omschrijven](/basisvaardigheden/#formules-omschrijven) om AB vrij te maken:

    $$\large{AB \cdot \sin(\theta) = BC}$$

    $$\large{AB = \frac{BC}{\sin(\theta)}}$$

    Nu vullen we $\theta = 36.869...$ en $BC = 6$ in:

    $$\large{AB = \frac{6}{\sin(36.869... ^{\circ})}}$$

    Zorg er dus voor dat je $\theta$ niet tussendoor afrond, want dan krijg je ook een (iets) ander antwoord. Als we dit invullen op onze rekenmachine, dan vinden we:

    !!! quote ""
        $$\large{AB = 10}$$

<hr style="height: 1.5px; background-color: #575757; border: none;">