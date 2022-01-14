import utility
import train

def inference_engine(fname="model.h5",processing_directory="./static/processing/",input_shape=(32,32,3),alpha=0):
    if fname==None:
        train.train()
        model=utility.Model_CNN()()
        model.load_model("model.h5")
    else:
        model=utility.Model_CNN()
        model.load_model(fname)
    if len(input_shape)==3:
        color_mode=1-alpha
    else:
        color_mode=0
    data=utility.Data(widthX=input_shape[0],widthY=input_shape[1])
    #while(len(utility.listdir(processing_directory+"images"))!=0 or len(utility.listdir(processing_directory+"videos"))!=0):
    X,files=data.read_data(processing_directory+"images/",mode=0,color_mode=color_mode)
    X=utility.array(X)
    if X.shape[0]!=0:
        prediction=model.predict(X)
        for i in range(prediction.shape[0]):
            if utility.argmax(prediction[i])==0:
                # Unsafe
                utility.rename(processing_directory+"images/"+files[i],f"./static/prediction/unsafe/{files[i]}")
            else:
                 # Safe
                utility.rename(processing_directory+"images/"+files[i],f"./static/prediction/safe/{files[i]}")
    X,files,frame_offset=data.read_data(processing_directory+"videos/",mode=1,color_mode=color_mode)
    X=utility.array(X)
    if len(X)!=0:   
        prediction=model.predict(X)
        i=0
        j=0
        while(i<prediction.shape[0]):
            unsafe_flag=False
            for k in range(i,i+frame_offset[j]):
               if utility.argmax(prediction[k])==0:
                    # Unsafe
                    unsafe_flag=True
                    break
            if unsafe_flag==True:
                utility.rename(processing_directory+"videos/"+files[j],f"./static/prediction/unsafe/{files[j]}")
            else:
                utility.rename(processing_directory+"videos/"+files[j],f"./static/prediction/safe/{files[j]}")
            i+=frame_offset[j]
            j+=1
    print("No more image or video present in processing directory.")

if __name__=='__main__':
    inference_engine()


    


