from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key = True, nullable = False)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key = True, nullable = False)
    user_email = Column(ForeignKey("users.email"))
    title = Column(String, nullable = True)
    content = Column(String, nullable = False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    last_edit = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    attachment = Column(String, nullable = True) # will likely alter this from string later
    
class Tag(Base):
    __tablename__ = "tags"

    name = Column(String, primary_key = True)

class Tag_Entry(Base):
    __tablename__ = "tag_entry_join"

    tag_name = Column(ForeignKey("tags.name"), primary_key = True)
    entry_id = Column(ForeignKey("entries.id"), primary_key = True)
    