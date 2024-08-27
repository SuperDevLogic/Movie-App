from fastapi import HTTPException,status
from typing import Dict
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from api.app.schema import MovieCreate, MovieBase,MovieResponse,UserCreate,UserUpdate,UserBase,UserDB,UserRead,RatingCreate,Comment,CommentResponse,CommentEdit
from api.app.database import movies_collection,users_collection,ratings_collection,comments_collection
from api.app.serializer import user_serializer,Subcomment_serializer,user_serializer_password,movie_serializer,rating_serializer,comment_serializer,ratings_serializer,comments_serializer,Comment_edit_serializer

      #MOVIE CRUD
class CRUDService:
    @staticmethod
    def create_movie(movie_in: MovieCreate):
        movie_in.user_id = str(movie_in.user_id)
        movie_in_data = jsonable_encoder(movie_in)
        movie_id = movies_collection.insert_one(movie_in_data).inserted_id
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        return movie_serializer(movie)
 
    @staticmethod
    def get_all_movies(skip: int = 0, limit: int = 10):
        movies = movies_collection.find().skip(skip).limit(limit)  
        return [movie_serializer(movie) for movie in movies]
    
  
    
    @staticmethod
    def update_movie(movie_id: str, movie_update_in: MovieResponse):
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})

        if not movie:
            return None

        movie_update_data = movie_update_in.model_dump(exclude_unset=True)
        movie_updated = movies_collection.find_one_and_update(
            {"_id": ObjectId(movie_id)}, {"$set": movie_update_data}, return_document=True
        )
        return movie_serializer(movie_updated)
    @staticmethod
    def delete_movie(movie_id):
        movies_collection.find_one_and_delete({"_id": ObjectId(movie_id)})
        return {"message": "movie deleted successfully"}


   #USER CRUD
class UserCRUDService:
    @staticmethod
    def create_user(user_data: UserCreate, hashed_password: str):
        # verify if user exists
        if users_collection.find_one({"username": user_data.username}):
            raise HTTPException(detail='User already exists', status_code=status.HTTP_400_BAD_REQUEST)
        # continue if user does not exist
        user_data = jsonable_encoder(user_data)
        user_document_data = users_collection.insert_one(
            {
                "username": user_data.get('username'),
                "name": user_data.get('name'),
                "full_name": user_data.get('full_name'),
                "hashed_password": hashed_password
            }
        )
        user_id = user_document_data.inserted_id
        user_document = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )
        return user_serializer(user_document)
    
    @staticmethod
    def get_user_by_username(username: str) -> UserDB:
        user = users_collection.find_one({"username": username})
        if user:
            return user_serializer(user)
        return None
    
    @staticmethod
    def get_user_by_username_with_hash(username: str) -> UserDB:
        user = users_collection.find_one({"username": username})
        if user:
            return user_serializer_password(user)
        return None
    

     #RATING CRUD
class RatingCRUDService:
    @staticmethod
    def create_rating(rating_in: RatingCreate):
        rating_in.user_id = str(rating_in.user_id)
        rating_in.movie_id = str(rating_in.movie_id)
        rating_in.rate = int(rating_in.rate)
        rating_in_data = jsonable_encoder(rating_in)
        rating_id = ratings_collection.insert_one(rating_in_data).inserted_id
        rating = ratings_collection.find_one({"_id":ObjectId (rating_id)})
        return rating_serializer(rating)
 
    @staticmethod
    def get_all_ratings(skip:int=0, limit:int=10):
        ratings = ratings_collection.find().skip(skip).limit(limit)  
        return [ratings_serializer(ratings)]
    
    
    
     #COMMENTS CRUD
class COMMENTService:
    @staticmethod
    def create_comment(comment_in: Comment):
        comment_in.movie_id = str(comment_in.movie_id)
        comment_in.user_id = str(comment_in.user_id)
        comment_in.created_at = str(comment_in.created_at)
        comment_in.comments = dict(comment_in.comments)
        comment_in_data = jsonable_encoder(comment_in)
        comment_id = comments_collection.insert_one(comment_in_data).inserted_id
        comment = comments_collection.find_one({"_id":ObjectId(comment_id)})
        return comment_serializer(comment)
    



    @staticmethod
    def create_sub_comment(sub:CommentResponse):
        sub.user_id = str(sub.user_id)
        sub.movie_id = str(sub.movie_id)
        sub.parent_user_id = str(sub.parent_user_id)
        sub.created_at = str(sub.created_at)
        sub.content = str(sub.content)
        subdata = jsonable_encoder(sub)
        subd = comments_collection.find_one_and_update({"_id": ObjectId(sub.parent_user_id)},
        {"$push": {"comments": subdata}})
        return comment_serializer(subd)
 

    @staticmethod
    def get_all_comments(skip:int= 0, limit:int= 10):
        comments = comments_collection.find().skip(skip).limit(limit)  
        return [Subcomment_serializer(comment) for comment in comments]
    
    
    
    @staticmethod
  
    
    @staticmethod
    def update_comment(comment_id: str, comment_update_in: CommentEdit):
        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
     
        if not comment:
            return None

        comment_update_data = comment_update_in.model_dump(exclude_unset=True)
        comment_updated = comments_collection.find_one_and_update(
            {"_id": ObjectId(comment_id)}, {"$set": comment_update_data}, return_document=True
        )

        return Comment_edit_serializer(comment_updated)
    
    @staticmethod
    def delete_comment(comment_id):
       com = comments_collection.find_one_and_delete({"_id": ObjectId(comment_id)})
       return com
    

    @staticmethod
    def get_comments_by_movie_id(movie_id: str):
        comments = comments_collection.find({"movie_id": movie_id})  
        return [comment_serializer(comments)]
   
    @staticmethod
    def get_comment_by_parent_id(parent_id: str):
        comment = comments_collection.find({"parent_id": parent_id})
        if comment:
            return comment_serializer(comment)
        return None
   
    @staticmethod
    def delete_comments_by_movie_id(movie_id: str):
        comments_collection.delete_many({"movie_id": movie_id})
        return None
    
    
rate_crud = RatingCRUDService    
comments_crud = COMMENTService
crud_service = CRUDService()
user_crud_service = UserCRUDService()