# Lab1

---

1. Skopiowac plik lokalnie i stworzyć swoje repozytorium z nazwą Lab-1_<twój-numer-studenta> i umieścić prywatne repozytorium w organizacji PJATK-ASI-2024
   
2. a) Zmień nazwę pliku `train.py` na `<twój-numer-studenta>.py`.  
   b) W skrypcie stwórz funkcję, która będzie generowała automatycznie dwa zbiory danych. Każdy zbiór ma być chmurą zbliżonych punktów, a zbiory powinny być na tyle odległe, aby można było gołym okiem określić ich położenie. Wielkość chmury powinna wynosić od 50 do 100 punktów.  
   c) Wykorzystując wygenerowane dane, stwórz model w skrypcie, który będzie w stanie przewidywać, do którego zbioru/chmury należy dany punkt.

3. Uzupełnij plik `requirements.txt`.

4. Uzupełnij plik `.github/workflows/ci.yml`, tak aby komenda:

   ```yaml
   run: cat accuracy.txt
   ```

   wyświetlała:
   ```
   Model trained with accuracy: <wynik-w-procentach>%
   ```

---
