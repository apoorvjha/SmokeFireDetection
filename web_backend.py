from flask import Flask
from werkzeug import secure_filename
import Auth
import utility
import train

app=Flask(__name__)
app.secret_key="qazwsx@2022"

@app.route('/')
def Home():
    return "<h1>Home</h1>"

@app.route('/about')
def About():
    return "<h1>About us</h1>"

@app.route('/register',methods=['GET','POST'])
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


@app.route('/api')
def API_Home():
    return "<h1>api home</h1>"

@app.route('/api/fetch/<N_Smoke_Fire_Images>')
def API_Fetch(N_Smoke_Fire_Images):
    return f"{N_Smoke_Fire_Images} smoke and fire images are selected and served randomly!"

@app.route('/api/train/<Epochs>')
def API_Train(Epochs):
    accuracy=train(epochs=Epochs)
    # return paths for plots.
    return f"<h1>The {accuracy} acheived!</h1>"

@app.route('/api/predict/image',methods=['POST'])
def API_Predict_Image():
    if session['token'] == "":
        return {"status" : 404, "message" : "Token does not exists!", "response" : {}}  
    if request.method == 'POST':
        image=request.files['image']
        filename=secure_filename(token + image.filename)
        image.save('./static/uploaded/images/'+ filename)
        model=utility.Model_CNN()
        model.load_model("model.h5")
        data=utility.Data(widthX=32,widthY=32)
        X,files=data.read_data(processing_directory+"images/",mode=0,color_mode=1)
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



if __name__=='__main__':
    app.run(debug=True, port=5000)