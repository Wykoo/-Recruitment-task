import json
import csv
import os
from datetime import datetime
#Global data
global name_counter
global x

#Menu for the user
def start():
  print("1.Make a reservation")
  print("2.Cancel a reservation")
  print("3.Print Scheduale")
  print("4.Save scheduale to a file")
  print("5.Exit\n")

#Menu for the choice of hours
def choice():
  print("How long would you like to book court?")
  print("1) 30 Minutes")
  print("2) 60 Minutes")
  print("3) 90 Minutes")

#Checking if the name user have given isn't used more than 2 times
def check_name(name):
  global name_counter
  name_counter = 0
  #Opnening file to check names
  if os.path.exists('Edit_info.json'):
    with open('Edit_info.json') as f:
      data = json.load(f)
      #Counting how many times user made reservation
      for dates in data:
        for item in data[dates]:
          if item["name"] == name:
            name_counter += 1

#Function using date from user to check if there is avaible court for given hours
def check_date(date):
  
  with open('Edit_info.json') as f:
    data = json.load(f)
    free_time = []
    #Slicing data to set new variables for Day and month and hours
    date_to_cut = datetime.strptime(date, "%d.%m.%Y %H:%M")
    day_mon = date_to_cut.strftime("%d.%m")
    start_time = date_to_cut.strftime("%H:%M")
    current_time = datetime.now()

    #Checking if the data is less than 1 hour
    if(date_to_cut - current_time).total_seconds() < 3600:
      print("Selected time is less than 1 hour from now! You need to choose different date!")
      return
    
    for dates in data:
      if day_mon == dates:
        for item in data[dates]:
          #Check if there is a reservation on the given date that overlaps with the given time frame
          if item["start_time"] <= start_time < item["end_time"]:
            print(
              f"\nThe time you chose {start_time} is unavaible.\n\nThis frame time from {item['start_time']} to {item['end_time']} is already reserved\n"
            )
            free_time.append(item["end_time"])

          if item["start_time"] > start_time:
            print(
              f"Another reservation is from {item['start_time']} to {item['end_time']}"
            )
            free_time.append(item["start_time"])
            break

    if not free_time and free_time >= data[day_mon]:
      print(f'All schedule for {day_mon} is available. Select the time for your eservation: ')
      z = input("On what time would you like to reserve court? {HH:MM}\n")
      return


    #Here i was trying to type function for suggestion the closest time with adlist 1 hour space but after long hours couldnt figure it out 
    '''
    if free_time:
      ad_list_time = datetime.strptime(free_time[0], "%H:%M")
      
      for time in free_time:
        new_time = datetime.strptime(time, "%H:%M")
        
        if(new_time - date_to_cut).total_seconds() > 0 and (new_time - date_to_cut).total_seconds() < (ad_list_time - date_to_cut).total_seconds():
          ad_list_time = new_time
          
      sug = (ad_list_time + datetime.timedelta(hours=1)).strftime("%H:%M")
      
      print(f'All time slots for {day_mon} are reserved. The closest available time slor is {sug}')
      z = input("On what time would you like to reserve court? {HH:MM}\n") 
      return
      '''
      
            
    
    z = input("On what time would you like to reserve court? {HH:MM}\n")

#Function for saving all user data on json file with user choice of hours
def pick_minutes(date, name):
  with open('Edit_info.json') as f:
    data = json.load(f)
    try:
      date_to_cut = datetime.strptime(date, "%d.%m.%Y %H:%M")
    except ValueError:
      print("Please enter the date once agaian with correct format{DD.MM.YYYY HH:MM}")
      return
    
    day_mon = date_to_cut.strftime("%d.%m")
    Min = date_to_cut.strftime("%M")
    temp = data[day_mon]
    Hour = int(date_to_cut.hour)
    Minutes = int(date_to_cut.minute)

    print("How long would you like to book court?")
    print("1) 30 Minutes")
    print("2) 60 Minutes")
    print("3) 90 Minutes\n")
    y = input('')
    #On each condition we are adding 30min/1hour/1,5hour
    #We are checking this only if user gave full or half full hour for ex. 14:00/14:30/15:00 etc.
    while y not in ['1', '2', '3']:
      print("Wrong Input! Please select the number from 1-3")
      choice()
      y = input('')

    try:
      y = int(y)
      if y == 1:
        Minutes_1 = Minutes + 30
        if Minutes_1 >= 60:
          Hour_1 = str(Hour + 1)
          Minutes_1 = Min
        else:
          Hour_1 = str(Hour)
        with open('Edit_info.json', 'w') as f:
          t = {
            "name": name,
            "start_time": z,
            "end_time": f'{Hour_1}:{str(Minutes_1).zfill(2)}'
          }
          #Adding the specifie data to a json file with function dump
          temp.append(t)
          json.dump(data, f, indent=2)
          print("Reservation made !")
      elif y == 2:
        Hour_1 = str(Hour + 1)
        with open('Edit_info.json', 'w') as f:
          t = {"name": name, "start_time": z, "end_time": f'{Hour_1}:{Min}'}
          temp.append(t)
          json.dump(data, f, indent=2)
          print("Reservation made !")
      elif y == 3:
        Minutes_1 = Minutes + 90
        if Minutes_1 >= 60:
          Hour_1 = Hour + 1
          Minutes_1 -= 60
        else:
          Hour1 = Hour
        with open('Edit_info.json', 'w') as f:
          t = {
            "name": name,
            "start_time": z,
            "end_time": f'{Hour_1}:{str(Minutes_1).zfill(2)}'
          }
          temp.append(t)
          json.dump(data, f, indent=2)
          print("Reservation made !")
      else:
        print("you need to Type number from 1-3!")
        choice()
        y = input('')

    except ValueError:
      print("Wrong Input! Please select the number from 1-3")
      choice()
      y = input('')
        
# Removing the user 
def Cancelation(date_can, name_can):
  with open('Edit_info.json') as f:
    
    d = datetime.strptime(date_can, "%d.%m.%Y %H:%M")
    data = json.load(f)
    Day_Mon = d.strftime("%d.%m")
    #Statement if that checks if data that user put is less than one hour from now
    diff = d - datetime.now()
    if diff.days < 0 or (diff.days == 0 and diff.seconds < 3600):
      print("You cannot cancel your reservation less than 1 hour from now")
    
    #Checking if the there is an info abour reservation that user gave
    for dates in data:
      if dates == Day_Mon:
        for items in data[dates]:
          if items['name'] == name_can:
            
            #Deleting each item
            del items['name']
            del items['start_time']
            del items['end_time']
            #Writing to the same file but without deleted user
            open('Edit_info.json', 'w').write(json.dumps(data, indent=2))
            print("Deleted!\n")
            break
          else:
            print("There is no reservation on this name!")
        print("There is no reservation for this user on specified date!")
        return
      else:
        print("There is not avaiable data for that day yet!")

#Function for printing the scheduale with specified date
def Show_list(start_date, end_date):
  try:
    start = datetime.strptime(start_date, "%d.%m.%Y %H:%M")
    end = datetime.strptime(end_date, "%d.%m.%Y %H:%M")
  except ValueError:
    print("Invalid date format. Please enter dates in the format DD.MM.YYY HH:SS")
    return
    
  with open('Edit_info.json') as f:
    new_data = []
    data = json.load(f)
    now = datetime.now()
    start_d = start.strftime("%d.%m")
    end_d = end.strftime("%d.%m")
    now_d = now.strftime("%d.%m")
    #Looping and printing for each day that is between given dates
    for dates in data:
      while start_d <= dates <= end_d:
        if now_d == dates:
          print("Today \n")
        #Spliting date to create weekday
        #adding '2023' for easier verification
        whole_date = dates + '.2023'
        main_date = datetime.strptime(whole_date,"%d.%m.%Y")
        main_day = main_date.strftime("%A")
        print(f"{dates} ({main_day})")
        #Printing whole schedule and writing it to a new file that later is used
        #for saving data to a file
        for item in data[dates]:
          print(item["name"], ":",item["start_time"], "-", item["end_time"])
          with open('Print.json', 'w') as f:
            t = {
              "name": item["name"],
              "Day" : f"{dates} ({main_day})",
              "start_time": item["start_time"],
              "end_time": item["end_time"]
            }
            new_data.append(t)
            json.dump(new_data, f, indent=2)

        break

#Saving scheduale to json file 
#This won't work if user didnt print schedule before
def  Save_Schedule_json(s_date_print, e_date_print, file_format, file_name):
  connect_name = file_name + file_format
  
  if os.path.exists(connect_name):
    print(f"File of name {connect_name} already exists!")
    return
    
  with open('Print.json', 'r') as f:
    data = json.load(f)
    
  with open(connect_name, 'w') as new_file:
    json.dump(data, new_file, indent = 2)

  print(f"Schedule saved to file {connect_name}")
#Looking for the headers and appending them to a new list    
def get_header_items(items, obj):
  for x in obj:
    if isinstance(obj[x], dict):
      items.append(x)
      get_header_items(items, obj[x])
    else:
      items.append(x)

#Adding items to list for each header
def add_items_to_data(items, obj):
  for x in obj:
    if isinstance(obj[x], dict):
      items.append("")
      get_header_items(items, obj[x])
    else:
      items.append(obj[x])

#Saving scheduale to csv file 
#This won't work if user didnt print schedule before
def Save_Schedule_csv(s_date_print, e_date_print, file_format, file_name):
  name_connect = file_name + file_format
  with open('Print.json') as f:
    list1 = []
    data = json.loads(f.read())
    temp = data[0]
    header_items = []
    get_header_items(header_items, temp)
    list1.append(header_items)
    #Adding items to a list, that is later saved to csv file
    for obj in data:
      d = []
      add_items_to_data(d, obj)
      list1.append(d)
    #Writing schedule to csv file
    with open(name_connect, 'w') as output:
      for a in list1:
        output.write(','.join(map(str, a)) + '\r')


#Main
while True:
  #Main
  start()
  choice = input("Type your choice:\n")
  if choice.isdigit():
    x = int(choice)
  
    if x == 1:
      name = str(input("Whats yout name and surname {Name Surname}?\n"))
      #If the user have more than 2 reservations user need to pass new
      #data schedule
      check_name(name)
      if name_counter <= 2:
        date = input("When would you like to book? {DD.MM.YYYY HH:MM}\n")
        check_date(date)
        pick_minutes(date, name)
      else:
        #User have more than 2 reservations and is given to a menu
        print("You cant have more than 2 reservation a week!")

      start()
      print("\n")
      x = int(input(''))

    elif x == 2:
      print("Please give us two of the following to cancel your reservation: \n")
      name_can = str(input("Your name: \n"))
      date_can = input("Date of a reservation: {DD.MM.YYYY HH:MM(Start time)}\n")
      Cancelation(date_can, name_can)

      start()
      print("\n")
      x = int(input(''))
    
    elif x == 3:
      start_date = input("Please input the start date{DD.MM.YYYY HH:MM}:\n")
      end_date = input("Please input the end date{DD.MM.YYYY HH:MM}: \n")
      print("\n")
      Show_list(start_date, end_date)
      start()
      print("\n")
      x = int(input(''))
    
    elif x == 4:
      s_date_print = input("Please input the start date you want to print: {DD:MM:YY     HH:MM}\n")
    
      e_date_print = input("Please input the end date you want to print: {DD:MM:YY HH:MM}\n")
    
      file_format = input("Please input file format {.csv/json}\n")
      #Checking if the format user gave is correct
      if file_format != '.csv' and file_format != '.json':
        print("Wrong file format!")
      
      file_name = input("Please input File name: \n")
      if file_format == '.csv':
        Save_Schedule_csv(s_date_print, e_date_print, file_format, file_name)
      
      if file_format == '.json':
        Save_Schedule_json(s_date_print, e_date_print, file_format, file_name)

      start()
      print("\n")
      x = int(input(''))
    
    elif x == 5:
      break

    else:
        print("You need to pick one of the following 1-5!")
        start()
        x = int(input(''))
  else:
    print("Error! Please enter an integer!")
