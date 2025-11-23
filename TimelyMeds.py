# app.py
# A quick medicine reminder system, built in Flask.
# Only works if the page is kept open!

import os
from datetime import datetime, timedelta
import threading
import time

from flask import (
    Flask, render_template_string, request,
    redirect, url_for, send_from_directory, flash
)
# We need this to prevent bad file uploads
from werkzeug.utils import secure_filename

# --- App Setup ---
app = Flask(__name__)
# Just a placeholder, don't forget to change it.
app.secret_key = "secret-key-change-this"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RINGTONE_FOLDER = os.path.join(BASE_DIR, "static", "ringtones")

# Make sure the folder is there
os.makedirs(RINGTONE_FOLDER, exist_ok=True)

# These are the only extensions we will allow
ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg"}

# This is where all the reminder objects live
reminders = []
reminder_id_counter = 0 # Starting ID at 0, should probably start at 1, oh well

print("Ringtones found currently:", os.listdir(RINGTONE_FOLDER))


def allowed_file(filename: str) -> bool:
    # Quick check for the extension, slightly lazy way
    return filename.lower().endswith(('.mp3', '.wav', '.ogg'))

# --- HTML Template ---
# The entire front end is crammed in here.
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Pill Pop Reminder</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>

    body { font-family: Arial, sans-serif; background:#f4f4f4; margin:0; padding:0; }
    .container { max-width: 900px; margin: 20px auto; background:#fff; padding:20px; border-radius:8px; }
    h1 { text-align:center; color:#2c3e50; }
    label { display:block; margin-top:10px; font-size:1.05em; }

    input[type=text], input[type=time], textarea, select {
      width:100%; padding:10px; margin-top:5px; border-radius:4px; border:1px solid #ccc; font-size:1em;
    }
    textarea { resize:vertical; min-height:60px; }

    button { margin-top:15px; padding:10px 15px; font-size:1em; border:none; border-radius:4px;
              background:#27ae60; color:white; cursor:pointer; }
    button.delete { background:#c0392b; }
    button.small { padding:5px 8px; font-size:0.9em; }
    .reminder-list { margin-top:20px; }
    .card { background:#ecf0f1; padding:10px; border-radius:6px; margin-bottom:10px; }
    .card strong { display:block; font-size:1.1em; }

    .alert { background:#f39c12; color:#000; padding:10px; border-radius:4px; margin-bottom:10px; font-weight:bold; }
    .section-title { margin-top:25px; border-bottom:1px solid #ddd; padding-bottom:5px; }
    .flash { color:#c0392b; margin-top:10px; }
  </style>
</head>
<body>
<div class="container">
  <h1>Medicine Reminder</h1>

  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for m in messages %}
        <div class="flash">{{ m }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}


  {% if alerts %}
    {% for a in alerts %}
      <div class="alert">
        💊 **REMINDER DUE!** for {{ a["name"] }}: Take **{{ a["medicine"] }}** now (set for {{ a["time"] }}).
        {% if a["ringtone"] %}
          <br>Playing sound: {{ a["ringtone"] }}
        {% endif %}
      </div>
    {% endfor %}
  {% endif %}

  <h2 class="section-title">Upload Alarm Sound</h2>
  <form method="post" action="{{ url_for('upload_ringtone') }}" enctype="multipart/form-data">
    <input type="file" name="file" accept=".mp3,.wav,.ogg" required>
    <button type="submit">Upload Audio</button>
  </form>

  {% if ringtones %}
    <p>Available custom sounds:</p>
    <ul>
      {% for r in ringtones %}
        <li>{{ r }}</li>
      {% endfor %}
    </ul>
  {% else %}
    <p>No custom sounds uploaded yet.</p>
  {% endif %}

  <h2 class="section-title">Set a New Daily Reminder</h2>
  <form method="post" action="{{ url_for('add_reminder') }}">
    <label>Patient/Person's Name</label>
    <input type="text" name="name" required>

    <label>Medicine Name/Dose</label>
    <input type="text" name="medicine" required>

    <label>Time (Daily, e.g., 10:30)</label>
    <input type="time" name="time" required>

    <label>Notes (optional, e.g., "with food")</label>
    <textarea name="notes"></textarea>

    <label>Select custom sound</label>
    <select name="ringtone">
      <option value="">(Default/No Sound)</option>
      {% for r in ringtones %}
        <option value="{{ r }}">{{ r }}</option>
      {% endfor %}
    </select>

    <button type="submit">Add New Reminder</button>
  </form>

  <div class="reminder-list">
    <h2 class="section-title">Active Reminders</h2>
    {% if reminders %}
      {% for r in reminders %}
        <div class="card">
          <strong>{{ r["name"] }}</strong>
          Medicine: {{ r["medicine"] }}<br>
          Daily Time: **{{ r["time"] }}**<br>
          Next check time: {{ r["next_time"].strftime('%Y-%m-%d %H:%M') }}<br>
          Alarm Sound: {{ r["ringtone"] if r["ringtone"] else "None (Silent)" }}<br>
          {% if r["notes"] %}Notes: {{ r["notes"] }}<br>{% endif %}
          <form method="post" action="{{ url_for('delete_reminder', rid=r['id']) }}" style="margin-top:8px;">
            <button class="delete small" type="submit">Remove</button>
          </form>
        </div>
      {% endfor %}
    {% else %}
      <p>No reminders set.</p>
    {% endif %}
  </div>

  <h2 class="section-title">Help</h2>
  <ul>
    <li>Upload MP3/WAV/OGG files.</li>
    <li>**Keep this page open**.</li>
    <li>Alarm auto-resets daily.</li>
  </ul>
</div>


{% if alerts and alerts[0]["ringtone"] %}
<audio id="alarm-audio" autoplay>

  <source src="{{ url_for('serve_ringtone', filename=alerts[0]['ringtone']) }}" type="audio/mpeg">
  Your browser does not support the audio tag.
</audio>
<script>

  const audio = document.getElementById("alarm-audio");
  if (audio) {
    audio.play().catch(function(error){
        console.log("Autoplay failed.", error);
    });
  }
</script>
{% endif %}

</body>
</html>
"""

# --- Helper Logic ---

def compute_next_time(time_str: str) -> datetime:

    # Split time from input
    hour, minute = map(int, time_str.split(":"))
    current_time = datetime.now()


    # Set the time for today
    candidate_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)


    # If it's in the past, push it to tomorrow.
    if candidate_time < current_time:
        candidate_time += timedelta(days=1)

    return candidate_time


def reminder_checker():
    # This runs forever in the background thread.
    while True:
        current_time_now = datetime.now()


        for this_reminder in reminders:

            # Check if time to fire and if it's not already due
            if this_reminder["next_time"] <= current_time_now and not this_reminder["due"]:
                print("ALARM! %s needs %s" % (this_reminder['name'], this_reminder['medicine']))
                this_reminder["due"] = True

                # Reset the next trigger time for the next 24 hours
                this_reminder["next_time"] = compute_next_time(this_reminder["time"])


        # Don't check too often
        time.sleep(30)


# --- Flask Routes ---

@app.route("/", methods=["GET"])
def index():

    # Get reminders that are set to fire now
    active_alerts = [r for r in reminders if r.get("due")]


    for r in active_alerts:
        r["due"] = False # clear the flag


    available_ringtones = sorted(os.listdir(RINGTONE_FOLDER))


    return render_template_string(
        HTML_TEMPLATE,
        reminders=reminders,
        alerts=active_alerts,
        ringtones=available_ringtones,
    )


@app.route("/upload_ringtone", methods=["POST"])
def upload_ringtone():
    if "file" not in request.files:
        flash("No file part.")
        return redirect(url_for("index"))

    file_to_upload = request.files["file"]

    if file_to_upload.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))


    if file_to_upload and allowed_file(file_to_upload.filename):

        file_name = secure_filename(file_to_upload.filename)
        save_path = os.path.join(RINGTONE_FOLDER, file_name)
        file_to_upload.save(save_path)
        flash("Ringtone '" + file_name + "' uploaded successfully.")
    else:
        flash("File type not allowed.")

    return redirect(url_for("index"))


@app.route("/ringtones/<path:filename>")
def serve_ringtone(filename):

    return send_from_directory(RINGTONE_FOLDER, filename)


@app.route("/add", methods=["POST"])
def add_reminder():
    global reminder_id_counter

    # Grab the fields from the form
    name = request.form.get("name", "").strip()
    medicine = request.form.get("medicine", "").strip()
    time_str = request.form.get("time", "").strip()
    notes = request.form.get("notes", "").strip()
    ringtone = request.form.get("ringtone", "").strip()


    if name and medicine and time_str:

        reminder_id_counter += 1
        new_id = reminder_id_counter


        reminders.append(
            {
                "id": new_id,
                "name": name,
                "medicine": medicine,
                "time": time_str,
                "next_time": compute_next_time(time_str),
                "due": False,
                "notes": notes,
                "ringtone": ringtone,
            }
        )
        flash("Reminder added for %s." % name)
    else:
         flash("Error: Missing fields.")

    return redirect(url_for("index"))


@app.route("/delete/<int:rid>", methods=["POST"])
def delete_reminder(rid):
    global reminders

    # Rebuild the list without the deleted item
    reminders = [r for r in reminders if r["id"] != rid]

    flash("Reminder deleted.")

    return redirect(url_for("index"))


# --- Main Entry Point ---

if __name__ == "__main__":

    # Start the check thread
    t = threading.Thread(target=reminder_checker, daemon=True)
    t.start()


    # Run the web app
    app.run(debug=True, port=5000)