import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Etapy procesu
stages = [
    "Planowanie", "Eksploracja", "Automatyzacja", "Obróbka",
    "Trenowanie", "Walidacja", "Konteneryzacja", "Publikacja i monitorowanie",
    "Doskonalenie modelu", "Prezentacja", "Retrospektywa"
]

# Customowa odległość między etapami
positions = [
    0,  # Planowanie
    2.5,  # Eksploracja
    5.0,  # Automatyzacja
    7.5,  # Obróbka
    10.0,  # Trenowanie
    12.5,  # Walidacja
    15.0,  # Konteneryzacja
    17.5,  # Publikacja i monitorowanie
    20.8,  # Doskonalenie modelu
    23.2,  # Prezentacja
    25.7  # Retrospektywa
]

# Wykres setup
fig, ax = plt.subplots(figsize=(35, 2))
ax.axis('off')

# Narysuj boxy i połączenia
for i, stage in enumerate(stages):
    # Dostosowywanie szerokości dla "Publikacja i monitorowanie"
    box_width = 2.6 if stage == "Publikacja i monitorowanie" else 1.8

    # Narysuj box
    box = patches.FancyBboxPatch((positions[i], 0.5), box_width, 0.3, boxstyle="round,pad=0.1", edgecolor="black",
                                 facecolor="#add8e6")
    ax.add_patch(box)
    ax.text(positions[i] + box_width / 2, 0.65, stage, ha="center", va="center", fontsize=9, weight="bold")

    # Narysuj linie połączeń
    if i < len(stages) - 1:
        next_line_start = positions[i] + box_width
        line_end = positions[i + 1]
        # Rysuj linię poziomą między boxami
        ax.plot([next_line_start, line_end], [0.65, 0.65], color="black", lw=1)

# Zapis wykresu
plt.savefig("workflow_diagram.png", bbox_inches="tight")