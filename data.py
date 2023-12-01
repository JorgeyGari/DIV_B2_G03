import pandas as pd

df = pd.read_json('data.json')

# He tenido que borrar manualmente a Kanye West, a SZA y a Lana del Rey. Podemos considerar volver a añadirlos
# De hecho, me da que algo raro pasó allí en el primer proyecto...

"""
# Información General
print(df.info())

# Conciertos de cada artista
print(df.loc["Concerts"])

# Conciertos de Taylor Swift
print(df.loc["Concerts"]["Taylor Swift"])
"""
# Nombres y precios de conciertos de Taylor Swift
for concert in df.loc["Concerts"]["Taylor Swift"]:
    print(concert["Concert Name"], end=" --> ") 
    print(concert["Ticketmaster Cheapest Price"], end=" ")
    print(concert["Currency"])
