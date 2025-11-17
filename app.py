import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from movie_recommender import MovieRecommender
import os

# Configuración de la página
st.set_page_config(
    page_title="🎬 IA Recomendadora de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - Modo oscuro elegante
st.markdown("""
    <style>
    /* Header personalizado */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Badge de similitud mejorado */
    .similarity-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.4);
    }
    
    /* Cards de recomendaciones con fondo sutil */
    .stContainer > div {
        background-color: rgba(102, 126, 234, 0.08);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .stContainer > div:hover {
        background-color: rgba(102, 126, 234, 0.12);
        transform: translateX(5px);
    }
    
    /* Botones elegantes */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
    }
    
    /* Métricas destacadas */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: #b0b0b0;
    }
    
    /* Inputs con estilo */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Separadores elegantes */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2.5rem 0;
    }
    
    /* Mejorar contraste de texto */
    h1, h2, h3 {
        color: #eaeaea !important;
    }
    
    /* Expanders mejorados */
    .streamlit-expanderHeader {
        background-color: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    /* Info boxes con mejor estilo */
    .stInfo {
        background-color: rgba(102, 126, 234, 0.15);
        border-left: 4px solid #667eea;
        border-radius: 8px;
    }
    
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.15);
        border-left: 4px solid #4CAF50;
        border-radius: 8px;
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.15);
        border-left: 4px solid #f44336;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: rgba(255, 152, 0, 0.15);
        border-left: 4px solid #ff9800;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    """Carga el recomendador (cached para mejor rendimiento)"""
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'movies.csv')
    return MovieRecommender(csv_path)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 IA Recomendadora de Películas</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Cargar el recomendador
    recommender = load_recommender()
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navegación")
        page = st.radio(
            "Selecciona una opción:",
            ["🏠 Recomendaciones", "📊 Estadísticas", "🔍 Búsqueda Avanzada", "⚖️ Comparar Películas"]
        )
        st.markdown("---")
        st.info("💡 **Tip**: Escribe el nombre completo o parcial de una película para obtener recomendaciones")
    
    # Página principal: Recomendaciones
    if page == "🏠 Recomendaciones":
        st.header("🎯 Sistema de Recomendación Inteligente")
        st.markdown("### Ingresa el nombre de una película y te recomendaremos otras similares")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            movie_input = st.text_input(
                "🎬 Nombre de la película:",
                placeholder="Ej: El Padrino, Matrix, Inception...",
                key="movie_input"
            )
        
        with col2:
            n_recommendations = st.number_input(
                "Número de recomendaciones:",
                min_value=1,
                max_value=10,
                value=5,
                step=1
            )
        
        if st.button("🔍 Buscar Recomendaciones", type="primary", use_container_width=True):
            if movie_input:
                with st.spinner("🤖 Analizando películas y buscando recomendaciones..."):
                    movie, recommendations = recommender.recommend_movies(movie_input, n_recommendations)
                    
                    if movie:
                        st.success(f"✅ Película encontrada: **{movie['title']}**")
                        
                        # Mostrar información de la película
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("⭐ Rating", f"{movie['rating']}/10")
                        with col2:
                            st.metric("📅 Año", movie['year'])
                        with col3:
                            st.metric("🎭 Género", movie['genre'].split('/')[0])
                        with col4:
                            st.metric("🎬 Director", movie['director'])
                        
                        st.markdown(f"**📝 Sinopsis:** {movie['description']}")
                        st.markdown(f"**👥 Reparto:** {movie['cast']}")
                        st.markdown(f"**🌍 País:** {movie['country']}")
                        
                        st.markdown("---")
                        st.subheader("🎯 Películas Recomendadas")
                        
                        # Mostrar recomendaciones
                        for i, rec in enumerate(recommendations, 1):
                            with st.container():
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"### {i}. {rec['title']} ({rec['year']})")
                                    st.markdown(f"**Género:** {rec['genre']} | **Director:** {rec['director']}")
                                    st.markdown(f"**⭐ Rating:** {rec['rating']}/10")
                                    st.markdown(f"**📝 {rec['description'][:200]}...**")
                                with col2:
                                    similarity = rec['similarity_score']
                                    st.markdown(f'<div class="similarity-badge">Similitud: {similarity}%</div>', unsafe_allow_html=True)
                                    
                                    # Barra de progreso para similitud
                                    st.progress(similarity / 100)
                                
                                st.markdown("---")
                    else:
                        st.error(f"❌ No se encontró la película '{movie_input}'. Intenta con otro nombre.")
                        st.info("💡 **Sugerencia**: Verifica la ortografía o intenta con el nombre en español")
            else:
                st.warning("⚠️ Por favor, ingresa el nombre de una película")
    
    # Página de Estadísticas
    elif page == "📊 Estadísticas":
        st.header("📊 Estadísticas de la Base de Datos")
        
        stats = recommender.get_movie_stats()
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎬 Total de Películas", stats['total_movies'])
        with col2:
            st.metric("⭐ Rating Promedio", f"{stats['avg_rating']}/10")
        with col3:
            st.metric("🏆 Mejor Rating", f"{stats['max_rating']}/10")
        with col4:
            st.metric("📅 Rango de Años", stats['year_range'])
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎭 Top 5 Géneros")
            genres_df = pd.DataFrame(list(stats['top_genres'].items()), columns=['Género', 'Cantidad'])
            fig_genres = px.bar(
                genres_df, 
                x='Género', 
                y='Cantidad',
                color='Cantidad',
                color_continuous_scale='viridis'
            )
            fig_genres.update_layout(showlegend=False)
            st.plotly_chart(fig_genres, use_container_width=True)
        
        with col2:
            st.subheader("🎬 Top 5 Directores")
            directors_df = pd.DataFrame(list(stats['top_directors'].items()), columns=['Director', 'Películas'])
            fig_directors = px.pie(
                directors_df,
                values='Películas',
                names='Director',
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_directors, use_container_width=True)
        
        # Distribución de ratings
        st.subheader("⭐ Distribución de Ratings")
        fig_ratings = px.histogram(
            recommender.df,
            x='rating',
            nbins=20,
            labels={'rating': 'Rating', 'count': 'Cantidad de Películas'},
            color_discrete_sequence=['#667eea']
        )
        fig_ratings.update_layout(showlegend=False)
        st.plotly_chart(fig_ratings, use_container_width=True)
        
        # Películas por año
        st.subheader("📅 Películas por Año")
        year_counts = recommender.df['year'].value_counts().sort_index()
        fig_years = px.line(
            x=year_counts.index,
            y=year_counts.values,
            labels={'x': 'Año', 'y': 'Cantidad de Películas'},
            markers=True
        )
        fig_years.update_traces(line_color='#764ba2', marker_color='#667eea')
        st.plotly_chart(fig_years, use_container_width=True)
    
    # Búsqueda Avanzada
    elif page == "🔍 Búsqueda Avanzada":
        st.header("🔍 Búsqueda Avanzada")
        
        search_type = st.radio(
            "Buscar por:",
            ["🎭 Género", "🎬 Director", "📅 Año", "⭐ Rating"]
        )
        
        if search_type == "🎭 Género":
            all_genres = set()
            for genres in recommender.df['genre'].dropna():
                all_genres.update(genres.split('/'))
            selected_genre = st.selectbox("Selecciona un género:", sorted(all_genres))
            
            if st.button("🔍 Buscar"):
                results = recommender.get_movies_by_genre(selected_genre)
                st.success(f"✅ Se encontraron {len(results)} películas")
                
                for idx, movie in results.iterrows():
                    with st.expander(f"🎬 {movie['title']} ({movie['year']}) - ⭐ {movie['rating']}/10"):
                        st.write(f"**Director:** {movie['director']}")
                        st.write(f"**Género:** {movie['genre']}")
                        st.write(f"**Sinopsis:** {movie['description']}")
        
        elif search_type == "🎬 Director":
            all_directors = sorted(recommender.df['director'].dropna().unique())
            selected_director = st.selectbox("Selecciona un director:", all_directors)
            
            if st.button("🔍 Buscar"):
                results = recommender.get_movies_by_director(selected_director)
                st.success(f"✅ Se encontraron {len(results)} películas")
                
                for idx, movie in results.iterrows():
                    with st.expander(f"🎬 {movie['title']} ({movie['year']}) - ⭐ {movie['rating']}/10"):
                        st.write(f"**Género:** {movie['genre']}")
                        st.write(f"**Sinopsis:** {movie['description']}")
        
        elif search_type == "📅 Año":
            min_year = int(recommender.df['year'].min())
            max_year = int(recommender.df['year'].max())
            year_range = st.slider("Rango de años:", min_year, max_year, (min_year, max_year))
            
            if st.button("🔍 Buscar"):
                results = recommender.df[
                    (recommender.df['year'] >= year_range[0]) & 
                    (recommender.df['year'] <= year_range[1])
                ]
                st.success(f"✅ Se encontraron {len(results)} películas")
                
                results_sorted = results.sort_values('rating', ascending=False)
                for idx, movie in results_sorted.iterrows():
                    with st.expander(f"🎬 {movie['title']} ({movie['year']}) - ⭐ {movie['rating']}/10"):
                        st.write(f"**Director:** {movie['director']}")
                        st.write(f"**Género:** {movie['genre']}")
        
        elif search_type == "⭐ Rating":
            min_rating = float(recommender.df['rating'].min())
            max_rating = float(recommender.df['rating'].max())
            rating_range = st.slider("Rango de rating:", min_rating, max_rating, (7.0, max_rating), 0.1)
            
            if st.button("🔍 Buscar"):
                results = recommender.df[
                    (recommender.df['rating'] >= rating_range[0]) & 
                    (recommender.df['rating'] <= rating_range[1])
                ]
                st.success(f"✅ Se encontraron {len(results)} películas")
                
                results_sorted = results.sort_values('rating', ascending=False)
                for idx, movie in results_sorted.iterrows():
                    with st.expander(f"🎬 {movie['title']} ({movie['year']}) - ⭐ {movie['rating']}/10"):
                        st.write(f"**Director:** {movie['director']}")
                        st.write(f"**Género:** {movie['genre']}")
    
    # Comparar Películas
    elif page == "⚖️ Comparar Películas":
        st.header("⚖️ Comparar Películas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            movie1 = st.text_input("🎬 Película 1:", placeholder="Ej: El Padrino")
        
        with col2:
            movie2 = st.text_input("🎬 Película 2:", placeholder="Ej: Goodfellas")
        
        if st.button("⚖️ Comparar", type="primary", use_container_width=True):
            if movie1 and movie2:
                with st.spinner("🔄 Comparando películas..."):
                    result = recommender.compare_movies(movie1, movie2)
                    
                    if result and result[0] and result[1]:
                        movie1_data, movie2_data, comparison = result
                        
                        st.success("✅ Comparación realizada")
                        
                        # Mostrar comparación lado a lado
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"### 🎬 {movie1_data['title']}")
                            st.metric("⭐ Rating", f"{movie1_data['rating']}/10")
                            st.write(f"**Año:** {movie1_data['year']}")
                            st.write(f"**Director:** {movie1_data['director']}")
                            st.write(f"**Género:** {movie1_data['genre']}")
                            st.write(f"**País:** {movie1_data['country']}")
                        
                        with col2:
                            st.markdown(f"### 🎬 {movie2_data['title']}")
                            st.metric("⭐ Rating", f"{movie2_data['rating']}/10")
                            st.write(f"**Año:** {movie2_data['year']}")
                            st.write(f"**Director:** {movie2_data['director']}")
                            st.write(f"**Género:** {movie2_data['genre']}")
                            st.write(f"**País:** {movie2_data['country']}")
                        
                        st.markdown("---")
                        st.subheader("📊 Análisis de Similitud")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("🎯 Similitud", f"{comparison['similarity']}%")
                            st.progress(comparison['similarity'] / 100)
                        with col2:
                            st.metric("⭐ Diferencia de Rating", f"{comparison['rating_diff']}")
                        with col3:
                            st.metric("📅 Diferencia de Años", f"{comparison['year_diff']} años")
                    else:
                        st.error("❌ No se pudieron encontrar una o ambas películas")
            else:
                st.warning("⚠️ Por favor, ingresa ambas películas")

if __name__ == "__main__":
    main()

