from celery import Celery
from src.modals.tables import SortUrls
from src.configure.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

@celery_app.task
def expire_urls():
    """Expire URLs older than 30 days.""" 
    db = next(get_db())
    get_thirty_days_ago = datetime.now() - timedelta(days=30)
    expired_urls = SortUrls.query.filter(SortUrls.created_at < get_thirty_days_ago).all()
    for url in expired_urls:
        db.delete(url)
        db.commit()
    return "Expired URLs older than 30 days have been deleted."
    