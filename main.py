import streamlit as st
import pickle
import requests
import io
import gdown

import pickle
import gdown

# Google Drive file IDs
movies_id = "11XkOdT4KVXoMT4MffyZhQfdW4gneBqdm"
similarity_id = "1cBGkyZCZ7ftavRCZ5SHj-3zFLba-6ojb"

# Direct download URLs
movies_url = f"https://drive.google.com/uc?id={movies_id}"
similarity_url = f"https://drive.google.com/uc?id={similarity_id}"

# Download files locally
movies_file = gdown.download(movies_url, "movies.pkl", quiet=False)
similarity_file = gdown.download(similarity_url, "similarity.pkl", quiet=False)

# Load pickles
df = pickle.load(open(movies_file, "rb"))
similarity = pickle.load(open(similarity_file, "rb"))


API_KEY = "93386f77dbca2edf367b5dce0ace14c1"

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    index = df[df['title_y'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = df.iloc[i[0]].movie_id  # needs to exist in your df
        recommended_movies.append(df.iloc[i[0]].title_y)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters
# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.markdown("""
This is a **Content-Based Movie Recommendation System**.  
Select a movie from the dropdown, and the app will suggest 5 similar movies 
based on genres, cast, keywords, and overview.
""")

selected_movie = st.selectbox("Select a movie:", df['title_y'].values)

if st.button("Recommend"):
    st.subheader("Top 5 Recommended Movies")
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

st.sidebar.markdown("### About this app")
st.sidebar.write("Built with the TMDB 5000 Movies dataset and Streamlit.")
st.sidebar.write("Author: Hrishi Kale")