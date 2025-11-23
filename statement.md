##  Medication Reminder Application: Project Overview

This document outlines the problem, scope, target users, and key features for a Minimum Viable Product (MVP) of a web-based daily medication reminder system built on **Python Flask**.

---

## 1. Problem Statement

The primary problem this application addresses is the **human failure to consistently adhere to time-critical daily schedules, specifically for medication dosage**. Many individuals struggle to reliably remember the exact prescribed time for taking pills or administering doses. Missed doses or erratic timing directly compromise **treatment efficacy and patient health**.

This necessitates a straightforward, dedicated digital solution that runs continuously to provide **unambiguous, recurring, and customizable alerts** exactly when medication is due, thereby improving patient compliance and management efficiency.

---

## 2. Scope of the Project

The project's scope is strictly limited to an **MVP web-based daily reminder system** built on **Python Flask**. Its functionality is centered on local, single-user operation with **non-persistent data storage**.

### In-Scope Functionality:

* **Single-Page Web Interface:** Allows a user to **create, view, and delete** reminders (CRUD functionality).
* **Next Recurrence Logic:** Logic for calculating the next daily trigger time.
* **Multi-Threaded Background Checker:** A dedicated background thread ($\text{reminder\_checker}$) that polls the reminder list every **30 seconds**.
* **Customizable Audible Alarms:** Support for user-uploaded **MP3, WAV, or OGG files**, which are played only when the user is **actively viewing the web page**.
* **Visual Alert:** Highly visible alert displayed on the web page when a reminder is triggered.

### Out-of-Scope Limitations:

* **No Data Persistence:** All reminders are **lost upon server shutdown**.
* **Single-User System:** **No authentication** is supported.
* **Simple Recurrence Only:** Limited to **simple daily recurrence**; lacks advanced scheduling (e.g., weekly, monthly, or interval-based).
* **No External Notifications:** Relies entirely on the open web page for alerts; lacks integration with external notification systems (SMS, email, or OS-level push notifications).

---

## 3. Target Users

The application targets two primary user groups who require reliable, scheduled medication alerts.

### Primary Target: Individuals Managing Personal Medication

* A patient or individual who is **self-managing a predictable, recurring medication schedule**.
* Needs a simple, visual, and loud alert system requiring **minimal technical setup** beyond running the application locally.

### Secondary Target: Caregivers and Family Managers

* A key secondary user responsible for administering medication to dependents (e.g., the elderly, young children, or those with memory issues).
* For this group, the application acts as a **reliable scheduling assistant**, ensuring they fulfill their responsibilities at the correct time.

**Assumed User Environment:** The target user is expected to run the application on a **dedicated local machine** and can access a web browser, but they are not expected to be skilled in database management or complex server configuration.

---

## 4. High-Level Features

The application is characterized by four primary features designed for immediacy and ease of use:

### 1. Comprehensive Daily Reminder Management (CRUD)

Users can easily manage their entire schedule through a single form, inputting essential details:
* **Patient/Person's Name** (Context)
* **Medicine Name/Dose** (Action)
* **Required Daily Time** (Schedule Trigger)
* **Optional Notes** (e.g., "with food")
They also have clear controls to **remove** any existing reminder.

### 2. Audible and Customizable Alarm System

* The application supports the upload of **custom MP3, WAV, and OGG audio files**, allowing the user to select a unique and recognizable sound for each reminder.
* When a reminder is triggered, it displays a highly visible visual alert on the page and attempts to play the designated audio file **automatically through the browser**, providing both **auditory and visual cues**.

### 3. Non-Blocking, Concurrent Monitoring

* The core logic runs via a separate **reminder checker**.
* This non-blocking architecture ensures the **web server remains responsive** while the timer continuously **polls the list of reminders every 30 seconds**.
* This allows the system to check for due alarms independently of user interaction with the web interface.

### 4. Autonomous Recurrence Reset

* When an alarm condition is met (the set time is reached), the system instantly flags the reminder as 'due' for alerting purposes.
* It immediately calculates its next trigger time by adding exactly **24 hours**.
* This ensures the daily schedule is **automatically maintained** without requiring manual intervention from the user after the alarm has fired.
