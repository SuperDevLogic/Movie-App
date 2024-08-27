def movie_serializer(movie) -> dict:
    """Converts a MongoDB movie object to a Python dictionary"""
    return {
        "id": str(movie.get("_id")),
        "title": movie.get("title"),
        "description": movie.get("description"),
        "release_year": movie.get("release_year"),
        "producer": movie.get("producer"),
        "user_id": movie.get("user_id"),
    }
 

# def movies_serializer(movies) -> list:
#     """Converts a MongoDB cursor object to a list of Python dictionaries"""
#     return [movies_serializer(movies) ]



def user_serializer(user) -> dict:
    """Converts a MongoDB user object to a Python dictionary"""
    return {
        "id": str(user.get("_id")),
        "name": user.get("name"),
        "username": user.get("username"),
        "fullname": user.get("fullname"),
    }




def user_serializer_password(user) -> dict:
    """Converts a MongoDB user object to a Python dictionary"""
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "hashed_password": user.get("hashed_password")
    }
def rating_serializer(rating) -> dict:
    """Converts a MongoDB rating object to a Python dictionary"""
    return {
        "id": str(rating.get("_id")),
        "user_id": str(rating.get("user_id")),
        "movie_id": str(rating.get("movie_id")),
        "rate": rating.get("rate"),
        "rating_comment": rating.get("rating_comment"),
        "user_id": str(rating.get("user_id")),
    }

def ratings_serializer(ratings) -> list:
    """Converts a MongoDB rating object to a list of Python dictionaries"""
    return [rating_serializer(rating) for rating in ratings]


def comments_serializer(comments) ->list:
    """Converts a MongoDB rating object to a list of Python dictionaries"""
    return [comment_serializer(comment) for comment in comments]




def comment_serializer(comment) -> dict:
    """Converts a MongoDB comment object to a Python dictionary"""
    return {
        "id": str(comment.get("_id")),
        "movie_id": comment.get("movie_id"),
        "user_id": comment.get("user_id"),
        "created_at": comment.get("created_at"),
        "content" : comment.get("content"),
        "comments": dict(comment.get("comments")),
    }

def Subcomment_serializer(comment) -> dict:
    """Converts a MongoDB comment object to a Python dictionary"""
    return {
        "id": str(comment.get("_id")),
        "user_id": comment.get("user_id"),
        "movie_id": comment.get("movie_id"),
        "parent_id": comment.get("parent_id"),
        "created_at": comment.get("created_at"),
        "content": comment.get("content"),
        "comments": comment.get("comments"),
    }
 
 
 

def Comment_edit_serializer(comment) -> dict:
    """Converts a MongoDB comment object to a Python dictionary"""
    return {
        "created_at": comment.get("created_at"),
        "content": comment.get("content"),
    }
 

 