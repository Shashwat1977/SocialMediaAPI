from unittest import skip
from .. import schemas
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import utils
from ..database import SessionLocal, engine,get_db
from .. import models
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    tags = ['Post']
)

@router.get('/posts',response_model=List[schemas.PostOut])
def posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),skip:int=0,limit:int=10,search:Optional[str]=""):
    # return {'posts':'This is the post'}
    # return myposts
    # cursor.execute(""" SELECT * FROM \"Posts\" """)
    # post = cursor.fetchall()
    # print(current_user)
    # post = db.query(models.Post).offset(skip).limit(limit).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter = True).group_by(models.Post.id).all()
    print(results)
    return results

# @app.post('/createpost')
# def create(payload : dict = Body(...)):
#     return f'Title {payload["title"]} '

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def post(post:schemas.PostCreate,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # print(post.title)
    # my_post = post.dict()
    # my_post['id'] = randrange(1,10000000)
    # myposts.append(my_post)
    # return {"Message": "Post Created Succesfully",
    #         "Content" : post.dict()}
    # cursor.execute("""INSERT INTO \"Posts\" (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    # return {"data":post}

    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Creating a route for getting a specific route

# def get_pos(id):
#     for p in myposts:
#         if p['id'] == id:
#             return p
    

@router.get('/posts/{id}',response_model= schemas.PostOut)
def get_post(id : int,response : Response,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)): # Validating the int with help of FASTAPI
    # cursor.execute("""SELECT * FROM \"Posts\" WHERE id = %s""",((str)(id)))
    # pos = cursor.fetchone()
    # pos = db.query(models.Post).filter(models.Post.id == id).first()
    pos = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not pos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given id : {id} does not exist")
    return pos

# defining the functionality for delete function

# def find_index(id):
#     for i,p in enumerate(myposts):
#         if p['id'] == id:
#             return i
#     return None

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id : int,response : Response,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # index = find_index((int)(id))
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given id : {id} does not exist")
    # myposts.pop(index)
    # cursor.execute(""" DELETE FROM \"Posts\" WHERE id = %s RETURNING *""",((str)(id)))
    # pos = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given id : {id} does not exist")
    # conn.commit()
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Unauthorized access not allowed")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#definingggg te functionality for the update request

@router.put("/posts/{id}",response_model = schemas.Post)
def update(id:int,post:schemas.PostCreate,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # ind = find_index((int)(id))
    # if ind == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given id : {id} does not exist")
    # post_data = post.dict()
    
    # post_data['id'] = id
    # myposts[ind] = post_data
    # return {"Message": post_data}
    # cursor.execute("""UPDATE \"Posts\" SET title = %s,content=%s,published=%s WHERE id = %s RETURNING *""",
    # (post.title,post.content,post.published,(str)(id)))
    # pos = cursor.fetchone()
    pos = db.query(models.Post).filter(models.Post.id == id)
    
    if pos.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The given id : {id} does not exist")
    # conn.commit()
    if pos.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Unauthorized access not allowed")
    pos.update(post.dict(),synchronize_session=False)
    db.commit()
    return pos.first()
