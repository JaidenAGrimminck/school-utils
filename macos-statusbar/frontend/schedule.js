
let editsMade = {};
let refreshShown = true;

let refreshDialog;

function makeEdit(index, key, value) {
    editsMade[index] = { ...editsMade[index], [key]: value };

    if (!refreshShown) {
        toggleRefreshDialog();
    }
}

function toggleRefreshDialog() {
    if (refreshDialog === undefined) {
        refreshDialog = document.getElementById('refresh');
    }

    if (refreshShown) {
        refreshDialog.style.display = 'none';
    } else {
        refreshDialog.style.display = 'flex';
    }

    refreshShown = !refreshShown;
}

class Schedule {
    constructor() {
        this.schedule = [];

        this.viewingDate = new Date();
    }

    async getTodaysSchedule() {
        const req = fetch("/api/schedule/today");

        const res = await req;

        if (res.ok) {
            this.schedule = await res.json();
        }
    }

    async getSchedule() {
        const req = fetch("/api/schedule/day/" + this.viewingDate.getFullYear() + "/" + (this.viewingDate.getMonth() + 1) + "/" + this.viewingDate.getDate());

        const res = await req;

        if (res.ok) {
            this.schedule = await res.json();
        }
    }

    async goToToday() {
        this.viewingDate = new Date();

        await this.getTodaysSchedule();
        await createScheduleItems();
    }

    async goBackOneDay() {
        this.viewingDate.setDate(this.viewingDate.getDate() - 1);

        await this.getSchedule();
        await createScheduleItems();
    }

    async goForwardOneDay() {
        this.viewingDate.setDate(this.viewingDate.getDate() + 1);

        await this.getSchedule();
        await createScheduleItems();
    }
}

window.addEventListener("load", async () => {
    const schedule = new Schedule();
    await schedule.getTodaysSchedule();

    window.schedule = schedule;
    
    await createScheduleItems();

    //document.getElementById()
});