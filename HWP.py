# Project Group 5
# Team Knows Nothing
# Members: Richard Nguyen, Travis Moret
# URL: http://flip2.engr.oregonstate.edu:5640/

# Import Flask libraries
from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

#create the application for routing
webapp = Flask(__name__)

# Create Routes for CRUD functionality for each page


############### CRUD for Students Page ###############


# Display (READ/SELECT) Students in database
@webapp.route('/index')

def show_students():
   
   print('Showing all students in database')
   db_connection = connect_to_database()
   query = 'SELECT ID, Student_Lname, Student_Fname, Student_Birthdate, Student_Year,(SELECT House_Name FROM Houses WHERE Students.House_ID = Houses.ID) FROM Students ORDER BY Student_Lname ASC;'
   result = execute_query(db_connection, query).fetchall()
   print(result)
   return render_template('index.html', rows=result)


# Add (INSERT) Students into database
@webapp.route('/insert_student', methods=['POST'])

def insert_student():

   # Connect to database
   db_connection = connect_to_database()

   if request.method == 'POST':
      # Print actions to terminal
      print("Added a student to the database")

      # Gather input fields into variables
      first_name = request.form['first_name_input']
      last_name = request.form['last_name_input']
      birthdate = request.form['birthdate_input']
      year = request.form['year_input']
      house = request.form['house_input']

      # Insert Input variables into database
      query = 'INSERT INTO Students (Student_Fname,Student_Lname,Student_Birthdate,Student_Year,House_ID) VALUES(%s,%s,%s,%s,%s)'
      data = (first_name,last_name,birthdate,year,house)
      execute_query(db_connection, query, data)
      return ('Student added')


# DELETE Student from the database


# UPDATE Student information in database


############### CRUD for Houses Page ###############


# Display (READ/SELECT) Houses in database
@webapp.route('/houses')

def show_houses():
   
   print('Showing all Houses in database')
   db_connection = connect_to_database()
   query = 'SELECT House_Name, House_Mascot, House_Founder, House_Head FROM Houses;'
   result = execute_query(db_connection, query).fetchall()
   print(result)
   return render_template('Houses.html', rows=result)


# Add (INSERT) a House into database
@webapp.route('/insert_house', methods=['POST'])

def insert_house():

   # Connect to database
   db_connection = connect_to_database()

   if request.method == 'POST':
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
      return ('House added')


# DELETE a House from the database


# UPDATE House information in database


############### CRUD for Professors Page ###############


# Display (READ/SELECT) Professors in database
@webapp.route('/professors')

def show_professors():
   
   print('Showing all Professors in database')
   db_connection = connect_to_database()
   query = 'SELECT Professor_Lname,Professor_Fname,(SELECT House_Name FROM Houses WHERE Professors.House_ID = Houses.ID)FROM `Professors` ORDER BY `Professor_Lname` ASC;'
   result = execute_query(db_connection, query).fetchall()
   print(result)
   return render_template('Professors.html', rows=result)


# Add (INSERT) a Professor into database
@webapp.route('/insert_professor', methods=['POST'])

def insert_professor():

   # Connect to database
   db_connection = connect_to_database()

   if request.method == 'POST':
      # Print actions to terminal
      print("Added a professor to the database")

      # Gather input fields into variables
      last_name = request.form['last_name_input']
      first_name = request.form['first_name_input']
      house = request.form['house_input']

      # Insert Input variables into database
      query = 'INSERT INTO Professors (Professor_Fname,Professor_Lname,House_ID) VALUES (%s,%s,%s)'
      data = (last_name,first_name,house)
      execute_query(db_connection, query, data)
      return ('Professor added')


# DELETE a Professor from the database


# UPDATE Professor information in database


############### CRUD for Classes Page ###############


# Display (READ/SELECT) Classes in database
@webapp.route('/classes')

def show_classes():
   
   print('Showing all Classes in database')
   db_connection = connect_to_database()
   query = 'SELECT ID, Class_Name, Class_Credit, (SELECT Professor_Lname FROM Professors WHERE Classes.Professor_ID = Professors.ID) FROM `Classes` ORDER BY `Class_Name` ASC;'
   result = execute_query(db_connection, query).fetchall()
   print(result)
   return render_template('Classes.html', rows=result)


# Add (INSERT) a Class into database
@webapp.route('/insert_class', methods=['POST'])

def insert_class():

   # Connect to database
   db_connection = connect_to_database()

   if request.method == 'POST':
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
      return ('Class added')


# DELETE a Class from the database


# UPDATE Class information in database


############### CRUD for Registrations Page ###############


# Display (READ/SELECT) Registrations in database
@webapp.route('/registrations')

def show_registrations():
   
   print('Showing all Registrations in database')
   db_connection = connect_to_database()
   query = 'SELECT Student_ID,(SELECT Student_LName FROM Students WHERE Registrations.Student_ID = Students.ID), (SELECT Student_FName FROM Students WHERE Registrations.Student_ID = Students.ID),Class_ID, (SELECT Class_Name FROM Classes WHERE Registrations.Class_ID = Classes.ID)FROM `Registrations` ORDER BY `Student_Lname` ASC;'
   result = execute_query(db_connection, query).fetchall()
   print(result)
   return render_template('Registrations.html', rows=result)


# Add (INSERT) a Registration into database
@webapp.route('/insert_registrations', methods=['POST'])

def insert_class():

   # Connect to database
   db_connection = connect_to_database()

   if request.method == 'POST':
      # Print actions to terminal
      print("Added a registration to the database")

      # Gather input fields into variables
      student_id = request.form['student_id_input']
      class_id = request.form['class_id_input']

      # Insert Input variables into database
      query = 'INSERT INTO Registrations (Student_ID, Class_ID)  VALUES (%s,%s)'
      data = (student_id,class_id)
      execute_query(db_connection, query, data)
      return ('Registration added')


# DELETE a Registration from the database


