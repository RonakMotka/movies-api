from sqlalchemy.orm import Session

from libs.utils import generate_id
from models import MovieModel




def get_movie_by_id(db: Session, movie_id: str):
    return db.query(MovieModel).filter(MovieModel.id == movie_id, MovieModel.is_deleted == False).first()




def add_movie(db: Session, user_id: str, ):
    db_movie = MovieModel(
        id=generate_id(),
        title="test",
        description="test is description",
        path="/movies/id.mkv",
        year=2022,
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
