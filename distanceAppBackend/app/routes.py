from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud

router = APIRouter()


@router.post("/distance", response_model=schemas.DistanceQueryRead)
def calculate_distance(
    query_data: schemas.DistanceQueryCreate,
    db: Session = Depends(get_db)
):
    db_result = crud.create_distance_query(db, query_data)
    if db_result is None:
        raise HTTPException(status_code=400, detail="Unable to get distance for given addresses.")

    distance_read = schemas.DistanceQueryRead.model_validate(db_result)
    return distance_read


@router.get("/history", response_model=list[schemas.DistanceQueryRead])
def read_history(db: Session = Depends(get_db)):
    return crud.get_all_queries(db)
