import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify

geolocator = Nominatim(user_agent="myuse")

app = Flask(__name__)

df = pd.read_json('suppliers_data.json')

df['City'] = df['City'].str.lower()

df.loc[3,'City']='alger'

# Select rows where t:he Category column equals a specific value, for example 'SomeCategory'
def wilaya(selected_wilaya):
    return df[df['City'].str.strip() == selected_wilaya]



random_values=set(df['Activities/Services'].values)
random_values = [i for i in  random_values if i !=None ]

df['Activities/Services'].fillna(pd.Series(np.random.choice(random_values, size=len(df.index))), inplace=True)

wilayas_of_algeria= [
    "adrar", "chlef", "laghouat", "oum el bouaghi", "batna", "bejaia",
    "biskra", "bechar", "blida", "bouira", "tamanrasset", "tebessa",
    "tlemcen", "tiaret", "tizi ouzou", "algiers", "djelfa", "jijel",
    "setif", "saida", "skikda", "sidi bel abbes", "annaba", "guelma",
    "constantine", "medea", "mostaganem", "m'sila", "mascara", "ouargla",
    "oran", "el bayadh", "illizi", "bordj bou arreridj", "boumerdes",
    "el tarf", "tindouf", "tissemsilt", "el oued", "khenchela", "souk ahras",
    "tipaza", "mila", "ain defla", "naama", "ain temouchent", "ghardaia",
    "relizane", "el m'ghair", "bordj badji mokhtar", "ouled djellal",
    "beni abbes", "timimoun", "touggourt", "djanet", "in salah", "in guezzam",
    "el menia"
]

df['City'].replace('',np.nan,inplace=True)
df['City'].fillna(pd.Series(np.random.choice(wilayas_of_algeria, size=len(df.index))), inplace=True)
df['City'] = df['City'].str.replace(' \(algérie\)', '', regex=True)


wilayas=df['City'].unique()


coordinates=[]
for i in wilayas:
    if geolocator.geocode(i)!=None:
        coordinates.append({i:(geolocator.geocode(i).latitude, geolocator.geocode(i).longitude)})

#
from geopy.distance import geodesic
distances=[]
for i in coordinates:
    b=[]
    for j in coordinates:
        for c in i:
            for k in j:
                b.append({k:geodesic(i[c], j[k]).kilometers})
        sorted_data = sorted(b, key=lambda x: next(iter(x.values())))
    for c in i:
        distances.append({c:sorted_data})

#
dists=[]
for i in distances:
    b=[]
    for j in i:
        for k in i[j]:
            for d in k:
                b.append(d)
        dists.append({j:b})


# Inserting a new column 'nearest distance' at index 1 with a list of values
df.insert(4, 'nearest distance','')

for i in range(df.shape[0]):
    for d in dists:
        for l in d:
            if l == df.loc[i,'City']:
                print(d[l])
                t=''
                for r in d[l]:
                    t=t+' '+r
                df.loc[i,'nearest distance'] = t   
     

def wilaya2(selected_wilaya, products):
    filtered_df = df[(df['City'].str.strip() == selected_wilaya)
                      & (df['Activities/Services'].str.strip() == products)]
    return filtered_df['Address']

selected_wilaya = 'alger'
products = 'Association . Organisme.'
# Call the wilaya2 function to filter the DataFrame
result_df = wilaya2(selected_wilaya, products)
print(result_df)

# @app.route('/GetBestSupliers', methods=['GET'])
# def filter_data():
#     # Get parameters from the request
#     selected_wilaya = request.args.get('wilaya')
#     products = request.args.get('product')

#     selected_wilaya = 'alger'
#     products = 'Association . Organisme.'
#     # Call the wilaya2 function to filter the DataFrame
#     result_df = wilaya2(selected_wilaya, products)
#     print(result_df)
#     # Convert the filtered DataFrame to a JSON response
#     return jsonify(result_df.to_dict(orient='records'))

# if __name__ == '__main__':
#     app.run(debug=True)