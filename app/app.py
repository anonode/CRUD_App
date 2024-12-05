from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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
    SubType = request.form['SubType']
    Customer_id = request.form['Customer_id']
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO subscriptions (SubType, Customer_id) VALUES (%s, %s)", (SubType, Customer_id))
    mysql.connection.commit()
    cursor.close()

    flash('Subscription added successfully!', 'success')
    return redirect(url_for('create'))


@app.route('/create_publication', methods=['POST'])
def create_publication():
    pubname = request.form['PubName']
    pubtype = request.form['PubType']

    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO publications (PubName, PubType) VALUES (%s, %s)", (pubname, pubtype))
    mysql.connection.commit()
    cursor.close()

    flash('Publication added successfully!', 'success')
    return redirect(url_for('create'))

@app.route('/create_magazine', methods=['POST'])
def create_magazine():
    start_date_str = request.form['StartDate']
    number_of_issues = request.form['NumberOfIssues']
    price = request.form['Price']
    sub_id = request.form['SubId']
    customer_id = request.form['Customer_id']
    frequency = request.form['frequency']
    
    
    # check for subid
    if sub_id == "":
        flash('please enter a subscription ID', 'error')
        return redirect(url_for('create'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM subscriptions WHERE SubId = %s', (sub_id,))
    check = cur.fetchone()
    cur.close()
    if not check:
        flash('Subscription ID does not exist in database', 'error')
        return redirect(url_for('create'))
    
    
    
    # convert date to datetime object
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()  # Expecting "YYYY-MM-DD" format
    except ValueError:
        flash('Invalid date format for Start Date. Please use YYYY-MM-DD.', 'error')
        return redirect(url_for('create'))

    # Calculate the end date based on the number of issues and the subscription type
    try:
        number_of_issues = int(number_of_issues)  # Convert to integer
    except ValueError:
        flash('Number of issues must be a number.', 'error')
        return redirect(url_for('create'))

    end_date = None

    if frequency == 'weekly':
        # Calculate end date for weekly subscription
        end_date = start_date + timedelta(weeks=number_of_issues)
    elif frequency == 'monthly':
        # Calculate end date for monthly subscription
        end_date = start_date + relativedelta(months=number_of_issues)
    elif frequency == 'quarterly':
        # Calculate end date for quarterly subscription
        end_date = start_date + relativedelta(months=3 * number_of_issues)
    else:
        flash('Invalid subscription type. Please choose from weekly, monthly, or quarterly.', 'error')
        return redirect(url_for('create'))

    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO magazine (NumberOfIssues, StartDate, EndDate, Price, Frequency, SubId, Customer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (number_of_issues, start_date, end_date, price, frequency, sub_id, customer_id))
        mysql.connection.commit()
        flash('Magazine subscription created successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'An error occurred while creating the subscription: {str(e)}', 'error')
    finally:
        cur.close()

    return redirect(url_for('create'))

@app.route('/create_newspaper', methods=['POST'])
def create_newspaper():
    start_date = request.form['StartDate']
    number_of_months = int(request.form['NumberOfMonths'])
    price_per_month = float(request.form['Price'])
    sub_id = int(request.form['SubId'])
    customer_id = int(request.form['Customer_id'])
    frequency = request.form['frequency']  # 7-day, 5-day, 2-day
    
    
    # check for valid subid
    if sub_id == "":
        flash('please enter a subscription ID', 'error')
        return redirect(url_for('create'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM subscriptions WHERE SubId = %s', (sub_id,))
    check = cur.fetchone()
    cur.close()
    if not check:
        flash('Subscription ID does not exist in database', 'error')
        return redirect(url_for('create'))    
    
    
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Calculate end date based on the subscription duration
    if frequency == '2-day':  # Weekend subscription
        # Calculate the end date by adding the number of months to the start date
        end_date = start_date + relativedelta(months=number_of_months)

        # Calculate the number of weekends (Saturday and Sunday) in the specified months
        weekends_count = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == 5 or current_date.weekday() == 6:  # Saturday (5) or Sunday (6)
                weekends_count += 1
            current_date += timedelta(days=1)
        
        # For a 2-day subscription, you charge for weekends (Saturdays and Sundays) within the month(s)
        total_price = weekends_count * (price_per_month / 4)  # Roughly assuming 4 weekends per month

    elif frequency == '5-day':  # Weekdays (Monday to Friday) subscription
        end_date = start_date + relativedelta(months=number_of_months)
        total_price = price_per_month * number_of_months  # Price for weekdays

    elif frequency == '7-day':  # 7-day subscription (all days)
        end_date = start_date + relativedelta(months=number_of_months)
        total_price = price_per_month * number_of_months  # Price for all days

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO newspaper (NumberOfMonths, StartDate, EndDate, Price, SubType, SubId, Customer_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (number_of_months, start_date, end_date, total_price, frequency, sub_id, customer_id))
    mysql.connection.commit()
    cur.close()

    flash('Newspaper subscription created successfully!', 'success')
    return redirect(url_for('create'))



######## HANDLERS FOR READ

@app.route('/read_customer', methods=['GET'])
def read_customer():
    customer_id = request.args.get('Customer_id')
    f_initial = request.args.get('FName')
    lname = request.args.get('LName')
    address = request.args.get('Address')

    if customer_id == "" and f_initial == "" and lname == "" and address == "":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customer")
        customers = cur.fetchall()
        return render_template('read.html', customers=customers)
    if customer_id:
        try:
            customer_id = int(customer_id)
        except ValueError:
            flash(f'You did not enter a valid integer for Customer_ID. Here is what you entered: {customer_id}', 'error')
            return redirect(url_for('read'))

    set_clauses = []
    params = []

    if customer_id != "":
        set_clauses.append("IdNo = %s")
        params.append(customer_id)
    if f_initial != "":
        set_clauses.append("FName LIKE %s")
        params.append(f"%{f_initial}%") 
    if lname != "":
        set_clauses.append("LName LIKE %s")
        params.append(f"%{lname}%") 
    if address != "":
        set_clauses.append("Address LIKE %s")
        params.append(f"%{address}%")

    if set_clauses:
        where_clause = " AND ".join(set_clauses)
        query = f"SELECT * FROM customer WHERE {where_clause};"
    else:
        flash('You must enter at least one parameter to search for a customer.', 'error')
        return redirect(url_for('read'))

    cur = mysql.connection.cursor()
    cur.execute(query, tuple(params))
    customers = cur.fetchall()
    cur.close()

    if customers:
        return render_template('read.html', customers=customers)
    else:
        flash('No customers found based on the given parameters.', 'error')
        return redirect(url_for('read'))

@app.route('/read_subscription', methods=['GET'])
def read_subscription():
    subtype = request.args.get('SubType')
    customer_id = request.args.get('Customer_id')

    # Handle invalid subscription type
    if subtype != "" and subtype not in pubtypes:
        flash(f'The subtype you entered does not exist. Must be one of the following: {" ".join([ptype for ptype in pubtypes])}', 'error')
        return redirect(url_for('read'))
    
    # Handle customer ID validity
    if customer_id != "":
        try:
            customer_id = int(customer_id)
        except ValueError:
            flash(f'You did not enter a valid customer ID. Here is what you entered: {customer_id}', 'error')
            return redirect(url_for('read'))

    cur = mysql.connection.cursor()
    
    # If both subtype and customer_id are empty, fetch all subscription data
    if subtype == "" and customer_id == "":
        cur.execute("""
            SELECT s.*, 
                   m.NumberOfIssues, m.Frequency AS MagazineFrequency, m.Price AS MagazinePrice,
                   n.NumberOfMonths, n.Frequency AS NewspaperFrequency, n.Price AS NewspaperPrice,
                   p.PubName AS MagazineTitle, p.PubType, p.Frequency AS PublicationFrequency
            FROM subscriptions s
            LEFT JOIN magazine m ON s.SubId = m.SubId
            LEFT JOIN newspaper n ON s.SubId = n.SubId
            LEFT JOIN publications p ON m.Frequency = p.Frequency
        """)
        subscriptions = cur.fetchall()
    # If only customer_id is provided, fetch subscriptions for the given customer
    elif subtype == "":
        cur.execute("""
            SELECT s.*, 
                   m.NumberOfIssues, m.Frequency AS MagazineFrequency, m.Price AS MagazinePrice,
                   n.NumberOfMonths, n.Frequency AS NewspaperFrequency, n.Price AS NewspaperPrice,
                   p.PubName AS MagazineTitle, p.PubType, p.Frequency AS PublicationFrequency
            FROM subscriptions s
            LEFT JOIN magazine m ON s.SubId = m.SubId
            LEFT JOIN newspaper n ON s.SubId = n.SubId
            LEFT JOIN publications p ON m.Frequency = p.Frequency
            WHERE s.Customer_id = %s
        """, (customer_id,))
        subscriptions = cur.fetchall()
    # If only subtype is provided, fetch subscriptions for the given subscription type
    elif customer_id == "":
        cur.execute("""
            SELECT s.*, 
                   m.NumberOfIssues, m.Frequency AS MagazineFrequency, m.Price AS MagazinePrice,
                   n.NumberOfMonths, n.Frequency AS NewspaperFrequency, n.Price AS NewspaperPrice,
                   p.PubName AS MagazineTitle, p.PubType, p.Frequency AS PublicationFrequency
            FROM subscriptions s
            LEFT JOIN magazine m ON s.SubId = m.SubId
            LEFT JOIN newspaper n ON s.SubId = n.SubId
            LEFT JOIN publications p ON m.Frequency = p.Frequency
            WHERE s.SubType = %s
        """, (subtype,))
        subscriptions = cur.fetchall()
    # If both subtype and customer_id are provided, fetch subscriptions for both
    else:
        cur.execute("""
            SELECT s.*, 
                   m.NumberOfIssues, m.Frequency AS MagazineFrequency, m.Price AS MagazinePrice,
                   n.NumberOfMonths, n.Frequency AS NewspaperFrequency, n.Price AS NewspaperPrice,
                   p.PubName AS MagazineTitle, p.PubType, p.Frequency AS PublicationFrequency
            FROM subscriptions s
            LEFT JOIN magazine m ON s.SubId = m.SubId
            LEFT JOIN newspaper n ON s.SubId = n.SubId
            LEFT JOIN publications p ON m.Frequency = p.Frequency
            WHERE s.SubType = %s AND s.Customer_id = %s
        """, (subtype, customer_id))
        subscriptions = cur.fetchall()
    
    cur.close()
    return render_template('read.html', subscriptions=subscriptions)



@app.route('/read_publication', methods=['GET'])
def read_publication():
    pubname = request.args.get('PubName')
    pubtype = request.args.get('PubType')
    if pubname == "" and pubtype == "":
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM publications")
        publications = cur.fetchall()
        cur.close()
        return render_template('read.html', publications=publications)
    if pubtype not in pubtypes:
        flash(f'The pubtype you entered is not correct. Must be one of the following: {" ".join(pub for pub in pubtypes)}', 'error')
        return redirect(url_for('read'))
    
    cur = mysql.connection.cursor
    cur.execute('SELECT * FROM publications WHERE PubType = %s AND PubName = %s', (pubtype, pubname))    
    pubs = cur.fetchall()
    cur.close()
    
    return render_template('read.html', publications=pubs)

@app.route('/read_magazine', methods=['GET'])
def read_magazine():
    sub_id = request.args.get('SubId')
    customer_id = request.args.get('Customer_id')
    num_of_issues = request.args.get('NumberOfIssues')
    start_date = request.args.get('StartDate')
    end_date = request.args.get('EndDate')
    
    
    print(f"{type(sub_id)}, {type(customer_id)}, {type(num_of_issues)}, {type(start_date)}, {type(end_date)}")
    if all(form == "" for form in [sub_id, customer_id, num_of_issues, start_date, end_date]):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM magazine')
        magazines = cur.fetchall()
        cur.close()
        return render_template('read.html', magazines=magazines)
    try:
        if sub_id:
            sub_id = int(sub_id)
    except ValueError:
        flash(f'Invalid SubId. Here is what you entered: {sub_id}', 'error')
        return redirect(url_for('read'))

    try:
        if customer_id:
            customer_id = int(customer_id)
    except ValueError:
        flash(f'Invalid Customer_id. Here is what you entered: {customer_id}', 'error')
        return redirect(url_for('read'))

    set_clauses = []
    params = []

    if sub_id:
        set_clauses.append("SubId = %s")
        params.append(sub_id)
    if customer_id:
        set_clauses.append("Customer_id = %s")
        params.append(customer_id)
    if num_of_issues:
        set_clauses.append("NumberOfIssues LIKE %s")
        params.append(f"%{num_of_issues}%")
    if start_date:
        set_clauses.append("StartDate = %s")
        params.append(start_date)
    if end_date:
        set_clauses.append("EndDate = %s")
        params.append(end_date)

    if set_clauses:
        where_clause = " AND ".join(set_clauses)
        query = f"SELECT * FROM magazine WHERE {where_clause};"
    else:
        flash('Please enter at least one search criterion for the magazine.', 'error')
        return redirect(url_for('read'))

    cur = mysql.connection.cursor()
    cur.execute(query, tuple(params))
    magazines = cur.fetchall()
    cur.close()

    if magazines:
        return render_template('read.html', magazines=magazines)
    else:
        flash('No magazines found based on the given criteria.', 'error')
        return redirect(url_for('read'))

@app.route('/read_newspaper', methods=['GET'])
def read_newspaper():
    sub_id = request.args.get('SubId')
    customer_id = request.args.get('Customer_id')
    num_of_months = request.args.get('NumberOfMonths')
    start_date = request.args.get('StartDate')
    end_date = request.args.get('EndDate')

    if all(form == "" for form in [sub_id, customer_id, num_of_months, start_date, end_date]):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM magazine')
        newspapers = cur.fetchall()
        cur.close()
        return render_template('read.html', newspapers=newspapers)
    try:
        if sub_id:
            sub_id = int(sub_id)
    except ValueError:
        flash(f'Invalid SubId. Here is what you entered: {sub_id}', 'error')
        return redirect(url_for('read'))

    try:
        if customer_id:
            customer_id = int(customer_id)
    except ValueError:
        flash(f'Invalid Customer_id. Here is what you entered: {customer_id}', 'error')
        return redirect(url_for('read'))

    set_clauses = []
    params = []

    if sub_id:
        set_clauses.append("SubId = %s")
        params.append(sub_id)
    if customer_id:
        set_clauses.append("Customer_id = %s")
        params.append(customer_id)
    if num_of_months:
        set_clauses.append("NumberOfMonths = %s")
        params.append(num_of_months)
    if start_date:
        set_clauses.append("StartDate = %s")
        params.append(start_date)
    if end_date:
        set_clauses.append("EndDate = %s")
        params.append(end_date)

    if set_clauses:
        where_clause = " AND ".join(set_clauses)
        query = f"SELECT * FROM newspaper WHERE {where_clause};"
    else:
        flash('Please enter at least one search criterion for the newspaper.', 'error')
        return redirect(url_for('read'))

    cur = mysql.connection.cursor()
    cur.execute(query, tuple(params))
    newspapers = cur.fetchall()
    cur.close()

    if newspapers:
        return render_template('read.html', newspapers=newspapers)
    else:
        flash('No newspapers found based on the given criteria.', 'error')
        return redirect(url_for('read'))

### handlers for update

@app.route('/update_customer', methods=['POST'])
def update_customer():
    f_initial = request.form['FName']
    lname = request.form['LName']
    address = request.form['Address']
    customer_id = request.form['Customer_id']

    if not customer_id.isdigit():
        flash(f'You did not enter a natural number for the customer_id. Here is what you entered: {customer_id}')
        return redirect(url_for('update'))
    if lname == "" and address == "" and f_initial == "":
        flash('You need to enter at least one parameter to update', 'error')
        return redirect(url_for('update'))
    
    set_clauses = []
    params = []
    if f_initial != "":
        set_clauses.append("FName = %s")
        params.append(f_initial)

    if lname != "":
        set_clauses.append("LName = %s")
        params.append(lname)

    if address != "":
        set_clauses.append("Address = %s")
        params.append(address)
    
    params.append(customer_id)

    setclause = ", ".join(set_clauses)
    cur = mysql.connection.cursor()
    query = f"UPDATE customer SET {setclause} WHERE IdNo = %s"
    cur.execute(query, tuple(params))
    mysql.connection.commit()
    cur.close()
    flash('Update done successfully', 'success')
    return redirect(url_for('update'))
    
@app.route('/update_subscription', methods=['POST'])
def update_subscription():
    customer_id = request.form['Customer_id']
    subtype = request.form['subtype']
    
    if subtype not in pubtypes:
        flash('the subtype you entered is not valid. try again.', 'error')
        return redirect(url_for('update'))
    cur = mysql.connection.cursor()
    cur.execute("UPDATE subscription SET SubType = %s WHERE Customer_id = %s", (subtype, customer_id))
    mysql.connection.commit()
    cur.close()
    flash('update of subscriptions done successfully.', 'success')
    return redirect(url_for('update'))

@app.route('/update_publication', methods=['POST'])
def update_publication():
    pubname = request.form['PubName']
    pubtype = request.form['PubType']
    
    if pubtype not in pubtypes:
        flash(f'Invalid Pubtype. Try again. You entered: {pubtype}', 'error')
        return redirect(url_for('update'))
    cur = mysql.connection.cursor()
    cur.execute('UPDATE publications SET PubType = %s WHERE PubName = %s', (pubtype, pubname))
    mysql.connction.commit()
    cur.close()
    flash('update of publications done successfully', 'success')
    return redirect(url_for('update'))

@app.route('/update_magazine', methods=['POST'])
def update_magazine():
    mag_id = request.form['MagId']
    num_of_issues = request.form['NumberOfIssues']
    start_date = request.form['StartDate']
    end_date = request.form['EndDate']
    price = request.form['Price']
    sub_id = request.form['SubId']
    customer_id = request.form['Customer_id']

    if not mag_id.isdigit():
        flash(f'You did not enter a natural number for the MagId. Here is what you entered: {mag_id}')
        return redirect(url_for('update'))
    
    if num_of_issues == "" and start_date == "" and end_date == "" and price == "":
        flash('You need to enter at least one parameter to update', 'error')
        return redirect(url_for('update'))
    
    set_clauses = []
    params = []

    if num_of_issues != "":
        set_clauses.append("NumberOfIssues = %s")
        params.append(num_of_issues)

    if start_date != "":
        set_clauses.append("StartDate = %s")
        params.append(start_date)

    if end_date != "":
        set_clauses.append("EndDate = %s")
        params.append(end_date)

    if price != "":
        set_clauses.append("Price = %s")
        params.append(price)

    if sub_id != "":
        set_clauses.append("SubId = %s")
        params.append(sub_id)

    if customer_id != "":
        set_clauses.append("Customer_id = %s")
        params.append(customer_id)

    set_clause = ", ".join(set_clauses)
    cur = mysql.connection.cursor()
    query = f"UPDATE magazine SET {set_clause} WHERE MagId = %s"
    params.append(mag_id)
    cur.execute(query, tuple(params))
    mysql.connection.commit()
    cur.close()
    flash('Magazine update done successfully', 'success')
    return redirect(url_for('update'))

@app.route('/update_newspaper', methods=['POST'])
def update_newspaper():
    news_id = request.form['NewsId']
    num_of_months = request.form['NumberOfMonths']
    start_date = request.form['StartDate']
    end_date = request.form['EndDate']
    price = request.form['Price']
    sub_id = request.form['SubId']
    customer_id = request.form['Customer_id']

    if not news_id.isdigit():
        flash(f'You did not enter a natural number for the NewsId. Here is what you entered: {news_id}')
        return redirect(url_for('update'))
    
    if num_of_months == "" and start_date == "" and end_date == "" and price == "":
        flash('You need to enter at least one parameter to update', 'error')
        return redirect(url_for('update'))
    
    set_clauses = []
    params = []

    if num_of_months != "":
        set_clauses.append("NumberOfMonths = %s")
        params.append(num_of_months)

    if start_date != "":
        set_clauses.append("StartDate = %s")
        params.append(start_date)

    if end_date != "":
        set_clauses.append("EndDate = %s")
        params.append(end_date)

    if price != "":
        set_clauses.append("Price = %s")
        params.append(price)

    #update the SubId or Customer_id if they are included (ensure validation)
    if sub_id != "":
        set_clauses.append("SubId = %s")
        params.append(sub_id)

    if customer_id != "":
        set_clauses.append("Customer_id = %s")
        params.append(customer_id)

    set_clause = ", ".join(set_clauses)
    cur = mysql.connection.cursor()
    query = f"UPDATE newspaper SET {set_clause} WHERE NewsId = %s"
    params.append(news_id)
    cur.execute(query, tuple(params))
    mysql.connection.commit()
    cur.close()
    flash('Newspaper update done successfully', 'success')
    return redirect(url_for('update'))



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
                flash('Deletion successful', 'success')
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

@app.route('/delete_magazine', methods=['POST'])
def delete_magazine():
    mag_id = request.form['MagId']
    sub_id = request.form['SubId']
    customer_id = request.form['Customer_id']
    
    try:
        mag_id = int(mag_id)
    except ValueError:
        flash('Magazine ID should be an integer. Here is what you entered: ' + mag_id, 'error')
        return redirect(url_for('delete'))
    
    if customer_id == "":
        flash("Customer ID is required to delete the magazine subscription.", 'error')
        return redirect(url_for('delete'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM magazine WHERE MagId = %s AND SubId = %s AND Customer_id = %s", (mag_id, sub_id, customer_id))
    magazine = cur.fetchone()
    
    if not magazine:
        flash("No matching magazine found to delete.", 'error')
        cur.close()
        return redirect(url_for('delete'))

    cur.execute("DELETE FROM magazine WHERE MagId = %s AND SubId = %s AND Customer_id = %s", (mag_id, sub_id, customer_id))
    mysql.connection.commit()
    cur.close()
    flash("Magazine record deleted successfully.", 'success')
    
    return redirect(url_for('delete'))

@app.route('/delete_newspaper', methods=['POST'])
def delete_newspaper():
    news_id = request.form['NewsId']
    sub_id = request.form['SubId']
    customer_id = request.form['Customer_id']
    
    try:
        news_id = int(news_id)
    except ValueError:
        flash('Newspaper ID should be an integer. Here is what you entered: ' + news_id, 'error')
        return redirect(url_for('delete'))
    
    if customer_id == "":
        flash("Customer ID is required to delete the newspaper subscription.", 'error')
        return redirect(url_for('delete'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM newspaper WHERE NewsId = %s AND SubId = %s AND Customer_id = %s", (news_id, sub_id, customer_id))
    newspaper = cur.fetchone()
    
    if not newspaper:
        flash("No matching newspaper found to delete.", 'error')
        cur.close()
        return redirect(url_for('delete'))

    cur.execute("DELETE FROM newspaper WHERE NewsId = %s AND SubId = %s AND Customer_id = %s", (news_id, sub_id, customer_id))
    mysql.connection.commit()
    cur.close()
    flash("Newspaper record deleted successfully.", 'success')
    
    return redirect(url_for('delete'))


if __name__ == '__main__':
    app.run(debug=True)