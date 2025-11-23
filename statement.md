1. Problem Statement 
The primary problem this application aims to solve is the human failure to consistently adhere to time-critical daily schedules, specifically for medication dosage. Many individuals, whether managing chronic conditions or simply following a temporary course of treatment, struggle with reliably remembering the exact time prescribed for taking pills or administering doses. Missed doses or erratic timing can compromise treatment efficacy and patient health. This necessitates a straightforward, dedicated digital solution that runs continuously to provide unambiguous, recurring, and customizable alerts exactly when medication is due, thereby improving patient compliance and management efficiency.



2. Scope of the Project 
The project's scope is strictly limited to a minimum viable product (MVP) web-based daily reminder system built on Python Flask. Its functionality centers on local, single-user operation with non-persistent data storage.

In-Scope Functionality: The core scope covers the development of a single-page web interface that allows a user to create, view, and delete reminders. It includes the logic for calculating the next daily recurrence time and a dedicated, multi-threaded background checker that polls the reminder list every 30 seconds. Crucially, it must support customizable audible alarms via user-uploaded MP3, WAV, or OGG files, which are played only when the user is actively viewing the web page.

Out-of-Scope Limitations: This application does not support data persistence; all reminders are lost upon server shutdown. It is strictly a single-user system with no authentication. It is also limited to simple daily recurrence and lacks advanced scheduling options (e.g., weekly, monthly, or interval-based reminders). Furthermore, it relies entirely on the open web page for alerts and lacks integration with external notification systems (SMS, email, or OS-level push notifications).



3. Target Users 
The application targets two primary user groups who share a common need for reliable, scheduled medication alerts.

Individuals Managing Personal Medication: The primary target is a patient or individual who is self-managing a predictable, recurring medication schedule. These users need a simple, visual, and loud alert system that requires minimal technical setup beyond running the application locally.

Caregivers and Family Managers: A key secondary user is a caregiver responsible for administering medication to dependents (such as the elderly, young children, or those with memory issues). For this group, the application acts as a reliable scheduling assistant, ensuring they fulfill their responsibilities at the correct time.

The target user is assumed to be running the application on a dedicated local machine and can access a web browser, but they are not expected to be skilled in database management or complex server configuration.



4. High-Level Features 
The application is characterized by four primary high-level features designed for immediacy and ease of use:

Comprehensive Daily Reminder Management (CRUD): Users can easily manage their entire schedule through a single form, inputting essential details: the Patient/Person's Name (context), the specific Medicine Name/Dose (action), the required Daily Time (schedule trigger), and optional Notes (e.g., "with food"). They also have clear controls to remove any existing reminder.

Audible and Customizable Alarm System: The application supports the upload of custom MP3, WAV, and OGG audio files, allowing the user to select a unique and recognizable sound for each reminder. When a reminder is triggered, it displays a highly visible visual alert on the page and attempts to play the designated audio file automatically through the browser, providing both auditory and visual cues.

Non-Blocking, Concurrent Monitoring: The application's core logic runs via a separate background thread (reminder_checker). This non-blocking architecture ensures the web server remains responsive while the timer continuously polls the list of reminders every 30 seconds. This allows the system to check for due alarms independently of user interaction with the web interface.

Autonomous Recurrence Reset: When an alarm condition is met (the set time is reached), the system instantly flags the reminder as 'due' for alerting purposes, and immediately calculates its next trigger time by adding exactly 24 hours. This ensures the daily schedule is automatically maintained without requiring manual intervention from the user after the alarm has fired.
