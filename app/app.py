from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = 'perfectchemical'

mysql = MySQL(app)

###### PAGE ROUTING ######

@app.route('/')
def homepage():
    return render_template('index.html') #render_template() will do automatic HTML escaping to prevent XSS attacks

@app.route('/create.html')
def create():
    return render_template('create.html')

@app.route('/read.html')
def read():
    return render_template('read.html') #render_template() will do automatic HTML escaping to prevent XSS attacks

@app.route('/update.html')
def update():
    return render_template('update.html')


@app.route('/delete.html')
def delete():
    return render_template('delete.html')


#### POST METHODS - APPLICATION LOGIC HERE ##### 

@app.route('/create', methods=['POST'])
def create_record():
    FName = request.form['FName']
    LName = request.form['LName']
    Address = request.form['Address']

    ### check if data follows rules. e.g., address has to be like 255 chars
    error = ""
    if not FName or not LName or not Address:
        error = f"You didn't enter all fields. Try again."
    elif len(FName) > 1:
        error += f"\FName was too long at {len(FName)} characters. Only enter the first initial."
    elif len(LName) > 45:
        error += f"\LName was too long at {len(LName)} characters"
    elif len(Address) > 255:
        error += f"\nAddress was too long at {len(Address)}"
    elif not FName.isalpha() or not LName.isalpha():
        error += f"\nDon't use non-alphamumeric characters."
    
    if error != "":
        flash(error, 'error')
    else:
        cur = mysql.connection.cursor()

        query = "INSERT INTO customer (FName, LName, Address) VALUES (%s, %s, %s)" # primary key is set to auto_increment
        
        try:
            cur.execute(query, (FName, LName, Address)) #should be resistant to SQL injection, not building the string anymore
            mysql.connection.commit()
            flash('Customer record added successfully! View the contents of the records in ./create.html', 'success') # shouldn't not work
            
        except Exception as e:
            flash(f'Error adding customer record: {str(e)}', 'error') # something went wrong with the query. could be the cursor
        finally:
            cur.close()
            
    return render_template('create.html')








if __name__ == '__main__':
    app.run(debug=True)