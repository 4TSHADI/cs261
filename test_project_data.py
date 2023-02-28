import random
import sqlite3
import datetime
import numpy as np

# Connect to the database
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# create users
for i in range(50):
    username = "user" + str(i)
    firstname = str(i)
    lastname = str(i)
    phone_number = str(12345) + str(i)
    department_id = 1
    language = "en"
    timezone = "GMT+0"
    currency = "£"
    email = "user" + str(i) + "@gmail.com"
    password = "password"
    working = True
    yearsAtCompany = 5
    user = [username, password, firstname, lastname, email, phone_number, department_id, language,
                    timezone, currency, working, yearsAtCompany]
    cursor.execute('INSERT INTO user (username, password, firstname, lastname, email, phone_number, department_id, language, timezone, currency, working, yearsAtCompany) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', user) 
    conn.commit()
    
# Generate and insert the data into the database
for i in range(50):
    # project
    name = "project" + str(i)
    manager_id = random.randint(1, 20)
    budget = random.randint(1000,100000)
    start_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 365))
    dt = datetime.timedelta(days=random.randint(1, 365))
    deadline = start_date + dt
    scope = random.randint(1,5)
    days = dt.days
    
    # user project relation
    no_team_mem = random.randint(3,20)
    upr = []
    tms = []
    for j in range(no_team_mem):
        user_id = j
        project_id = i
        if j == 0:
            role = "Project Manager"
            is_manager = True
        else:
            role = "Software Engineer"
            is_manager = False
        upr.append([user_id, project_id, is_manager, role])

        # team member survey
        experience = random.randint(1, 5)
        working_environment = random.randint(1, 5)
        hours_worked = random.randint(20, 69)
        communication = random.randint(1, 5)
        timestamp = datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 365))
        tms.append([user_id, project_id, experience, working_environment, hours_worked, communication, timestamp])

    exp_mean = np.mean([row[2] for row in tms])
    we_mean = np.mean([row[3] for row in tms])
    hw_mean = np.mean([row[4] for row in tms])
    comm_mean = np.mean([row[5] for row in tms])
    success = budget/100000 + days/365 + scope/5 + no_team_mem/20 + exp_mean/5 + we_mean/5 + hw_mean/69 + comm_mean/5
    is_success = 3.5 < success < 6.5

    #random resampling 
    if random.randint(0,100) < 20:
        is_success = not is_success

    # Insert project table
    project = (name, manager_id, budget, start_date.strftime('%Y-%m-%d %H:%M:%S'), deadline.strftime('%Y-%m-%d %H:%M:%S'), scope, True, is_success)
    cursor.execute('INSERT INTO project (name, manager_id, budget, start_date, deadline, scope, is_completed, is_success) VALUES (?,?,?,?,?,?,?,?)', project)
    conn.commit()

    # Insert user project relation table
    for j in range(no_team_mem):
        cursor.execute('INSERT INTO user_project_relation (user_id, project_id, is_manager, role) VALUES (?,?,?,?)', upr[j])
        conn.commit()

    # Insert team member survey table
    for j in range(no_team_mem):
        cursor.execute('INSERT INTO team_member_survey (user_id, project_id, experience, working_environment, hours_worked, communication, timestamp) VALUES (?,?,?,?,?,?,?)', tms[j])
        conn.commit()

# Close the database connection
conn.close()

