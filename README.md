# Závislost přítomnosti poslanců na počasí

Projekt zkoumá vztah mezi přítomností poslanců na hlasováních poslanecké sněmovny a počasím v Praze.

## Získání dat

Pro získání dat o hlasováních byl vytvořen skript `psp_scrapper.py`. Ten projde stránky [poslanecké sněmovny](http://www.psp.cz/), najde všechna zasedání v aktuálním volebním období a uloží informace o jednotlivých hlasováních.

Do výstupního souboru `psp_data.csv` jsou pak zapsána následující data:

| Sloupec | Popis |
| --- | --- |
| Identifikace poslance | Jméno a příjmení poslance, kterého se řádek týká. |
| Způsob hlasování | Informace o tom, jak při tomto hlasování poslanec hlasoval. Sloupec může nabývat následjících hodnot: A = pro, N = proti, 0 = nepřihlášen, M = omluven, Z = zdržel se. |
| Číslo schůze | Číselný identifikátor schůze. |
| Číslo hlasování | Číselný identifikátor hlasování v rámci schůze. |
| Rok | Rok, ve kterém hlasování proběhlo. |
| Měsíc | Číselné označení měsíce, ve kterém hlasování proběhlo. |
| Den | Den, ve kterém hlasování proběhlo. |
| Hodina | Hodina uzavření hlasování. |
| Minuta | Minuta uzavření hlasování. |

*Datový soubor měl po stažení informací o prvních 29 schůzích velikost okolo 25 MB.*
