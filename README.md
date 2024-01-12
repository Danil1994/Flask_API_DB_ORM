### INSTALL

1. Run 'git clone https://github.com/Danil1994/Flask_API_DB_ORM.git'
2. Install requirements, run _'pip install -r requirements.txt'_
3. Create .env file like .env.example
4. Create **PostgreSQL** database.
5. Run _'python entrypoint.py_' to create DB tables.
6. You may create test data, run _'python create_test_data.py'_ **!!!WARNING!!! before create**
   this func delete all existing data.
7. Run application **'python main.py'**
8. Test ability of this project by link _http://127.0.0.1:5000/apidocs_

* **GET /api/v1/groups** - Find all groups with less or equals student count (default 20)
* **DELETE /api/v1/students/** - Delete student by STUDENT_ID
* **GET /api/v1/students/** - Find all students with given parameters !!!which has course!!!
* **POST /api/v1/students/** - Add new student. !!!without course!!!
* **DELETE /api/v1/students/courses/** - Remove the student from one of his or her courses
* **PATCH /api/v1/students/courses/** - Add a student to the course. After it you can find student by the link GET
* **/api/v1/students/**

This application may inserts/select/updates/deletes data in the database using sqlalchemy
and flask rest framework.

