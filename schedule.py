import sys
import sqlite3
import os

def main():
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    while databaseexisted and not check_if_table_is_empty():





















def check_if_table_is_empty():
    databaseexisted = os.path.isfile('schedule.db')
    if databaseexisted:
        dbcon = sqlite3.connect('schedule.db')
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM courses")
        coursesList = cursor.fetchall();
        if len(coursesList.fetchall())==0:
            return True
        else:
            return False
    else:
        return False



if __name__ == '__main__':
    main()