#pandas

import pandas as pd
import numpy as np
#series in pandas
# s=pandas.Series([34,43,67,89],index=['sugam','sakriya','sangam','cigar'])
# print(s.describe())

#dataframe in pandas

# py=[90,95,89,77]
# o_r=[90,95,89,77]
# i_s=[90,95,89,77]
# m_s=[90,95,89,77]
# marks=[py,o_r,i_s,m_s]
# # marks={
# #     'Python':py,
# #     'Operational Research':o_r,
# #     'Information Security':i_s,
# #     'Multimedia':m_s
# # }
# students=['Sakriya','Sugam','Sangam','Ritee']
# df=pd.DataFrame(marks)
# # df.iloc('')
# df=pd.DataFrame(marks,index=students,columns=['py','o_r','i_s','m_s'])

# # print(df['Python'].describe())
# ##total marks
# # df['Total']=df['Python']+df['Operational Research']+df['Information Security']+df['Multimedia']
# # df['Percentage']=df['Total']/4
# print(df.transpose)

py=[90,95,89,77]
o_r=[90,95,89,77]
i_s=[90,95,89,77]
m_s=[90,95,89,77]
marks={
    'Python':py,
    'Operational Research':o_r,
    'Information Security':i_s,
    'Multimedia':m_s
}
students=['Sakriya','Sugam','Sangam','Ritee']
df=pd.DataFrame(marks,index=students)
df['Total']=df['Python']+df['Operational Research']+df['Information Security']+df['Multimedia']
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

df['Grade'].loc['Sakriya']=np.nan
print(df)
# print(df.isnull())
print(df.isna().sum())

print(df['Percentage'].max())



