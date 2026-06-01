"""
CodeGuard Test File
קובץ בדיקה שנועד להפעיל את כל חוקי ה-AST:
1. פונקציה ארוכה מדי (מעל 20 שורות)
2. חוסר בתיעוד (Missing Docstring)
3. משתנים ללא שימוש (Unused Variables)
"""


def calculate_good_square(number):
    """Calculates the square of a number and returns it."""
    # פונקציה תקינה לחלוטין - קצרה ויש לה דוקסטרינג
    return number * number


def undocumented_function(a, b):
    # שגיאה: פונקציה ללא דוקסטרינג!
    result = a + b
    return result


def function_with_unused_variables():
    """This function has a docstring but contains bad unused variables."""
    active_variable = 10

    # שגיאות: המשתנים הבאים מוגדרים אך אף אחד לא משתמש בהם!
    unused_counter = 0
    forgotten_secret = "hidden_value"
    temporary_data = [1, 2, 3]

    return active_variable * 2


def monster_long_function_calculated_grades(students_list):
    """
    This function is way too long! It violates the 20-line rule intentionally
    to make sure our Matplotlib Histogram and Alerts system catch it perfectly.
    """
    print("Starting huge batch processing for student grades...")
    total_students = len(students_list)
    passed_students = 0
    failed_students = 0
    grades_sum = 0

    print("Looping through students database...")
    for student in students_list:
        grade = student.get("grade", 0)
        grades_sum += grade

        if grade >= 60:
            print(f"{student.get('name')} passed!")
            passed_students += 1
        else:
            print(f"{student.get('name')} failed.")
            failed_students += 1

    print("Finalizing calculations for statistical report...")
    if total_students > 0:
        average = grades_sum / total_students
    else:
        average = 0

    print(f"Total: {total_students}, Passed: {passed_students}, Failed: {failed_students}")
    print(f"The calculated class average is: {average}")
    print("Processing completed successfully. Returning dictionary.")

    return {
        "average": average,
        "passed": passed_students,
        "failed": failed_students
    }