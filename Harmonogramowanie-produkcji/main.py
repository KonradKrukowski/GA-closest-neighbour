import pandas as pd
import random

# data
# adres pliku zrodlowego powinien byc zmieniony w zaleznosci od jego lokalizacji
source = r'C:\Users\Konrad\PycharmProjects\Harmonogramowanie-produkcji\data.csv'
data_source = pd.read_csv(source, sep=';', index_col=0)

list_p = []

i = 0
while i < len(data_source):
    list_p.append(pd.Series.tolist(data_source.iloc[i]))
    i += 1

wariancje = []
first_solution = list(range(1, len(list_p)+1))
random.shuffle(first_solution) # works in place
print("Wylosowane rozwiązanie pierwsze:" + str(first_solution))
actual_solution = first_solution

# Obliczanie wartosci funkcji celu


def oblicz_wartosc_f_celu(solution):
    data = {}
    for index, element in enumerate(solution):
        data[index+1] = list_p[element-1]

    Pji = pd.DataFrame(data)

    i = 0
    for index, element in enumerate(Pji.iloc[0]):
        i += element
        Pji.iloc[0][index] = i

    for index, element in enumerate(Pji.iloc[1]):
        if index == 0:
            Pji.iloc[1, 0] = element + Pji.iloc[0, 0]
        else:
            Pji.iloc[1, index] = element + max(Pji.iloc[1, index-1], Pji.iloc[0, index])

    wartosc_f_celu = max(Pji.iloc[1])
    return wartosc_f_celu


# Tworzenie kombinacji sasiednich
def znajdz_najblizszych_sasiadow(solution):
    for index1, i in enumerate(solution):
        for index2, j in enumerate(solution):
            mock_list = solution.copy()
            if i != j:
                mock_list[index1], mock_list[index2] = mock_list[index2], mock_list[index1]
                if mock_list not in wariancje:
                    wariancje.append(mock_list)
    return wariancje


print("Wartość funkcji celu dla rozwiązania początkowego: " + str(oblicz_wartosc_f_celu(first_solution)))
iteracja = 1
while iteracja < 5:
    print("Iteracja nr " + str(iteracja))
    rozwiazania_sasiednie = znajdz_najblizszych_sasiadow(actual_solution)
    rozwiazania_sasiednie_fcelu = []
    for index, element in enumerate(rozwiazania_sasiednie):
        print(str(rozwiazania_sasiednie[index]) + " " + str(oblicz_wartosc_f_celu(element)))
        rozwiazania_sasiednie_fcelu.append(oblicz_wartosc_f_celu(element))

    najlepszy_sasiad_fcelu = min(rozwiazania_sasiednie_fcelu)
    if najlepszy_sasiad_fcelu <= oblicz_wartosc_f_celu(actual_solution):
        for index, element in enumerate(rozwiazania_sasiednie):
            if oblicz_wartosc_f_celu(element) == najlepszy_sasiad_fcelu:
                actual_solution = rozwiazania_sasiednie[index]
                break
        print("Nowa optymalna kolejność: " + str(rozwiazania_sasiednie[index]))
        print("wartosc f celu dla nowej kolejnosci: " + str(oblicz_wartosc_f_celu(actual_solution)))
        rozwiazania_sasiednie.clear()
        rozwiazania_sasiednie_fcelu.clear()
        znajdz_najblizszych_sasiadow(actual_solution)
    else:
        print("Brak lepszego rozwiązania")
        print("Rozwiązanie ostateczne: " + str(actual_solution))
        break
    iteracja += 1
