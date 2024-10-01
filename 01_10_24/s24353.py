import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Generowanie prostego zbioru danych
def generate_data():
    # Ustalenie losowej liczby punktów w każdej chmurze (od 50 do 100)
    num_points_1 = np.random.randint(50, 101)
    num_points_2 = np.random.randint(50, 101)

    # Generowanie chmury punktów 1 w okolicach (10, 10)
    cluster_1 = np.random.normal(loc=[10, 10], scale=1.5, size=(num_points_1, 2))

    # Generowanie chmury punktów 2 w okolicach (50, 50)
    cluster_2 = np.random.normal(loc=[50, 50], scale=1.5, size=(num_points_2, 2))

    # Tworzenie etykiet: 0 dla cluster_1, 1 dla cluster_2
    labels_1 = np.zeros(num_points_1)
    labels_2 = np.ones(num_points_2)

    # Łączenie danych i etykiet
    X = np.vstack((cluster_1, cluster_2))
    y = np.concatenate((labels_1, labels_2))

    return X, y

# Trenowanie prostego modelu regresji logistycznej
def train_model():
    # Generowanie danych
    X, y = generate_data()

    # Podział na zbiór treningowy i testowy (80% treningowy, 20% testowy)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Trenowanie modelu regresji logistycznej
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predykcja na zbiorze testowym
    y_pred = model.predict(X_test)

    # Wyliczenie dokładności
    accuracy = accuracy_score(y_test, y_pred)

    # Zapis wyniku do pliku
    with open("accuracy.txt", "w") as f:
        f.write(f"Model trained with accuracy: {accuracy * 100:.2f}%\n")

    # Wyświetlenie dokładności
    print(f"Model trained with accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    train_model()
