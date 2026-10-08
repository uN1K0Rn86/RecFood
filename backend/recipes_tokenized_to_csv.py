import json
import pandas as pd


with open('recipes_tokenized.json') as tiedosto:
    data = tiedosto.read()
reseptit = json.loads(data)

print('data:', type(data))
print('reseptit:', type(reseptit))
print(reseptit[0]['ingredients'][0]['lemmatized'][0]['analysis'][0])
print(len(reseptit))

df = pd.DataFrame(columns=['name', 'ing_name', 'token', 'baseform', 'tclass', 'number'])

for i in range(len(reseptit)):
    
    name = reseptit[i]['name']
    ingredients = reseptit[i]['ingredients']
    
    for j in range(len(ingredients)):

        ing_name = ingredients[j]['name']
        lem = ingredients[j]['lemmatized']

        for k in range(len(lem)):

                token = lem[k]['token']
                analysis = lem[k]['analysis']

                for l in range(len(analysis)):
                    baseform = analysis[l]['BASEFORM']
                    tclass = analysis[l]['CLASS']
                    try:
                        number = analysis[l]['NUMBER']
                    except:
                        number = None


                    new_row = pd.Series({'name':name, 'ing_name':ing_name, 'token':token, 'baseform':baseform, 'tclass':baseform, 'number':number})
                    df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

print(df.head())

df.to_csv('reseptit.csv')

# aineet = reseptit['ingredients']

# print('aineet:', type(aineet))

""" lem = reseptit['ingredients']['lemmatized']

print(lem)

import pandas as pd

df = pd.json_normalize(lem)

print(df.head())
 """
""" 
# print(reseptit)

import pandas as pd

# df = pd.read_json('recipes_tokenized.json')

# print(df.columns)

# print(df['ingredients'].head())

df = pd.json_normalize(reseptit)

print(df.head())
print(df.columns)
print(df['ingredients'].head())

df_uusi = pd.DataFrame(df, columns=['name', 'ingredients'])

print(df_uusi.head())

df_uusi.to_csv('reseptit.csv')

 """
