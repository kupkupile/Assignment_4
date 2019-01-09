import sys
import sqlite3
import os

def main():
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    while databaseexisted and not check_if_table_is_empty():
        cursor = dbcon.cursor()
        cursor




















def check_if_table_is_empty():
    databaseexisted = os.path.isfile('schedule.db')
    if databaseexisted:
        dbcon = sqlite3.connect('schedule.db')
        cursor = dbcon.cursor()
        coursesList = cursor.execute("SELECT * FROM courses")
        if len(coursesList)==0:
            return True
        else:
            return False
    else:
        return False



if __name__ == '__main__':
    main()