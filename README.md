


#  Pill Pop Reminder — Medicine Reminder Web App

A lightweight Flask-based web application that helps users remember to take their medications on time.
This app runs a background thread that continually checks for due reminders and triggers alerts with optional custom ringtones.

---

##  Overview

**Pill Pop Reminder** allows you to:

* Create daily medication reminders with:

  * Patient name
  * Medicine name/dosage
  * Time of day
  * Optional notes
  * Optional custom alarm sound
* Upload MP3/WAV/OGG ringtones for alert sounds
* Automatically play audio reminders in the browser
* View and delete active reminders
* Automatically re-schedule reminders for the next day
* Receive in-page alert banners when a reminder is due

The app must remain **open in the browser** to play sounds.

---

##  Features

### ✔ Reminder Management

* Add unlimited daily reminders
* Each reminder stores:

  * Name
  * Medication
  * Time
  * Notes
  * Selected ringtone
* Removal with a single click

###  Background Scheduler

* Runs in a separate Python thread
* Checks every **30 seconds**
* Triggers reminders and resets next day
* Flags alerts for the web interface to display

###  Audio Alerts

* Custom ringtone support
* Upload via the web interface
* Plays automatically when a reminder is due

###  Clean Web UI

* Responsive HTML layout
* Lists all reminders
* Displays due alerts at the top

---

##  Technologies Used

| Component     | Technology                       |
| ------------- | -------------------------------- |
| Backend       | **Python 3**, **Flask**          |
| Frontend      | HTML5, CSS, JavaScript           |
| Storage       | In-memory lists (no DB required) |
| File Handling | Werkzeug secure file uploads     |
| Scheduling    | Python `threading`, `datetime`   |



##  Installation & Setup

### 1️ Clone the Project




### 3️⃣ Install Dependencies



*(No other libraries needed)*

### 4️⃣ Directory Structure

Ensure this folder exists (the app creates it if missing):



### 5️⃣ Run the Application

```bash
python app.py
```

You should see output like:

```
Ringtones found currently: [...]
 * Running on http://127.0.0.1:5000/
```

Open the displayed URL in your browser.

---

## ▶ Using the App

### Add a Reminder

1. Fill in:

   * Name
   * Medication
   * Daily Time
   * Notes (optional)
   * Ringtone (optional)
2. Click **“Add New Reminder”**

### Upload Custom Sounds

1. Scroll to **“Upload Alarm Sound”**
2. Select an MP3/WAV/OGG file
3. Upload
4. Use it in your reminders

### How Alerts Work

* The background thread detects when a reminder is due
* The browser shows a bright banner
* A ringtone plays automatically (if selected)

💡 **Important:** Keep the webpage open, or audio may not play.

---

##  Testing Checklist

Use this list to confirm everything functions:

###  **Ringtone System**

* [ ] Upload an MP3/WAV/OGG file
* [ ] Verify it appears in the “Available custom sounds” list
* [ ] Add a reminder using the sound
* [ ] Wait for the time → sound should autoplay

###  **Reminder Scheduling**

* Set reminders very close to the current time (e.g. 1–2 min ahead)
* [ ] Alert banner appears
* [ ] Reminder plays (if sound selected)
* [ ] Reminder re-schedules for the next day automatically

###  **Reminder Deletion**

* [ ] Add two reminders
* [ ] Delete one
* [ ] Remaining reminder still works

###  **Thread Functionality**

* [ ] Terminal prints “ALARM!” when a reminder triggers
* [ ] Page refresh shows alerts

Everything working? You're good to go! �

---

##  Security Notes

* Change `app.secret_key` before deploying
* App uses no authentication—use only locally or behind a protected network

---

