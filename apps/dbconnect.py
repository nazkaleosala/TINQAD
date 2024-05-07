import psycopg2
import pandas as pd

def getdblocation():
    db = psycopg2.connect(
        host='localhost',
        database='TINQAD-database',
        user='postgres',
        port=5432,
        password='nat31602'
    )

    return db

print(getdblocation())


def modifydatabase(sql, values):
    db = getdblocation()

    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

def querydatafromdatabase(sql, values, dfcolumns):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows

def query_single_value(sql):
    try:
        db = getdblocation()
        cur = db.cursor()
        cur.execute(sql)
        result = cur.fetchone()[0]
        db.close()
        return result
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        return None

def get_college(selected_degree_program):
    try:
        # Establish a connection to your PostgreSQL database
        conn = getdblocation()

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute the query to fetch the college name based on the selected degree program
        cursor.execute("SELECT c.college_name FROM college c INNER JOIN degree_programs d ON c.college_id = d.college_id WHERE d.degree_id = %s", (selected_degree_program,))
        college = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # If college is found, return its name, otherwise return None
        if college:
            return college[0]
        else:
            return "No college found for this degree program"

    except psycopg2.Error as e:
        # Print or log the error
        print("Error fetching college:", e)
        return None
