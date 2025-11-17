import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown', quiet=True)

class RecomendadorPeliculas:
    def __init__(self, ruta_csv):
        self.df = pd.read_csv(ruta_csv)
        self.vectorizador = None
        self.matriz_similitud = None
        self._preparar_datos()
        self._construir_matriz_similitud()
    
    def _preparar_datos(self):
        self.df['caracteristicas_combinadas'] = (
            self.df['genre'].fillna('') + ' ' +
            self.df['director'].fillna('') + ' ' +
            self.df['cast'].fillna('') + ' ' +
            self.df['description'].fillna('')
        )
        self.df['titulo_minusculas'] = self.df['title'].str.lower()
    
    def _construir_matriz_similitud(self):
        self.vectorizador = TfidfVectorizer(stop_words='english', max_features=5000)
        matriz_tfidf = self.vectorizador.fit_transform(self.df['caracteristicas_combinadas'])
        self.matriz_similitud = cosine_similarity(matriz_tfidf, matriz_tfidf)
    
    def buscar_pelicula(self, titulo_pelicula):
        titulo_minusculas = titulo_pelicula.lower().strip()
        
        coincidencia_exacta = self.df[self.df['titulo_minusculas'] == titulo_minusculas]
        if not coincidencia_exacta.empty:
            return coincidencia_exacta.index[0]
        
        coincidencia_parcial = self.df[self.df['titulo_minusculas'].str.contains(titulo_minusculas, na=False)]
        if not coincidencia_parcial.empty:
            return coincidencia_parcial.index[0]
        
        palabras_clave = titulo_minusculas.split()
        for palabra in palabras_clave:
            coincidencia_palabra = self.df[self.df['titulo_minusculas'].str.contains(palabra, na=False)]
            if not coincidencia_palabra.empty:
                return coincidencia_palabra.index[0]
        
        return None
    
    def recomendar_peliculas(self, titulo_pelicula, num_recomendaciones=5):
        indice_pelicula = self.buscar_pelicula(titulo_pelicula)
        
        if indice_pelicula is None:
            return None, None
        
        pelicula = self.df.iloc[indice_pelicula]
        
        puntuaciones_similitud = list(enumerate(self.matriz_similitud[indice_pelicula]))
        puntuaciones_similitud = sorted(puntuaciones_similitud, key=lambda x: x[1], reverse=True)
        
        peliculas_top = puntuaciones_similitud[1:num_recomendaciones + 1]
        
        recomendaciones = []
        for indice, puntuacion in peliculas_top:
            pelicula_rec = self.df.iloc[indice].to_dict()
            pelicula_rec['puntuacion_similitud'] = round(puntuacion * 100, 2)
            recomendaciones.append(pelicula_rec)
        
        return pelicula.to_dict(), recomendaciones
    
    def obtener_estadisticas(self):
        estadisticas = {
            'total_peliculas': len(self.df),
            'rating_promedio': round(self.df['rating'].mean(), 2),
            'rating_maximo': self.df['rating'].max(),
            'rating_minimo': self.df['rating'].min(),
            'rango_anios': f"{self.df['year'].min()} - {self.df['year'].max()}",
            'top_generos': self.df['genre'].str.split('/').explode().value_counts().head(5).to_dict(),
            'top_directores': self.df['director'].value_counts().head(5).to_dict(),
            'top_paises': self.df['country'].value_counts().head(5).to_dict()
        }
        return estadisticas
    
    def obtener_peliculas_por_genero(self, genero):
        return self.df[self.df['genre'].str.contains(genero, case=False, na=False)]
    
    def obtener_peliculas_por_director(self, director):
        return self.df[self.df['director'].str.contains(director, case=False, na=False)]
    
    def comparar_peliculas(self, titulo_pelicula1, titulo_pelicula2):
        indice1 = self.buscar_pelicula(titulo_pelicula1)
        indice2 = self.buscar_pelicula(titulo_pelicula2)
        
        if indice1 is None or indice2 is None:
            return None, None
        
        pelicula1 = self.df.iloc[indice1].to_dict()
        pelicula2 = self.df.iloc[indice2].to_dict()
        
        similitud = self.matriz_similitud[indice1][indice2]
        
        comparacion = {
            'similitud': round(similitud * 100, 2),
            'diferencia_rating': round(abs(pelicula1['rating'] - pelicula2['rating']), 2),
            'diferencia_anios': abs(pelicula1['year'] - pelicula2['year'])
        }
        
        return pelicula1, pelicula2, comparacion
