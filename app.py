import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
     url = "https://api.themoviedb.org/3/movie/{}?api_key=dacda2fa8da729aef00ca1bcae9cc061".format(movie_id)
     data = requests.get(url).json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
     return full_path

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values


st.set_page_config(page_title="Movie Recommender", page_icon="🎬")


st.title("🎥 Movie Recommender System")
st.subheader("Discover new movies based on your preferences!")


select_value = st.selectbox("Select a movie from the dropdown", movies_list)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster


if st.button("Show Recommendations"):
    recommended_movies, recommended_posters = recommend(select_value)

   
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.text(recommended_movies[i])
            st.image(recommended_posters[i], use_column_width=True)

