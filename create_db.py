import sys
import sqlite3
import os

def main():
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')

    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted:
            cursor.execute("""CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL);""")
            cursor.execute("""CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL ,student TEXT NOT NULL, number_of_students INTEGER NOT NULL, class_id INTEGER REFERENCES classrooms(id) ,course_length INTEGER NOT NULL);""")
            cursor.execute("""CREATE TABLE classrooms(id INTEGER PRIMARY KEY ,location TEXT NOT NULL ,current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL);""")

    inputfilename = sys.args[1]
    with open(inputfilename) as inputfile:
         for line in inputfile:
             line = line.strip()
             list_Of_Line = line.split(',')
             if list_Of_Line[0] == 'C':
                 cursor.execute("INSERT INTO courses(id,course_name,student,number_of_students,class_id,classrooms) VALUES(?,?,?,?,?,?)", (list_Of_Line[1].strip(), list_Of_Line[2].strip(),list_Of_Line[3].strip(),list_Of_Line[4].strip(),list_Of_Line[5].strip(),list_Of_Line[6].strip()))

             if list_Of_Line[0] == 'S':
                cursor.execute("INSERT INTO students(grade,count) VALUES(?,?)",(list_Of_Line[1].strip(),list_Of_Line[2].strip()))

             if list_Of_Line[0] == 'R':
                 cursor.execute("INSERT INTO students(id,location,current_course_id,current_course_time_left) VALUES(?,?,0,0)", (list_Of_Line[1], list_Of_Line[2]))

if __name__ == '__main__':
    main()