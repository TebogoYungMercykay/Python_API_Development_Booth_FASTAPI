from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, aliased
from typing import List, Optional
from fastapi.responses import JSONResponse

from sqlalchemy import func
from .. import models, schemas, utils, oauth2 
from ..database import get_db

MESSAGE_UNAUTHORIZED = "You are not authorized to perform this action."

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", response_model=schemas.JSONListPostOut)
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)\
            .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "Posts not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    return schemas.JSONListPostOut(status="success", id=current_user.id, data=posts)

@router.post("/all_posts", response_model=schemas.JSONAllPostOut)
def all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 8, skip: int = 0, search: Optional[str] = ""):
    posts_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .group_by(models.Post.id).order_by(models.Post.created_at.desc())\
        .limit(limit).offset(skip)

    posts_and_votes = posts_query.all()
    
    if not posts_and_votes:
        error_response = {
            "status": "error",
            "id": -1,
            "data": "Posts not found."
        }
        return JSONResponse(content=error_response, status_code=404)
    
    replies_dict = {post.id: [] for post, _ in posts_and_votes}
    replies_query = db.query(models.Reply).filter(models.Reply.post_id.in_([post.id for post, _ in posts_and_votes]))

    for reply in replies_query.all():
        replies_dict[reply.post_id].append(reply)

    all_posts_out_list = []
    for post, votes in posts_and_votes:
        post_out = schemas.AllPostOut(Post=post, votes=votes, replies=replies_dict.get(post.id, []))
        all_posts_out_list.append(post_out)

    return schemas.JSONAllPostOut(status="success", id=current_user.id, data=all_posts_out_list)


@router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=schemas.JSONPost)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return schemas.JSONPost(status="success", id=current_user.id, data=new_post)


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if vote.dir > 1:
        vote.dir = 1
    elif vote.dir < 0:
        vote.dir = 0
    
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
        
        return {"status": "success", "id": current_user.id, "data": "successfully added vote"}
    
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


@router.post("/{id}", response_model=schemas.JSONPostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post, votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    replies = db.query(models.Reply).filter(models.Reply.post_id == id).all()
    
    if not post:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"post with id: {id} was not found"
        }
        return JSONResponse(content=error_response, status_code=404)

    return schemas.JSONPostOut(status="success", id=current_user.id,
                               data=schemas.PostOut(Post=post, votes=votes, replies=replies))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"post with id: {id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)

    if post.owner_id != current_user.id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)

    post_query.delete(synchronize_session=False)
    db.commit()

    content_response = {
        "status": "success",
        "id": -1,
        "data": "No Content"
    }
    return JSONResponse(content=content_response, status_code=204)


@router.put("/{id}", response_model=schemas.JSONPost)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"post with id: {id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)

    if post.owner_id != current_user.id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    return schemas.JSONPost(status="success", id=current_user.id, data=post_query.first())


@router.post('/create_reply/{id}', response_model=schemas.JSONRepliesData)
def create_reply(id: int, reply_post: schemas.Replies, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.doctor_id == current_user.id).first()
    if not doctor or id != reply_post.post_id:
        error_response = {
            "status": "error",
            "id": -1,
            "data": MESSAGE_UNAUTHORIZED
        }
        return JSONResponse(content=error_response, status_code=401)

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        error_response = {
            "status": "error",
            "id": -1,
            "data": f"post with id: {id} does not exist"
        }
        return JSONResponse(content=error_response, status_code=404)

    new_post = models.Reply(user_id=current_user.id, **reply_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    response_obj = {"reply": new_post, "doctor": doctor }
    return schemas.JSONRepliesData(status="success", id=current_user.id, data=response_obj)

