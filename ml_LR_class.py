import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

data=pd.read_csv('C:\\Users\\Dell\\Downloads\\insurance.csv')

print(f'Number of duplicate data: {data.duplicated().sum()}')
print(f'Number of Null data: \n{data.isna().sum()}')
data.drop_duplicates(inplace=True)
print(f'Number of duplicate data after cleaning: {data.duplicated().sum()}')

data['sex']=data['sex'].astype('category')
data['smoker']=data['smoker'].astype('category')
data['region']=data['region'].astype('category')
data['sex']=data['sex'].cat.codes
data['smoker']=data['smoker'].cat.codes
data['region']=data['region'].cat.codes
X=data.drop(columns='charges')
Y=data['charges']
X=X.values
Y=Y.values.reshape(Y.shape[0],1)
print(X.shape)
print(Y.shape)


def linearR(x,y,learning_rate,iterations):
    m=x.shape[0]
    beta=np.zeros((x.shape[1],1))
    print(x.shape)
    print(beta.shape)
    for i in range(iterations):
        y_pred=np.dot(x,beta)
        cost=(1/(2*m))*np.sum(np.square(y_pred-y))
        d_beta=(1/m)*np.dot(x.T,y_pred-y)
        beta=beta-learning_rate*d_beta
        # print(cost)
    error=np.sum(np.square(y-y_pred))/np.sum(np.square(y-y.mean()))
    return beta, error
    
beta, error=linearR(X,Y,0.00009,1000000)
predict=np.dot([25,1,33,2,1,4],beta)
print(predict, error)
