import numpy as np
import pandas as pd
data=pd.read_csv('C:\\Users\\Dell\\Downloads\\used_cars_data.csv') 
# df=pd.DataFrame(data['Fuel_Type'])
# df2=df
# df2['Fuel_Type']=df['Fuel_Type'].astype('category')
# df2['Fuel_Type']=df2['Fuel_Type'].cat.codes

# # if(df2['Fuel_Type'].isna):
# df2['Fuel_Type'].fillna('Petrol',inplace=True)


# print(df2)
catego=['Fuel_Type','Transmission','Owner_Type','Seats']
df=data
for ca in catego:
    
    df[ca]=df[ca].astype('category')
    df[ca]=df[ca].cat.codes
if df[ca].isnull().all() or (df[ca] == 0).all():
    df.drop(rows=[ca], inplace=True)

print(df['Transmission'])
print(df['Fuel_Type'])
print(df['Owner_Type'])
print(df['Seats'])
# df.query('Seats==0',inplace=True)
# print(df)
    
