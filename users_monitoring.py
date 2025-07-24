from mastodon import Mastodon, StreamListener
from sqlalchemy.exc import IntegrityError
from config.database import SessionLocal, Post, MonitoredUser, Hashtag
from multiprocessing import Process
import os
import time
from dotenv import load_dotenv

class UserListener(StreamListener):
    def __init__(self, monitored_users_username):
        self.monitored_users_username = monitored_users_username

    def on_update(self, status):
        acct = status['account']['acct']
        print(f"Stream received toot from @{acct}")
        if acct in self.monitored_users_username:
            print(f"New post from @{acct}: {status['url']}")
            fetch_and_store_post(status)

def fetch_and_store_post(post_data):
    session = SessionLocal()

    acct = post_data['account']['acct']

    if "@" not in acct:
        domain = post_data['account']['url'].split('/')[2]
        acct_withoutdomain = acct
        acct = f"{acct}@{domain}"

    print(f"Saving toot from @{acct}")


    user = session.query(MonitoredUser).filter_by(acct=acct).first()

    if not user:
        print(f"User @{acct} not found in Data Base")
        session.close()
        return

    existing = session.query(Post).filter_by(url=post_data['url']).first()
    if existing:
        print(f"Post already saved: {post_data['url']}")
        session.close()
        return


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

    p = Post(
        user=user.id,
        content=post_data['content'],
        created_at=post_data['created_at'],
        url=post_data['url'],
        hashtags=hashtag_objs
    )

    try:
        session.add(p)
        session.commit()
        print(f"Saved post from @{acct}: {post_data['url']}")
    except IntegrityError:
        print(f"Error saving post from @{acct}")
        session.rollback()
    finally:
        session.close()

def get_monitored_user_ids(limit=10):
    session = SessionLocal()
    users = session.query(MonitoredUser.acct).limit(limit).all()
    session.close()
    users_list = ['likethecoins@infosec.exchange', 'vulnerability_lookup@social.circl.lu', 'NickAEsp@mastodon.social', 'Ransomlook@social.circl.lu', 'RedPacketSecurity@mastodon.social', 'certvde@infosec.exchange', 'urldna@infosec.exchange', 'fr@pubeurope.com', 'us@pubeurope.com', 'uk@pubeurope.com', 'CCINL', '0x58', 'Hackread', 'CuratedHackerNews', 'RedPacketSecurity']
    return users_list

    # return [u[0] for u in users]

def stream_for_user(username, max_retries=2):
    retries = 0
    while retries < max_retries:
        try:
            mastodon = Mastodon(
                client_id=os.getenv("MASTO_CLIENT_ID", os.getenv("MASTO_CLIENT_ID")),
                client_secret=os.getenv("MASTO_CLIENT_SECRET", os.getenv("MASTO_CLIENT_SECRET")),
                access_token=os.getenv("MASTO_ACCESS_TOKEN", os.getenv("MASTO_ACCESS_TOKEN")),
                api_base_url=os.getenv("MASTO_API_BASE_URL", 'https://infosec.exchange'),
            )
            listener = UserListener(username)
            mastodon.stream_user(listener)
            #print(f"Listening user {username}")
        except Exception as e:
            retries += 1
            wait_time = 2 * retries
            print(f"Error for {username} (try {retries}/{max_retries}): {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    print(f"Finishing stream for {username} due to many errors.")

if __name__ == "__main__":
    load_dotenv()
    usernames = get_monitored_user_ids()
    print(f"Monitoring users: {usernames}")
    processes = []

    for acct in usernames:
        p = Process(target=stream_for_user, args=(acct,), daemon=True)
        p.start()
        print(f"Started process for {acct}")
        processes.append(p)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Finishing...")
        for p in processes:
            p.terminate()
            p.join()