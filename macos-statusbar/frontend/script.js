
const deleteGoogleTranslateExtensionCauseItsAnnoying = false;

const beginningOffset = 10;
const pixelToHour = 40;

if (deleteGoogleTranslateExtensionCauseItsAnnoying) {
    window.addEventListener("load", () => {
        setInterval(() => {
            if (document.getElementById("gtx-trans") != null) {
                document.getElementById("gtx-trans").remove();
            }
        }, 1)
    })
}


async function createScheduleItems() {
    const classContainer = document.getElementsByClassName('classes')[0];

    const element = document.createElement('div');

    element.classList.add('class');
    element.style.top = `${beginningOffset}px`;

    const name = document.createElement('div');
    name.classList.add('class-name');
    element.appendChild(name);

    const time = document.createElement('div');
    time.classList.add('class-time');
    element.appendChild(time);

    classContainer.innerHTML = '';

    let createdHeights = 0;

    for (const item of window.schedule.schedule) {
        const classItem = element.cloneNode(true);

        classItem.getElementsByClassName('class-name')[0].innerText = item.class.name;
        classItem.getElementsByClassName('class-time')[0].innerText = `${to12HourTime(item.start)} - ${to12HourTime(item.end)}`;

        const start = getTime(item.start);
        const end = getTime(item.end);

        const startTime = start.hour + (start.minute / 60);
        const endTime = end.hour + (end.minute / 60);

        classItem.style.top = `${beginningOffset + (pixelToHour * (startTime)) - createdHeights}px`;
        classItem.style.height = `${(endTime - startTime) * pixelToHour}px`;

        classItem.style.backgroundColor = item.class.color;

        //if too dark background color, change text color to white
        const rgb = classItem.style.backgroundColor.match(/\d+/g);
        const brightness = Math.round(((parseInt(rgb[0]) * 299) + (parseInt(rgb[1]) * 587) + (parseInt(rgb[2]) * 114)) / 1000);
        if (brightness > 125) {
            classItem.style.color = "black";
        } else {
            classItem.style.color = "white";
        }

        // if (createdHeights == 0) {
        //     createdHeights += beginningOffset;
        // }
        createdHeights += (endTime - startTime) * pixelToHour;

        classContainer.appendChild(classItem);
    }

    // update the date
    const date = document.getElementById('date');

    date.innerText = window.schedule.viewingDate.toDateString();

    if (window.schedule.viewingDate.toDateString() === new Date().toDateString()) {
        date.innerText = "Today • " + date.innerText;
    } else if (window.schedule.viewingDate.toDateString() === new Date(new Date().setDate(new Date().getDate() + 1)).toDateString()) {
        date.innerText = "Tomorrow • " + date.innerText;
    }
}

function to12HourTime(hour) {
    if (typeof hour == "number") {
        if (hour === 0) {
            return 12;
        } else if (hour > 12) {
            return hour - 12;
        } else {
            return hour;
        }
    } else if (typeof hour == "string") {
        const [hour_, minute, second] = hour.split(':').map(Number);

        let str = '';
        if (hour_ === 0) {
            str = `12:${minute}:${second}`;
        } else if (hour_ > 12) {
            str = `${hour_ - 12}:${minute}:${second}`;
        } else {
            str = `${hour_}:${minute}:${second}`;
        }

        let spltStr = str.split(":");
        for (let i = 0; i < 3; i++) {
            if (spltStr[i].length == 1) {
                spltStr[i] = "0" + spltStr[i];
            }
        }

        return spltStr[0] + ":" + spltStr[1];
    }
}

function getTime(timeStr) {
    const [hour, minute, second] = timeStr.split(':').map(Number);

    return {hour, minute, second};
}

window.addEventListener("load", async () => {
    const timeContainer = document.getElementsByClassName('time')[0];

    for (let i = 0; i < 24; i++) {
        const time = document.createElement('div');
        time.classList.add('time-item');
        time.innerText = to12HourTime(i);
        timeContainer.appendChild(time);
    }
    
    toggleEditorShown();
    toggleRefreshDialog();
})

let editorShown = true;
let currentClassEditing = null;
const editor = document.getElementById('editor');

function moveEditorToMouse() {

    // move to mouse position
    editor.style.left = `${event.clientX}px`;
    editor.style.top = `${event.clientY - 10}px`;
}

function toggleEditorShown() {
    if (editorShown) {
        editor.style.display = 'none';
    } else {
        editor.style.display = 'block';
    }

    editorShown = !editorShown;
}

function updateEditorColor() {
    if (currentClassEditing) {
        let color = currentClassEditing.style.backgroundColor;

        if (color.includes("rgb")) {
            const rgb = color.match(/\d+/g);
            color = `#${parseInt(rgb[0]).toString(16).padStart(2, '0')}${parseInt(rgb[1]).toString(16).padStart(2, '0')}${parseInt(rgb[2]).toString(16).padStart(2, '0')}`;
        }

        editor.getElementsByClassName('editor-color')[0].value = color;
    }
}

//right clickl
document.addEventListener('contextmenu', event => {
    event.preventDefault();

    if (!editorShown) {
        toggleEditorShown();
    }

    moveEditorToMouse();

    //if clicked on class
    if (event.target.classList.contains('class')) {
        currentClassEditing = event.target;
        updateEditorColor();
    } else {
        currentClassEditing = null;
        toggleEditorShown();
    }
});

document.addEventListener('click', event => {
    //check if not clicking on editor
    if (!editor.contains(event.target) && editorShown) {
        toggleEditorShown();
    }
});

editor.getElementsByClassName('editor-color')[0].addEventListener('input', event => {
    if (currentClassEditing) {
        currentClassEditing.style.backgroundColor = event.target.value;
        let classIndex = Array.from(currentClassEditing.parentElement.children).indexOf(currentClassEditing);
        makeEdit(classIndex, "color", event.target.value);
    }
});

// on button click
editor.getElementsByClassName('editor-name')[0].addEventListener('click', event => {
    if (!currentClassEditing)
        return;

    const name = prompt("Enter new class name");

    if (currentClassEditing) {
        currentClassEditing.getElementsByClassName('class-name')[0].innerText = name;
        let classIndex = Array.from(currentClassEditing.parentElement.children).indexOf(currentClassEditing);
        makeEdit(classIndex, "name", name);
    }
});

function updateTimeStrip() {
    const time = 24 - (new Date().getHours() + (new Date().getMinutes() / 60));
    document.getElementsByClassName('current-time')[0].style.top = `${-(pixelToHour * (time))}px`;
}

setInterval(updateTimeStrip, 1000)
updateTimeStrip();