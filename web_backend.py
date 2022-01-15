from flask import Flask
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
import Auth
import utility
import train

app=Flask(__name__)
app.secret_key="qazwsx@2022"
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/register',methods=['GET','POST'])
@cross_origin()
def Register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        status, message = Auth.register(username,password)
        return {"status" : status, "message" : message}

    elif request.method == 'GET':
        username=request.args.get('username')
        password=request.args.get('password')
        status, message = Auth.register(username,password)
        return {"status" : status, "message" : message}
    else:
        return {"status" : 404, "message" : "Method not supported!"}

@app.route('/login',methods=['GET','POST'])
@cross_origin()
def Login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        status, message, token = Auth.check(username,password)
        if status == 200 : 
            session['username'] = username
            session['token'] = token 
        return {"status" : status, "message" : message, "token" : token}

    elif request.method == 'GET':
        username=request.args.get('username')
        password=request.args.get('password')
        status, message, token = Auth.check(username,password) 
        return {"status" : status, "message" : message, "token" : token}
    else:
        return {"status" : 404, "message" : "Method not supported!", "token" : ""}

@app.route('/logout')
@cross_origin()
def Logout():
    session.pop('username',None)
    session.pop('token',None)
    return {"status" : 200, "message" : "Logout successfull"}

@app.route('/api')
@cross_origin()
def API_Home():
    return "<h1>api home</h1>"

@app.route('/api/train/<Epochs>')
@cross_origin()
def API_Train(Epochs):
    if Auth.checkToken(session['username'], session['token']):
        return {"status" : 404, "message" : "Token does not exists!", "response" : {}}
    else:    
        accuracy=train(epochs=Epochs)
        # return paths for plots.
        return f"<h1>The {accuracy} acheived!</h1>"

@app.route('/api/predict/image',methods=['POST'])
@cross_origin()
def API_Predict_Image():
    if Auth.checkToken(session['username'], session['token']):
        return {"status" : 404, "message" : "Token does not exists!", "response" : {}}  
    if request.method == 'POST':
        image=request.files['image']
        filename=secure_filename(token + image.filename)
        image.save('./static/uploaded/images/'+ filename)
        model=utility.Model_CNN()
        model.load_model("model.h5")
        data=utility.Data(widthX=32,widthY=32)
        X,files=data.read_data('./static/uploaded/images/',mode=0,color_mode=1)
        X=utility.array(X)
        res={}
        if X.shape[0]!=0:
            prediction=model.predict(X)
            for i in range(prediction.shape[0]):
                if utility.argmax(prediction[i])==0:
                    # Unsafe
                    res[filename] = "unsafe"    
                else:
                    # Safe
                    res[filename] = "safe"
        return {"status" : 200, "message" : "Inference completed Successfully!", "response" : res}
    else:
        return {"status" : 404, "message" : "unsupported method.", "response" : {}}


@app.route('/api/predict/video',methods=['POST'])
@cross_origin()
def API_Predict_Video():
    if Auth.checkToken(session['username'], session['token']):
        return {"status" : 404, "message" : "Token does not exists!", "response" : {}}  
    if request.method == 'POST':
        video=request.files['video']
        filename=secure_filename(token + video.filename)
        image.save('./static/uploaded/videos/'+ filename)
        model=utility.Model_CNN()
        model.load_model("model.h5")
        data=utility.Data(widthX=32,widthY=32)
        X,files=data.read_data('./static/uploaded/videos/',mode=0,color_mode=1)
        X=utility.array(X)
        res={}
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
                res[filename] = "unsafe"
            else:
                res[filename] = "safe"
            i+=frame_offset[j]
            j+=1
        return {"status" : 200, "message" : "Inference completed Successfully!", "response" : res}
    else:
        return {"status" : 404, "message" : "unsupported method.", "response" : {}}


if __name__=='__main__':
    app.run(debug=True, port=5000)