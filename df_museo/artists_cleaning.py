import pandas as pd
from geopy.geocoders import Nominatim

df = pd.read_csv('dataset/artists.csv', dtype={'Birth Year': 'Int64', 'Death Year': 'Int64'})

# inizializzare il geolocalizzatore
geolocator = Nominatim(user_agent="my_geocoder")

# funzione per il geocoding che avevo utilizzato nel progetto books
def geocode_country(country):
    try:
        print(f"Inizio geocoding per il paese: {country}")
        location = geolocator.geocode(country, timeout=60, language='en')
        if location:
            country_name = location.raw['display_name'].split(",")[-1].strip()
            print(f"Geocoding completato per il paese: {country_name}")
            return country_name
        else:
            print(f"Nessuna posizione trovata per il paese: {country}")
            return None
    except Exception as e:
        print(f"Errore durante il geocoding per il paese {country}: {e}")
        return None

# funzione per creare la colonna nationality1 usando la col nationality
def crea_nuova_colonna_naz(row):
    if pd.isnull(row['Nationality']):
        l = row['Name'].split(',')
        if len(l) > 1:
            return l[-1].strip()
    return row['Nationality']

# applico la funzione e creo la col nationality1
df['Nationality1'] = df.apply(crea_nuova_colonna_naz, axis=1)

# creo la mappatura per alcuni dei problemi che geopy non riesce a risolvere
# in maniera corretta (se ne trovate altri meglio)
country_map = {
    "Inc.": None,
    "Ltd.": None,
    "Ltd)": None,
    "LLC": None,
    "PLLC": None,
    "est.": None,
    "West Germany (now Germany)": "Germany",
    "CA": "Canada",
    "MA": "United States",
    "MN": "United States",
    "Moscow-Kherson": "Russia",
    "UK": "United Kingdom",
    "PA": "United States",
    "company design": None,
    "commercially printed": None,
    "Organizing Committee of the XIX Olympiad": None,
    "Bergen Street Sign Shop": None,
    "Czechoslovakia": "Czech Republic",
    "Yugoslavia": "Slovenia",
    "Yugoslavia (now Slovenia)":"Slovenia",
    "CT": "United States"
}

# applico la funzione di geocoding solo alle righe
# in cui ho nationality null e  nationality1 not null
df_to_geocode = df[pd.isnull(df['Nationality']) & df['Nationality1'].notnull()]

# creo un'altra funzione che applica la funzione geocode_country
# solo nel caso in cui il nome del paese non è nella country map
def validate_and_map_country(name):
    if name in country_map:
        return country_map[name]
    else:
        return geocode_country(name)

df_to_geocode['Country'] = df_to_geocode['Nationality1'].apply(validate_and_map_country)

# creo mappatura da country a nazionalità
country_to_nationality = {
    "Germany": "German",
    "France": "French",
    "United States": "American",
    "Finland": "Finnish",
    "Italy": "Italian",
    "Austria": "Austrian",
    "Denmark": "Danish",
    "Sweden": "Swedish",
    "Moldova": "Moldovan",
    "Japan": "Japanese",
    "Canada": "Canadian",
    "Netherlands": "Dutch",
    "Egypt": "Egyptian",
    "Montenegro": "Montenegrin",
    "United Kingdom": "British",
    "Israel": "Israeli",
    "Czechia": "Czech",
    "Switzerland": "Swiss",
    "India": "Indian",
    "Spain": "Spanish",
    "Serbia": "Serbian",
    "Libya": "Libyan",
    "Vatican City": "Vatican",
    "Brazil": "Brazilian",
    "Taiwan": "Taiwanese",
    "Belgium": "Belgian",
    "Australia": "Australian",
    "Latvia": "Latvian",
    "Thailand": "Thai",
    "Greece": "Greek",
    "Morocco": "Moroccan",
    "Russia": "Russian",
    "South Korea": "South Korean",
    "Argentina": "Argentinian",
    "Norway": "Norwegian",
    "South Africa": "South African",
    "Botswana": "Botswanan",
    "Gabon": "Gabonese",
    "Mexico": "Mexican",
    "Chile": "Chilean",
    "Croatia": "Croatian",
    "Czech Republic": "Czech"
}

# mappo i risultati del geocoding con la nazionalità corrispondente
df_to_geocode['Nationality_Final'] = df_to_geocode['Country'].map(country_to_nationality)

# unisco i risultati con il df originale
df.loc[df_to_geocode.index, 'Country'] = df_to_geocode['Country']
df.loc[df_to_geocode.index, 'Nationality'] = df_to_geocode['Nationality_Final']

# rimuovo le colonne 'Nationality1' e 'Country'
df.drop(columns=['Nationality1', 'Country'], inplace=True)

#manca la parte per sistemare/lasciare solo il primo nome nella colonna Name
df.to_csv('dataset/artists_cleaned.csv', index=False)