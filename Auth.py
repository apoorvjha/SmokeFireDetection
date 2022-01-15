from random import choices
from string import ascii_lowercase, ascii_uppercase, digits
import mysql.connector as mysql


class DataBase:
	def __init__(self,credsFileName="credential.txt"):
		with open(credsFileName,'r') as authCred:
			self.credentials=authCred.read().split('\n')
	def dbServerlogin(self):
		con=mysql.connect(host=self.credentials[0],user=self.credentials[1],password=self.credentials[2],database=self.credentials[3])
     # connection setup with our database.
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

def register(username,password):
    db=DataBase()
    con=db.dbServerlogin()
    query="SELECT count(*) FROM `credentials` WHERE `username`=%s AND `password=%s`"
    val=(username,password)
    count=db.executeQuery(con, query, val)
    if count!=0:
        return 300, "User with same username already exists."
    else:
        query="INSERT INTO `credentials`(`username`,`password`) VALUES(%s,%s)"
        val=(username,password)
        db.executeQuery(con, query, val, ReturnMode=False)
        return 200, "Successfully registered. Thanks for choosing us; We appreciate your choice!"

def login(username,password):
    db=DataBase()
    con=db.dbServerlogin()
    query="SELECT count(*) FROM `credentials` WHERE `username`=%s AND `password=%s`"
    val=(username,password)
    count=db.executeQuery(con, query, val)
    if count!=1:
        return 404, "Incorrect credentials. Please try again!"
    else:
        token=''.join(choices(ascii_uppercase + digits + ascii_lowercase, k = 10))
        return 200, "Login Successfull.", token



