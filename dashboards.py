import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from config.database import Post, Hashtag, post_hashtag

engine = create_engine('sqlite:///./mastodon.db')
Session = sessionmaker(bind=engine)
session = Session()

st.set_page_config(page_title="Cyber Threat Monitor", layout="wide")
st.title("🛡️ Cyber Threat Intelligence Dashboard")


st.subheader("📌 Recent Posts ")
posts = session.query(Post).order_by(Post.created_at.desc()).limit(50).all()
post_data = [
    {
        "Datetime": p.created_at.strftime("%Y-%m-%d %H:%M"),
        "User": p.user,
        "Content": p.content,
        "URL": p.url,
        "Source": p.source,
        "Hashtags": ", ".join(h.name for h in p.hashtags)
    }
    for p in posts
]
post_df = pd.DataFrame(post_data)
st.dataframe(post_df, use_container_width=True)


st.subheader("🏷️ Most frequent Hashtags")
hashtag_counts = (
    session.query(Hashtag.name, func.count(post_hashtag.c.post_id))
    .join(post_hashtag, Hashtag.id == post_hashtag.c.hashtag_id)
    .group_by(Hashtag.name)
    .order_by(func.count(post_hashtag.c.post_id).desc())
    .limit(10)
    .all()
)
hashtag_df = pd.DataFrame(hashtag_counts, columns=["Hashtag", "Amount"])
st.bar_chart(hashtag_df.set_index("Hashtag"))

st.subheader("👤 Most active users")
user_counts = (
    session.query(Post.user, func.count(Post.id))
    .group_by(Post.user)
    .order_by(func.count(Post.id).desc())
    .limit(10)
    .all()
)
user_df = pd.DataFrame(user_counts, columns=["User", "Amount"])
st.bar_chart(user_df.set_index("User"))


st.subheader("📈 Timeline")
time_series = (
    session.query(func.strftime('%Y-%m-%d', Post.created_at), func.count(Post.id))
    .group_by(func.strftime('%Y-%m-%d', Post.created_at))
    .order_by(func.strftime('%Y-%m-%d', Post.created_at))
    .all()
)
time_df = pd.DataFrame(time_series, columns=["Datetime", "Posts"])
time_df["Datetime"] = pd.to_datetime(time_df["Datetime"])
st.line_chart(time_df.set_index("Datetime"))
