import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_path = fetch_poster(movie_id)
        recommended_movies.append({'title': movies.iloc[i[0]].title, 'poster_path': poster_path})
    return recommended_movies

# Set background color to white
st.markdown(
    """
    <style>
    body {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header('FlickFeasta')

# Load pickled files
movies = pd.read_pickle('model/movie_list.pkl')
similarity = pd.read_pickle('model/similarity.pkl')

# Add more vertical spacing
st.write("\n\n\n\n\n")  

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Please enter a movie name",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie, movies, similarity)
    cols = st.columns(5)
    for i, movie in enumerate(recommended_movies):
        with cols[i]:
            st.image(movie['poster_path'], width=100)
            st.markdown(f"**{movie['title']}**")
        st.write("")  # Add some space between columns
