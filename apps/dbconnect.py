import psycopg2
import pandas as pd

def getdblocation():
    db = psycopg2.connect(
        host='10.206.100.41',
        database='tinquaddb',
        user='qaotinqad',
        port=5432,
        password='qaotinqad123'
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





def get_rankingbody(evidence_id_rankingbody):
    try:
        conn = getdblocation()
        cursor = conn.cursor()

        query = """
            SELECT rb.ranking_body_name 
            FROM kmteam.SDGSubmission s
            JOIN kmteam.ranking_body rb ON s.sdg_rankingbody = rb.ranking_body_id
            WHERE s.sdgsubmission_id  = %s
        """
        cursor.execute(query, (evidence_id_rankingbody,))
        rankingbody = cursor.fetchone()

        cursor.close()
        conn.close()

        if rankingbody:
            return rankingbody[0]
        else:
            return "No selected evidence name"

    except psycopg2.Error as e:
        print("Error fetching ranking body:", e)
        return None
    


def get_sdgrdescription(evidence_id_descript):
    try:
        conn = getdblocation()
        cursor = conn.cursor()

        query = """
            SELECT s.sdg_description 
            FROM kmteam.SDGSubmission s 
            WHERE s.sdgsubmission_id  = %s
        """
        cursor.execute(query, (evidence_id_descript,))
        rankingbody = cursor.fetchone()

        cursor.close()
        conn.close()

        if rankingbody:
            return rankingbody[0]
        else:
            return "No selected evidence name"

    except psycopg2.Error as e:
        print("Error fetching description:", e)
        return None
    

def get_sdgroffice(evidence_id_office):
    try:
        conn = getdblocation()
        cursor = conn.cursor()

        query = """
            SELECT o.office_name
            FROM kmteam.SDGSubmission s 
            JOIN maindashboard.offices o ON s.sdg_office_id = o.office_id
            WHERE s.sdgsubmission_id = %s
        """
        cursor.execute(query, (evidence_id_office,))
        rankingbody = cursor.fetchone()

        cursor.close()
        conn.close()

        if rankingbody:
            return rankingbody[0]
        else:
            return ""

    except psycopg2.Error as e:
        print("Error fetching office:", e)
        return None



def get_sdgrdepartment(evidence_id_department):
    try:
        conn = getdblocation()
        cursor = conn.cursor()

        query = """
            SELECT d.deg_unit_name 
            FROM kmteam.SDGSubmission s 
            JOIN public.deg_unit d ON s.sdg_deg_unit_id = d.deg_unit_id 
            WHERE s.sdgsubmission_id = %s
        """
        cursor.execute(query, (evidence_id_department,))
        rankingbody = cursor.fetchone()

        cursor.close()
        conn.close()

        if rankingbody:
            return rankingbody[0]
        else:
            return ""

    except psycopg2.Error as e:
        print("Error fetching department:", e)
        return None



def get_sdgrnotes(evidence_id_notes):
    try:
        conn = getdblocation()
        cursor = conn.cursor()

        query = """
            SELECT s.sdg_notes
            FROM kmteam.SDGSubmission s 
            WHERE s.sdgsubmission_id  = %s
        """
        cursor.execute(query, (evidence_id_notes,))
        rankingbody = cursor.fetchone()

        cursor.close()
        conn.close()

        if rankingbody:
            return rankingbody[0]
        else:
            return ""

    except psycopg2.Error as e:
        print("Error fetching notes:", e)
        return None
