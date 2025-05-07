import streamlit as st
import json
from app import (
    get_genres,
    get_movies_by_genre,
    search_movie,
    get_movie_details,
    recommend_movies,
    recognize_speech
)

st.set_page_config(layout="wide", page_title="AI Movie Recommender")

# Custom CSS
st.markdown("""
    <style>
        .movie-row {
            display: flex;
            overflow-x: auto;
            padding-bottom: 10px;
        }
        .movie-card {
            flex: 0 0 auto;
            width: 200px;
            margin-right: 10px;
        }
        .movie-card img {
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 AI-Powered Movie Recommender")

tab1, tab2 = st.tabs(["🔍 Discover Movies", "🎞️ Short Films"])

with tab1:
    search_method = st.radio("Choose Input Method:", ["Text", "Speech"], horizontal=True)

    if search_method == "Text":
        movie_query = st.text_input("Enter a movie name:")
    else:
        st.info("Click the button and speak your movie...")
        if st.button("🎙️ Recognize Speech"):
            movie_query = recognize_speech()
            st.success(f"You said: {movie_query}")
        else:
            movie_query = ""

    if movie_query:
        movie = search_movie(movie_query)
        if movie:
            details = get_movie_details(movie['id'])
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=300)
            st.subheader(details.get("title", "No Title"))
            st.write("📖 Description:", details.get("overview", "No overview"))
            st.write("⭐ Rating:", details.get("vote_average", "N/A"))
            st.write("🎭 Cast:", ", ".join(details.get("cast", [])))
            st.write("🎬 Crew:", ", ".join(details.get("crew", [])))
            st.markdown("---")

            # Recommendations
            st.subheader("🎯 Recommended Movies (ML-based):")
            recommended = recommend_movies(movie_query)
            if recommended:
                st.markdown('<div class="movie-row">', unsafe_allow_html=True)
                for rec in recommended:
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="https://image.tmdb.org/t/p/w500{rec.get('poster_path', '')}">
                            <div style="text-align:center">{rec['title']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No recommendations found.")
        else:
            st.error("Movie not found.")

    # Genre-wise
    st.subheader("🍿 Popular Movies by Genre")
    genres = get_genres()
    for genre in genres:
        st.markdown(f"### {genre['name']}")
        movies = get_movies_by_genre(genre['id'])
        if movies:
            st.markdown('<div class="movie-row">', unsafe_allow_html=True)
            for movie in movies[:10]:
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="https://image.tmdb.org/t/p/w500{movie['poster_path']}">
                        <div style="text-align:center">{movie['title']}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.header("🎬 My Short Films")
    with open("short_films.json", "r") as f:
        short_films = json.load(f)

    for idx, film in enumerate(short_films, 1):
        st.subheader(f"{idx}. {film['title']}")
        st.image(film["poster"], width=300)
        st.video(film["video"])
