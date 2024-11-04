from flask import Flask, request, jsonify
import psycopg2
import psycopg2.pool
import os
import logging

logging.basicConfig(level=logging.DEBUG)

db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT', 5432)
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD')

def create_database():
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"CREATE DATABASE {db_name};")
            logging.info(f"Database '{db_name}' created successfully (if it didn't exist).")
        except psycopg2.errors.DuplicateDatabase:
            logging.info(f"Database '{db_name}' already exists.")
        except Exception as e:
            logging.error(f"Error creating database: {str(e)}")
    conn.close()

create_database()

pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1, 
    maxconn=10,
    dsn=f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"
)

app = Flask(__name__)

def create_table_with_columns(table_name, columns):
    with pool.getconn() as conn:
        try:
            with conn.cursor() as cursor:
                create_table_sql = f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY
                    );
                """
                cursor.execute(create_table_sql)
                conn.commit()

                # Add or alter columns to be of type TEXT
                for column in columns:
                    try:
                        cursor.execute(f"""
                            DO $$ 
                            BEGIN
                                IF NOT EXISTS (
                                    SELECT 1 FROM information_schema.columns 
                                    WHERE table_name='{table_name}' AND column_name='{column}'
                                ) THEN
                                    ALTER TABLE {table_name} ADD COLUMN {column} TEXT;
                                END IF;
                            END $$;
                        """)
                        conn.commit()
                    except Exception as e:
                        logging.error(f"Error adding column '{column}': {str(e)}")
                        conn.rollback()
        except Exception as e:
            logging.error(f"Error creating table or columns: {str(e)}")
        finally:
            pool.putconn(conn)

def insert_data(table_name, data):
    conn = pool.getconn()
    try:
        with conn.cursor() as cursor:
            columns = data.keys()
            values = tuple(data.values())
            sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
            logging.debug(f"Inserting data: {data}")  # Log the data being inserted
            cursor.execute(sql, values)
            conn.commit()
        return True 
    except Exception as e:
        logging.error(f"Error inserting data: {str(e)}")
        conn.rollback()
        return False
    finally:
        pool.putconn(conn)

@app.route('/', methods=['POST'])
def index():
    table_name = "salt_data"

    if request.is_json:
        data = request.json
        columns = data.keys()
    else:
        raw_data = request.data.decode('utf-8').strip()
        data = {'message': raw_data}
        columns = ['message']

    create_table_with_columns(table_name, columns)

    if insert_data(table_name, data):
        return jsonify({'message': 'Data received and stored successfully', 'data': data})
    else:
        return jsonify({'message': 'Error storing data'}), 500

if __name__ == '__main__':
    app.run()
