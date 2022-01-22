import mysql.connector as mysql
from passlib.hash import sha256_crypt

class DataBase:
	def __init__(self,credsFileName="credential.txt"):
		with open(credsFileName,'r') as authCred:
			self.credentials=authCred.read().split('\n')
	def dbServerlogin(self):
		con=mysql.connect(host=self.credentials[0],user=self.credentials[1],password=self.credentials[2],database=self.credentials[3])
		return con
	def executeQuery(self,con,query,val=(),ReturnMode=True):
		myCursor=con.cursor()
		if ReturnMode==True:		
			myCursor.execute(query,val)
			res=myCursor.fetchall()
			return res
		else:
			myCursor.execute(query,val)
			con.commit()
			return

def checkCredentials(userId,password):
    db=DataBase()
    con=db.dbServerlogin()
    query="SELECT count(*) FROM `credentials` WHERE `username`=%s AND `password`=%s"
    val=(userId,password)
    count=db.executeQuery(con, query, val)
    if((count[0][0]==1) and (checkActiveStatus(userId)==True)):
        status=True
        msg="You are successfully logged in!"
        category='alert alert-success'
        query_data="SELECT `username`,`email`,`profilePic`,`type`,`userID` FROM `credentials` WHERE `username`=%s"
        val=(userId,)
        res=db.executeQuery(con, query_data, val)
    elif((count[0][0]==1) and (checkActiveStatus(userId)==False)):
        status=False
        msg="Your account is pending to be activated by administrator!"
        res=""
        category='alert alert-danger'
    else:
        status=False
        msg="Wrong credentials!"
        res=""
        category='alert alert-danger'        
    return status, res, msg, category

def checkActiveStatus(userId):
    db=DataBase()
    con=db.dbServerlogin()
    query="SELECT count(*) FROM `credentials` WHERE `username`=%s AND `isActive`=%s"
    val=(userId,1)
    count=db.executeQuery(con, query, val)
    if count[0][0]==1:
        return True
    else:
        return False

def register(userId,password,email,profilePath):
    db=DataBase()
    con=db.dbServerlogin()
    query_check="SELECT count(*) FROM `credentials` WHERE `username`=%s"
    val=(userId,)
    count=db.executeQuery(con, query_check, val)
    if count[0][0]!=0:
        return False 
    else:   
        query="INSERT INTO `credentials`(`username`,`password`,`email`,`profilePic`,`type`,`isActive`) VALUES (%s,%s,%s,%s,%s,%s)"
        val=(userId,password,email,profilePath,'user',1)
        db.executeQuery(con, query, val, ReturnMode=False)
        return True

def getUsers():
    db=DataBase()
    con=db.dbServerlogin()
    query="SELECT `userID`,`profilePic`,`username`,`email`,`isActive` FROM `credentials` WHERE `type`='user'"
    data=db.executeQuery(con, query)
    return data

def activate(id):
    db=DataBase()
    con=db.dbServerlogin()
    query="UPDATE `credentials` SET `isActive`=1 WHERE `userID`=%s"
    val=(id,)
    data=db.executeQuery(con, query,val, ReturnMode=False)
    return

def deactivate(id):
    db=DataBase()
    con=db.dbServerlogin()
    query="UPDATE `credentials` SET `isActive`=0 WHERE `userID`=%s"
    val=(id,)
    data=db.executeQuery(con, query,val, ReturnMode=False)
    return

def changeUserName(id,newName):
    db=DataBase()
    con=db.dbServerlogin()
    query="UPDATE `credentials` SET `username`=%s WHERE `userID`=%s"
    val=(newName,id)
    data=db.executeQuery(con, query,val, ReturnMode=False)
    return

def changePassword(id,newPass):
    db=DataBase()
    con=db.dbServerlogin()
    query="UPDATE `credentials` SET `password`=%s WHERE `userID`=%s"
    val=(newPass,id)
    data=db.executeQuery(con, query,val, ReturnMode=False)
    return

def changeEmail(id,newEmail):
    db=DataBase()
    con=db.dbServerlogin()
    query="UPDATE `credentials` SET `email`=%s WHERE `userID`=%s"
    val=(newEmail,id)
    data=db.executeQuery(con, query,val, ReturnMode=False)
    return