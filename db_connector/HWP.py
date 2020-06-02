from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)


#route typed in browser
@app.route('/')
#cosmetic name of function
def homepage():
	# output html, render html page
    return "<i>Hogwarts Wizarding Portal ?</i>"

#  Students Page
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


# UPDATE students
@app.route('/update_students/<int:id>', methods=['POST','GET'])
def update_student(id):
	print('Updating student')
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('The GET request')
		student_query = 'SELECT ID, Student_Fname, Student_Lname, Student_Birthdate, Student_year from Students WHERE id = %s' % (id)
		student_result = execute_query(db_connection, student_query).fetchone()
		# query for FK columns
		house_query = 'SELECT ID, House_Name from Houses'
		house_results = execute_query(db_connection, house_query).fetchall()
		print('Returning')
		return render_template('update_students.html', house = house_results, student = student_result)
	elif request.method == 'POST':
		print('The POST request')
		first_name = request.form['first_name_input']
		last_name = request.form['last_name_input']
		birthday = request.form['birthdate_input']
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

		query = "UPDATE Students SET Student_Fname = %s, Student_Lname = %s, Student_Birthdate = %s, Student_Year = %s ,House_ID = %s WHERE id = %s"		
		data = (first_name, last_name, birthday, year, house, id)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated")

		return redirect('/index')

# Display (READ/SELECT) Houses in database
@app.route('/Houses', methods = ['POST', 'GET'])
def show_houses():
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('Showing all Houses in database')
		query = 'SELECT House_Name, House_Mascot, House_Founder, House_Head, ID FROM Houses;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('houses.html', rows=result)
	elif request.method == 'POST':
		if request.form['post_type'] == "add":
			# Print actions to terminal
			print("\n------- Houses POST add -----")
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


		elif request.form['post_type'] == "delete":
			print("\n------- Houses POST delete -----")
			print("\nDeleting a house from the database")

			# Gather input fields into variable data
			ID = request.form['entry_id']

			# Construct query, with data
			query = 'DELETE FROM Houses WHERE ID = %s'
			data = (ID,)
			execute_query(db_connection, query, data)
		
		# Display table
		query = 'SELECT House_Name, House_Mascot, House_Founder, House_Head, ID FROM Houses;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('houses.html', rows=result)

# UPDATE houses
@app.route('/update_houses/<int:id>', methods=['POST','GET'])
def update_house(id):
	print('Updating house')
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('The GET request')
		house_query = 'SELECT ID, House_Name, House_Mascot, House_Founder, House_Head from Houses WHERE id = %s' % (id)
		house_results = execute_query(db_connection, house_query).fetchone()
		print('Returning')
		return render_template('update_houses.html', house = house_results)
	elif request.method == 'POST':
		print('The POST request')
		name = request.form['house_name_input']
		mascot = request.form['house_mascot_input']
		founder = request.form['house_founder_input']
		head = request.form['house_head_input']
		



		query = "UPDATE Houses SET House_Name = %s, House_Mascot = %s, House_Founder = %s, House_Head = %s WHERE id = %s"		
		data = (name, mascot, founder, head, id)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated")
		
		return redirect('/Houses')


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
		if request.form['post_type'] == "add":
			# Print actions to terminal
			print("\n------- Professors POST add -----")
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
			elif house == "None":
				house = None

			# Insert Input variables into database
			query = 'INSERT INTO Professors (Professor_Fname,Professor_Lname,House_ID) VALUES (%s,%s,%s)'
			data = (first_name,last_name,house)
			execute_query(db_connection, query, data)

		if request.form['post_type'] == "delete":
			print("\n------- Professors POST delete -----")
			print("\nDeleting a house from the database")

			# Gather input fields into variable data
			ID = request.form['entry_id']

			# Construct query, with data
			query = 'DELETE FROM Professors WHERE ID = %s'
			data = (ID,)
			execute_query(db_connection, query, data)

		# Display Table
		query = 'SELECT ID, Professor_Lname,Professor_Fname,(SELECT House_Name FROM Houses WHERE Professors.House_ID = Houses.ID)FROM `Professors` ORDER BY `Professor_Lname` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('professors.html', rows=result)


@app.route('/update_professors/<int:id>', methods=['POST','GET'])
def update_professor(id):
	print('Updating professor')
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('The GET request')
		professor_query = 'SELECT ID, Professor_Fname, Professor_Lname, House_ID from Professors WHERE id = %s' % (id)
		professor_result = execute_query(db_connection,professor_query).fetchone()
		print('Returning')
		return render_template('update_professors.html', professor = professor_result)
	elif request.method == 'POST':
		print('The POST request')
		first_name = request.form['first_name_input']
		last_name = request.form['last_name_input']
		house = request.form['house_input']
		if house == "Gryffindor":
			house = 1
		elif house == "Slytherin":
			house = 2
		elif house == "Hufflepuff":
			house = 3
		elif house == "Ravenclaw":
			house = 4
		elif house == "None":
			house = None

		query = "UPDATE Professors SET Professor_Fname = %s, Professor_Lname = %s, House_ID = %s WHERE id = %s"		
		data = (first_name, last_name, house, id)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated")
		return redirect('/Professors')

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
		if request.form['post_type'] == "add":
			# Print actions to terminal
			print("\n------- Classes POST delete -----")
			print("Added a class to the database")

			# Gather input fields into variables
			class_title = request.form['class_title_input']
			class_credits = request.form['class_credits_input']
			professor = request.form['class_professor_input']

			# Insert Input variables into database
			query = 'INSERT INTO Classes (Class_Name,Class_Credit,Professor_ID) VALUES (%s,%s,%s)'
			data = (class_title,class_credits,professor)
			execute_query(db_connection, query, data)
		
		if request.form['post_type'] == "delete":
			print("\n------- Classes POST delete -----")
			print("\nDeleting a class from the database")

			# Gather input fields into variable data
			ID = request.form['entry_id']

			# Construct query, with data
			query = 'DELETE FROM Classes WHERE ID = %s'
			data = (ID,)
			execute_query(db_connection, query, data)

		# Display Table
		query = 'SELECT ID, Class_Name, Class_Credit, (SELECT Professor_Lname FROM Professors WHERE Classes.Professor_ID = Professors.ID) FROM `Classes` ORDER BY `Class_Name` ASC;'
		result = execute_query(db_connection, query).fetchall()
		print(result)
		return render_template('classes.html', rows=result)

#display update form and process any updates, using the same function
@app.route('/update_classes/<int:id>', methods=['POST','GET'])
def update_class(id):
	print('Updating class')
	db_connection = connect_to_database()
	if request.method == 'GET':
		print('The GET request')
		classes_query = 'SELECT ID, Class_Name, Class_Credit, Professor_ID from Classes WHERE id = %s' % (id)
		classes_result = execute_query(db_connection,classes_query).fetchone()
		print('Returning')
		return render_template('update_classes.html', classes = classes_result)
	elif request.method == 'POST':
		print('The POST request')
		class_name = request.form['class_title_input']
		class_credit = request.form['class_credits_input']
		professor = request.form['class_professor_input']
		query = "UPDATE Classes SET Class_Name = %s, Class_Credit = %s, Professor_ID = %s WHERE id = %s"		
		data = (class_name, class_credit, professor, id)
		result = execute_query(db_connection, query, data)
		print(str(result.rowcount) + " row(s) updated")
		return redirect('/Classes')
		

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
		if request.form['post_type'] == "add":
			# Print actions to terminal
			print("\n------- Registrations POST add -----")
			print("Added a registration to the database")

			# Gather input fields into variables
			student_id = request.form['student_id_input']
			class_id = request.form['class_id_input']

			# Insert Input variables into database
			query = 'INSERT INTO Registrations (Student_ID, Class_ID)  VALUES (%s,%s)'
			data = (student_id,class_id)
			execute_query(db_connection, query, data)
		if request.form['post_type'] == "delete":
			print("\n------- Registrations POST delete -----")
			print("\nDeleting a registration from the database")

			# Gather input fields into variable data
			registration_student_id = request.form['registration_student_id']
			registration_class_id = request.form['registration_class_id']

			# Construct query, with data
			query = 'DELETE FROM Registrations WHERE Student_ID = %s AND Class_ID = %s'
			data = (registration_student_id, registration_class_id)
			execute_query(db_connection, query, data)

		# Display Table
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






