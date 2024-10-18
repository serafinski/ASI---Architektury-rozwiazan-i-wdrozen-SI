# Raport z Analizy Danych
### Ostatnia aktualizacja: Thu Oct 17 00:58:04 UTC 2024
## Przed Czyszczeniem Danych
### Histogram dla Score
![Histogram](histogram.png)
### Wykresy Punktowe
![Wykresy Punktowe](scatter_plots.png)
### Zmienne Kategoryczne
![Zmienne Kategoryczne](distribution.png)
## Po Czyszczeniu Danych
### Histogram dla Score
![Histogram Processed](histogram_processed.png)
### Wykresy Punktowe
![Wykresy Punktowe Processed](scatter_plots_processed.png)
### Zmienne Kategoryczne
![Zmienne Kategoryczne Processed](distribution_processed.png)
## Opis statystyczny danych numerycznych
| index | count | mean | std | min | 25% | 50% | 75% | max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| score | 4739.0 | 50.88902933684601 | 8.701909614072397 | 28.950000762939453 | 43.92499923706055 | 51.18999862670898 | 57.76999855041504 | 72.80999755859375 |
| unemp | 4739.0 | 7.597214581091511 | 2.763580873344847 | 1.399999976158142 | 5.900000095367432 | 7.099999904632568 | 8.899999618530273 | 24.899999618530277 |
| wage | 4739.0 | 9.500506478338005 | 1.3430670761078358 | 6.590000152587891 | 8.850000381469727 | 9.68000030517578 | 10.149999618530272 | 12.960000038146973 |
| distance | 4739.0 | 1.8028698056546362 | 2.297127839272774 | 0.0 | 0.4000000059604645 | 1.0 | 2.5 | 20.0 |
| tuition | 4739.0 | 0.8146082493518823 | 0.3395038198597169 | 0.2575100064277649 | 0.4849900007247925 | 0.8244799971580505 | 1.127020001411438 | 1.4041600227355957 |
| education | 4739.0 | 13.807765351339945 | 1.7891065138770221 | 12.0 | 12.0 | 13.0 | 16.0 | 18.0 |
## Opis zmiennych kategorycznych
| index | count | unique | top | freq |
| --- | --- | --- | --- | --- |
| gender | 4739 | 2 | female | 2600 |
| ethnicity | 4739 | 3 | other | 3050 |
| fcollege | 4739 | 2 | no | 3753 |
| mcollege | 4739 | 2 | no | 4088 |
| home | 4739 | 2 | yes | 3887 |
| urban | 4739 | 2 | no | 3635 |
| income | 4739 | 2 | low | 3374 |
| region | 4739 | 2 | other | 3796 |
## Dystrybucja zmiennych kategorycznych
Dystrybucja dla zmiennej gender:

| gender | count |
| --- | --- |
| female | 2600 |
| male | 2139 |

Dystrybucja dla zmiennej ethnicity:

| ethnicity | count |
| --- | --- |
| other | 3050 |
| hispanic | 903 |
| afam | 786 |

Dystrybucja dla zmiennej fcollege:

| fcollege | count |
| --- | --- |
| no | 3753 |
| yes | 986 |

Dystrybucja dla zmiennej mcollege:

| mcollege | count |
| --- | --- |
| no | 4088 |
| yes | 651 |

Dystrybucja dla zmiennej home:

| home | count |
| --- | --- |
| yes | 3887 |
| no | 852 |

Dystrybucja dla zmiennej urban:

| urban | count |
| --- | --- |
| no | 3635 |
| yes | 1104 |

Dystrybucja dla zmiennej income:

| income | count |
| --- | --- |
| low | 3374 |
| high | 1365 |

Dystrybucja dla zmiennej region:

| region | count |
| --- | --- |
| other | 3796 |
| west | 943 |

### Heatmap Korelacji
![Heatmap Korelacji](correlation_heatmap.png)
