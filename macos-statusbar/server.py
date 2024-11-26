import flask
import threading
import classes
import json
import datetime

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = flask.Flask(__name__)

# use /frontend as the root directory
@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route("/status")
def status():
    return "OK"

@app.route("/api/schedule/today")
def todaySchedule():
    now = datetime.datetime.now() #datetime.datetime(2024, 11, 13)
    today = classes.getDaySchedule(now)
    for (i, block) in enumerate(today):
        today[i]["start"] = str(block["start"])
        today[i]["end"] = str(block["end"])
    return json.dumps(today)

@app.route("/api/schedule/day/<int:year>/<int:month>/<int:day>")
def daySchedule(year, month, day):
    today = classes.getDaySchedule(datetime.datetime(year, month, day))
    for (i, block) in enumerate(today):
        today[i]["start"] = str(block["start"])
        today[i]["end"] = str(block["end"])
    return json.dumps(today)

# /api/schedule/edit post request
@app.route("/api/schedule/edit", methods=["POST"])
def editSchedule():
    data = flask.request.json
    
    keys = data.keys()
    # keys are a list of numbers, where each number is the index of the block of the day to edit.
    date = data["date"]

    # get the day schedule
    day = classes.getDaySchedule(datetime.datetime(date["year"], date["month"], date["day"]))

    for key in keys:
        if key == "date":
            continue

        key = int(key)
        block = day[key]
        className = block["class"]["name"]
        edits = data[str(key)]

        editingClass = None
            
        for classKey in classes.classData["classes"].keys():
            if classes.classData["classes"][classKey]["name"] == className:
                editingClass = classes.classData["classes"][classKey]
                break
        
        if editingClass == None:
            return "false"

        for editKey in edits.keys():
            if editKey == "class":
                className = edits[editKey]
                continue

            editingClass[editKey] = edits[editKey]
    
    classes.saveClassesData()
    return "true"

@app.route("/<path:path>")
def static_file(path):
    if path == "favicon.ico":
        return app.send_static_file("favicon.ico")
    if path == "/":
        return app.send_static_file("index.html")
    
    return app.send_static_file(path)

app.static_folder = "./frontend"

def createServer(port, searchForNewPort=False):
    if not searchForNewPort:
        # check if port is in use
        try:
            # make it not verbose
            app.run(port=port)
            print(f"Server started on port {port}")
        except OSError:
            print(f"Port {port} is already in use. Please try another port.")
            print(OSError)
            return
    else:
        while True:
            try:
                app.run(port=port)
                break
            except OSError:
                port += 1
                print(f"Port {port - 1} is already in use. Trying port {port}...")
    

def startServer(port, searchForNewPort=False):
    threading.Thread(target=createServer, args=(port, searchForNewPort)).start()

    print(f"Server starting on port {port}...")

if __name__ == "__main__":
    startServer(11732, False)
