import rumps
import requests
import threading
import json
import datetime
import copy
import flask
import classes
import sys
from datetime import timedelta

url = ""

preferences = {}

# for an animated "snore" effect on the str lol
snore_phase = 0
snores = [
    ".",
    ".z",
    ".zZ",
    ".z"
]

"""
Loads the URL to request the money on the student card from from the .env file
"""
def loadURL():
    global url

    # check if .env file exists
    try:
        with open(".env") as f:
            for line in f:
                if line.find("UPDATE_URL") != -1:
                    url = line[line.find("=") + 1:len(line)]
                    break
    except:
        with open(".env", "w") as f:
            f.write("UPDATE_URL=")

        url = ""
        print("created .env file")
        return

def loadPreferences():
    global preferences

    with open("data/preferences.json") as f:
        data = json.load(f)

        preferences = data

    print("loaded your preferences!")

MAIN_DISPLAY = None

class DisplayOption(rumps.MenuItem):
    def __init__(self, key, title):
        super(DisplayOption, self).__init__(title, callback=self.clicked)
        self._key = key

        if preferences["display"][key]:
            self.state = 1
        else:
            self.state = 0

    def clicked(self, arg1=None, arg2=None, arg3=None, arg4=None):
        preferences["display"][self._key] = not preferences["display"][self._key]

        with open("data/preferences.json", "w") as f:
            json.dump(preferences, f)

        #print("Updated display preferences")
        # update the display
        self.state = 1 if preferences["display"][self._key] else 0

        MAIN_DISPLAY.updateTitle()

"""
A menu containing all of the display options
"""
class DisplayMenu(rumps.MenuItem):
    def __init__(self):
        super(DisplayMenu, self).__init__("Display")
        
        # add the display options
        for key in preferences["display"].keys():
            if key == "divider":
                continue
            if type(preferences["display"][key]) is not bool:
                continue
            if not preferences["has_updating_scheme"] and key == "euros":
                continue
            
            self.add(DisplayOption(key, key.capitalize()))

class UpdatableMenu(rumps.MenuItem):
    def __init__(self, placeholder="", callback=None):
        super(UpdatableMenu, self).__init__(placeholder, callback=self.clicked)

        self.cback = callback

    def clicked(self, _=None, __=None, ___=None):
        if self.cback != None:
            self.cback()
        pass

    def updateTitle(self, title):
        self.title = title

"""
The main menu that lives in the status bar.
"""
class PriceBarApp(rumps.App):
    def __init__(self):
        super(PriceBarApp, self).__init__(preferences["text"]["default"])
        self.menu = [
            UpdatableMenu("time_update", lambda: self.openClassEditor()),
            UpdatableMenu("money", lambda: self.updateURL()) if preferences["has_updating_scheme"] else rumps.separator,
            rumps.separator,
            "Update URL" if preferences["has_updating_scheme"] else rumps.separator, 
            rumps.separator, DisplayMenu(), rumps.separator]

        self.euroCount = -1
        self.centCount = -1

        self.currentClass = None
        self.nextClass = None
        self.day = None

        self.updateClass()

        if preferences["has_updating_scheme"]:
            # setup an interval to update the price every 10 minutes
            self.update()

            set_interval(self.update, 600)
        else:
            self.updateTitle()

        set_interval(self.updateTitle, 1)

    def openClassEditor(self):
        # open the class editor
        print("Opening class editor")
        pass

    @rumps.clicked("Update URL")
    def updateURL(self, _):
        global url

        # ask for a prompt
        response = rumps.Window("""
        1. Scan the QR code on the back of your student ID card with your phone\n
        2. Copy the URL from the browser, and open it on your computer\n
        2. Enter the URL here to update the price:\n
        """).run()

        if response.clicked:
            url = response.text
            
            if url.find("https://mijnkniponline.nl") == -1:
                rumps.alert("Invalid URL", "The URL must be from mijnkniponline")
            else:
                with open(".env", "w") as f:
                    f.write("UPDATE_URL=" + url)

                self.update()

    def update(self):
        global url

        print("loading from " + url + " ...")
        
        response = None

        try:
            response = requests.get(url)
        except:
            self.euroCount = -1
            self.centCount = -1
            self.updateTitle()
            print("Error loading from " + url)
            return

        if response.status_code == 200:
            text = response.text

            euroIndex = text.find("€")

            if euroIndex != -1:
                substr = text[euroIndex + 1:len(text)]
                end = substr.find("<")

                if end != -1:
                    substr = substr[0:end]

                    euro = substr[0:substr.find(",")]
                    cent = substr[substr.find(",") + 1:len(substr)]

                    self.euroCount = int(euro)
                    self.centCount = int(cent)
                    
                    print("Euro: " + str(self.euroCount) + " Cent: " + str(self.centCount))
        else:
            self.euroCount = -1
            self.centCount = -1
        
        self.updateTitle()

    def updateClass(self):
        time = classes.dnow()

        class_ = classes.getClass(time)
        day_schedule = classes.getDaySchedule(time)
        if class_ != False:
            self.currentClass = class_
            index = day_schedule.index(class_)
            if index + 1 < len(day_schedule):
                self.nextClass = day_schedule[index + 1]
            else:
                self.nextClass = None
        else:
            self.currentClass = None

            if len(day_schedule) > 0:
                prev = datetime.time(0, 0)
                for i in range(0, len(day_schedule)):
                    block = day_schedule[i]

                    if time.time() < block["start"] and time.time() > prev:
                        self.nextClass = block
                        break

                    prev = block["end"]
            else:
                self.nextClass = None
                
        self.day = classes.getDayTimeSchedule(time)

    def updateTitle(self):
        global snore_phase

        euroStr = ""

        if self.euroCount != -1 and self.centCount != -1:
            centStr = str(self.centCount)
            if len(centStr) == 1:
                centStr = "0" + centStr

            euroStr = "€" + str(self.euroCount) + "." + centStr
        else:
            euroStr = "€ -.--"

        classStr = ""
        fullStr = ""

        time = classes.now()

        if (self.currentClass != None):
            cclass = self.currentClass

            diff = classes.time_difference(cclass["end"], time)

            if (time >= cclass["start"] and time <= cclass["end"]):
                classStr = preferences["text"]["ends_in"]

                classStr = classStr.replace("$CLASS$", cclass["class"]["name"])
                classStr = classStr.replace("$TIME$", str(diff))

                fullStr = str(classStr)

                if preferences["display"]["time only"]:
                    classStr = str(time)
            else:
                self.updateClass()
                classStr = "-:--"
        elif self.nextClass != None:
            time_till = classes.time_difference(self.nextClass["start"], time)

            classStr = preferences["text"]["starts_in"]

            classStr = classStr.replace("$CLASS$", self.nextClass["class"]["name"])
            classStr = classStr.replace("$TIME$", str(time_till))

            fullStr = str(classStr)

            if preferences["display"]["time only"]:
                classStr = str(time)
        else:
            if self.day["school"]:
                classStr = preferences["text"]["no_more_classes"]
            else:
                classStr = preferences["text"]["no_classes"]
            
            fullStr = str(classStr)
        
        if fullStr.find("$SNORE$") != -1:
            fullStr = fullStr.replace("$SNORE$", snores[snore_phase])

        if classStr.find("$SNORE$") != -1:
            classStr = classStr.replace("$SNORE$", snores[snore_phase])
            snore_phase += 1
            if snore_phase >= len(snores):
                snore_phase = 0

        # update the first menu item
        self.menu["time_update"].updateTitle(fullStr)
        
        title = []

        if (preferences["has_updating_scheme"]):
            if preferences["display"]["euros"]:
                title.append(euroStr)
            self.menu["money"].updateTitle(euroStr)
        
        if preferences["display"]["class"]:
            title.append(classStr)

        if len(title) == 0:
            title.append(preferences["text"]["default"])

        #print("Title: " + preferences["display"]["divider"].join(title))

        self.title = preferences["display"]["divider"].join(title)
        pass

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

if __name__ == "__main__":
    # get arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            print("Success!")
            sys.exit(0)
    else:
        loadURL()
        loadPreferences()

        MAIN_DISPLAY = PriceBarApp()
        MAIN_DISPLAY.run()
