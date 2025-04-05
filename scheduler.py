import schedule
import time
import subprocess

def job():
    subprocess.run(["python3", "etl_pipeline.py"])
    subprocess.run(["python3", "load_to_db.py"])

schedule.every().day.at("11:11").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
