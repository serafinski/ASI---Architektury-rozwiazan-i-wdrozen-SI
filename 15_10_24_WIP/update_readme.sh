#!/bin/bash

{
  echo "# Raport z Analizy Danych"
  echo "### Ostatnia aktualizacja: $(date)"

  echo "## Przed Czyszczeniem Danych"

  echo "### Opis statystyczny danych numerycznych"
  cat pre_numeric_analysis.txt

  echo "### Opis zmiennych kategorycznych"
  cat pre_categorical_analysis.txt

  echo "### Dystrybucja zmiennych kategorycznych"
  cat pre_categorical_distribution.txt

  echo "### Histogram dla Score"
  echo "![Histogram](histogram.png)"
  echo "### Wykresy Punktowe"
  echo "![Wykresy Punktowe](scatter_plots.png)"
  echo "### Zmienne Kategoryczne"
  echo "![Zmienne Kategoryczne](distribution.png)"

  echo "## Po Czyszczeniu Danych"

  echo "### Opis statystyczny danych numerycznych"
  cat post_numeric_analysis.txt

  echo "### Opis zmiennych kategorycznych"
  cat post_categorical_analysis.txt

  echo "### Dystrybucja zmiennych kategorycznych"
  cat post_categorical_distribution.txt

  echo "### Histogram dla Score"
  echo "![Histogram Processed](histogram_processed.png)"
  echo "### Wykresy Punktowe"
  echo "![Wykresy Punktowe Processed](scatter_plots_processed.png)"
  echo "### Zmienne Kategoryczne"
  echo "![Zmienne Kategoryczne Processed](distribution_processed.png)"

  echo "## Heatmap'a Korelacji"
  echo "![Heatmapa Korelacji](correlation_heatmap.png)"
} > README.md
