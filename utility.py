from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics  import AUC, CategoricalAccuracy, FalsePositives
from cv2 import imread, VideoCapture, GaussianBlur, cvtColor, INTER_CUBIC,COLOR_BGR2GRAY, resize, imshow, waitKey, destroyAllWindows
from numpy import array, max
from os.path import exists
from os import listdir
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

class Model:
    def __init__(self,input_shape,stride=(1,1),dilation=(1,1),kernel_n=3,pooling_size=(2,2),dropout_p=0.2,n_output=2,learning_rate=1e-3):
        log.log("[+] Model Initilaizing...")
        self.kernel_n=kernel_n
        self.input_shape=input_shape 
        self.stride=stride      # skips, kernel makes at every convolution
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
    def __init__(self,widthX=128,widthY=128):
        self.data_folder="./static/dataset/"
        self.dimension=(widthX,widthY)
    def get_data_dataset(self,mode=0,color_mode=0):
        # mode=0 ; Image data will be returned.
        # mode=1 ; Video data will be returned.
        # color_mode=0 ; greyscale image/frame.
        # color_mode=1 ; colour channel image/frame.
        # color_mode=-1 ; color channel along with alpha channel image/frame.
        if mode==0:
            X=[]
            Y=[]
            directory=self.data_folder+"images/FIRE_SMOKE/"
            for i in listdir(directory):
                X.append(imread(directory+i,color_mode))
                Y.append(1)
            directory=self.data_folder+"images/NONE/"
            for i in listdir(directory):
                X.append(imread(directory+i,color_mode))
                Y.append(0)
            return X,Y
        else:
            X=[]
            Y=[]
            directory=self.data_folder+"videos/FIRE_SMOKE/"
            for i in listdir(directory):
                cap=VideoCapture(directory+i)
                while(cap.isOpened()):
                    ret,frame=cap.read()
                    if ret==True:
                        X.append(frame,color_mode)
                        Y.append(1)
            directory=self.data_folder+"videos/NONE/"
            for i in listdir(directory):
                cap=VideoCapture(directory+i)
                while(cap.isOpened()):
                    ret,frame=cap.read()
                    if ret==True:
                        X.append(frame)
                        Y.append(0)
            return X,Y
    def read_data(self,directory,mode=0,color_mode=0):
        if mode==0:
            X=[]
            for i in listdir(directory):
                X.append(imread(directory+i,color_mode))
            return X
        else:
            X=[]
            for i in listdir(directory):
                cap=VideoCapture(directory+i)
                while(cap.isOpened()):
                    ret,frame=cap.read()
                    if ret==True:
                        X.append(frame)
            return X
    def preprocessing(self,image):
        # Noise removal using gaussian smoothing operator.
        image=GaussianBlur(image,(3,3),0)
        image=resize(image,self.dimension,interpolation=INTER_CUBIC)
        return image
    def normalize(self,image):
        return image/255
    def show_image(self,image,window_name):
        imshow(window_name, image)
        waitKey(0) 
        destroyAllWindows()


            



data=Data()
images,classes=data.get_data_dataset(color_mode=1)
data.show_image(images[0], "RAW")
print(max(images[0])) 
image=data.preprocessing(images[0])
data.show_image(image, "PEOCESSED")
