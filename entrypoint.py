from web_app.db.db_tools import create_db_table
from config import conn_params

if __name__ == '__main__':
    create_db_table(conn_params)
