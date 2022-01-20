import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, DateTime, Integer, String, UnicodeText
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))
SQLITE_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sqlite_python.db')

engine = create_engine(SQLITE_DATABASE_URI)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(String(9), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    def __repr__(self):
        return f'<User {self.id} {self.tg_id} {self.role_id}>'

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(UnicodeText)
    approved = Column(Boolean)
    posted_datetime = Column(DateTime(timezone=True), server_default=func.now())
    approver_id = Column(Integer, ForeignKey('users.id'), default=None)

    def __repr__(self):
        return f'<Message {self.id} {self.sender_id} {self.text} {self.approved} {self.approver_id}>'

class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    address = Column(UnicodeText(200))
    title_name = Column(UnicodeText(100))
    favicon_path = Column(String)
    admin_id = Column(Integer, ForeignKey('users.id'))
    channel_id = Column(Integer)

    def __repr__(self):
        return f'<House {self.id} {self.address} {self.title_name} {self.channel_id}>'

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __repr__(self):
        return f'<Roles {self.id} {self.name}>'


class Thematic(Base):
    __tablename__ = 'thematics'
    id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    name = Column(String(100))
    moderation = Column(Boolean)

    def __repr__(self):
        return f'<User {self.id} {self.tg_id} {self.role_id}>'


class ThematicMessage(Base):
    __tablename__ = 'thematics_messages'
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    thematic_id = Column(Integer, ForeignKey('thematics.id'))


class RoleHouse(Base):
    __tablename__ = 'roles_houses'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    house_id = Column(Integer, ForeignKey('houses.id'))


class HouseUser(Base):
    __tablename__ = 'houses_users'
    id = Column(Integer, primary_key=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

Base.metadata.create_all(engine)

