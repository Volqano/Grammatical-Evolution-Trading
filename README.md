# Projekt na algorytmy ewolucyjne

### Problem: ewolucja reguł decyzyjnych dla inwestycji finansowych za pomocą grammatical evolution

### 1. Opis rozpatrywanego zagadnienia:

- Korzystając z algorytmu ewolucyjnego - Grammatical Evolution, chcemy generować reguły decyzyjne analizujące różne czynniki (ceny zamknięcia, RSI, średnie itp.), które mówią kiedy najbardziej opłaca się kupić/sprzedać akcje. 

### 2. Definicja rozważanego problemu optymalizacji

- **Przestrzeń przeszukiwań** - Jest zdefiniowana przez gramatykę bezkontekstową (`grammar.py`). Każdy punkt w tej przestrzeni to poprawna składniowo reguła logiczna. Rozmiar przestrzeni przeszukiwań rośnie wykładniczo, dlatego w algorytmie ustalamy maksymalną głębokość takiego drzewa.
- **Funkcja celu** - Jako funkcje celu początkowo przyjąłem maksymalizację całkowitego zwrotu, podejście to ma jednak pewien problem, bardzo overfittuje do danych treningowych szukając największych skoków w cenie. Dlatego wprowadziłem też dodatkową funkcje celu opartą na wskaźniku Sharpe'a. Ocenia on czy efektywność inwestycji wynika z faktycznie dobrych decyzji czy większego ryzyka. Wzór z jakiego korzystam to:
$$Sharpe_{annual} = \sqrt{252} \cdot \frac{\overline{R}_{daily}}{\sigma_{daily}}$$

* $\overline{R}_{daily}$ - Średnia dzienna stopa zwrotu

* $\sigma_{daily}$ - Odchylenie standardowe dziennych zwrotów

* rok giełdowy składa się średnio z 252 dni, aby znormalizować wzkaźnik sharpe'a mnożymy dodatkowo właśnie przez pierwiastek z tego

### 3. Opis użytych algorytmów ewolucyjnych 
Algorytm działa na podstawie SGA z dodatkową funkcja zamiany genotypu na fenotyp
- **Reprezentacja** - Genotypem jest tablica liczb całkowitych. Algorytm w celu zamiany genotypu na fenotyp dokonuje wyboru reguły w gramatyce poprzez operacje modulo. Fenotypem jest wygenerowana strategia składająca się z reguł gramatyki.
- **Operatory genetyczne**: 
    -  Selekcja - Wykorzystuje selekcje turniejową, jest szybka, odporna na różny fitness i zachowuje dobrą różnorodność populacji
    - Crossover - Wykorzystuje One-point crossover, zachowuje ona spójne bloki w genotypie, w tym problemie spójne bloki lączą się w sensowne fragmenty reguły
    - Mutacja - Wykorzystuje losową mutacje

### 4. Szegółowy opis implementacji użytych metod
- **Wektoryzowany backtesting** - zamiast liczyć zwroty w kolejne dni, obliczamy je dla całego szeregu jednocześnie używając numpy
- **SGA** - jako baza, klasyczna implementacja z wykładu wzbogacona o mapowanie genotypu na reguły (fenotyp), które potem ewaluujemy
- **Mapowanie genotypu na fenotyp** - startujemy od symbolu startowego `<start>`, w każdym kroku pobieramy kolejny gen z genotypu i dzięki niemu wybieramy odpowiednią regułę. Gdy przejdziemy przez wszystkie geny genotypu, stosujemy tzw. wrapping - wracamy na początek genotypu, co pozwala na wielokrotne korzystanie z tego samego genu.
- **Reprezentacja reguł** - reguły są reprezentowane jako drzewo (korzystamy ze słownika pythonowego), gdzie węzły to operatory logiczne, a liście to jakieś stałe liczbowe czy wskaźniki rynkowe.

### 5. Szegółowy opis uzyskanych wyników
Prowadziłem eskperymenty na danych finansowch z `yfinance` na zróżnicowanym zestawie spółek giełdowych. Aby przetestować faktyczne działanie reguł utworzonych przez algorytm podzieliłem dane na okres treningowy oraz testowy (ok. 80%/20%). Reguły zrobione przez algorytm porównywałem z prostą strategią Buy and Hold (kupujemy na początku, sprzedajemy na samym końcu)
- Zacząłem od przestestowania algorytmu z funkcją przystosowania ustawioną na maksymalizację zysku. Na zbiorze treningowym algorytm osiągał bardzo dobre wyniki, przewyższając B&H, ale na zbiorze testowym skuteczność bardzo spadała. Oznacza to mocny overfitting do danych treningowych, przez to, że algorytm maksymalizuje sam zysk, dostosowuje algorytm tak by kupił akcje w przed największymi górkami na treningu, szansa, że taka górka będzie też w danych testowych jest całkiem mała.
- Skoro sama maksymalizacja zysku prowadzi do overfittingu, spróbujmy jednocześnie zmniejszyć wariancje, algorytm będzie szukał bardziej stabilnych zarobków. Dlatego tutaj algorytm testowałem na nowej funkcji celu, opierającej się o wskaźnik Sharpe'a, który jednocześnie maksymalizuje zysk oraz minimalizuje wariancję. Tutaj także początkowa wersja wskazywała na overfitting, dlatego pobawiłem się trochę parametrami algorytmu. Dobrym sposobem na zmniejszenie overfittingu okazała się zmiana maksymalnej głębokości reguł na mniejszą, przy max_depth = 4 i funkcji straty wykorzystującej wskaźnik Sharpe'a algorytm osiągał najlepsze wyniki, zarabiał troszkę mniej od Buy and Hold na akcjach w hossie, ale gdy akcje miały gorszy okres buy and hold tracił dużo więcej od mojego algorytmu. 

### 6. Wnioski końcowe
- Użycie GE do ewolucji reguł decyzyjnych dla inwestycji finansowych jest ciekawym pomysłem, algorytm potrafił osiągnąć lekki ale stabilny zysk dla większości akcji, a przy tych źle posperujących, tracił bardzo mało.
- Dostosowanie odpowiedniej funkcji straty jest kluczowe dla tego problemu, sama maksymalizacja zysku prowadzi do mocnego overfittingu, warto pobawić się dodatkowo wariancją
- Prostsze reguły decyzyjne (o mniejszej głębokości) prowadzą do zmniejszenia overfittingu i lepszej generalizacji na nowe dane

### 7. Perspektywy rozwoju
- Rozbudowa gramatyki o nowe zmienne
- Pomyśleć o innych funkcjach strat jakich można użyć
- Optymalizacja wielokryterialna - użycie np. NSGA-2 do znalezienia frontu pareto z maksymalnymi zyskami i minimalnym ryzykiem