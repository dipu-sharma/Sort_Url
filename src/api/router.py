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


@router.get("/short.ly/{short_code}")
async def redirect_short_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Redirects short URL to original URL and tracks clicks
    """
    full_short_url = f"http://localhost:8000/short.ly/{short_code}"

    short_url = db.query(SortUrls).filter(SortUrls.short_url == full_short_url).first()
    
    if not short_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    click = db.query(Clicks).filter(Clicks.sort_url_id == short_url.id).first()
    
    if click:
        click.click_count += 1
        click.last_clicked_at = datetime.now()
        db.commit()
        db.refresh(click)
    else:
        print("No click found, creating a new one")
        click = Clicks(
            sort_url_id=short_url.id,
            click_count= 1,
            last_clicked_at=datetime.now()
        )
        db.add(click)
        db.commit()
        db.refresh(click)

    return {"click_count": click.click_count, "last_clicked_at": click.last_clicked_at}
    
    