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
@app.route('/index', methods = ['POST', 'GET'])
def show_students():
	db_connection = connect_to_database()
	if request.method == 'GET':
		print("\n------- index GET -----")
		print("\nExecuting a sample query on the database using the credentials from db_credentials.py")
		query = 'SELECT ID, Student_Lname, Student_Fname, Student_Birthdate, Student_Year,(SELECT House_Name FROM Houses WHERE Students.House_ID = Houses.ID) FROM Students ORDER BY `Student_Lname` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print("\nTable select Result:\n",result)
		return render_template('index.html', rows=result)
	elif request.method == 'POST':
		if request.form['post_type'] == "add":
			print("\n------- index POST add -----")
			print("\nAdding a student to the database")



			# Gather input fields into variables
			first_name = request.form['first_name_input']
			last_name = request.form['last_name_input']
			birthdate = request.form['birthdate_input']
			year = request.form['year_input']
			house = request.form['house_input']

			if house == "Gryffindor":
				house = 1
			elif house == "Slytherin":
				house = 2
			elif house == "Hufflepuff":
				house = 3
			elif house == "Ravenclaw":
				house = 4

			# Construct query, payload
			query = 'INSERT INTO Students (Student_Fname,Student_Lname,Student_Birthdate,Student_Year,House_ID) VALUES(%s,%s,%s,%s,%s)'
			data = (first_name,last_name,birthdate,year,house)
			execute_query(db_connection, query, data)

		elif request.form['post_type'] == "delete":
			print("\n------- index POST delete -----")
			print("\nDeleting a student from the database")

			# Gather input fields into variable data
			ID = request.form['entry_id']

			# Construct query, with data
			query = 'DELETE FROM Students WHERE ID = %s'
			data = (ID,)
			execute_query(db_connection, query, data)



		query = 'SELECT ID, Student_Lname, Student_Fname, Student_Birthdate, Student_Year,(SELECT House_Name FROM Houses WHERE Students.House_ID = Houses.ID) FROM Students ORDER BY `Student_Lname` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print("GET FOR INDEX PAGE",result)
		return render_template('index.html', rows=result)


# Display (READ/SELECT) Houses in database
@app.route('/Houses', methods = ['POST', 'GET'])
def show_houses():
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('Showing all Houses in database')
		query = 'SELECT House_Name, House_Mascot, House_Founder, House_Head FROM Houses;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('houses.html', rows=result)
	elif request.method == 'POST':
		# Print actions to terminal
		print("Added a House to the database")

		# Gather input fields into variables
		house_name = request.form['house_name_input']
		house_mascot = request.form['house_mascot_input']
		house_founder = request.form['house_founder_input']
		house_head = request.form['house_head_input']

		# Insert Input variables into database
		query = 'INSERT INTO Houses (House_Name,House_Mascot,House_Founder,House_Head) VALUES (%s,%s,%s,%s)'
		data = (house_name,house_mascot,house_founder,house_head)
		execute_query(db_connection, query, data)

		query = 'SELECT House_Name, House_Mascot, House_Founder, House_Head FROM Houses;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('houses.html', rows=result)
	

# Display (READ/SELECT) Professors in database
@app.route('/Professors', methods = ['POST', 'GET'])
def show_professors():
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('Showing all Professors in database')
		db_connection = connect_to_database()
		query = 'SELECT ID, Professor_Lname,Professor_Fname,(SELECT House_Name FROM Houses WHERE Professors.House_ID = Houses.ID)FROM `Professors` ORDER BY `Professor_Lname` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('professors.html', rows=result)
	elif request.method == 'POST':
		# Print actions to terminal
		print("Adding a professor to the database")

		# Gather input fields into variables
		last_name = request.form['last_name_input']
		first_name = request.form['first_name_input']
		house = request.form['house_input']

		if house == "Gryffindor":
			house = 1
		elif house == "Slytherin":
			house = 2
		elif house == "Hufflepuff":
			house = 3
		elif house == "Ravenclaw":
			house = 4

		# Insert Input variables into database
		query = 'INSERT INTO Professors (Professor_Fname,Professor_Lname,House_ID) VALUES (%s,%s,%s)'
		data = (last_name,first_name,house)
		execute_query(db_connection, query, data)

		query = 'SELECT ID, Professor_Lname,Professor_Fname,(SELECT House_Name FROM Houses WHERE Professors.House_ID = Houses.ID)FROM `Professors` ORDER BY `Professor_Lname` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('professors.html', rows=result)

# Display (READ/SELECT) Classes in database
@app.route('/Classes', methods = ['POST', 'GET'])
def show_classes():
	db_connection = connect_to_database()
	if request.method == 'GET':	
		print('Showing all Classes in database')
		query = 'SELECT ID, Class_Name, Class_Credit, (SELECT Professor_Lname FROM Professors WHERE Classes.Professor_ID = Professors.ID) FROM `Classes` ORDER BY `Class_Name` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('classes.html', rows=result)
	elif request.method == 'POST':
		# Print actions to terminal
		print("Added a class to the database")

		# Gather input fields into variables
		class_title = request.form['class_title_input']
		class_credits = request.form['class_credits_input']
		professor = request.form['class_professor_input']

		# Insert Input variables into database
		query = 'INSERT INTO Classes (Class_Name,Class_Credit,Professor_ID) VALUES (%s,%s,%s)'
		data = (class_title,class_credits,professor)
		execute_query(db_connection, query, data)

		query = 'SELECT ID, Class_Name, Class_Credit, (SELECT Professor_Lname FROM Professors WHERE Classes.Professor_ID = Professors.ID) FROM `Classes` ORDER BY `Class_Name` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('classes.html', rows=result)
		

# Display (READ/SELECT) Registrations in database
@app.route('/Registrations', methods = ['POST', 'GET'])

def show_registrations():
	db_connection = connect_to_database()
	if request.method == 'GET':	
		print('Showing all Registrations in database')
		query = 'SELECT Student_ID,(SELECT Student_LName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `Last Name` , (SELECT Student_FName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `First Name` ,Class_ID, (SELECT Class_Name FROM Classes WHERE Registrations.Class_ID = Classes.ID) FROM `Registrations` ORDER BY `Last Name` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('registrations.html', rows=result)
	elif request.method == 'POST':	
		# Print actions to terminal
		print("Added a registration to the database")

		# Gather input fields into variables
		student_id = request.form['student_id_input']
		class_id = request.form['class_id_input']

		# Insert Input variables into database
		query = 'INSERT INTO Registrations (Student_ID, Class_ID)  VALUES (%s,%s)'
		data = (student_id,class_id)
		execute_query(db_connection, query, data)

		query = 'SELECT Student_ID,(SELECT Student_LName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `Last Name` , (SELECT Student_FName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `First Name` ,Class_ID, (SELECT Class_Name FROM Classes WHERE Registrations.Class_ID = Classes.ID) FROM `Registrations` ORDER BY `Last Name` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('registrations.html', rows=result)
		

		# elif student_ID_search:
		# 	query = 'SELECT Student_ID,(SELECT Student_LName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `Last Name` , (SELECT Student_FName FROM Students WHERE Registrations.Student_ID = Students.ID) AS `First Name` ,Class_ID, (SELECT Class_Name FROM Classes WHERE Registrations.Class_ID = Classes.ID) FROM `Registrations` WHERE Student_ID = (%s) ORDER BY `Last Name` ASC;'
		# 	data = student_ID_search
		# 	result = execute_query(db_connection, query,data).fetchall()
			
		# 	print(result)
		# 	return render_template('registrations.html', rows=result)






