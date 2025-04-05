## **Goniometrische Vergelijkingen**

Deze goniometrische vergelijkingen worden vaak gebruikt om wat lastigere vergelijkingen op te lossen.

???+ Belangrijk
    **<p style="font-size:19px;">Regels</p>**

    **<p style="font-size:16px;">Basis</p>**

    1. $$\large{\tan(\theta) = \dfrac{\sin(\theta)}{\cos(\theta)}}$$
    1. $$\large{\sin^2(\theta) + \cos^2(\theta) = 1}$$

    **<p style="font-size:16px;">Verdubbelingsformules</p>**

    1. $$\large{\sin(2 \theta) = 2 \sin(\theta) \cos(\theta)}$$
    1. $$\large{\cos(2 \theta) = 2 \cos^2(\theta) - 1}$$
    1. $$\large{\cos(2 \theta) = \cos^2(\theta) - \sin^2(\theta)}$$
    1. $$\large{\cos(2 \theta) = 1 - 2 \sin^2(\theta)}$$

    **<p style="font-size:16px;">Som- en Verschilformules</p>**

    1. $$\large{\sin(\theta + \phi) = \sin(\theta) \cos(\phi) + \cos(\theta) \sin(\phi)}$$
    1. $$\large{\sin(\theta - \phi) = \sin(\theta) \cos(\phi) - \cos(\theta) \sin(\phi)}$$
    1. $$\large{\cos(\theta + \phi) = \cos(\theta) \cos(\phi) - \sin(\theta) \sin(\phi)}$$
    1. $$\large{\cos(\theta - \phi) = \cos(\theta) \cos(\phi) + \sin(\theta) \sin(\phi)}$$

De eerste twee basisvergelijkingen moet je onthouden, maar de andere krijg je vaak gegeven bij toetsen (ook bij het eindexamen). 

We kunnen deze basisvergelijkingen ook zelf bewijzen met de [goniometrische functies](#goniometrische-functies) die we eerder hebben gezien.

??? abstract "Bewijs"
    **<p style="text-align: center;font-size:20px;">Bewijs eerste vergelijking</p>** 

    We kijken als eerst naar de eerste vergelijking: 

    $$\large{\tan(\theta) = \frac{\sin(\theta)}{\cos(\theta)}}$$

    Laten we proberen om de sinus en cosinus te herschrijven zodat we er een tangens uit krijgen. We kunnen dit doen door gebruik te maken van de formules bij de [goniometrische functies](#goniometrische-functies):

    $$\large{\frac{\sin(\theta)}{\cos(\theta)} = \frac{\frac{\mathrm{Overstaand}}{\mathrm{Schuin}}}{\frac{\mathrm{Aanliggend}}{\mathrm{Schuin}}}}$$

    Dit kunnen we weer versimpelen door de "$\mathrm{Schuin}$" in de teller en noemer tegen elkaar weg te delen. We houden dan over:

    $$\large{\frac{\sin(\theta)}{\cos(\theta)} = \frac{\mathrm{Overstaand}}{\mathrm{Aanliggend}}}$$

    Maar we hadden bij [Goniometrische Functies](#goniometrische-functies) gezien dat dit de definitie van een tangens was. Er geldt dus dat:

    !!! quote ""
        $$\large{\frac{\sin(\theta)}{\cos(\theta)} = \tan(\theta)}$$

    En dit is precies wat we moesten bewijzen.
    
    <br>
    **<p style="text-align: center;font-size:20px;">Bewijs tweede vergelijking</p>**

    Laten we nu naar de tweede vergelijking kijken:

    $$\large{\sin^2(\theta) + \cos^2(\theta) = 1}$$

    Laten we proberen om hier zelf op te komen door de sinus en cosinus te herschrijven. We doen dit weer door de formules bij de [goniometrische functies](#goniometrische-functies) te gebruiken:

    $$\large{\sin^2(\theta) + \cos^2(\theta) = \frac{\mathrm{Overstaand}^2}{\mathrm{Schuin}^2} + \frac{\mathrm{Aanliggend}^2}{\mathrm{Schuin}^2}}$$

    Omdat de noemers hetzelfde zijn kunnen we hier 1 breuk van maken (zie eventueel [Regels bij Breuken](/basisvaardigheden/#regels-bij-breuken)):

    $$\large{\sin^2(\theta) + \cos^2(\theta) = \frac{\mathrm{Overstaand}^2 + \mathrm{Aanliggend}^2}{\mathrm{Schuin}^2}}.$$

    Kunnen we dit nog verder versimpelen? Ja! Met de [Stelling van Pythagoras](/pythagoras/) weten we dat de twee rechthoekszijdes in het kwadraat gelijk zijn aan de schuine zijde in het kwadraat. Dus we kunnen de teller herschrijven op deze manier:

    $$\large{\sin^2(\theta) + \cos^2(\theta) = \frac{\mathrm{Schuin}^2}{\mathrm{Schuin}^2}}$$
    
    En omdat iets gedeeld door zichzelf altijd gelijk is aan 1, vinden we dus dat:
    
    !!! quote ""
        $$\large{\sin^2(\theta) + \cos^2(\theta) = 1}$$
    
    en dit is precies wat we moesten bewijzen.

### **Voorbeelden**

??? example "Voorbeeld 1: $\sin^2(x)  = - \cos^2(x) + \tan(x)$"
    **<p style="text-align: center;font-size:20px;">Bereken x: $\sin^2(x)  = - \cos^2(x) + \tan(x)$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We beginnen eerst met aan beide kanten $+\cos^2(x)$ te doen, zodat deze term naar de linkerkant komt:

    $$\large{\sin^2(x) + \cos^2(x) = \tan(x)}$$

    We kunnen nu de [tweede basisvergelijking](#goniometrische-vergelijkingen) gebruiken:

    $$\large{\tan(x) = 1}$$

    Als we nu de [eerste basisvergelijking](#goniometrische-vergelijkingen) gebruiken, dan kunnen we dit schrijven als:

    $$\large{\frac{\sin(x)}{\cos(x)} = 1}$$

    Nu kunnen we beide kanten vermenigvuldigen met $\cos(x)$:

    $$\large{\sin(x) = \cos(x)}$$

    We willen nu óf aan beide kanten een cosinus hebben óf aan beide kanten een sinus. We kiezen er hier voor om de cosinus [om te schrijven](#sinus-en-cosinus-omschrijven) naar een sinus:

    $$\large{\sin(x) = \sin(x + \frac{1}{2} \pi)}$$

    Dit kunnen we nu oplossen met de [algemene oplossing](#algemene-oplossing):

    $$\large{x = x + \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ x = \pi - (x + \frac{1}{2} \pi) + k \cdot 2 \pi}$$

    $$\large{x = x + \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ x = \frac{1}{2} \pi - x + k \cdot 2 \pi}$$

    Nu halen we alle termen met $x$ naar de linkerkant:

    $$\large{0 = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 2x = \frac{1}{2} \pi + k \cdot 2 \pi}$$

    Alle termen met $x$ zijn in de linker vergelijking weggevallen, dus daar hebben we niks meer aan. Met de rechter vergelijking kunnen we wel nog door. We delen dan aan beide kanten alles door $2$ om te vinden:

    !!! quote ""
        $$\large{x = \frac{1}{4} \pi + k \cdot \pi}$$


??? example "Voorbeeld 2: $\frac{1}{2} \sin(x) \cos(x) = \frac{1}{4}$"
    **<p style="text-align: center;font-size:20px;">Bereken x: $\frac{1}{2} \sin(x) \cos(x) = \frac{1}{4}$</p>**
    **<p style="text-align: center;font-size:20px;">Uitwerking</p>**

    We zien hier een $\sin(x) \cos(x)$ term, dus is het handig om dit te herschrijven met behulp van de [Verdubbelingsformules](#goniometrische-vergelijkingen). We doen dan aan beide kanten keer $4$ om links $2 \sin(x) \cos(x)$ te krijgen:

    $$\large{2 \sin(x) \cos(x) = 1}$$

    Nu kunnen we dus de [verdubbelingsformule](#goniometrische-vergelijkingen) gebruiken:

    $$\large{\sin(2x) = 1}$$

    Nu willen we aan beide kanten een sinus hebben om dit te kunnen oplossen. We moeten dus kijken welke hoek $1$ geeft als we de sinus nemen. We kunnen de [eenheidscirkel](#de-eenheidscirkel) gebruiken of de $\arcsin$ nemen van $1$. We vinden dan dat $1 = \sin(\frac{1}{2} \pi)$ en dit kunnen we dus gaan invullen:

    $$\large{\sin{(2x)} = \sin{(\frac{1}{2} \pi)}}$$

    Als we dit nu [uitwerken](#algemene-oplossing), dan vinden we:

    $$\large{2x = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 2x = \pi - \frac{1}{2} \pi + k \cdot 2 \pi}$$

    $$\large{2x = \frac{1}{2} \pi + k \cdot 2 \pi \ \vee \ 2x = \frac{1}{2} \pi + k \cdot 2 \pi}$$

    In dit geval zijn dus beide oplossingen hetzelfde. We houden dus alleen over:

    $$\large{2x = \frac{1}{2} \pi + k \cdot 2 \pi}$$

    Nu delen we beide kanten door $2$ om te vinden dat:

    !!! quote ""
        $$\large{x = \frac{1}{4} \pi + k \cdot \pi}$$
