#=====importing libraries===========
from datetime import datetime
import time
import os.path

# Date and time variables.
now = datetime.now()
date_time = now.strftime("%d %b %Y")

# Variables for formatting, and login system.
stars = "==" * 40
gap = " " * 3
logged_in_user = ""

# Totals of tasks and users variables.

with open("tasks.txt", "r") as tasks:
    number_of_tasks = len(tasks.readlines())

with open("user.txt", "r") as users:
    number_of_users = len(users.readlines())


# ====Defining Functions====


# Registering new users.
def register():
    print("Register a new user")
    print("--------------------")
    with open("user.txt", "r") as users:
        users_passwords = dict(a.strip().split(", ") for a in users)
    while True:
        new_user = input("Please enter new username: ")
        if new_user in users_passwords:
            print("Username already exists, please try again.")
        else:
            break
    new_pass = input("Please enter a password: ")
    pass_conf = input("Confirm password: ")
    if new_pass == pass_conf:
        with open("user.txt", "a") as file:
            file.write("\n" + new_user + ", " + new_pass)
        print("New user created!")
        menu()


# Adding new task to tasks.txt file.
def add_task():
    number_of_tasks_plus_one = number_of_tasks + 1
    print("Add a new task to the manager: ")
    user_task = input("Who is this task assigned to?: ")
    task_title = input("Title of this task: ")
    task_desc = input("Task description: ")
    due_date = input("Task due date: ")
    info = (f"{user_task}, {task_title}, {task_desc}, {due_date}, {date_time}, No, {number_of_tasks_plus_one}")
    with open("tasks.txt", "a") as file:
        file.write("\n" + info)
    return("Task added successfully!")
    menu()

# View all tasks. Reads from tasks.txt file.
def view_all():
    with open("tasks.txt", "r") as tasks:
        for lines in tasks:
            task_details_list = lines.strip().split(", ")
            print(f"""{stars}
Task Number:        {task_details_list[6]}
Task:               {task_details_list[1]}
Assigned to:        {task_details_list[0]}
Date Assigned:      {task_details_list[4]}
Due Date:           {task_details_list[3]}
Task Complete?      {task_details_list[5]}
Task Description:   {task_details_list[2]}
{stars}
""")
    menu()

# View tasks for logged in user. Reads from tasks.txt file. Uses logged_in_user variable.
def view_my_tasks():
    with open("tasks.txt", "r") as tasks:
        for lines in tasks:
            task_details_list = lines.strip().split(", ")
            if logged_in_user == task_details_list[0]:
                print(f"""{stars}
Task Number:        {task_details_list[6]}
Task:               {task_details_list[1]}
Assigned to:        {task_details_list[0]}
Date Assigned:      {task_details_list[4]}
Due Date:           {task_details_list[3]}
Task Complete?      {task_details_list[5]}
Task Description:   {task_details_list[2]}
{stars}""")


# Asks user which of logged in users tasks they would like to view.
    while True:
        task_selection = int(input("""Please enter the task number you would like to view:
Enter \'-1\' to return to main menu.
Selection: """))
        task_selection_user = task_selection-1
        with open("tasks.txt", "r") as tasks:
            for i, line in enumerate(tasks):
                if i == task_selection_user:
                    list_lines = line.strip().split(", ")
                    print(f"""{stars}
Task Number:        {list_lines[6]}
Task:               {list_lines[1]}
Assigned to:        {list_lines[0]}
Date Assigned:      {list_lines[4]}
Due Date:           {list_lines[3]}
Task Complete?      {list_lines[5]}
Task Description:   {list_lines[2]}
{stars}""")

                    # Asking user to mark task as complete or edit.
                    while True:
                        edit_or_complete = input("Enter \'E\' to edit, \'C\' to mark as complete, or \'B\' to return: ")


                        # Mark as complete section here. Checks to see if task already completed first, and edits task by line if not.
                        if edit_or_complete.lower() == "c":
                            if list_lines[5] == "Yes":
                                print("Task completed previously!")
                            else:
                                new_task = (
                                    f"{list_lines[0]}, {list_lines[1]}, {list_lines[2]}, {list_lines[3]}, {list_lines[4]}, Yes, {list_lines[6]}")
                                with open("tasks.txt", "r") as file:
                                    data = file.readlines()
                                    data[task_selection_user] = new_task + "\n"
                                with open("tasks.txt", "w") as file:
                                    file.writelines(data)
                                print("Task updated successfully!")

                        # Edit task here, can only reassign task to new user, and edit the due date.
                        elif edit_or_complete.lower() == "e":
                            if list_lines[5] == "Yes":
                                print("You cannot edit a completed task!")
                            else:
                                new_user = input("Please enter the user you would like to reassign this task to: ")
                                new_date = input("Please enter the new due date: ")
                                edited_task = (
                                    f"{new_user}, {list_lines[1]}, {list_lines[2]}, {new_date}, {list_lines[4]}, {list_lines[5]}, {list_lines[6]}")
                                with open("tasks.txt", "r") as file:
                                    data = file.readlines()
                                    data[task_selection_user] = edited_task + "\n"
                                with open("tasks.txt", "w") as file:
                                    file.writelines(data)
                                print("Task updated successfully!")
                        if edit_or_complete.lower() == "b":
                            break
        if task_selection == -1:
            break
    main()

# Displaying stats. Generates new reporting first to update before reading files.
def display_stats():
    generate_reports()
    with open("task_overview.txt", "r") as file:
        task_overview = file.read()
        print(task_overview)
    print("\n")
    with open("user_overview.txt", "r") as file:
        user_overview = file.read()
        print(user_overview)
    menu()


# Defining main menu. For use in menu function.
def main():
   menu()


# Menu function.
def menu():
    if logged_in_user == "admin":
        menu = input('''Select one of the following Options below:
                    R  - Registering a user
                    A  - Adding a task
                    VA - View all tasks
                    VM - View my task
                    GR - Generate reports
                    DS  - Display Stats
                    E  - Exit
                    : ''').lower()

        if menu == "r":
            register()
        elif menu == "a":
            add_task()
        elif menu == "va":
            view_all()
        elif menu == "vm":
            view_my_tasks()
        elif menu == "ds":
            display_stats()
        elif menu == "e":
            exit()
        elif menu == "gr":
            generate_reports()
            time.sleep(2)
            print("Reporting completed!")
            time.sleep(1)
            main()
        else:
            print("Please try again")
            main()
    else:
        menu = input('''Select one of the following Options below:
                    A  - Adding a task
                    VA - View all tasks
                    VM - View my task
                    E  - Exit
                    : ''').lower()
        if menu == "a":
            add_task()
        elif menu == "va":
            view_all()
        elif menu == "vm":
            view_my_tasks()
        elif menu == "e":
            exit()
        else:
            print("Please try again")
            main()

# Generating reporting files.
def generate_reports():

    # Variables here for use below.
    total_completed_tasks = 0
    total_incomplete_tasks = 0
    total_overdue = 0

    # Opening tasks.txt and adding +1 to variables above depending on if statements.
    with open("tasks.txt", "r") as file:
        for data in file:
            tasks = data.strip().split(", ")
            if tasks[5] == "Yes":
                total_completed_tasks += 1
            elif tasks[5] == "No":
                total_incomplete_tasks += 1
            tasks_date = tasks[3]
            converted_date = datetime.strptime(tasks_date, "%d %b %Y")
            if converted_date < now and tasks[5] == "No":
                total_overdue += 1

    # Variables for percentages. Rounded down to 1 decimal place.
    percentage_overdue = (total_overdue / number_of_tasks * 100).__round__(1)
    percentage_incomplete = (total_incomplete_tasks / number_of_tasks * 100).__round__(1)

    # Writing info to new file in user friendly manner.
    with open("task_overview.txt", "w") as file:
        file.write(f"""Task Overview
{stars}
Total Number of Tasks:                              {number_of_tasks}
Total Number of Completed Tasks:                    {total_completed_tasks}
Total Number of Incompleted Tasks:                  {total_incomplete_tasks}
Total Number of Incompleted and Overdue tasks:      {total_overdue}

Percentage of Tasks Incomplete:                     {percentage_incomplete}%
Percentage of Tasks Overdue:                        {percentage_overdue}%
{stars}
""")


    # Section to create user_overview.txt
    usernames = []

    # Pulling usernames from users.txt, writing to usernames variable.
    with open("user.txt", "r") as file:
        for lines in file:
            usernames_temp_list = lines.strip().split("\n")
            for lines in usernames_temp_list:
                split_usernames_temp = lines.split(", ")
                usernames.append(split_usernames_temp[0])


    # Creating blank dictionaries using the usernames variable above.
    tasks_assigned_dict = {users: 0 for users in usernames}
    user_complete_dict = {users: 0 for users in usernames}
    user_incomplete_dict = {users: 0 for users in usernames}
    user_incomplete_overdue_dict = {users: 0 for users in usernames}

    perc_total_tasks_dict = {users: 0 for users in usernames}
    perc_user_complete_dict = {users: 0 for users in usernames}
    perc_user_incomplete_dict = {users: 0 for users in usernames}
    perc_incomplete_overdue_dict = {users: 0 for users in usernames}


    # Writing information to dictionaries. Makes use of if statements.
    with open("tasks.txt", "r") as file:
        for data in file:
            tasks = data.strip().split(", ")
            for users in tasks:
                if users in tasks_assigned_dict:
                    tasks_assigned_dict[users] = tasks_assigned_dict[users] + 1
                if users in user_complete_dict and tasks[5] == "Yes":
                    user_complete_dict[users] = user_complete_dict[users] + 1
                if users in user_incomplete_dict and tasks[5] == "No":
                    user_incomplete_dict[users] = user_incomplete_dict[users] + 1
                tasks_date = tasks[3]
                converted_date = datetime.strptime(tasks_date, "%d %b %Y")
                if users in user_incomplete_overdue_dict and tasks[5] == "No" and converted_date < now:
                    user_incomplete_overdue_dict[users] = user_incomplete_overdue_dict[users] + 1


    # Creating percentages from info above.
    for key, value in perc_total_tasks_dict.items():
        perc_total_tasks_dict[key] = (tasks_assigned_dict[key]/number_of_tasks*100).__round__(1)

    for key, value in user_complete_dict.items():
        if value == 0:
            perc_user_complete_dict[key] = 0
        else:
            perc_user_complete_dict[key] = tasks_assigned_dict[key] / user_complete_dict[key] * 100

    for key, value in user_incomplete_dict.items():
        if value == 0:
            perc_user_incomplete_dict[key] = 0
        else:
            perc_user_incomplete_dict[key] = tasks_assigned_dict[key] / user_incomplete_dict[key] * 100

    for key, value in user_incomplete_overdue_dict.items():
        if value == 0:
            perc_incomplete_overdue_dict[key] = 0
        else:
            perc_incomplete_overdue_dict[key] = tasks_assigned_dict[key] / user_incomplete_overdue_dict[key] * 100


    # Creating nested dictionary
    from collections import defaultdict

    combined_dictionaries = defaultdict(list)
    for d in (tasks_assigned_dict, perc_total_tasks_dict, perc_user_complete_dict, perc_user_incomplete_dict, perc_incomplete_overdue_dict):
        for key, value in d.items():
            combined_dictionaries[key].append(value)


    # Writing info to file.
    headers = ["User", "Tasks", "% of total tasks", "% of user tasks complete", "% of user tasks incomplete", "% of user tasks overdue"]

    with open("user_overview.txt", "w") as file:
        file.write(f"""User Overview
{stars}============================================
Registered Users: {number_of_users}\nTotal number of tasks: {number_of_tasks}
{stars}============================================
{headers[0]}  |  {headers[1]}   |  {headers[2]:}  |  {headers[3]:}  |  {headers[4]:}  |  {headers[5]:}
{stars}============================================\n""")

        for key, value in combined_dictionaries.items():
            file.write(f"""{key: <11}{value[0]: <15}{value[1]: <24}{value[2]: <31}{value[3]: <30}{value[4]}\n""")


#====Login Section====

print("Welcome to the Task Manager app\n")

# While loop for login.
while True:
    username_input = input("Please enter your username: ")
    logged_in = False

    # Opening user.txt as read only. For loop reads each line and splits data into usernames and passwords variables.
    with open("user.txt", "r") as users:
        for lines in users:
            username, password = lines.strip().split(", ")

            # If statement to check input is equal to anything in the username variable. Moves onto check password if match found.
            if username_input == username:
                pass_input = input("Please enter your password: ")
                if pass_input == password:

                    # Logged_in variable changed to true. logged_in_user changed to input entered above.
                    logged_in = True
                    logged_in_user = username_input
                    print(f"Welcome {username_input}")
                    break
                else:
                    print("Incorrect password")
                    continue
    if logged_in == True:
        break


# Menu section.

main()