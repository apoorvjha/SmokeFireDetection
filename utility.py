from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics  import AUC, CategoricalAccuracy, FalsePositives
#from cv2 import 
#from numpy import
from os.path import exists
from datetime import datetime

class Logger:
    def __init__(self,fname="log.txt"):
        self.fname=fname
    def log(self,data):
        with open(self.fname,'a') as log_file:
            log_file.write(f"[ {datetime.now()} ] - ")
            log_file.write(data)
            log_file.write('\n')


log=Logger()
'''
https://towardsdatascience.com/comparative-performance-of-deep-learning-optimization-algorithms-using-numpy-24ce25c2f5e2
'''
class Model:
    def __init__(self,input_shape,stride=(1,1),dilation=(1,1),kernel_n=3,pooling_size=(2,2),dropout_p=0.2,n_output=2,learning_rate=1e-3):
        log.log("[+] Model Initilaizing...")
        self.kernel_n=kernel_n
        self.input_shape=input_shape 
        self.stride=stride      # skips kernel makes at every convolution
        self.dilation=dilation  # kernel coverage
        self.pooling_size=pooling_size
        self.dropout_p=dropout_p
        self.n_output=n_output
        self.learning_rate=learning_rate
        self.model=Sequential()
        self.model.add(Conv2D(filters=16,kernel_size=self.kernel_n,activation='relu',
        padding='same',input_shape=self.input_shape[1:],strides=self.stride, dilation_rate=self.dilation))
        self.model.add(MaxPool2D(pool_size=self.pooling_size))
        self.model.add(Conv2D(filters=32,kernel_size=self.kernel_n,activation='relu',
        padding='same',strides=self.stride, dilation_rate=self.dilation))
        self.model.add(MaxPool2D(pool_size=self.pooling_size))
        self.model.add(Conv2D(filters=64,kernel_size=self.kernel_n,activation='relu',
        padding='same',strides=self.stride, dilation_rate=self.dilation))
        self.model.add(MaxPool2D(pool_size=self.pooling_size))
        self.model.add(Conv2D(filters=128,kernel_size=self.kernel_n,activation='relu',
        padding='same',strides=self.stride, dilation_rate=self.dilation))
        self.model.add(MaxPool2D(pool_size=self.pooling_size))
        self.model.add(Flatten())
        self.model.add(Dense(units=self.input_shape[0] * 128,activation='relu'))
        self.model.add(Dropout(self.dropout_p))
        self.model.add(Dense(units=128,activation='relu'))
        self.model.add(Dropout(self.dropout_p))
        self.model.add(Dense(units=64,activation='relu'))
        self.model.add(Dropout(self.dropout_p))
        self.model.add(Dense(units=32,activation='relu'))
        self.model.add(Dropout(self.dropout_p))
        self.model.add(Dense(units=16,activation='relu'))
        self.model.add(Dropout(self.dropout_p))
        self.model.add(Dense(units=self.n_output))
        self.model.compile(optimizer=Adam(learning_rate=self.learning_rate),loss=CategoricalCrossentropy(),metrics=[AUC(),CategoricalAccuracy(),FalsePositives()])
        log.log("[+] Model Initialized!")
    def get_instnce(self):
        return self.model
    def save_model(self,fname):
        self.model.save(fname)
        log.log(f"[+] Model saved in {fname} file.")
    def load_model(self,fname):
        assert exists(fname)==True , f"{fname} model file does not exists!"
        self.model=load_model(fname)
        log.log(f"[+] Model loaded from {fname} file.")
    def fit(self,X,Y,batch_size,epochs):
        log.log("[+] Model training started.")
        self.model.fit(X,Y,batch_size=batch_size,epochs=epochs)
        log.log("[+] Model training completed.")
    def predict(self,X):
        return self.model.predict(X)
        log.log("[+] Model completed the prediction.")
    def getStats(self):
        log.log("--------------------------- Parameters -------------------------")
        log.log(f"Kernel size : {self.kernel_n}")
        log.log(f"Input shape : {self.input_shape}") 
        log.log(f"Strides : {self.stride}")
        log.log(f"Dilation : {self.dilation}")
        log.log(f"Pooling size : {self.pooling_size}")
        log.log(f"Dropot probability : {self.dropout_p}")
        log.log(f"Output shape : {self.n_output}")
        log.log(f"Learning rate : {self.learning_rate}")
        log.log("----------------------------------------------------------------")

class Data:
    def __init__(self):
        pass


model=Model(input_shape=(10,28,28,3))
model.getStats()