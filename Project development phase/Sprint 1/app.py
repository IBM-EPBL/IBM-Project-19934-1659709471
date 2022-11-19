from flask import Flask, render_template, flash, request, redirect, url_for, session
import sqlite3 

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("userdb.db")
con.execute("create table if not exists users(pid integer primary key,name TEXT, email TEXT, phone TEXT, city TEXT, blood_group TEXT, password TEXT, password1 TEXT)")
con.close()



@app.route('/')
def home():
   return render_template('home.html')

@app.route('/profile/<EMAIL>')
def profile(EMAIL):
   con = sqlite3.connect("userdb.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from users where email=?",[EMAIL])
   
   users = cur.fetchall();
   return render_template('profile.html', users=users)

@app.route('/about')
def about():
   return render_template('about.html')



   


@app.route('/signin',methods=["GET","POST"])
def signin():
   if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect("userdb.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where email=? and password=?",(email,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["email"]=data["email"]
            session["password"]=data["password"]
            return redirect(url_for("profile",EMAIL=session["email"]))
        else:
            flash("Username and Password Mismatch","danger")
            return redirect(url_for("signin"))
   return render_template('signin.html')

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         phone=request.form['phone']
         city = request.form['city']
         blood_group=request.form['blood_group']
         password = request.form['password']
         password1 = request.form['password1']
         if(password==password1):
            con=sqlite3.connect("userdb.db")
            cur = con.cursor()
            cur.execute("INSERT INTO users (name,email,phone,city,blood_group,password,password1) VALUES (?,?,?,?,?,?,?)",(name,email,phone,city,blood_group,password,password1))
            con.commit()
            flash("Register successfully","success")   
         else:
            flash("Password Mismatch","danger")  
      except:
            flash("Error","danger")
         
      finally:
            return redirect(url_for("signin"))
            con.close()
   return render_template('signup.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("signin"))


if __name__ == '__main__':
   app.run(debug = True)

