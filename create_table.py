# Python code to demonstrate table creation and
# insertions with SQL

# importing module
import sqlite3
from capture_image_order import image_capture
from read_aruco_order import read_tag
import cv2
import numpy as np

def put_data(crsr, connection):

    flag = True
    name = input("Name: ")
    drink = input("Drink:   ")
    ids = None

    while flag:

        frame = image_capture()

        #print(ids)
        ids = read_tag(frame,True)
        #print("New",ids)
        if ids != None:

            print ("writing")
            #SQL command to insert the data in the table
            sql_command = "insert into emp values (?, ?, ?)",(str(ids), str(name), str(drink))
            try:
                crsr.execute("insert into emp values (?, ?, ?)",(int(ids[0]), str(name), str(drink)))
            except:
                 print("Cup already used")
            #     return False
            # To save the changes in the files. Never skip this.
            # If we skip this, nothing will be saved in the database.
            connection.commit()

            flag = False
            #cv2.destroyAllWindows()

        ##Display the resulting frame
        cv2.imshow('order_frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':

    try:
        # connecting to the database
        connection = sqlite3.connect("order.db")
        # cursor
        crsr = connection.cursor()
        print('connected to', connection)
        # #SQL command to create a table in the database
        sql_command = """CREATE TABLE emp (ids INTEGER PRIMARY KEY,name VARCHAR(20),drink VARCHAR(30));"""
        # #execute the statement
        crsr.execute(sql_command)
    except:
        pass

    # while True:
    put_data(crsr, connection)
        # if a == False:
        #     break

    cv2.destroyAllWindows()

    # close the connection
    connection.close()
