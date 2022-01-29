from flask import Flask, render_template, redirect, flash, request, url_for, session
from werkzeug.utils import secure_filename
import json
import Auth
import time
import os
from os import listdir
import utility

app=Flask(__name__)
app.secret_key="qazwsx@2022"

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/logout')
def logout():
    if session['username']:
        session.pop('username',None)
        session.pop('email',None)
        session.pop('profilePic',None)
        session.pop('type',None)
        session.pop('userId',None)        
        flash("Successfully logged out!",'alert alert-success')        
    return redirect(url_for('index'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/loginBack',methods=['POST'])
def login_back():
    if request.method=='POST':
        userId=request.form['userId']
        password=request.form['password']
        status,res,msg,category=Auth.checkCredentials(userId,password)
        flash(msg,category)
        if status==True:
            session['username']=res[0][0]
            session['email']=res[0][1]
            session['profilePic']=res[0][2]
            session['type']=res[0][3]
            session['userId']=res[0][4]
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        flash("Unsupported method of request! Please use POST instead.",'alert alert-danger')
        return redirect(url_for('index'))
@app.route('/registerBack',methods=['POST'])
def registerBack():
    if request.method=='POST':
        userId=request.form['userId']
        password=request.form['password']
        email=request.form['email']
        profilePic=request.files['profilePic']
        fileName=userId + secure_filename(profilePic.filename)
        profilePic.save('static/PROFILE_PIC/'+fileName)
        profilePath='static/PROFILE_PIC/'+fileName
        status=Auth.register(userId,password,email,profilePath)
        if status==True:
            # as we advance, incorporate functionality of OTP verification as well.
            flash("You are successfully registered!.",'alert alert-success') 
            return redirect(url_for('index'))
        else:
            flash("User with provided data already exists! ",'alert alert-danger')
            return redirect(url_for('register'))
    else:
        flash("Unsupported method of registration! Please use the registration tab instead.",'alert alert-danger')
        return redirect(url_for("HomePage"))
@app.route('/users')
def getUsers():
    if session['type']=='admin':
        response={"users" : []}
        users=Auth.getUsers()
        for i in users:
            response["users"].append({"userID" : i[0],"profilePic" : i[1], "username" : i[2], "email" : i[3],"isActive" : i[4]})
        return response
    else:
        #flash("You donot have access to this endpoint!","alert alert-danger")
        return {"status" : 404}

@app.route('/activate/<id>')
def activate(id):
    if session['type']=='admin':
        Auth.activate(id)
        #flash("User activated successfully!","alert alert-success")
        return {"status" : 200}
    else:
        #flash("You donot have access to this endpoint!","alert alert-danger")
        return {"status" : 404}

@app.route('/deactivate/<id>')
def deactivate(id):
    if session['type']=='admin':
        Auth.deactivate(id)
        #flash("User deactivated successfully!","alert alert-success")
        return {"status" : 200}
    else:
        #flash("You donot have access to this endpoint!","alert alert-danger")
        return {"status" : 404}
@app.route('/settings')
def settings():
    return render_template('settings.html')
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/changeCredentials',methods=['POST'])
def changeCredentials():
    if session['userId']:
        if request.method=='POST':
            mode=request.form['mode']
            value=request.form["value"]
            if mode==0:
                Auth.changeUserName(session['userId'],value)
            elif mode==1:
                Auth.changePassword(session['userId'],value)
            else:
                Auth.changeEmail(session['userId'],value)
            return {"status" : 200}
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}

@app.route('/changeProfilePicture',methods=['POST'])
def changeProfPic():
    if session['userId']:
        if request.method=='POST':
            # change profile pic.
            profilePic=request.files['profpic']	
            fileName=session['profilePic']
            profilePic.save(fileName)
            flash("Profile pic changed successfully!","alert alert-success")
            return redirect(url_for('index'))
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}

@app.route('/inference',methods=['POST'])
def inference():
    if session['userId']:
        if request.method=='POST':
            image=request.files['file']	
            print(image.filename)
            fileName=str(session['userId']) + secure_filename(image.filename)
            image.save('static/uploaded/'+fileName)
            start=time.time()
            data=utility.Data(widthX=32,widthY=32)
            X=[]
            X.append(data.preprocessing(utility.imread('static/uploaded/'+fileName,1)))
            X=utility.array(X)
            model=utility.Model_CNN()
            model.load_model("model.h5")
            prediction=model.predict(X)
            print(prediction)
            if utility.argmax(prediction[0])==0:
                pred="Unsafe"
            else:
                pred="Safe"
            time_taken=time.time() - start
            return {"image" : 'static/uploaded/'+fileName,"prediction" : pred, "status" : 200,"response_time" : round(time_taken,3)}
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}
@app.route('/getModelStats')
def getModelStats():
    if session['userId']:
        if request.method=='GET':
            response={"params" : [],"status" : 200}
            response["params"].append({"name" : "Logging Mode","value" : utility.logging_mode})
            response["params"].append({"name" : "Test ratio","value" : 0.2})
            response["params"].append({"name" : "n_output","value" : 2})
            response["params"].append({"name" : "dropout_probability","value" : 0.2})
            response["params"].append({"name" : "learning_rate","value" : 1e-3})
            response["params"].append({"name" : "batch_size","value" : 4})
            response["params"].append({"name" : "epochs","value" : 10})
            response["params"].append({"name" : "model_name","value" : "model.h5"})
            response["params"].append({"name" : "validation_split","value" : 0.2})
            response["params"].append({"name" : "random_state","value" : 42})
            response["params"].append({"name" : "verbose","value" : 0})
            response["params"].append({"name" : "Interpolation","value" : "INTER_CUBIC"}) 
            return response
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}

@app.route('/getDataset')
def getDataset():
    if session['userId']:
        if request.method=='GET':
            response={"images" : [], "videos" : [],"status" : 200}
            path='./static/dataset/images/'
            directories=['FIRE_SMOKE','NONE']
            for i in range(len(directories)):
                for j in listdir(path+directories[i]+'/'):
                    response["images"].append({"name" : directories[i],"image" : path+directories[i]+'/'+j})
            path='./static/dataset/videos/'
            directories=['FIRE_SMOKE','NONE']
            for i in range(len(directories)):
                for j in listdir(path+directories[i]+'/'):
                    response["videos"].append({"name" : directories[i],"video" : path+directories[i]+'/'+j})
            return response
        else:
            return {"status" : 404}
    else:
        return {"status" : 500}

if __name__=='__main__':
    app.run(debug=True,port=5000)