import requests
import json
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = "90227923bef532ff489659f76221e7f8"
BASE_URL = "https://api.themoviedb.org/3"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Say something!")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError:
            print("Error with the recognition service.")
            return ""

def get_genres():
    try:
        url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
        response = requests.get(url)
        data = response.json()
        return data.get("genres", [])
    except:
        return []

def get_movies_by_genre(genre_id):
    try:
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
        response = requests.get(url)
        data = response.json()
        return data.get("results", [])
    except:
        return []

def search_movie(query):
    try:
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
        response = requests.get(url)
        data = response.json()
        if data.get("results"):
            return data["results"][0]
        return None
    except:
        return None

def get_movie_details(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
        response = requests.get(url)
        data = response.json()
        cast = [member['name'] for member in data.get("credits", {}).get("cast", [])[:5]]
        crew = [member['name'] for member in data.get("credits", {}).get("crew", [])[:5]]
        data['cast'] = cast
        data['crew'] = crew
        return data
    except:
        return {}

def recommend_movies(movie_title):
    try:
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(url)
        movies = response.json().get("results", [])
        if not movies:
            return []

        movie_titles = [movie['title'] for movie in movies]
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(movie_titles)
        query_vector = tfidf.transform([movie_title])
        similarity = cosine_similarity(query_vector, tfidf_matrix)
        indices = similarity[0].argsort()[-6:-1][::-1]
        return [movies[i] for i in indices if i < len(movies)]
    except:
        return []
