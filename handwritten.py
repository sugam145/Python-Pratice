from sklearn.metrics import confusion_matrix, classification_report,accuracy_score
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt
(X_train, y_train),(X_test,y_test)=keras.datasets.mnist.load_data()
print(X_test[10])
plt.matshow(X_test[1])
plt.show()
X_train=X_train/255
X_test=X_test/255
X_train=X_train.reshape(len(X_train),28*28)
X_test=X_test.reshape(len(X_test),28*28)
model=keras.Sequential([
    keras.layers.Dense(10, input_shape=(784,), activation='sigmoid'),
    # keras.layers.Dense(10, input_shape=(784,), activation='sigmoid')
])
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train,y_train,epochs=7)

y=model.predict(X_test)
y_pred=y.argmax(axis=1)
print(y_test[1])
print(y_pred[1])
