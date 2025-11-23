Pill Pop Reminder: Simple Medicine Alarm Web App
 Overview of the Project
Pill Pop Reminder is a lightweight, single-page web application built with Flask (Python) designed to help individuals or caregivers keep track of daily medicine schedules. The application runs a dedicated background thread to continuously monitor the current time against set reminder times, triggering a visual alert and an audible alarm directly in the browser when a dose is due.

 IMPORTANT NOTE: This application is designed as a functional prototype. All reminder data is stored in memory and will be lost if the application or server restarts. It is intended to run continuously on a local machine.

 Features
Daily Recurring Reminders: Set a specific time (HH:MM) for a daily reminder, including the patient's name and medication details.

Custom Alarm Sounds: Users can upload their own .mp3, .wav, or .ogg files to use as unique ringtones for different reminders.

Background Monitoring: A dedicated Python thread checks all active reminders every 30 seconds to ensure timely alerts.

Visual and Audible Alerts: When a reminder is due, a prominent alert box appears on the main page, and the selected custom sound (or default silent behavior) is played via the browser's audio tag.

Automatic Daily Reset: After an alarm triggers, the system automatically calculates the next due time for the following day.

Simple CRUD Interface: Easily add or remove reminders via the single web dashboard.

 Technologies/Tools Used
Backend Framework: Flask (Python)

Concurrency: Python's native threading module for background scheduling.

File Handling: werkzeug.utils.secure_filename for securing uploaded ringtone filenames.

Frontend: Simple HTML and CSS embedded directly in the Python file using render_template_string.

 Steps to Install & Run the Project
1. Prerequisites
You must have Python 3 installed on your system.

2. Setup
Create a new directory for your project and save the provided code as app.py inside it.

3. Install Dependencies
You need to install the Flask framework and werkzeug.

Bash

pip install Flask werkzeug
4. Run the Application
Execute the Python file. The application will start and run on your local machine.

Bash

python app.py
5. Access the Web App
Open your web browser and navigate to the following address:

http://127.0.0.1:5000/
You should see the main reminder dashboard.

 Instructions for Testing
Follow these steps to quickly test the main features of the application.

1. Test Ringtone Upload
In the "Upload Alarm Sound" section, click "Choose File."

Select an audio file (must be .mp3, .wav, or .ogg).

Click "Upload Audio".

A success message will flash, and the filename should appear in the "Available custom sounds" list.

2. Test Reminder Creation
Navigate to the "Set a New Daily Reminder" section.

Set the Time to be approximately one minute ahead of the current time (e.g., if it's 10:00, set it to 10:01).

Fill out the Name and Medicine Name/Dose fields.

(Optional) Select your uploaded custom sound from the dropdown.

Click "Add New Reminder".

3. Test Alarm Triggering
KEEP THE BROWSER PAGE OPEN and visible.

Wait for the scheduled time (the background thread checks every 30 seconds).

When the time is reached, a yellow alert box will appear at the top of the screen, and the selected audio will play automatically.

Once the main page is reloaded (which happens automatically if the browser is kept open), the alarm state will be cleared, and the "Next check time" for that reminder will jump ahead by 24 hours.

4. Test Reminder Deletion
Find an active reminder in the "Active Reminders" section.

Click the "Remove" button next to it.

The reminder will be instantly removed from the list.

 Screenshots (Recommended)
Description	Image Tag
The main reminder dashboard showing the input forms and active alarms.	
A visual representation of the background thread checking the time.# TimelyMeds
Helping seniors take medicines on time, every time
