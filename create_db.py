import sys
import sqlite3
import os

def main():
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')

    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted:
            cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL);")
            cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL ,student TEXT NOT NULL, number_of_students INTEGER NOT NULL, class_id INTEGER REFERENCES classrooms(id) ,course_length INTEGER NOT NULL);")
            cursor.execute("CREATE TABLE classrooms(id INTEGER PRIMARY KEY ,location TEXT NOT NULL ,current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL);")

            inputfilename = sys.argv[1]
            with open(inputfilename) as inputfile:
                for line in inputfile:
                    line = line.strip()
                    list_Of_Line = line.split(',')
                    if list_Of_Line[0] == 'C':
                        cursor.execute("INSERT INTO courses(id,course_name,student,number_of_students,class_id,course_length) VALUES(?,?,?,?,?,?)", (list_Of_Line[1].strip(), list_Of_Line[2].strip(),list_Of_Line[3].strip(),list_Of_Line[4].strip(),list_Of_Line[5].strip(),list_Of_Line[6].strip()))
                        dbcon.commit()
                    if list_Of_Line[0] == 'S':
                        cursor.execute("INSERT INTO students(grade,count) VALUES(?,?)",(list_Of_Line[1].strip(),list_Of_Line[2].strip()))
                        dbcon.commit()
                    if list_Of_Line[0] == 'R':
                        cursor.execute("INSERT INTO classrooms(id,location,current_course_id,current_course_time_left) VALUES(?,?,0,0)", (list_Of_Line[1].strip(), list_Of_Line[2].strip()))
                        dbcon.commit()
            printAllTables()

def printAllTables():
    dbcon = sqlite3.connect('schedule.db')
    cursor = dbcon.cursor()
    cursor.execute("SELECT * FROM courses")
    list_of_all_courses = cursor.fetchall()
    print("courses")
    for course in list_of_all_courses:
        print(course)
    cursor.execute("SELECT * FROM classrooms")
    list_of_all_classrooms = cursor.fetchall()
    print("classrooms")
    for classroom in list_of_all_classrooms:
        print(classroom)
    cursor.execute("SELECT * FROM students")
    list_of_all_students = cursor.fetchall()
    print("students")
    for student in list_of_all_students:
        print(student)

if __name__ == '__main__':
    main()

