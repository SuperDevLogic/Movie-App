import os
import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from fastapi import status
from motor.motor_asyncio import AsyncIOMotorClient
from .main import app
# from app.database import database




load_dotenv()

MongoDB_details = os.getenv('MongoDB_details',"mongodb://localhost:27017" )


@pytest.fixture(autouse=True)
def initialize_db():
    test_client = AsyncIOMotorClient(MongoDB_details)
    test_database = test_client.MOVIE_DB
    global test_collection
    test_collection = test_database.get_collection("test")

    yield

    test_client.drop_database("MOVIE_DB")

# @pytest.mark.parametrize


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


client = TestClient(app)

# def test_signup_users():
#     response = client.post("/signup", json={"username": "username", "password": "password"})
#     assert response.status_code == status.HTTP_200_OK
    # assert response.json()['username'] == "John"
    # assert "id" in response.json()

# @pytest.mark.parametrize("username, password", [("newuser2", "123")])
def test_login():
    # First, sign up the user
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    assert response.status_code == status.HTTP_200_OK
    # Then login the user
    response = client.post(
        "/login",
        data = {"username": 'username', "password": 'password'}
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"


def test_create_movie():
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    assert response.status_code == status.HTTP_200_OK
    # Then login the user
    response = client.post(
        "/login",
        data = {"username": 'username', "password": 'password'}
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    token = response.json()["access_token"]

    response = client.post("/MoviesCreate", headers={"Authorization":f"Bearer{token}"}, json={"title":"lambic ", "description":"some description","release_year":2020,"producer":"some producer","user_id":"17177171"})
    assert response.status_code == status.HTTP_201_CREATED
    # assert response.json()["title"] == "lambic"

def test_get_movies():                    

       #First Sign up a user
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/login", data={"username": 'username', "password": 'password'})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Then, create a movie
    movie_data = {"title": "Test Movie", "description":"Test Description","release_year":2020,"producer":"matt","user_id":"29929"}
    response = client.post("/MoviesCreate", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    response = client.get("/Movies")
    assert response.status_code == status.HTTP_200_OK


def test_create_movies():
       #First Sign up a user
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/login", data={"username": 'username', "password": 'password'})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Then, create a movie
    movie_data = {"title": "Test Movie", "description":"Test Description","release_year":2020,"producer":"matt","user_id":"29929"}
    response = client.post("/MoviesCreate", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # assert data.get("description") == "Test Description"
    # assert data["title"] == "Test Movie"
    # assert data.get("id") == 1


# def test_update_movies():
#     response = client.put("/movies",json={"title":"jdj ", "description":"some description","release_year":2020,"producer":"some producer","user_id":"17177171"})
#     assert response.status_code == status.HTTP_404_NOT_FOUND
def test_update_movie():
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    
    response = client.post("/login", data={"username": "username", "password": "password"})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    movie_data = {"title": "Test Movie", "description":"Test Description","release_year":2020,"producer":"matt","user_id":"29929"}
    response = client.post("/MoviesCreate", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()


    movie_data = {"title": "Updated Test Movie", "description": "Updated Test Description","release_year":2020,"producer":"matt","id":"29929"}
    response = client.put("/MovieEdit/1", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("title") == "Updated Test Movie"
    assert response.json().get("description") == "Updated Test Description"
    assert response.json() == {
       "id": response.json()['id'],
        "title": "Updated Test Movie",
        "description": "Updated Test Description",
        "release_date": f"{response.json()['release_date']}",
        "updated_at": f"{response.json()['updated_at']}"
    }

def test_delete_movie():
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    
    #First Login an Authorized User
    response = client.post("/login", data={"username": "username", "password": "password"})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    movie_data = {"title": "Test Movie", "description":"Test Description","release_year":2020,"producer":"matt","user_id":"29929"}
    response = client.post("/MoviesCreate", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    response = client.delete("/MovieDelete/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get("/Movie", headers={"Authorization": f"Bearer{token}" })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Movie not found"

# def test_fetch_movies_not_found():
#     response = client.get("/movies")
#     assert response.status_code == status.HTTP_404_NOT_FOUND



def test_get_movie_ratings():
    # Login a user and rate by the user to get an average rating
    response = client.post(
        "/signup",
        json={"username": 'username', "password": 'password'}
    )
    assert response.status_code == status.HTTP_200_OK
    # Then login the user
    response = client.post(
        "/login",
        data = {"username": 'username', "password": 'password'}
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["access_token"] is not None
    token = data["token_type"] == "bearer"
    
    response = client.post(
        "/ratings/{movies_id}/",
        json={
            "movie_id" : "1",
            "user_id" : "d999",
            "rate_comments":"dndndnn",
            "rating": 7
        },
        headers={
            "Authorization": f"Bearer {token}",
            "content_type": "application/json"
        }
    )
    #Get t
    #Get the ratings of the movie previously created in the module
    response = client.get("/ratings")
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == "average_rating : 6.5"
    # assert response.json().get("detail") == "message" "No movies found"

  # Clean up the database after tests



# @pytest.mark.parametrize("username,full_name,password",[("testusername","testfull_name", "testpasword")])
# def test_signup(client, username,full_name,password):
#     response = client.post("/signup", json={"username": username,"full_name":full_name ,"password": password})
#     assert response.status_code == status.HTTP_200_OK
#     # assert response.json()["username"] == "username"


# @pytest.mark.parametrize("username, password", [("newuser2", "123")])
# def test_login(client, username, password):
#     # First, sign up the user
#     response = client.post(
#         "/signup",
#         json={"username": username, "password": password}
#     )
#     assert response.status_code == status.HTTP_200_OK

# @pytest.mark.parametrize()
# def test_get_movie():
#     response = client.get("/movie")
#     assert response.status_code == status.HTTP_200_OK




# # from fastapi import FastAPI, HTTPException,Depends
# # from fastapi.security import OAuth2PasswordRequestForm
# # from movie.crud import user_crud_service,crud_service,comments_crud,rate_crud

# # from movie.schemas import UserCreate,UserBase,MovieCreate,UserDB,Movie,UserRead,Comment,CommentEdit,RatingCreate,CommentResponse

# # from movie.auth import pwd_context, authenticate_user, create_access_token, get_current_user

# # app = FastAPI() 

# # @app.post("/signup")
# # def signup(user: UserCreate):
# #     db_user = user_crud_service.get_user_by_username(username=user.username)
# #     if db_user:
# #         raise HTTPException(status_code=400, detail="Username already registered")
# #     hashed_password = pwd_context.hash(user.password)
# #     return user_crud_service.create_user(user_data=user, hashed_password=hashed_password)

# # @app.post("/login")
# # def login(form_data: OAuth2PasswordRequestForm = Depends()):
# #     user = authenticate_user(form_data.username, form_data.password)
# #     if not user:
# #         raise HTTPException(
# #             status_code=401,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
# #     access_token = create_access_token(data={"sub": user.get('username')})
# #     return {"access_token": access_token, "token_type": "bearer", "user_id": user.get('id')}



# # @app.post("/MoviesCreate")
# # def create_movie(movie_in: MovieCreate,user:UserBase = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to create a movie"})
# #     movie = crud_service.create_movie(movie_in)
# #     if not movie:
# #         raise HTTPException(status_code=400, detail={"message": "Invalid input"})
# #     return {
# #         "message": "movie created successfully!", "data": movie}


# # @app.get("/Movies")
# # def get_all_movies():
# #     movies = crud_service.get_all_movies()
# #     if not movies:
# #         raise HTTPException(status_code=404, detail={"message": "No movies found"})
# #     return {"mesage":"successfull","data":movies}




# # @app.put("/MovieEdit")
# # def update_movie(movie_id: str, movie_update_in:Movie,user:UserRead = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to update a movie"})
# #     movie = crud_service.update_movie(movie_id, movie_update_in)
# #     if movie["user_id"] != user ["id"]:
# #         raise HTTPException(status_code=403, detail={"message": "You are not authorized to update this movie"})
# #     if not movie:
# #         raise HTTPException(status_code=404, detail={"message": "movie does not exists"})
# #     return {"message": "movie updated successfully", "data": movie}


# # @app.delete("/MovieDelete")
# # def delete_movie(movie_id: str,user:UserBase = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to delete a movie"})
# #     results = crud_service.delete_movie(movie_id)

# #     if not results:
# #         raise HTTPException(status_code=404, detail={"message": "movie does not exists"})
# #     return {"message": "movie deleted successfully"}


# # @app.get("/comment")
# # def get_comments() -> list:
# #     comments = comments_crud.get_all_comments()
# #     if not comments:
# #         raise HTTPException(status_code=404, detail={"message": "No comments found for this movie"})
# #     return [comments]

# # @app.post("/comment")
# # def create_comment(comment_in:Comment, user:UserBase = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to create a comment"})
# #     comment = comments_crud.create_comment(comment_in)
# #     if not comment:
# #         raise HTTPException(status_code=400, detail={"message": "Invalid input"})
# #     return {
# #         "message": "comment created successfully!", "data": comment}

# # @app.post("/subcomment")
# # def create_reply_comment(comment_in: CommentResponse, user: UserBase = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to create a comment"})
# #     comment = comments_crud.create_sub_comment(comment_in)
# #     if not comment:
# #         raise HTTPException(status_code=400, detail={"message": "Invalid input"})
# #     return {
# #         "message": "comment created successfully!", "data": comment}

# # @app.put("/comments")
# # def update_comment(comment_id: str, comment_update_in: CommentEdit,user: UserBase = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to update a comment"})
# #     comment = comments_crud.update_comment(comment_id, comment_update_in)
   
# #     if not comment:
# #         raise HTTPException(status_code=404, detail={"message": "comment does not exists"})
# #     return {"message": "comment updated successfully", "data": comment}

# # @app.delete("/comments")
# # def delete_comment(comment_id: str, user: UserRead = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to delete a comment"})
# #     # 
# #     results = comments_crud.delete_comment(comment_id)
    
# #     if  results:
# #      return {"message": "comment deleted successfully"}

# # @app.post("/ratings")
# # def create_rating(rating_in: RatingCreate, user: UserBase = Depends(get_current_user)):
# #     if not user:
# #         raise HTTPException(status_code=401, detail={"message": "Unauthorized to create a rating"})
# #     rating = rate_crud.create_rating(rating_in)
# #     if not rating:
# #         raise HTTPException(status_code=400, detail={"message": "Invalid input"})
# #     return {
# #         "message": "rating created successfully!", "data": rating}

# # @app.get("/ratings")
# # def get_ratings():
# #     ratings = rate_crud.get_all_ratings()
# #     if not ratings:
# #         raise HTTPException(status_code=404, detail={"message": "No ratings found for this movie"})
# #     return ratings