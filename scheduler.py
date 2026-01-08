from apscheduler.schedulers.background import BackgroundScheduler
from youtube_fetcher import fetch_all

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_all,
        trigger="interval",
        minutes=5
    )
    scheduler.start()
    print("⏱ Scheduler démarré (toutes les 5 minutes)")
