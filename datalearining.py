import pandas as pd
import numpy as np

d={
    'Roll':[1,2,3,4,5],
    'Name':['sugam','sangam','ritee','sakriya','maya'],
    'Gender':['M','M','F','M','F']
}
df=pd.DataFrame(d)
print(df.info())
df2=df
df2['Gender']=df['Gender'].astype('category')
df2['Gender']=df2['Gender'].cat.codes
print(df2['Gender'].dtypes)

print(df2)
