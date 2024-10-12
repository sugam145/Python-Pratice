import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data=pd.read_csv('C:\\Users\\Dell\\Downloads\\insurance.csv')
data.drop_duplicates(inplace=True)
x=data.drop(columns='charges')
y=data['charges'].values
y=y.reshape(x.shape[0],1)
x['sex']=x['sex'].astype('category').cat.codes
x['smoker']=x['smoker'].astype('category').cat.codes
x['region']=x['region'].astype('category').cat.codes
# print(x.head())
print(x.shape)
X_train, X_test, Y_train, Y_test=train_test_split(x.values,y,test_size=0.2,random_state=0)
LR=LinearRegression()
LR.fit(X_train,Y_train)
print(LR.score(X_test,Y_test))
s=np.asarray([[25,1,33,2,1,4]])
print(f'The model predicted total charge to be NRs. {LR.predict(s)[0][0]}')