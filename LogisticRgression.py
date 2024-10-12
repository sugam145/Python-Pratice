import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
data=pd.read_csv('C:\\Users\\Dell\\Downloads\\heart.csv')
data.drop_duplicates(inplace=True)
x=data.drop(columns='target').values
y=data['target'].values.reshape(x.shape[0],1)
print(y.shape)
X_train, X_test, Y_train, Y_test=train_test_split(x,y,test_size=0.2,random_state=0)
print(X_train.shape,X_test.shape,Y_train.shape,Y_test.shape)

def model(x,y,lr,iteration):
    m=x.shape[1]
    
    W=np.zeros(x.shape[1],1)
    B=0
    for i in range(iteration):
        z=np.dot(W.T,x)+B
        y_pred=sigmoid(z)
        cost=-(1/m)*np.sum(y*np.log(y_pred)+(1-y)*np.log(1-y_pred))
        dw=(1/m)*np.dot(y_pred-y,x.t)
        db=(1/m)*np.sum(y_pred-y)
        B=B-lr*db
        W=W-lr*dw   
    return W,B
    
    
def sigmoid(z):
    y_pred=1/(1+np.exp(-z))
    return y_pred

W,B=model(x.T,y.T,0.000005,10000)

        


