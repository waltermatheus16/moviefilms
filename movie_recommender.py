import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import re
import nltk

# Descargar datos necesarios para TextBlob (solo si no están disponibles)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown', quiet=True)

class MovieRecommender:
    def __init__(self, csv_path):
        """Inicializa el recomendador con la base de datos de películas"""
        self.df = pd.read_csv(csv_path)
        self.vectorizer = None
        self.similarity_matrix = None
        self._prepare_data()
        self._build_similarity_matrix()
    
    def _prepare_data(self):
        """Prepara los datos combinando características para el análisis"""
        # Combinar características relevantes para la recomendación
        self.df['combined_features'] = (
            self.df['genre'].fillna('') + ' ' +
            self.df['director'].fillna('') + ' ' +
            self.df['cast'].fillna('') + ' ' +
            self.df['description'].fillna('')
        )
        
        # Normalizar títulos para búsqueda
        self.df['title_lower'] = self.df['title'].str.lower()
    
    def _build_similarity_matrix(self):
        """Construye la matriz de similitud usando TF-IDF"""
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    def find_movie(self, movie_title):
        """Encuentra una película por título (búsqueda flexible)"""
        movie_title_lower = movie_title.lower().strip()
        
        # Búsqueda exacta
        exact_match = self.df[self.df['title_lower'] == movie_title_lower]
        if not exact_match.empty:
            return exact_match.index[0]
        
        # Búsqueda parcial
        partial_match = self.df[self.df['title_lower'].str.contains(movie_title_lower, na=False)]
        if not partial_match.empty:
            return partial_match.index[0]
        
        # Búsqueda por palabras clave
        keywords = movie_title_lower.split()
        for keyword in keywords:
            keyword_match = self.df[self.df['title_lower'].str.contains(keyword, na=False)]
            if not keyword_match.empty:
                return keyword_match.index[0]
        
        return None
    
    def recommend_movies(self, movie_title, n_recommendations=5):
        """Recomienda películas similares basadas en el título dado"""
        movie_idx = self.find_movie(movie_title)
        
        if movie_idx is None:
            return None, None
        
        movie = self.df.iloc[movie_idx]
        
        # Obtener similitudes
        similarity_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Obtener las top N recomendaciones (excluyendo la película misma)
        top_movies = similarity_scores[1:n_recommendations + 1]
        
        recommendations = []
        for idx, score in top_movies:
            rec_movie = self.df.iloc[idx].to_dict()
            rec_movie['similarity_score'] = round(score * 100, 2)
            recommendations.append(rec_movie)
        
        return movie.to_dict(), recommendations
    
    def analyze_sentiment(self, text):
        """Analiza el sentimiento de un texto"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 a 1
        subjectivity = blob.sentiment.subjectivity  # 0 a 1
        
        if polarity > 0.1:
            sentiment = "Positivo"
        elif polarity < -0.1:
            sentiment = "Negativo"
        else:
            sentiment = "Neutral"
        
        return {
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3)
        }
    
    def get_movie_stats(self):
        """Obtiene estadísticas generales de la base de datos"""
        stats = {
            'total_movies': len(self.df),
            'avg_rating': round(self.df['rating'].mean(), 2),
            'max_rating': self.df['rating'].max(),
            'min_rating': self.df['rating'].min(),
            'year_range': f"{self.df['year'].min()} - {self.df['year'].max()}",
            'top_genres': self.df['genre'].str.split('/').explode().value_counts().head(5).to_dict(),
            'top_directors': self.df['director'].value_counts().head(5).to_dict(),
            'top_countries': self.df['country'].value_counts().head(5).to_dict()
        }
        return stats
    
    def get_movies_by_genre(self, genre):
        """Obtiene películas por género"""
        return self.df[self.df['genre'].str.contains(genre, case=False, na=False)]
    
    def get_movies_by_director(self, director):
        """Obtiene películas por director"""
        return self.df[self.df['director'].str.contains(director, case=False, na=False)]
    
    def compare_movies(self, movie1_title, movie2_title):
        """Compara dos películas"""
        idx1 = self.find_movie(movie1_title)
        idx2 = self.find_movie(movie2_title)
        
        if idx1 is None or idx2 is None:
            return None, None
        
        movie1 = self.df.iloc[idx1].to_dict()
        movie2 = self.df.iloc[idx2].to_dict()
        
        # Calcular similitud
        similarity = self.similarity_matrix[idx1][idx2]
        
        comparison = {
            'similarity': round(similarity * 100, 2),
            'rating_diff': round(abs(movie1['rating'] - movie2['rating']), 2),
            'year_diff': abs(movie1['year'] - movie2['year'])
        }
        
        return movie1, movie2, comparison

