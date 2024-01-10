from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/vote",
    tags=['Like/Dislike Posts']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"Post with id: {vote.post_id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            error_response = {
                "status": "error",
                "id": -1,
                "data": f"user {current_user.id} has alredy voted on post {vote.post_id}"
            }
            return JSONResponse(content=error_response, status_code=409)
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            error_response = {
                "status": "error",
                "id": -1,
                "data": "Vote does not exist"
            }
            return JSONResponse(content=error_response, status_code=404)

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"status": "success", "id": current_user.id, "data": "successfully deleted vote"}
