import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = "e8d238486a79fe13715b8ccf61aebb5e"  # 👈 Replace this with your key


def fetch_poster(movie_id):
    """Fetches a movie poster from TMDb, with debugging prints."""
    fallback_url = "https://via.placeholder.com/500x750?text=Poster+Not+Available"

    if pd.isna(movie_id):
        print("Error: Received a missing movie_id.")
        return fallback_url

    try:
        url = f'https://api.themoviedb.org/3/movie/{int(movie_id)}?api_key={API_KEY}&language=en-US'
        print(f"Fetching URL: {url}")  # Debug: See the URL being called

        response = requests.get(url, timeout=10)

        # Debug: Print the status code to check for errors like 401 (invalid key) or 404 (not found)
        print(f"Movie ID {movie_id}: Status Code {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                print(f"Success: Found poster for movie ID {movie_id}")
                return full_path
            else:
                print(f"Warning: No poster_path found for movie ID {movie_id}.")
                return fallback_url
        else:
            # If the status code is not 200, return the fallback
            return fallback_url

    except Exception as e:
        print(f"An error occurred fetching poster for movie ID {movie_id}: {e}")
        return fallback_url


import time  # 👈 Add this at the top with your imports

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

        time.sleep(0.5)  # ⏳ This line slows down requests to avoid API issues

    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values )

if st.button('Recommend') :
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0], width=150)

    with col2:
        st.text(names[1])
        st.image(posters[1], width=150)

    with col3:
        st.text(names[2])
        st.image(posters[2], width=150)

    with col4:
        st.text(names[3])
        st.image(posters[3], width=150)

    with col5:
        st.text(names[4])
        st.image(posters[4], width=150)





