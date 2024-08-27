from typing import Optional,List
from pydantic import BaseModel,EmailStr


#MOVIE
class MovieBase(BaseModel):
    title: str
    description: str
    release_year: int
    producer: str


class Movie(MovieBase):
    id: str


class MovieCreate(MovieBase):
    user_id: str



class MovieResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str 
    release_year: int 
    producer: str 


#RATING

class RatingBase(BaseModel):
    rating_comment: str = None

class RatingCreate(RatingBase):
    movie_id: str
    user_id: str
    rate: int 


class RateResponse(RatingBase):
    Rate_id: str


#COMMENT
class CommentBase(BaseModel):
    pass

 
class Comment(CommentBase):
    movie_id: str
    user_id: str
    parent_user_id: Optional[str]
    created_at: str
    content: str
    comments:Optional[dict]


class CommentEdit(CommentBase):
   
    created_at: str
    content: str
  
 




class CommentResponse(CommentBase):
    user_id: str
    movie_id: str
    parent_user_id: str 
    created_at: str
    content: str
    



    
    


#USER
class UserBase(BaseModel):
    username: str 
   

class UserCreate(UserBase):
    username: str 
    password: str 

class UserRead(UserBase):
    id: str

class UserDB(UserBase):
    full_name: str
    hash_password: str 

class UserUpdate(UserBase):
    username: str = None
    email: EmailStr = None
    password: str = None
