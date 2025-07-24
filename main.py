from mastodon import Mastodon, StreamListener
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from multiprocessing import Process
from config.database import SessionLocal, Post, Hashtag
from datetime import datetime
import os
import time

mastodon = Mastodon(
    client_id='N0BoW5pj0IWVBeMAk5-yOTGbH4HPXr3IEeIyFYZqU44',
    client_secret='yHQHuJAu8CxQfQC7Jzbd4J4NGaou9XNYnZoXd2W4b6s',
    access_token='IzVEwp8SUpvsKEaoYcYKfj_baJ1clcAEdzlZZQ2jMjM',
    api_base_url='https://infosec.exchange'
)


def fetch_and_store_post(post_data, fixed_hashtag=None):
    session = SessionLocal()
    tags_in_post = post_data.get('tags', [])
    hashtag_objs = []

    for t in tags_in_post:
        tag_name = t['name'].lower()
        hashtag = session.query(Hashtag).filter_by(name=tag_name).first()
        if not hashtag:
            hashtag = Hashtag(name=tag_name)
            session.add(hashtag)
            session.commit()
        hashtag_objs.append(hashtag)

    if fixed_hashtag:
        tag_name = fixed_hashtag.lower()
        hashtag = session.query(Hashtag).filter_by(name=tag_name).first()
        if not hashtag:
            hashtag = Hashtag(name=tag_name)
            session.add(hashtag)
            session.commit()
        if hashtag not in hashtag_objs:
            hashtag_objs.append(hashtag)

    existing = session.query(Post).filter_by(url=post_data['url']).first()
    if existing:
        for h in hashtag_objs:
            if h not in existing.hashtags:
                existing.hashtags.append(h)
        session.commit()
        session.close()
        return

    p = Post(
        user=post_data['account']['acct'],
        content=post_data['content'],
        created_at=post_data['created_at'],
        url=post_data['url'],
        source='mastodon',
        hashtags=hashtag_objs
    )
    try:
        session.add(p)
        session.commit()
    except IntegrityError:
        session.rollback()
    session.close()

class HashtagListener(StreamListener):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag

    def on_update(self, status):
        print(f"New post for  #{self.tag}: {status['url']}")
        fetch_and_store_post(status, fixed_hashtag=self.tag)

def stream_for_hashtag(tag):
    listener = HashtagListener(tag)
    print(f"Listening #{tag}")
    mastodon.stream_hashtag(tag, listener)

def get_all_hashtags():
    session = SessionLocal()
    tags = session.query(Hashtag).all()
    session.close()
    return [t.name for t in tags]


if __name__ == "__main__":
    hashtags = get_all_hashtags()
    processes = []
    for tag in hashtags:
        p = Process(target=stream_for_hashtag, args=(tag,))
        p.start()
        processes.append(p)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Finalizando procesos...")
        for p in processes:
            p.terminate()
            p.join()