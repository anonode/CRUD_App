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

pubtypes = ['Magazine', 'Newspaper']


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


#### APPLICATION LOGIC HERE ##### 


#### Handlers for create

@app.route('/create', methods=['POST']) #done
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


@app.route('/create_publication', methods=['POST'])
def create_publication():
    # Collect form data for the magazine
    pubname = request.form['PubName']
    pubtype = request.form['PubType']

    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO publications (PubName, PubType) VALUES (%s, %s)", (pubname, pubtype))
    mysql.connection.commit()
    cursor.close()

    flash('Publication added successfully!', 'success')
    return redirect(url_for('create'))


### handlers for read

@app.route('/read_customer', methods=['GET']) # later: consider outputing the subscriptions that the customer has as well
def read_customer():
    customer_id = request.args.get('Customer_id') # request.form['key'] syntax is only for retrieving form data from a POST request
    f_initial = request.args.get('FName')
    lname = request.args.get('LName')
    address = request.args.get('Address')
    try:
        customer_id = int(customer_id)
    except ValueError:
        flash(f'You did not enter an integer for Customer_ID. Here is what you entered: {customer_id}', 'error')

    cur = mysql.connection.cursor()
    if f_initial == "":
        if lname == "":
            cur.execute("SELECT * FROM customer WHERE IdNo = %s;",(customer_id,))  # fix this later
            customers = cur.fetchall()
            cur.close()
            return render_template('read.html', customers=customers)
        else:
            cur.execute("SELECT * FROM ") # finish this

    cur.close()
    return redirect(url_for('read')) ## might not want to redirect, could cause the query to be removed from the page

@app.route('/read_subscription', methods=['GET'])
def read_subscription():
    subtype = request.args.get('SubType')
    customer_id = request.args.get('Customer_id')

    if subtype not in pubtypes:
        flash(f'The subtype you entered does not exist. Must be one of the following: {" ".join([ptype for ptype in pubtypes])}', 'error')
        return redirect(url_for('read'))
    if customer_id != "":
        try:
            customer_id = int(customer_id)
        except ValueError:
            flash(f'You did not enter a valid customer ID. Here is what you entered: {customer_id}', 'error')
            return redirect(url_for('read'))

    if subtype == "" and customer_id == "":
        flash('You did not enter anything to search for. Please try again. Only one parameter is required for this search.', 'error')
        return redirect(url_for('read'))
    else:
        cur = mysql.connection.cursor()
        if subtype == "":
            cur.execute('SELECT * FROM subscriptions WHERE Customer_id = %s', (customer_id,))
            subscriptions = cur.fetchall()
        elif customer_id == "":
            cur.execute('SELECT * FROM subscriptions WHERE SubType = %s', (subtype,))
            subscriptions = cur.fetchall()
        else:
            cur.execute('SELECT * FROM subscriptions WHERE SubType = %s AND Customer_id = %s', (subtype, customer_id))
            subscriptions = cur.fetchall()
    cur.close()
    return render_template('read.html', subscriptions=subscriptions)


@app.route('/read_publication', methods=['GET'])
def read_publication():
    pubname = request.args.get('PubName')
    pubtype = request.args.get('PubType')
    
    if pubtype not in pubtypes:
        flash(f'The pubtype you entered is not correct. Must be one of the following: {" ".join(pub for pub in pubtypes)}', 'error')
        return redirect(url_for('read'))
    
    cur = mysql.connection.cursor
    cur.execute('SELECT * FROM publications WHERE PubType = %s AND PubName = %s', (pubtype, pubname))    
    pubs = cur.fetchall()
    cur.close()
    
    return render_template('read.html', publications=pubs)
    
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

@app.route('/update_magazine', methods=['POST'])
def update_magazine():
    pass

@app.route('/update_newspaper', methods=['POST'])
def update_newspaper():
    pass


### handlers for delete

@app.route('/delete_customer', methods=['POST']) #done
def delete_customer():
    customer_id = request.form['Customer_id']
    f_initial = request.form['FName']
    lname = request.form['LName']
    address = request.form['Address']
    try:
        customer_id = int(customer_id)
    except ValueError:
        flash('You did not enter an integer. Customers are referred to by their ID numbers.', 'error')
        return redirect(url_for('delete'))
    
    if not f_initial.isalpha():
        flash(f'Please provide a single initial with only alphabetic characters. Here is what you entered: {f_initial}', 'error')
        return redirect(url_for('delete'))
    else:
        if not lname.isalpha():
            flash(f'Your name must have only letters in it. Here is what you entered: {lname}', 'error')
            return redirect(url_for('delete'))
        else:
            if address != "":
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM Customer WHERE IdNo = %s AND FName = %s AND LName = %s AND Address = %s", (customer_id, f_initial, lname, address))
                mysql.connection.commit()
            else:
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM Customer WHERE IdNo = %s AND FName = %s AND LName = %s", (customer_id, f_initial, lname))
                mysql.connection.commit()
                flash('Deletion successful', 'success')
    cur.close()
    return redirect(url_for('delete'))
        

@app.route('/delete_subscription', methods=['POST']) #done
def delete_subscription():
    subtype = request.form['SubType']
    customer_id = request.form['Customer_id']
    if customer_id == "":
        flash("Need to enter the Customer_id to do anything.", 'error')
        return redirect(url_for('delete'))
    else:
        error = ""
        if subtype not in pubtypes or subtype == "":
            error += f"Publication type must be either: {" ".join([ptype for ptype in pubtypes])}"
            flash(error, 'error')
            return redirect(url_for('delete'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM subscriptions WHERE subtype = %s AND customer_id = %s", (subtype, customer_id))
            mysql.connection.commit()
    flash("Record deleted successfully", 'success')
    cur.close()
                
    return redirect(url_for('delete'))
    

@app.route('/delete_publication', methods=['POST']) #done
def delete_publication():
    pubname = request.form['PubName']
    pubtype = request.form['PubType'] # if nothing is passed, the type(pubtype): <class 'str'>. which means empty string comparisons work here
        ### check if data follows rules. e.g., address has to be like 255 chars
    error = ""
    if pubname == "":
        error += "Publication Name is required for publication deletion. Publication Type is optional."
        flash(error, 'error')
        return redirect(url_for('delete'))
    
    if pubtype != "" and pubtype not in pubtypes:
        # branch off
        error += f"Publication type must be either: {" ".join([ptype for ptype in pubtypes])}"
        flash(error, 'error')
        return redirect(url_for('delete'))

    cur = mysql.connection.cursor()


    if pubtype != "":
        cur.execute("DELETE FROM publications WHERE PubName = %s AND PubType = %s", (pubname, pubtype))
        mysql.connection.commit()
    else:
        cur.execute("DELETE FROM publications WHERE PubName = %s", (pubname,))
    
    flash("Record deleted successfully", 'success')
    cur.close()
                
    return redirect(url_for('delete'))
    



if __name__ == '__main__':
    app.run(debug=True)