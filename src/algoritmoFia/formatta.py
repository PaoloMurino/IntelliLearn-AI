import pandas as pd

"""CODICE UTILIZZATO PER FORMATTARE IL DATASET DI PUNTI IN 2 COLONNE: LATITUDINE, LONGITUDINE"""

# Carica il file CSV
file_csv = 'nomeEsempio.csv'  # Sostituisci con il tuo percorso del file CSV
df_csv = pd.read_csv(file_csv)

# Estrai colonne di latitudine e longitudine
wkt_colonna = 'WKT'  # Colonna contenente le coordinate nel formato WKT

# Estrai le coordinate dalla colonna WKT
df_csv[['Longitudine', 'Latitudine']] = df_csv[wkt_colonna].str.extract(r'POINT \(([^ ]+) ([^)]+)\)', expand=True)

# Crea un nuovo DataFrame solo con le colonne di latitudine e longitudine
df_result = df_csv[['Latitudine', 'Longitudine']].astype(float)

# Salvare il DataFrame in un file CSV
df_result.to_csv('coordinate.csv', index=False)

print("File CSV creato con successo.")
