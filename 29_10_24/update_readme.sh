#!/bin/bash

{
  echo "# Przewidywanie skuteczności kampanii marketingowej banku"
  echo "### Ostatnia aktualizacja: $(date)"

  echo "## Plan projektu"

  echo "### Opis tematu i problemu biznesowego/technicznego"
  echo "Projekt dotyczy przewidywania skuteczności kampanii telemarketingowych prowadzonych przez bank, których celem jest nakłonienie klientów do wykupienia lokat terminowych."
  echo ""
  echo "W bankowości skuteczność kampanii marketingowych ma kluczowe znaczenie dla zwiększenia zysków i zminimalizowania kosztów związanych z kontaktowaniem się z niechętnymi klientami."
  echo ""
  echo "Dlatego zrozumienie, które cechy klientów oraz wskaźniki społeczno-ekonomiczne zwiększają szansę na sprzedaż lokaty, pozwala bankom optymalizować działania marketingowe, skutecznie zarządzać zasobami i w efekcie osiągać lepsze wyniki finansowe."

  echo "### Źródło danych, ich charakterystyka i uzasadnienie wyboru zbioru danych"
  echo "Dane pochodzą z publicznie dostępnego zestawu Bank Marketing opublikowanego w 2014 roku przez Sérgio Moro, Paulo Cortez i Paulo Ritę dostępnego na [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing)."
  echo ""
  echo "Dane zawierają informacje z okresu od maja 2008 do listopada 2010 roku o klientach banku.
  Zostały one wzbogacone o pięć wskaźników społeczno-ekonomicznych na poziomie narodowym (m.in. kwartalna stopa zatrudnienia, miesięczny wskaźnik cen konsumpcyjnych, euribor), publikowanych przez Banco de Portugal.
  Zbiór zawiera 41 188 rekordów oraz 21 atrybutów dotyczących klientów banku, atrybutów kampanii telemarketingowej oraz danych makroekonomicznych, dzięki czemu analitycy mogą zrozumieć wpływ zarówno danych demograficznych, jak i kontekstu ekonomicznego na decyzje klientów."
  echo ""
  echo "Zbiór ten jest idealny do zastosowań związanych z modelowaniem predykcyjnym, gdyż zawiera wiele zróżnicowanych zmiennych wpływających na wyniki kampanii."

  echo "### Cele projektu"
  echo "Głównym celem projektu jest stworzenie modelu predykcyjnego, który prognozuje, czy dany klient zdecyduje się na zakup lokaty terminowej."

  echo "### Diagram przepływu"
  echo "![Diagram przepływu](workflow_diagram.png)"
} > README.md