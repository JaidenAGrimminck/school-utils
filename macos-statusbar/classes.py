import json
import datetime
from datetime import timedelta
import copy
import random as rand

classData = {
    "classes": {}, # class aliases
    "special": {}, # for the special schedule
    "schedule": {} # for the regular schedule
}

"""
Loads the stored class data from the .json files in the data folder
"""
def loadClassesData():
    global classData

    with open("data/classes.json") as f:
        data = json.load(f)

        classData["classes"] = data["aliases"]
    
    with open("data/special-schedule.json") as f:
        data = json.load(f)

        classData["special"] = data["special"]

    with open("data/schedule.json") as f:
        data = json.load(f)

        classData["schedule"] = data
    
    #print(classData)
    print("loaded your class data!")

"""
Saves the class data to the .json files in the data folder
"""
def saveClassesData():
    with open("data/classes.json", "w") as f:
        json.dump({"aliases": classData["classes"]}, f)

    with open("data/special-schedule.json", "w") as f:
        json.dump({"special": classData["special"]}, f)

    with open("data/schedule.json", "w") as f:
        json.dump(classData["schedule"], f)

"""
Gets the last sunday that occurred before the current or given date
:param date: the date to get the last sunday from
:return: the date of the last sunday
"""
def getLastSunday(date=None):
    if date == None:
        # get today's date
        today = datetime.datetime.today()

        # get the day of the week
        day = today.weekday()

        # get the date of the last sunday
        lastSunday = today - timedelta(days=day + 1)

        return lastSunday
    else:
        # get the day of the week
        day = date.weekday()

        # get the date of the last sunday
        lastSunday = date - timedelta(days=day + 1)

        return lastSunday

"""
Gets the special schedule for the week (if there is one)
:param sunday: the date of the last sunday
:return: the special schedule for the week (False if there isn't one)
"""
def specialScheduleThisWeek(sunday=getLastSunday()):
    lastSunday = sunday

    # get the year
    year = lastSunday.year
    # month
    month = lastSunday.month
    # day
    day = lastSunday.day

    key = str(year) + "-" + str(month) + "-" + str(day)

    if key in classData["special"]:
        return getClassData()["special"][key]
    else:
        return False

"""
Gets the class schedule for the day
:param day: the date to get the schedule for
:return: the class schedule for the day
"""
def getDayClassSchedule(day=None):
    # first get the date of the start rotation
    startRot = getClassData()["schedule"]["rotation_start_date"]

    # convert it to a datetime object
    startRot = datetime.datetime.strptime(startRot, "%Y-%m-%d")

    # then, we'll counting from that date, going through the rotation for each school date
    count = 0
    currentDate = startRot
    goal = day
    if goal == None:
        goal = datetime.datetime.today()
    
    while goal.date() != currentDate.date():
        currentDate += timedelta(days=1)
        specialSchedule = specialScheduleThisWeek(getLastSunday(currentDate))

        if specialSchedule != False:
            # get weekday number
            weekday = currentDate.weekday()

            # get the schedule for that day
            schedule = specialSchedule[weekday]

            if schedule == False:
                schedule = getClassData()["schedule"]["week"][weekday]

            if (schedule["school"] == False) or classData["schedule"]["rotation_ignored_over_special_week"]:
                continue
            else:
                count += 1

                if count >= len(classData["schedule"]["rotation"]):
                    count = 0
        else:
            currentDay = currentDate.weekday()

            if classData["schedule"]["week"][currentDay]["school"] == False:
                continue
            else:
                # add to count
                count += 1

                if count >= len(classData["schedule"]["rotation"]):
                    count = 0

    return getClassData()["schedule"]["rotation"][count]

"""
Gets the timetable for the week depending on the last sunday
:param lastSunday: the date of the last sunday
"""
def getWeeklySchedule(lastSunday=getLastSunday()):
    # check if it's a sunday
    # error prevention. if it's not a sunday, get the last sunday
    if lastSunday.weekday() != 6:
        lastSunday = getLastSunday(lastSunday)

    if specialScheduleThisWeek(lastSunday) != False:
        specialSchedule = specialScheduleThisWeek(lastSunday)

        for i in range(0, 7):
            if specialSchedule[i] == False:
                specialSchedule[i] = getClassData()["schedule"]["week"][i]
        return specialSchedule
    else:
        return getClassData()["schedule"]["week"]

"""
Gets the timing of the day's schedule
:param today: the date to get the schedule for
"""
def getDayTimeSchedule(today=datetime.datetime.today()):
    # get the weekly schedule
    weeklySchedule = getWeeklySchedule(getLastSunday(today))
    
    # get the day's schedule
    daySchedule = weeklySchedule[today.weekday() + 1 if today.weekday() != 6 else 0]

    return daySchedule

"""
Gets the timing and classes of the day's schedule
:param today: the date to get the schedule for
"""
def getDaySchedule(today=datetime.datetime.today()):
    # get the day's schedule
    daySchedule = getDayTimeSchedule(today)

    if daySchedule["school"] == False:
        return []
    
    daySchedule = daySchedule["schedule"]

    classSchedule = getDayClassSchedule(today)
    class_count = 0

    switchFromAMPM = False

    for i in range(0, len(daySchedule)):
        blockType = daySchedule[i][2]

        if blockType == "class":
            blockType = classSchedule[class_count]
            class_count += 1

        if classData["classes"].keys().__contains__(blockType):
            blockType = getClassData()["classes"][blockType]

        startTime = daySchedule[i][0]

        endTime = daySchedule[i][1]

        # convert from x:xx to datetime
        startTime = datetime.datetime.strptime(startTime, "%H:%M").time()
        endTime = datetime.datetime.strptime(endTime, "%H:%M").time()

        if switchFromAMPM:
            # add 12 hours to the time
            startTime = (datetime.datetime.combine(datetime.date.today(), startTime) + timedelta(hours=12)).time()
            endTime = (datetime.datetime.combine(datetime.date.today(), endTime) + timedelta(hours=12)).time()

        if startTime > endTime:
            switchFromAMPM = True
            endTime = (datetime.datetime.combine(datetime.date.today(), endTime) + timedelta(hours=12)).time()

        daySchedule[i] = {
            "start": startTime,
            "end": endTime,
            "class": blockType
        }
    
    return daySchedule

"""
Gets the current class that is happening at the time.
:param time: the time to check for the class
"""
def getClass(time=datetime.datetime.now()):
    schedule = getDaySchedule(time)

    if len(schedule) == 0:
        return False

    for i in range(0, len(schedule)):
        block = schedule[i]
        
        if block["start"] <= time.time() <= block["end"]:
            return block

    return False

def getClassData():
    # return deep copy
    return copy.deepcopy(classData)

def time_difference(a=datetime.datetime.now(), b=datetime.datetime.now()):
    return timedelta(hours=a.hour, minutes=a.minute, seconds=a.second) - timedelta(hours=b.hour, minutes=b.minute, seconds=b.second)

def dnow():
    return datetime.datetime.now() #(2024, 11, 8, 10, 5, 20)

def now():
    return dnow().time()

loadClassesData()