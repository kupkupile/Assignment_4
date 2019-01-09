import sys
import sqlite3
import os

def main():
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    while databaseexisted and not check_if_table_is_empty():
        #check if a course which is in a class room is finished
        cursor = dbcon.cursor()
        cursor.execute("SELECT * FROM classrooms WHERE current_course_id <> 0")
        list_of_all_occupied_tables = cursor.fetchall()
        for table in list_of_all_occupied_tables:
            table = (table[0],table[1],table[2],table[3]-1)
            if table[3]==0:
                cursor.execute("DELETE FROM courses WHERE id = (?)", table[2])
                cursor.execute("UPDATE classrooms SET current_course_id = 0 , current_course_time = 0 WHERE classrooms.id = (?)", table[0])



        cursor = dbcon.cursor()
        cursor.execute("SELECT id FROM classrooms WHERE current_course_time_left = 0")
        list_of_all_available_tables = cursor.fetchall()
        for var in list_of_all_available_tables:
            cursor.execute("SELECT TOP 1 * FROM courses WHERE classroom_id = (?) ORDER BY id ASC",var[0])
            enter_to_classroomTable = cursor.fetchone()
            cursor.execute("UPDATE classrooms SET current_course_id = (?) , current_course_time_left = (?) WHERE classrooms.id = (?)", [(enter_to_classroomTable[0],), (enter_to_classroomTable[5],), (enter_to_classroomTable[4],)])
            cursor.execute("SELECT count FROM students WHERE grade = (?)", enter_to_classroomTable[2])
            count = cursor.fetchone() - enter_to_classroomTable[3]
            if count <= 0:
                count = 0
            cursor.execute("UPDATE students SET count = (?) WHERE grade = (?)", [(count,), (enter_to_classroomTable[2])])

















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