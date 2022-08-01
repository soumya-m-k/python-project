from flask import *
import mysql.connector as mysql
import datetime as dt
app=Flask(__name__)
app.secret_key='hello'
@app.route('/')
def homepage():
    return render_template('homepage.html')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/enter',methods=['POST'])
def enter():
    fname=request.form['fname']
    lastname=request.form['lname']
    email=request.form['email']
    password=request.form['pass']
    mobilenumber=request.form['mnumber']
    con=mysql.connect(host="localhost",user="root",password="",database="register")
    cur=con.cursor()
    cur.execute('insert into baby values(%s,%s,%s,%s,%s)',(fname,lastname,email,password,mobilenumber))
    con.commit()
    con.close()
    flash('data saved')
    return render_template('register.html')
@app.route('/checkuser',methods=['POST'])
def checkuser():
    fname=request.form['fname']
    password=request.form['password']
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    cur.execute('select * from baby where fname=%s and password=%s',(fname,password))
    result=cur.fetchall()
    if(len(result)==0):
        flash('invalid username or password')
        return render_template('login.html')
    else:
        session['username']=fname
        return render_template('navigation.html')
@app.route('/navigation')
def navigation():
    return render_template('navigation.html')
@app.route('/bornregister') 
def bornregister():
    return render_template('bornregister.html')
@app.route('/born',methods=['POST']) 
def born():
    parentname=request.form['parentname']
    hospital=request.form['hospital']
    date=request.form['bdate']
    bdate=dt.datetime.strptime(date,'%Y-%m-%d')
    print(bdate)
    gender=request.form['gender']
    con=mysql.connect(host="localhost",user="root",password="",database="register")
    cur=con.cursor()
    cur.execute('insert into babyreg values(%s,%s,%s,%s)',(parentname,hospital,bdate,gender))
    con.commit()
    con.close()
    flash('data saved')
    return redirect('/display')
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')
@app.route('/display')
def display():
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    cur.execute('select * from babyreg')
    result=cur.fetchall()
    con.close()
    return render_template('display.html',result=result)
@app.route('/display/<parentname>')
def users(parentname):
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    cur.execute('select * from baby where parentname=%s',(parentname,))
    result=cur.fetchall()
    con.close()
    return render_template('display.html',result=result)
@app.route('/edituserform<parentname>')
def edituserform(parentname):
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    cur.execute('select * from babyreg where parentname=%s',(parentname,))
    result=cur.fetchone()
    con.close()
    return render_template('edituser.html',result=result)
@app.route('/updateuser',methods=['POST'])
def updateuser():
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    parentname=request.form['parentname']
    hospital=request.form['hospital']
    date=request.form['bdate']
    bdate=dt.datetime.strptime(date,'%Y-%m-%d')
    gender=request.form['gender']
    cur.execute('update babyreg set parentname=%s,hospital=%s,bdate=%s,gender=%s where parentname=%s',(parentname,hospital,bdate,gender,parentname))
    con.commit()
    if(cur.rowcount>0):
        flash('data updated successfully')
    else:
        flash('unable to update user')    
    con.close()
    return redirect('/display')
@app.route('/deleteuser<parentname>')
def deleteuser(parentname):
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    cur.execute('delete from babyreg where parentname=%s',(parentname,))
    con.commit()
    if(cur.rowcount>0):
        flash('user deleted successfully')
    else:
        flash('unable to delete user')    
    return redirect('/display') 
@app.route('/searchuser',methods=['POST'])
def searchuser():
    parentname=request.form['parentname']
    con=mysql.connect(host='localhost',user='root',password='',database='register')
    cur=con.cursor()
    cur.execute('select * from babyreg where parentname=%s',(parentname,))
    result=cur.fetchall()     
    if(len(result)==0):
        flash('users not found')
        return render_template('display.html',result=[])
    else:
        return render_template('display.html',result=result) 
@app.route('/add')
def add():
    return render_template('bornregister.html')



