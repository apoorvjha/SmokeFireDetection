from tensorflow.keras.models import Sequential, load_model, Model
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics  import AUC, CategoricalAccuracy, FalsePositives
from cv2 import imread, VideoCapture, GaussianBlur, cvtColor, CAP_PROP_FRAME_COUNT, INTER_CUBIC,COLOR_BGR2GRAY, resize, imshow, waitKey, destroyAllWindows
from tensorflow.keras.applications.vgg19 import VGG19
from numpy import array, max, argmax
from os.path import exists
from os import listdir, rename, environ
from datetime import datetime
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from subprocess import call
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import time
environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
logging_mode="info"


class Logger:
    def __init__(self,fname="log.txt"):
        self.fname=fname
    def log(self,data):
        if logging_mode=="debug":
            with open(self.fname,'a') as log_file:
                log_file.write(f"[ {datetime.now()} ] - ")
                log_file.write(data)
                log_file.write('\n')


log=Logger()

class Model_CNN:
    def __init__(self,transfer_learning=True,input_shape=None,stride=(1,1),dilation=(1,1),kernel_n=3,pooling_size=(2,2),dropout_p=0.2,n_output=2,learning_rate=1e-3):
        log.log("  Model Initilaizing...")
        if input_shape!=None:
            if transfer_learning:
                vgg_top = VGG19(weights='imagenet',input_shape=input_shape,classes=n_output,include_top=False)
                for layer in vgg_top.layers:
                    layer.trainable=False
                vgg_fc = Flatten() (vgg_top.output)
                vgg_fc = Dense(units=256,activation='relu')(vgg_fc)
                vgg_fc = Dropout(dropout_p)(vgg_fc)
                vgg_fc = Dense(units=128,activation='relu')(vgg_fc)
                vgg_fc = Dropout(dropout_p)(vgg_fc)
                vgg_fc = Dense(units=64,activation='relu')(vgg_fc)
                vgg_fc = Dropout(dropout_p)(vgg_fc)
                vgg_fc = Dense(units=32,activation='relu')(vgg_fc)
                vgg_fc = Dropout(dropout_p)(vgg_fc)
                vgg_fc = Dense(units=16,activation='relu')(vgg_fc)
                vgg_fc = Dropout(dropout_p)(vgg_fc)
                vgg_out = Dense(units=n_output,activation='softmax')(vgg_fc)  
                self.model = Model(inputs=vgg_top.input,outputs=vgg_out)
            else:
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
                padding='same',input_shape=self.input_shape,strides=self.stride, dilation_rate=self.dilation))
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
                self.model.add(Dense(units=self.n_output,activation="softmax"))
            self.model.compile(optimizer=Adam(learning_rate=learning_rate),loss=CategoricalCrossentropy(),metrics=[AUC(),CategoricalAccuracy(),FalsePositives()])
        log.log("  Model Initialized!")
    def get_instnce(self):
        return self.model
    def save_model(self,fname):
        self.model.save(fname)
        log.log(f"  Model saved in {fname} file.")
    def load_model(self,fname):
        assert exists(fname)==True , f"{fname} model file does not exists!"
        self.model=load_model(fname)
        log.log(f"  Model loaded from {fname} file.")
    def fit(self,X,Y,batch_size,epochs,validation_split=0.2):
        log.log("  Model training started.")
        start=time()
        self.history=self.model.fit(X,Y,batch_size=batch_size,epochs=epochs,validation_split=validation_split,verbose=0)
        print("Training took " + str(round(time()-start,4)) + " Seconds.")
        log.log("  Model training completed.")
    def predict(self,X):
        log.log("  Model completed the prediction.")
        return self.model.predict(X)
    def getStats(self):
        print(self.model.summary())
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
    def accuracy(self,Y1,Y2,precision=4):
        assert Y1.shape==Y2.shape , "Shape of both the parameters should be same."
        count=0
        for i in range(Y1.shape[0]):
            if argmax(Y1[i])==argmax(Y2[i]):
                count+=1
        return round(((count * 100) / Y1.shape[0]),precision)


class Data:
    def __init__(self,widthX=128,widthY=128):
        log.log("Initializing data handler...")
        self.data_folder="./static/dataset/"
        self.dimension=(widthX,widthY)
        self.plots_folder="./static/plots/"
        #self.sampling_ratio=10
        log.log("Data handler initialized.")
    def get_data_dataset(self,mode=0,color_mode=0):
        # mode=0 ; Image data will be returned.
        # mode=1 ; Video data will be returned.
        # color_mode=0 ; greyscale image/frame.
        # color_mode=1 ; colour channel image/frame.
        # color_mode=-1 ; color channel along with alpha channel image/frame.
        if mode==0:
            log.log("Retreiving data from the datset...")
            X=[]
            Y=[]
            directory=self.data_folder+"images/FIRE_SMOKE/"
            for i in listdir(directory):
                X.append(self.preprocessing(imread(directory+i,color_mode)))
                Y.append([1,0])
            directory=self.data_folder+"images/NONE/"
            for i in listdir(directory):
                X.append(self.preprocessing(imread(directory+i,color_mode)))
                Y.append([0,1])
            log.log("Dataset loaded successfully.")
            #X=self.parallelize(self.preprocessing, X,mode=1)
            return X,Y
        else:
            log.log("Retreiving data from the datset...")
            X=[]
            Y=[]
            directory=self.data_folder+"videos/FIRE_SMOKE/"
            for i in listdir(directory):
                cap=VideoCapture(directory+i)
                frame_count=0
                while(cap.isOpened()):
                    ret,frame=cap.read()
                    frame_count+=1
                    if color_mode==0:
                        frame=cvtColor(frame,COLOR_BGR2GRAY)
                    if ret==True:
                        X.append(self.preprocessing(frame))
                        Y.append([1,0])
                    else:
                        break
                cap.release()
                destroyAllWindows()
            directory=self.data_folder+"videos/NONE/"
            for i in listdir(directory):
                cap=VideoCapture(directory+i)
                frame_count=0
                while(cap.isOpened()):
                    ret,frame=cap.read()
                    frame_count+=1
                    if color_mode==0:
                        frame=cvtColor(frame,COLOR_BGR2GRAY)
                    if ret==True:
                        X.append(self.preprocessing(frame))
                        Y.append([0,1])
                    else:
                        break
                cap.release()
                destroyAllWindows()
            log.log("Dataset loaded successfully.")
            #X=self.parallelize(self.preprocessing, X,mode=1)
            return X,Y
    def read_data(self,directory,mode=0,color_mode=0):
        if mode==0:
            log.log("Loading data...")
            X=[]
            files=[]
            for i in listdir(directory):
                files.append(i)
                X.append(self.preprocessing(imread(directory+i,color_mode)))
            log.log("Data loaded successfully.")
            #X=self.parallelize(self.preprocessing, X,mode=1)
            return X,files
        else:
            log.log("Loading data...")
            X=[]
            files=[]
            frame_offset=[]
            for i in listdir(directory):
                files.append(i)
                cap=VideoCapture(directory+i)
                #print(cap.get(CAP_PROP_FRAME_COUNT))
                offset=0
                while(cap.isOpened()):
                    ret,frame=cap.read()
                    offset+=1
                    if ret==True:
                        X.append(self.preprocessing(frame))
                    else:
                        break
                cap.release()
                destroyAllWindows()
                frame_offset.append(offset)
            log.log("Data loaded successfully.")
            #X=self.parallelize(self.preprocessing, X,mode=1)
            return X,files,frame_offset
    def preprocessing(self,image):
        # Noise removal using gaussian smoothing operator.
        log.log("Applying preprocessing...")
        image=GaussianBlur(image,(3,3),0)
        image=resize(image,self.dimension,interpolation=INTER_CUBIC)
        log.log("Preprocessing done.")
        return self.normalize(image)
    def normalize(self,image):
        log.log("Normalizing the image...")
        return image/255
    def show_image(self,image,window_name):
        imshow(window_name, image)
        waitKey(0) 
        destroyAllWindows()
    def split(self,X,Y,test_ratio=0.2,shuffle=True,random_state=42):
        X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=test_ratio,shuffle=shuffle,random_state=random_state)
        return X_train, X_test, Y_train, Y_test
    def plot_in_time(self,X1,X2,title,label,legend,fname):
        plt.plot(X1)
        plt.plot(X2)
        plt.title(title)
        plt.xlabel(label[0])
        plt.ylabel(label[1])
        plt.legend(legend,loc="upper left")
        plt.savefig(self.plots_folder+fname)
        plt.close()
    def parallelize(self,function_name,inputs,mode=0):
        # mode=0; IO bound processes(MultiThreading)
        # mode=1; CPU bound processes(MultiProcessing)
        if mode==0:
            log.log("Executing the job in multithreading mode.")
            with ThreadPoolExecutor() as executor:
                result=executor.map(function_name,inputs) 
            return list(result)
        else:
            log.log("Executing the job in multiprocessing mode.")
            with ProcessPoolExecutor(max_workers=10) as executor:
                result=executor.map(function_name,inputs) 
            return list(result)

