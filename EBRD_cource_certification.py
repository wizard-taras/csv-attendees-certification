'''
Program file: EBRD_cource_certification.py

Purpose:
    This script is used for determining the number of attendees that can be certified as well as their names;
these people attended one specific webinar (single day of some of 5 Blocks of the Training course) and if
they pass the criterion of listening to 75% of the entire session - they have a chance to receive the certificate

Record of revisions:
    Date        Programmer      Description of change(-s)
    ----        ----------      -------------------------
    5/12/23     Koziupa Taras   Original code. Problem statement and .csv Attendee Report loading to the
working space
    6/12/23     Koziupa Taras   Create a set of unique attendees' email addresses for the deliverable.
Create a dictionary of certified attendees (who pass the criterion of total connection time > 148 min)
Write values (email + connected time) to the separate .csv file for certification stage.
    7/12/23     Koziupa Taras   Add the option of simultaneous first and last names addition to the
participants that satisfy the condition of connection time
    7/12/23     Koziupa Taras   Add the option of clearing all the necessary lists and dicts for
new .csv Attendee report (which is renewed in each main *for* loop (line 42))
    15/12/23     Koziupa Taras   Add the 'FINAL_report' section
    
'''

import csv

## Defining the criterion
criterion = 148
total_session_time = 195

arr = []
arr_mod = []
email_list = []
names = []
unique_set = {}
unique_att_dict = {}
certified_att_dict = {}

def clearing(list_iterables):
    for inst in list_iterables:
        inst.clear()


for i in range(1, 3):   # Change the x2 value in this range(x1, x2) function to 6 to loop through 5 lists of Attendees reports (for Blocks 1-3)
                        # or to 3 to loop through 2 lists of Attendees reports (for Block 4)
    
    ## Loading the Attendee Report
    with open(f'block4_d{i}.csv', mode='r') as report:
        csv_fl = csv.reader(report)
        for lines in csv_fl:
            arr.append(lines)

    ## Looping through the Attendee Report from 17th line (starting position of the attendees data) to the end of
    # the Report and copying the data of those attendees who have 'Yes' set in their 'Attended' condition
    for line in arr[2:]:
        if line[0] == 'Yes':
            arr_mod.append(line)
        if line[-1] == '':
            # Removing blank item at the end of the line
            del line[-1]

    ## Creating a set of unique attendees email addresses
    ind = 0
    for line in arr_mod:
        for item in line:
            if '@' in item:
                email_list.append(line[ind])
            ind += 1
        ind = 0

    unique_set = set(email_list)

    ## Creating a dictionary with keys == attendees emails, values == connection time
    temp_duration = 0
    for item in unique_set:
        for line in arr_mod:
            if item in line:
                temp_duration += int(line[-3])
        unique_att_dict[item] = temp_duration
        temp_duration = 0

    for item in unique_set:
        for line in arr_mod:
            if item in line and (f'{line[2]} {line[3]}' not in names):
                names.append(f'{line[2]} {line[3]}')
    # Printing out total connection time of each unique webinar participant
    # for key, value in unique_att_dict.items():
    #     print(f'{key}: {value}')

    ## Looping through all the attendees list and setting their connected time to 195 if max limit is reached
    for name, (key, value) in zip(names, unique_att_dict.items()):
        if value > criterion:
            certified_att_dict[key] = [name, value]

    with open(f'certified_b4_day{i}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Attendee email', 'Attendee name', 'Total connection time'])
        for key, value in certified_att_dict.items():
            writer.writerow([key, value[0], value[1]])
    
    ## Clear all the necessary lists and dicts for new .csv Attendee report
    clearing([certified_att_dict, unique_att_dict, names, arr_mod, unique_set, email_list, arr])


certif_reports_dict = {}
final_certif_dict = {}
count = 0

for i in range(1, 3):
    
    ## Loading the certified attendees .csv reports of each day to the *certif_reports_dict*
    with open(f'certified_b4_day{i}.csv', mode='r') as certified_report:
        csv_fl = csv.reader(certified_report)
        for lines in csv_fl:
            arr.append(lines)
        
        certif_reports_dict[f'day{i}'] = arr[1:]

        arr.clear()

for v in certif_reports_dict.values():
    for vv in v:
        if vv[0] in final_certif_dict.keys():
            count = final_certif_dict[vv[0]][1]
            count += 1
            final_certif_dict[vv[0]] = [vv[1], count]
        else: final_certif_dict[vv[0]] = [vv[1], 1]

with open(f'FINAL_certified_att-s_b4.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Attendee email', 'Attendee name', 'Total days'])
        for key, value in final_certif_dict.items():
            writer.writerow([key, value[0], value[1]])

## Activate ↓ this ↓ piece of code ONLY when you're making .csv report on what Blocks attendees are certified with
'''
arr.clear()
att_dict = {}

for i in range(1, 4):
    
    ## Loading the 'FINAL_certified_att-s_b{i}' Reports
    with open(f'FINAL_certified_att-s_b{i}.csv', mode='r') as report:
        csv_fl = csv.reader(report)
        for lines in csv_fl:
            arr.append(lines)

    ## Looping through the Attendee Report from 2nd line (starting position of the attendees data) to the end of
    # the Report and copying the data of attendees (email, name) into the dictionary 'att_dict'
    for line in arr[1:]:
        if line[0] in att_dict.keys() and int(line[2]) > 2:
            temp = att_dict[line[0]][1]
            att_dict.update({line[0]: [line[1], f'{temp} + {i}']})
        elif int(line[2]) > 2: att_dict[line[0]] = [line[1], i]

    arr.clear()

with open(f'FINAL_certified_att-s.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Attendee email', 'Attendee name', 'Blocks'])
        for key, value in att_dict.items():
            writer.writerow([key, value[0], value[1]])

arr.clear()

## Loading the 'FINAL_certified_att-s_b{i}' Reports
with open('FINAL_certified_att-s_b4.csv', mode='r') as report:
    csv_fl = csv.reader(report)
    for lines in csv_fl:
        arr.append(lines)

## Looping through the Attendee Report from 2nd line (starting position of the attendees data) to the end of
# the Report and copying the data of attendees (email, name) into the dictionary 'att_dict'
for line in arr[1:]:
    if line[0] in att_dict.keys():
        temp = att_dict[line[0]][1]
        att_dict.update({line[0]: [line[1], f'{temp} + 4']})
    else: att_dict[line[0]] = [line[1], i]

with open(f'FINAL_certified_att-s.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Attendee email', 'Attendee name', 'Blocks'])
    for key, value in att_dict.items():
        writer.writerow([key, value[0], value[1]])
'''