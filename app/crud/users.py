from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.models import User

def get_all_users(db: Session):
    stmt = select(User)
    result = db.execute(stmt)
    return result.scalars().all()

# get a user based on email
# Select * from users where (email = x)
def get_user(email, db:Session):
    stmnt = select(User).where(User.email == email)
    result = db.scalars(stmnt).all()
    return(result)

# add a user
# Insert INTO users (col) (values)
def add_user(email, username, password, created_on, db: Session):
    new_user = User(email = email, username = username, password = password, created_on = created_on)
    db.add(new_user)
    db.commit()

# update user
# Update user set col = val ... Where id = x
def change_password(email, password, db:Session):
    stmnt = update(User).where(email == email).values(password = password)
    db.execute(stmnt)

# delete a user based on id
# Delete from user where (id = x)
def delete_user(email, db:Session):
    stmnt = delete(User).where(email == email)
    db.execute(stmnt)