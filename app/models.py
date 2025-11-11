from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key = True, nullable = False)
    username = Column(String, nullable = False)
    hashed_password = Column(String, nullable = False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key = True, nullable = False, autoincrement= True)
    user_email = Column(ForeignKey("users.email"), nullable=False)
    title = Column(String, nullable = True)
    content = Column(String, nullable = False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    last_edit = Column(
    TIMESTAMP(timezone=True),
    server_default=text('now()'),
    onupdate=text('now()')
    )
    tags = relationship("Tag", secondary="tag_entry_join", back_populates="entries")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_email = Column(ForeignKey("users.email", ondelete="CASCADE"), nullable=False)

    entries = relationship("Entry", secondary="tag_entry_join", back_populates="tags")

    __table_args__ = (
        UniqueConstraint("user_email", "name", name="uq_tag_user_name"),
    )

class TagEntryJoin(Base):
    __tablename__ = "tag_entry_join"

    tag_id = Column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key = True)
    entry_id = Column(ForeignKey("entries.id", ondelete="CASCADE"), primary_key = True)
    