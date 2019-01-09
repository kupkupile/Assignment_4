import sys
import sqlite3
import os

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

def main():
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    number_of_iteration = 0;
    if check_if_table_is_empty():
        printAllTables()
    while databaseexisted and not check_if_table_is_empty():
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM classrooms ")
        list_of_all_classrooms = cursor.fetchall()
        for var in list_of_all_classrooms:
            if var[3] == 0:
                cursor.execute("SELECT * FROM courses WHERE class_id = (?) ORDER BY id ASC LIMIT 1", (var[0], ))
                enter_to_classroomTable = cursor.fetchone()
                if enter_to_classroomTable is not None and len(enter_to_classroomTable) != 0:
                    print("("+str(number_of_iteration)+") " + str(var[1]) + ": " + str(enter_to_classroomTable[1]) + " is schedule to start")
                    cursor.execute("UPDATE classrooms SET current_course_id = ? , current_course_time_left = ? WHERE classrooms.id = ?", [enter_to_classroomTable[0], enter_to_classroomTable[5], enter_to_classroomTable[4]])
                    cursor.execute("SELECT count FROM students WHERE grade = ?", [enter_to_classroomTable[2]])
                    count = cursor.fetchone()
                    count= count[0]- enter_to_classroomTable[3]
                    if count <= 0:
                        count = 0
                    cursor.execute("UPDATE students SET count = ? WHERE grade = ?", [count, enter_to_classroomTable[2]])
                    dbcon.commit()
            else:
                cursor.execute("SELECT course_name FROM courses WHERE id = ?", [var[2]])
                courseName = cursor.fetchone()
                if var[3]-1!=0:
                    print("("+str(number_of_iteration)+") " + str(var[1]) + ": " + "occupied by " + str(courseName[0]))
                    cursor.execute("UPDATE classrooms SET current_course_time_left = current_course_time_left -1 WHERE id = ?",
                                   [var[0]])
                    dbcon.commit()
                else:
                    print("("+str(number_of_iteration)+") " + str(var[1]) + ": " +  str(courseName[0]) + " is done")
                    cursor.execute("DELETE FROM courses WHERE id = ?", [var[2]])
                    cursor.execute("UPDATE classrooms SET current_course_time_left = 0 , current_course_id = 0 WHERE id = ?",
                                   [var[0]])
                    dbcon.commit()
                    cursor.execute("SELECT * FROM courses WHERE class_id = ? ORDER BY id ASC LIMIT 1", [var[0]])
                    enter_to_classroomTable = cursor.fetchone()

                    if enter_to_classroomTable is not None and len(enter_to_classroomTable) != 0:
                        print("(" + str(number_of_iteration) + ") " + str(var[1]) + ": " + str(
                            enter_to_classroomTable[1]) + " is schedule to start")
                        cursor.execute(
                            "UPDATE classrooms SET current_course_id = ? , current_course_time_left = ? WHERE classrooms.id = ?",
                            [enter_to_classroomTable[0], enter_to_classroomTable[5],
                             enter_to_classroomTable[4]])
                        dbcon.commit()
                        cursor.execute("SELECT count FROM students WHERE grade = (?)", (enter_to_classroomTable[2], ))
                        count = cursor.fetchone()
                        count = count[0] - enter_to_classroomTable[3]
                        if count <= 0:
                            count = 0
                        cursor.execute("UPDATE students SET count = ? WHERE grade = ?",
                                       [count, enter_to_classroomTable[2]])
                        dbcon.commit()
        number_of_iteration= number_of_iteration+1
        printAllTables()
















def check_if_table_is_empty():
    databaseexisted = os.path.isfile('schedule.db')
    if databaseexisted:
        dbcon = sqlite3.connect('schedule.db')
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM courses")
        coursesList = cursor.fetchall();
        if len(coursesList)==0:
            return True
        else:
            return False
    else:
        return False



if __name__ == '__main__':
    main()