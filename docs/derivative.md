# De Afgeleide Functie

Een afgeleide functie geeft op elk x coördinaat de bij behorende helling/richtingscoëfficient. Dit wordt in de onderstaande voorbeelden weergegeven.

## Voorbeelden
### Parabool
Een parabool heeft in het simpleste geval de vorm

$$f(x) = x^2.$$

De afgeleide van deze functie is gelijk aan 

$$f'(x) = 2x,$$ 

Waarbij $f'(x)$ aangeeft dat het gaat om de afgeleide van de functie $f(x)$ (zie de [Tabel met veel voorkomende functies](#tabel-met-veel-voorkomende-functies) sectie voor de toelichting van het antwoord van deze afgeleide).

In het onderstaande filmpje is er te zien dat de afgeleide gelijk is aan de helling op elk punt. Ook is er te zien dat bij een top geldt dat de helling (en dus de afgeleide) gelijk is aan $0$. Dit betekent dus dat als we het x coördinaat van een top willen bepalen, we moeten stellen dat

$$f'(x) = 0.$$


<video controls>
<source src="../videos/Parabola.mp4" type="video/mp4">
</video>

*<p style="text-align: center;">Visuele weergave van de afgeleide van de functie $f(x) = x^2$. Bij de top geldt dat de helling gelijk is aan 0. </p>*

### Exponentiele funtie 
Een exponentiele functie heeft de vorm

$f(x) = e^x$,

waar $e$ het getal van euler is. Er geldt dat $e = 2.7182818...$

<video controls>
<source src="../videos/Exponential.mp4" type="video/mp4">
</video>


## Tabel met veel voorkomende functies

| Functie                    | Afgeleide                        |
| -------------------------- | -------------------------------- |
| $\large{f(x) = x^n}$               | $\large{f'(x) = nx^{n-1}}$               |
| $\large{f(x) = e^x}$               | $\large{f'(x) = e^x}$                    |
| $\large{f(x) = a^x}$               | $\large{f'(x) = a^x \ * \ \ln{(x)}}$         |
| $\large{f(x) = \ln{(x)}}$          | $\large{f'(x) = \frac{1}{x}}$            |
| $\large{f(x) = \ ^a \! \log{(x)}}$ | $\large{f'(x) = \frac{1}{x \ * \ \ln{(a)}}}$ |
| $\large{f(x) = \sin{(x)}}$         | $\large{f'(x) = \cos{(x)}}$              |
| $\large{f(x) = \cos{(x)}}$         | $\large{f'(x) = -\sin{(x)}}$             |

waarbij $n$ en $a$ constantes zijn die niet afhankelijk van x zijn.

## Regels

|               | Functie                            | Afgeleide                                                                                             |
| ------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Somregel      | $\large{f(x) = g(x) + h(x)}$       | $\large{f'(x) = g'(x) + h'(x)}$                                                                       |
| Productregel  | $\large{f(x) = g(x) * h(x)}$       | $\large{f'(x) = g'(x) \  * \ h(x) + g(x) * h'(x)}$                                                    |
| Quotiëntregel | $\large{f(x) = \frac{g(x)}{h(x)}}$ | $\large{f'(x) = \frac{g'(x) \ * \ h(x) \ - \ g(x) \ * \ h'(x)}{h(x)^2}}$                              |
| Kettingregel  | $\large{f(x) = g(h(x))}$           | $\large{f'(x) = \frac{\mathrm{d} \ g(h)}{\mathrm{d} h} \ * \ \frac{\mathrm{d} \ h(x)}{\mathrm{d} x}}$ |

## Notatie
Een afgeleide kan op verschillende manieren worden weergegeven:

