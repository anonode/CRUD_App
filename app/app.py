from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = 'perfectchemical'


# store relational schema and attributes in dictionary for later use

schema_dict = {
    "customer": ["IdNo", "LName", "FName", "Address"],
    "subscriptions": ["SubId", "SubType", "Customer_id"],
    "magazine": ["MagId", "MagType", "NumberOfIssues", "StartDate", "EndDate", "Price", "SubId", "Customer_id"],
    "newspaper": ["NewsId", "NewsType", "NumberOfMonths", "StartDate", "EndDate", "Price", "SubId", "Customer_id"],
    "publications": ["PubName", "PubType"]
}


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


#### Handlers for create

@app.route('/create', methods=['POST'])
def create_customer():
    FName = request.form['FName']
    LName = request.form['LName']
    Address = request.form['Address']

    ### check if data follows rules. e.g., address has to be like 255 chars
    error = ""
    if not FName or not LName or not Address:
        error = f"You didn't enter all fields. Try again."
    elif len(FName) > 1:
        error += f"\nFName was too long at {len(FName)} characters. Only enter the first initial."
    elif len(LName) > 45:
        error += f"\nLName was too long at {len(LName)} characters"
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
            
    return redirect(url_for('create'))


# Handler for adding a new subscription
@app.route('/create_subscription', methods=['POST'])
def create_subscription():
    # Collect form data for the subscription
    SubType = request.form['SubType']
    Customer_id = request.form['Customer_id']
    
    # Insert into the subscriptions table
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO subscriptions (SubType, Customer_id) VALUES (%s, %s)", (SubType, Customer_id))
    mysql.connection.commit()
    cursor.close()

    flash('Subscription added successfully!', 'success')
    return redirect(url_for('create'))


# Handler for adding a new magazine
@app.route('/create_publication', methods=['POST'])
def create_publication():
    # Collect form data for the magazine
    MagType = request.form['MagType']
    NumberOfIssues = request.form['NumberOfIssues']
    StartDate = request.form['StartDate']
    EndDate = request.form['EndDate']
    Price = request.form['Price']
    
    # Insert into the magazine table
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO magazine (MagType, NumberOfIssues, StartDate, EndDate, Price) VALUES (%s, %s, %s, %s, %s)",
                    (MagType, NumberOfIssues, StartDate, EndDate, Price))
    mysql.connection.commit()
    cursor.close()

    flash('Magazine added successfully!', 'success')
    return redirect(url_for('create'))


### handlers for read

@app.route('/read_customer', methods=['GET'])
def read_customer():
    
    return redirect(url_for('read'))

@app.route('/read_subscription', methods=['GET'])
def read_subscription():
    pass

@app.route('/read_publication', methods=['GET'])
def read_publication():
    pass

### handlers for update

@app.route('/update_customer', methods=['POST'])
def update_customer():
    pass

@app.route('/update_subscription', methods=['POST'])
def update_subscription():
    pass

@app.route('/update_publication', methods=['POST'])
def update_publication():
    pass


### handlers for delete

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    pass

@app.route('/delete_subscription', methods=['POST'])
def delete_subscription():
    pass

@app.route('/delete_publication', methods=['POST'])
def delete_publication():
    pass


if __name__ == '__main__':
    app.run(debug=True)