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