This application may inserts/select/updates/deletes data in the database using sqlalchemy 
and flask rest framework.

Used PostgreSQL DB.

Models have next field

GroupModel:
id
name

StudentModel:
id
group_id
first_name
last_name

CourseModel:
id
description
name

There is relationship between StudentsModels and CourseModels

entrypoint.py - create empty tables in BD.

web_app/db/create_test_data.py - generate test data in the tables. !!!WARNING!!! before create 
this func delete all existing data.

web_app/db/orm_commands.py this file has funcs which work with BD. 

web_app/db/formated_fucn.py has funcs which handle and serialize response to json or xml format.

web_app/db/funс_to_create_date.py has funcs generating random data to the DB.
