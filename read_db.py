# Python code to demonstrate SQL to fetch data.

# importing the module
import sqlite3


def get_data(ids):
    # connect withe the myTable database
    connection = sqlite3.connect("order.db")

    # cursor object
    crsr = connection.cursor()
    #print (ids)
    command = "SELECT * FROM emp Where ids="+str(ids[0])
    #  #execute the command to fetch all the data from the table emp
    crsr.execute(command)

    # store all the fetched data in the ans variable
    ans = crsr.fetchall()

    return ans
