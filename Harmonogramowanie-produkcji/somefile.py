import pandas as pd

source = r'C:\Users\Konrad\PycharmProjects\Harmonogramowanie_najblizszy_sasiad\data.csv'
data_source = pd.read_csv(source, sep=';', index_col=0)

list_p = []

i = 0
while i < len(data_source):
    list_p.append(pd.Series.tolist(data_source.iloc[i]))
    i += 1

print(list_p)
