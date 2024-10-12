
import numpy as np
import pandas as pd

data=pd.read_json('C:\\Users\\Dell\\Downloads\\data.json')
df=pd.DataFrame(data)
df['Total']=df['Python']+df['Operational Research']+df['Information Security']+df['Multimedia System']
df['Percentage']=df['Total']/4
df['Grade']=''
for name in df.index:
    if df['Percentage'].loc[name]>80:
        df['Grade'].loc[name]='Distinction'
    elif df['Percentage'].loc[name]>60 and df['Percentage'].loc[name]:
        df['Grade'].loc[name]='Division'
    elif df['Percentage'].loc[name]>50 and df['Percentage'].loc[name]:
        df['Grade'].loc[name]=' Second Division'
    elif df['Percentage'].loc[name]<50:
        df['Grade'].loc[name]='Failed'
print(df)