import schedule
import time
import subprocess

def job():
    subprocess.run(["python", "etl_pipeline.py"])
    subprocess.run(["python", "load_to_db.py"])

schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
