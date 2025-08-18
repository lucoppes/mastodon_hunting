from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///mastodon.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

post_hashtag = Table(
    'post_hashtag', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('hashtag_id', Integer, ForeignKey('hashtags.id'), primary_key=True)
)



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("monitored_users.id"), index=True)
    content = Column(Text)
    created_at = Column(DateTime, index=True)
    url = Column(String, unique=True)

    hashtags = relationship("Hashtag", secondary=post_hashtag, back_populates="posts")

    monitored_user = relationship("MonitoredUser", back_populates="posts")


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    posts = relationship('Post', secondary=post_hashtag, back_populates='hashtags')

    posts = relationship("Post", secondary=post_hashtag, back_populates="hashtags")



class MonitoredUser(Base):
    __tablename__ = 'monitored_users'

    id = Column(Integer, primary_key=True)
    acct = Column(String, unique=True, nullable=False)

    posts = relationship("Post", back_populates="monitored_user")


Base.metadata.create_all(bind=engine)