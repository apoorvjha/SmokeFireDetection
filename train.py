import utility 

def read_config(fname):
    with open(fname,'r') as conf:
        config=utility.json.load(conf)
    pass



def train(fname_in=None,fname_out="model.h5",mode=0,input_shape=(28,28,3),alpha=0):
    # mode=0; train only on images.
    # mode=1; train only on video frames.
    # mode=2; train in a holistic fashion.
    if fname_in==None:
        model=utility.Model(input_shape=input_shape)
    else:
        model=utility.Model()
        model.load_model(fname_in)
    if len(input_shape)==3:
        color_mode=1-alpha
    else:
        color_mode=0
    data=utility.Data(widthX=input_shape[0],widthY=input_shape[1])
    if mode==0:
        X,Y=data.get_data_dataset(mode=mode,color_mode=color_mode)
    elif mode==1:
        X,Y=data.get_data_dataset(mode=mode,color_mode=color_mode)
    else:
        X=[]
        Y=[]
        X_i,Y_i=data.get_data_dataset(mode=0,color_mode=color_mode)
        X_v,Y_v=data.get_data_dataset(mode=1,color_mode=color_mode)
        X.extend(X_i)
        X.extend(X_v)
        Y.extend(Y_i)
        Y.extend(Y_v)
    X=utility.array(X)
    Y=utility.array(Y)
    X_train, X_test, Y_train, Y_test=data.split(X,Y,test_ratio=0.2,shuffle=True,random_state=42)
    model.fit(X_train,Y_train,batch_size=8,epochs=10,validation_split=0.2)
    data.plot_in_time(model.history.history['loss'],
    model.history.history['val_loss'],
    "Loss", ["Metrics","Epochs"],["Train","Validation"],"Loss.png")
    data.plot_in_time(model.history.history['categorical_accuracy'],
    model.history.history['val_categorical_accuracy'],
    "Loss", ["Metrics","Epochs"],["Train","Validation"],"accuracy.png")
    model.save_model(fname_out)
    

if __name__=="__main__":
    train()
