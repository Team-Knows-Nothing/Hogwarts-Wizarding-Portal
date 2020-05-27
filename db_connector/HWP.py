from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)

#the route is what you will type in browser
@app.route('/hello')
#the name of this function is just a cosmetic thing
def hello():
    #this is the output returned to browser
    return "Hello worldDDDDD!"

@app.route('/')
def index():
    return "<i>Are you looking for /db-test or /hello ?</i>"

# Display Students
@app.route('/index')
def show_students():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = 'SELECT ID, Student_Lname, Student_Fname, Student_Birthdate, Student_Year,(SELECT House_Name FROM Houses WHERE Students.House_ID = Houses.ID) FROM Students ORDER BY `Student_Lname` ASC;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('index.html', rows=result)


# Display (READ/SELECT) Houses in database
@app.route('/Houses')
def show_houses():

	print('Showing all Houses in database')
	db_connection = connect_to_database()
	query = 'SELECT House_Name, House_Mascot, House_Founder, House_Head FROM Houses;'
	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('houses.html', rows=result)

# Display (READ/SELECT) Professors in database
@app.route('/Professors')
def show_professors():
	print('Showing all Professors in database')
	db_connection = connect_to_database()
	query = 'SELECT Professor_Lname,Professor_Fname,(SELECT House_Name FROM Houses WHERE Professors.House_ID = Houses.ID)FROM `Professors` ORDER BY `Professor_Lname` ASC;'
	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('professors.html', rows=result)

# Display (READ/SELECT) Classes in database
@app.route('/Classes')
def show_classes():
	print('Showing all Classes in database')
	db_connection = connect_to_database()
	query = 'SELECT ID, Class_Name, Class_Credit, (SELECT Professor_Lname FROM Professors WHERE Classes.Professor_ID = Professors.ID) FROM `Classes` ORDER BY `Class_Name` ASC;'
	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('classes.html', rows=result)

# Display (READ/SELECT) Registrations in database
@app.route('/Registrations')

def show_registrations():

	print('Showing all Registrations in database')
	db_connection = connect_to_database()
	query = 'SELECT Student_ID,(SELECT Student_LName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `Last Name` , (SELECT Student_FName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `First Name` ,Class_ID, (SELECT Class_Name FROM Classes WHERE Registrations.Class_ID = Classes.ID) FROM `Registrations` ORDER BY `Last Name` ASC;'
	result = execute_query(db_connection, query).fetchall()
	print(result)
	return render_template('registrations.html', rows=result)



