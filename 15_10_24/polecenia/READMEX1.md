### Zadanie X1: Przewidywanie Przedziału Wyników na Podstawie Poziomu Edukacji

**Cel**: Zbudowanie modelu, który przewiduje przedział wyników (score) dla danego poziomu edukacji na podstawie dostępnych danych demograficznych, społecznych i ekonomicznych.

#### Opis Danych
Dane zawierają informacje o różnych osobach z poniższymi kolumnami:
- **rownames** - identyfikator rekordu
- **gender** - płeć
- **ethnicity** - pochodzenie etniczne
- **score** - wynik
- **fcollege** - czy ojciec uczęszczał na studia (0 lub 1)
- **mcollege** - czy matka uczęszczała na studia (0 lub 1)
- **home** - miejsce zamieszkania (np. własny dom, wynajem)
- **urban** - typ miejsca zamieszkania (miasto, wieś)
- **unemp** - wskaźnik bezrobocia
- **wage** - zarobki
- **distance** - odległość od miejsca zamieszkania do miejsca edukacji
- **tuition** - czesne
- **education** - poziom edukacji
- **income** - dochód gospodarstwa domowego
- **region** - region zamieszkania

#### Etap 1: Eksploracja Danych i Przygotowanie
1. **Analiza korelacji** - Zidentyfikuj korelacje między kolumną `score` a innymi kolumnami, ze szczególnym uwzględnieniem kolumny `education`.
   - Wartość korelacji między `score` i `education` wynosi <0.5, co sugeruje, że istnieje umiarkowana zależność między nimi.
  
2. **Grupowanie Wyników (`score`) według Poziomu Edukacji (`education`)**:
   - Podziel zmienną `score` na przedziały odpowiadające poziomom `education`. Na przykład: niski, średni i wysoki poziom wyników.
   - Ustal granice przedziałów tak, aby każda grupa odpowiadała poziomowi edukacji w sposób sensowny statystycznie i przydatny dla modelu.

#### Etap 2: Modelowanie
1. **Zadanie Modelu** - Celem jest przewidywanie przedziału wyników (`score`) na podstawie dostępnych cech (m.in. `gender`, `ethnicity`, `unemp`, `wage`, `income`, `region`).
2. **Wybór Modelu** - Zastosuj wybrany algorytm klasyfikacji, np. drzewa decyzyjne, Random Forest lub model logistyczny.
3. **Ewaluacja Modelu** - Oceń model przy użyciu miar takich jak dokładność (accuracy), macierz pomyłek (confusion matrix) i AUC, jeśli używasz modeli probabilistycznych.

#### Etap 3: Analiza i Wnioski
1. **Analiza Wpływu Zmiennych** - Przeanalizuj, które cechy miały największy wpływ na przewidywanie przedziałów wyników.
2. **Interpretacja** - Na podstawie wyników modelu przedstaw wnioski dotyczące zależności między poziomem edukacji a wynikiem oraz innymi zmiennymi.
3. **Optymalizacja Modelu** - Jeśli czas pozwoli, spróbuj dostroić hiperparametry modelu, aby poprawić jego skuteczność.

---

### Dodatkowe Pytania do Rozważenia dla Studentów:
- Jakie cechy mają największy wpływ na przewidywanie przedziału wyniku w odniesieniu do poziomu edukacji?
- Czy istnieją inne cechy, które mogłyby poprawić przewidywania modelu?
- Jakie wnioski można wyciągnąć o zależności między poziomem edukacji a wynikiem na podstawie modelu?
