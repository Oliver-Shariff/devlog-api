from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from app.models import User
from app.security import get_password_hash

def get_all_users(db: Session):
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()

# get a user based on email
# Select * from users where (email = x)

def get_user(email, db:Session):
    return db.get(User, email)

# add a user
# Insert INTO users (col) (values)
def add_user(email, username, password, created_on, db: Session):
    hashed = get_password_hash(password)
    new_user = User(email = email, username = username, hashed_password = hashed, created_on = created_on)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return(new_user)
    except IntegrityError:
        db.rollback()
        raise

# update user
# Update user set col = val ... Where id = x
def change_password(email, password, db:Session):
    hashed = get_password_hash(password)
    stmnt = update(User).where(User.email == email).values(hashed_password = hashed)
    result = db.execute(stmnt)
    if result.rowcount == 0:
        db.rollback()
        return False
    db.commit()
    return True

# delete a user based on id
# Delete from user where (id = x)
def delete_user(email, db:Session):
    user = db.get(User, email)

    if not user:
        return None
    db.delete(user)
    db.commit()
    return user