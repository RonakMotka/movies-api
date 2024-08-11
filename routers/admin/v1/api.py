
from datetime import datetime
from fastapi import APIRouter, Header, Response
from fastapi import HTTPException, status, Depends, Path, Query
from sqlalchemy.orm import Session
from typing import List

from routers.admin.v1 import schemas
from dependencies import get_db
from routers.admin.v1.crud import comments, movies, operations, ratings, roles, users

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserLoginResponse,
    tags=["Authentication"],
)
def sign_in(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = users.sign_in(db, user)
    return db_user


# Users

@router.post(
    "/sign-up",
    response_model=schemas.UserLoginResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def sign_up(
    user: schemas.UserSignUp,
    db: Session = Depends(get_db)
):
    data = users.sign_up(db, user=user)
    return data

@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    tags=["Users"]
)
def change_password(
    user: schemas.ChangePassword,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    users.change_password(db, user=user, token=token)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
    tags=["Users"],
)
def get_profile(token: str = Header(None), db: Session = Depends(get_db)):
    data = users.get_profile(db, token=token)
    return data


@router.put(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
    tags=["Users"],
)
def update_profile(
    user: schemas.UserUpdate,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    data = users.update_profile(db, token=token, user=user)
    return data



@router.get(
    "/users",
    response_model=schemas.AdminUserList,
    tags=["Admin - Users"]
)
def get_users(
    token: str = Header(None),
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=10),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation="List Users")
    data = users.get_users(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    tags=["Admin - Users"]
)
def add_user(
    user: schemas.UserAdd,
    token: str = Header(None),
    db: Session = Depends(get_db)
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, db_user.id, "Add User")
    user_id = users.add_user(db, user=user)
    return user_id


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Admin - Users"]
)
def get_my_profile(
    token: str = Header(None),
    user_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db)
):
    users.verify_token(db, token=token)
    db_user = users.get_user_profile(db, user_id=user_id)
    return db_user


@router.put(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Admin - Users"]
)
def update_profile(
    user: schemas.UserUpdate,
    token: str = Header(None),
    user_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    users.verify_token(db, token=token)
    db_user = users.update_user_profile(db, user=user, user_id=user_id)
    return db_user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=["Admin - Users"]
)
def delete_user(
    token: str = Header(None),
    user_id: str = Path(..., title="User ID", min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    users.verify_token(db, token=token)
    users.delete_user(db, user_id=user_id)
    return Response(status_code=status.HTTP_200_OK)

# End Users


# Operations
@router.get("/operations/verify", status_code=status.HTTP_200_OK, tags=["Operations"])
def check_user_operation(
    token: str = Header(None),
    operation: str = Query("all", min_length=3, max_length=50),
    db: Session = Depends(get_db),
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation=operation)
    return


@router.get("/operations/all", tags=["Operations"])
def get_all_operations(token: str = Header(None), db: Session = Depends(get_db)):
    users.verify_token(db, token=token)
    data = operations.get_all_operations(db)
    return data


# End Operations


# Roles
@router.get("/roles", response_model=schemas.RoleList, tags=["Roles"])
def get_roles(
    token: str = Header(None),
    start: int = 0,
    limit: int = 10,
    sort_by: str = Query("all", min_length=3, max_length=50),
    order: str = Query("all", min_length=3, max_length=4),
    search: str = Query("all", min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation="List Roles")
    data = roles.get_roles(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.get("/roles/all", response_model=List[schemas.Role], tags=["Roles"])
def get_all_roles(token: str = Header(None), db: Session = Depends(get_db)):
    users.verify_token(db, token=token)
    data = roles.get_all_roles(db)
    return data


@router.post("/roles", status_code=status.HTTP_201_CREATED, tags=["Roles"])
def add_role(
    role: schemas.RoleAdd, token: str = Header(None), db: Session = Depends(get_db)
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation="Add Role")
    role = roles.add_role(db, role=role)
    return


@router.get("/roles/{role_id}", response_model=schemas.RoleDetails, tags=["Roles"])
def get_role(
    role_id: str = Path(..., title="Role ID", min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation="Update Role")
    role = roles.get_role_details(db, role_id=role_id)
    return role


@router.put("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def update_role(
    role: schemas.RoleAdd,
    token: str = Header(None),
    role_id: str = Path(..., title="Role ID", min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation="Update Role")
    role = roles.update_role(db, role_id=role_id, role=role)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"]
)
def delete_role(
    token: str = Header(None),
    role_id: str = Path(..., title="Role ID", min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_user = users.verify_token(db, token=token)
    operations.verify_user_operation(db, user_id=db_user.id, operation="Delete Role")
    roles.delete_role(db, role_id=role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# End Roles


@router.post(
    "/movies",
    tags=["Movies"]
)
def add_movie(
    user_id: str = Query(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "add movies")
    data = movies.add_movie(db=db, user_id=user_id)
    return data


@router.get(
    "/movies/comments",
    response_model=schemas.CommentList,
    tags=["Movies"]
)
def get_comment_list(
    start: int = 0,
    limit: int = 10,
    search: str = Query("all", min_length=3, max_length=30),
    sort_by: str = Query("all", min_length=3, max_length=30),
    order: str = Query("all", min_length=3, max_length=4),
    movie_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db)
):
    data = comments.get_comment_list(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order,
        movie_id=movie_id
    )
    return data


@router.post(
    "/movies/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Comment,
    tags=["Movies"]
)
def add_comment(
    comment: schemas.CommentAdd,
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "add comments")
    data = comments.add_comment(db, comment, db_user.id)
    return data


@router.get(
    "/movies/{movie_id}/comments/all",
    response_model=schemas.MovieComment,
    tags=["Movies"]
)
def get_all_comments(
    db: Session = Depends(get_db),
    movie_id: str = Path(..., min_length=36, max_length=36),
):
    data = comments.get_all_comments(db=db, movie_id=movie_id)
    return data


@router.get(
    "/movies/{movie_id}/comments/{comment_id}",
    response_model=schemas.Comment,
    tags=["Movies"]
)
def get_comment(
    movie_id: str = Path(..., min_length=36, max_length=36),
    comment_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db)
):
    data = comments.get_comment(db=db, movie_id=movie_id, comment_id=comment_id)
    return data


@router.put(
    "/movies/{movie_id}/comments/{comment_id}",
    response_model=schemas.Comment,
    tags=["Movies"]
)
def update_comment(
    comment: schemas.CommentUpdate,
    movie_id: str = Path(..., min_length=36, max_length=36),
    comment_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "update comments")
    data = comments.update_comment(db=db, movie_id=movie_id, comment_id=comment_id, comment=comment)
    return data


@router.delete(
    "/movies/{movie_id}/comments/{comment_id}",
    response_model=schemas.Comment,
    tags=["Movies"]
)
def delete_comment(
    movie_id: str = Path(..., min_length=36, max_length=36),
    comment_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "delete comments")
    comments.delete_comment(db=db, movie_id=movie_id, comment_id=comment_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/movies/ratings",
    response_model=schemas.RatingList,
    tags=["Movies"]
)
def get_rating_list(
    start: int = 0,
    limit: int = 10,
    search: str = Query("all", min_length=3, max_length=40),
    sort_by: str = Query("all", min_length=3, max_length=40),
    order: str = Query("all", min_length=3, max_length=4),
    movie_id: str = Query("all", min_length=3, max_length=36),
    db: Session = Depends(get_db)
):
    data = ratings.get_rating_list(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order,
        movie_id=movie_id
    )
    return data


@router.post(
    "/movies/ratings",
    response_model=schemas.Rating,
    status_code=status.HTTP_201_CREATED,
    tags=["Movies"]
)
def add_rating(
    rating: schemas.RatingAdd,
    token: str = Header(None),
    db: Session = Depends(get_db)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "add ratings")
    data = ratings.add_rating(db, db_user.id, rating)
    return data


@router.get(
    "/movies/{movie_id}/ratings/all",
    response_model=schemas.MovieRatings,
    tags=["Movies"]
)
def get_all_ratings(
    movie_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db)
):
    data = ratings.get_all_ratings(db, movie_id)
    return data


@router.get(
    "/movies/{movie_id}/ratings/{rating_id}",
    response_model=schemas.Rating,
    tags=["Movies"]
)
def get_rating(
    movie_id: str = Path(..., min_length=36, max_length=36),
    rating_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db)
):
    data = ratings.get_rating(db, movie_id, rating_id)
    return data


@router.put(
    "/movies/{movie_id}/ratings/{rating_id}",
    response_model=schemas.Rating,
    tags=["Movies"]
)
def update_rating(
    rating: schemas.RatingUpdate,
    movie_id: str = Path(..., min_length=36, max_length=36),
    rating_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "update ratings")
    data = ratings.update_rating(db=db, movie_id=movie_id, rating_id=rating_id, rating=rating)
    return data


@router.delete(
    "/movies/{movie_id}/ratings/{rating_id}",
    response_model=schemas.Rating,
    tags=["Movies"]
)
def delete_rating(
    movie_id: str = Path(..., min_length=36, max_length=36),
    rating_id: str = Path(..., min_length=36, max_length=36),
    db: Session = Depends(get_db),
    token: str = Header(None)
):
    db_user = users.verify_token(db, token)
    operations.verify_user_operation(db, db_user.id, "delete ratings")
    ratings.delete_rating(db=db, movie_id=movie_id, rating_id=rating_id)
    return Response(status_code=status.HTTP_200_OK)
