import streamlit as st
import pickle
import pandas as pd
import requests

# loading the files
movie_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# fetch poster from TMDb
def fetch_poster(movie_id):
    api_key = "c6438f3f81b2f980cba2089a24e3fffb"  # v3 API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path")
    return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else None

# recommender function
def recommend(movie):
    movie_index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    posters = []
    for i in movies_list:
        movie_id = movie_list.iloc[i[0]].id
        recommended_movies.append(movie_list.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters


# ---------------- UI ---------------- #
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommender System 🍿</h1>
    <p style='text-align: center; font-size:18px;'>Discover movies similar to your favorites</p>
    """,
    unsafe_allow_html=True
)

mov_list = movie_list['title'].values

selected_movie_name = st.selectbox(
    "Select a movie you like 👇",
    mov_list,
    index=0,
    placeholder="Type or choose a movie..."
)

if st.button("✨ Recommend Movies"):
    recommended_movie_names, posters = recommend(selected_movie_name)
    st.subheader("Here are some similar movies you might enjoy 👇")

    cols = st.columns(5, gap="medium")
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], width=250)
            st.markdown(
                f"<p style='text-align:center; font-size:16px; font-weight:bold;'>{recommended_movie_names[idx]}</p>",
                unsafe_allow_html=True
            )
