import sqlite3
import csv # Use this to read the csv file


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file

    Parameters
    ----------
    Connection
    """
    conn = None
    try:
        with sqlite3.connect(db_file) as conn:
            return conn
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)


def update_employee_salaries(conn, increase):
    """

    Parameters
    ----------
    conn: Connection
    increase: float
    """
    cur = conn.cursor()
    cur.execute('''UPDATE ConstructorEmployee
                    SET SalaryPerDay = SalaryPerDay*{}
                    WHERE EID=	(SELECT E.EID
                    FROM Employee E JOIN ConstructorEmployee CE
                    ON E.EID = CE.EID
                    WHERE datetime('now')-E.BirthDate >=50)'''.format(1 + (increase/100))).fetchone()
    conn.commit()

update_employee_salaries(create_connection('B7_DB.db'), 3)

def get_employee_total_salary(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    int
    """
    cur = conn.cursor()
    cur.execute('SELECT sum(SalaryPerDay) FROM ConstructorEmployee')
    res = cur.fetchone()
    return res[0]



def get_total_projects_budget(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    float
    """
    cur = conn.cursor()
    cur.execute('SELECT sum(Budget) from Project')
    res = cur.fetchone()
    return res[0]




def calculate_income_from_parking(conn, year):
    """
    Parameters
    ----------
    conn: Connection
    year: str

    Returns
    -------
    float
    """
    cur = conn.cursor()
    cur.execute("""SELECT SUM(Cost)
                from CarParking
                WHERE StartTime and EndTime BETWEEN '{year}-01-01 01:01:01' AND '{year1}-12-31 01:01:01'""".format(year=year, year1=year))
    res = cur.fetchone()
    return res[0]

ב

def get_most_profitable_parking_areas(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    list[tuple]

    """
    cur = conn.cursor()
    res = cur.execute("""SELECT PA.AID, SUM(CP.Cost) AS Income
                    FROM ParkingArea PA JOIN CarParking CP
                    ON PA.AID = CP.AID
                    GROUP BY PA.AID
                    ORDER BY Income DESC, PA.AID ASC
                    LIMIT 5;""").fetchall()
    return res



def get_number_of_distinct_cars_by_area(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    list[tuple]

    """
    cur = conn.cursor()
    cur.execute("""SELECT AID AS ParkingAreaID, COUNT(DISTINCT CID) AS DistinctCarNumber
                FROM CarParking
                GROUP BY AID
                ORDER BY DistinctCarNumber DESC""")
    res = cur.fetchall()
    return res



def add_employee(conn, eid, firstname, lastname, birthdate, street_name, number, door, city):
    """
    Parameters
    ----------
    conn: Connection
    eid: int
    firstname: str
    lastname: str
    birthdate: datetime
    street_name: str
    number: int
    door: int
    city: str
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO Employee VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (eid, firstname, lastname, birthdate, street_name, number, door, city))
    conn.commit()


def load_neighborhoods(conn, csv_path):
    """
    Parameters
    ----------
    conn: Connection
    csv_path: str
    """
    cur = conn.cursor()
    with open(csv_path, 'r') as f:
        ngbr = list(f)
        clean_ngbr = []
        for i in ngbr:
            i=i.strip()
            i=(i.split(','))
            clean_ngbr.append(i)
    # print(clean_ngbr)
    for value in range(len(clean_ngbr)):
        cur.execute('INSERT INTO Neighborhood VALUES (?, ?)', (clean_ngbr[value][0], clean_ngbr[value][1]))
        conn.commit()



