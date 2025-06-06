from fastapi import APIRouter, HTTPException, Request, Depends
from src.modals.tables import SortUrls, Clicks
from src.configure.database import get_db
from datetime import datetime
from sqlalchemy.orm import Session

from src.api.service import create_sort_ulr, get_menual_long_url, update_menual_long_url

router = APIRouter()

@router.get("/{slug}")
async def get_long_url(slug: int, db: Session = Depends(get_db)):
    """Retrieves the original long URL using the short slug.
    Returns a 404 if the slug doesn’t exist.
    """
    response = await get_menual_long_url(slug, db)
    if not response:
        raise HTTPException(status_code=404, detail="Slug not found")   
    return response


@router.post("/shorten")
async def shorten_url(long_url: str, db: Session = Depends(get_db)):
    """
    Shortens a long URL and returns the shortened version.
    If the long URL already exists, return the existing short link.
    """
    # Logic to create a short URL from a long URL
    try:
        response = await create_sort_ulr(long_url, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{slug}")
async def update_long_url(slug: str, new_long_url: str, db: Session = Depends(get_db)):
    """
    Updates the long URL associated with an existing slug.
    Validates the new URL and applies expiration logic.
    """
    response = await update_menual_long_url(slug, new_long_url, db=db)
    if not response:
        raise HTTPException(status_code=404, detail="Slug not found")
    return response


@router.get("/")
async def url_clicks(request: Request, db:Session= Depends(get_db)):
    """
    Retrieves the number of clicks for each short URL.
    """
    # # Store the number of clicks each short URL has received.

    sort_urls = db.query(SortUrls).all()
    get_request_url = request.url.path('/')
    if get_request_url in sort_urls:
        clicks = db.query(Clicks).filter(Clicks.sort_url_id == sort_urls.id).first()
        if clicks:
            return {
                "short_url": sort_urls.short_url,
                "click_count": clicks.click_count,
                "last_clicked_at": clicks.last_clicked_at
            }
        else:
            click = Clicks(
                sort_url_id=sort_urls.id,
                click_count=clicks.click_count + 1 if clicks else 1,
                last_clicked_at=datetime.now()
            )
            db.add(click)
            db.commit()
            db.refresh(click)
            return {
                "short_url": sort_urls.short_url,
                "click_count": click.click_count,
                "last_clicked_at": click.last_clicked_at
            }
    
    