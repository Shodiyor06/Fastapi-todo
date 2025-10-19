from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Date

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=True)
    birth_date = Column(Date, nullable=True)
    phone = Column(String(length=20), nullable=True)
    email = Column(String(length=120), nullable=True, unique=True)

    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username})'
    

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), nullable=False, index=True)
    description = Column(Text, default='')
    status = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(length=50), nullable=True)
    priority = Column(Integer, default=3, nullable=False)
    def __repr__(self) -> str:
        return f'Task(id={self.id}, name={self.name})'
    