from apscheduler.schedulers.background import BackgroundScheduler
from youtube_fetcher import fetch_all

scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            fetch_all,
            trigger="interval",
            minutes=10,
            id="youtube_fetch_job",
            replace_existing=True
        )
        scheduler.start()
        print("⏱ Scheduler démarré (toutes les 10 minutes)")
