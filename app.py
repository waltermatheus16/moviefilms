import streamlit as st
import pandas as pd
import plotly.express as px
from movie_recommender import RecomendadorPeliculas
import os

st.set_page_config(
    page_title="🎬 IA Recomendadora de Películas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .badge-similitud {
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
    
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        color: #b0b0b0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2.5rem 0;
    }
    
    h1, h2, h3 {
        color: #eaeaea !important;
    }
    
    .streamlit-expanderHeader {
        background-color: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
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
def cargar_recomendador():
    ruta_csv = os.path.join(os.path.dirname(__file__), 'data', 'movies.csv')
    return RecomendadorPeliculas(ruta_csv)

def main():
    st.markdown('<h1 class="main-header">🎬 IA Recomendadora de Películas</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    recomendador = cargar_recomendador()
    
    with st.sidebar:
        st.header("🎯 Navegación")
        pagina = st.radio(
            "Selecciona una opción:",
            ["🏠 Recomendaciones", "📊 Estadísticas", "🔍 Búsqueda Avanzada", "⚖️ Comparar Películas"]
        )
        st.markdown("---")
        st.info("💡 **Tip**: Escribe el nombre completo o parcial de una película para obtener recomendaciones")
    
    if pagina == "🏠 Recomendaciones":
        st.header("🎯 Sistema de Recomendación Inteligente")
        st.markdown("### Ingresa el nombre de una película y te recomendaremos otras similares")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            entrada_pelicula = st.text_input(
                "🎬 Nombre de la película:",
                placeholder="Ej: El Padrino, Matrix, Inception...",
                key="entrada_pelicula"
            )
        
        with col2:
            num_recomendaciones = st.number_input(
                "Número de recomendaciones:",
                min_value=1,
                max_value=10,
                value=5,
                step=1
            )
        
        if st.button("🔍 Buscar Recomendaciones", type="primary", use_container_width=True):
            if entrada_pelicula:
                with st.spinner("🤖 Analizando películas y buscando recomendaciones..."):
                    pelicula, recomendaciones = recomendador.recomendar_peliculas(entrada_pelicula, num_recomendaciones)
                    
                    if pelicula:
                        st.success(f"✅ Película encontrada: **{pelicula['title']}**")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("⭐ Rating", f"{pelicula['rating']}/10")
                        with col2:
                            st.metric("📅 Año", pelicula['year'])
                        with col3:
                            st.metric("🎭 Género", pelicula['genre'].split('/')[0])
                        with col4:
                            st.metric("🎬 Director", pelicula['director'])
                        
                        st.markdown(f"**📝 Sinopsis:** {pelicula['description']}")
                        st.markdown(f"**👥 Reparto:** {pelicula['cast']}")
                        st.markdown(f"**🌍 País:** {pelicula['country']}")
                        
                        st.markdown("---")
                        st.subheader("🎯 Películas Recomendadas")
                        
                        for i, rec in enumerate(recomendaciones, 1):
                            with st.container():
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"### {i}. {rec['title']} ({rec['year']})")
                                    st.markdown(f"**Género:** {rec['genre']} | **Director:** {rec['director']}")
                                    st.markdown(f"**⭐ Rating:** {rec['rating']}/10")
                                    st.markdown(f"**📝 {rec['description'][:200]}...**")
                                with col2:
                                    similitud = rec['puntuacion_similitud']
                                    st.markdown(f'<div class="badge-similitud">Similitud: {similitud}%</div>', unsafe_allow_html=True)
                                    st.progress(similitud / 100)
                                
                                st.markdown("---")
                    else:
                        st.error(f"❌ No se encontró la película '{entrada_pelicula}'. Intenta con otro nombre.")
                        st.info("💡 **Sugerencia**: Verifica la ortografía o intenta con el nombre en español")
            else:
                st.warning("⚠️ Por favor, ingresa el nombre de una película")
    
    elif pagina == "📊 Estadísticas":
        st.header("📊 Estadísticas de la Base de Datos")
        
        estadisticas = recomendador.obtener_estadisticas()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎬 Total de Películas", estadisticas['total_peliculas'])
        with col2:
            st.metric("⭐ Rating Promedio", f"{estadisticas['rating_promedio']}/10")
        with col3:
            st.metric("🏆 Mejor Rating", f"{estadisticas['rating_maximo']}/10")
        with col4:
            st.metric("📅 Rango de Años", estadisticas['rango_anios'])
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎭 Top 5 Géneros")
            df_generos = pd.DataFrame(list(estadisticas['top_generos'].items()), columns=['Género', 'Cantidad'])
            fig_generos = px.bar(
                df_generos, 
                x='Género', 
                y='Cantidad',
                color='Cantidad',
                color_continuous_scale='viridis'
            )
            fig_generos.update_layout(showlegend=False)
            st.plotly_chart(fig_generos, use_container_width=True)
        
        with col2:
            st.subheader("🎬 Top 5 Directores")
            df_directores = pd.DataFrame(list(estadisticas['top_directores'].items()), columns=['Director', 'Películas'])
            fig_directores = px.pie(
                df_directores,
                values='Películas',
                names='Director',
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_directores, use_container_width=True)
        
        st.subheader("⭐ Distribución de Ratings")
        fig_ratings = px.histogram(
            recomendador.df,
            x='rating',
            nbins=20,
            labels={'rating': 'Rating', 'count': 'Cantidad de Películas'},
            color_discrete_sequence=['#667eea']
        )
        fig_ratings.update_layout(showlegend=False)
        st.plotly_chart(fig_ratings, use_container_width=True)
        
        st.subheader("📅 Películas por Año")
        conteos_anio = recomendador.df['year'].value_counts().sort_index()
        fig_anios = px.line(
            x=conteos_anio.index,
            y=conteos_anio.values,
            labels={'x': 'Año', 'y': 'Cantidad de Películas'},
            markers=True
        )
        fig_anios.update_traces(line_color='#764ba2', marker_color='#667eea')
        st.plotly_chart(fig_anios, use_container_width=True)
    
    elif pagina == "🔍 Búsqueda Avanzada":
        st.header("🔍 Búsqueda Avanzada")
        
        tipo_busqueda = st.radio(
            "Buscar por:",
            ["🎭 Género", "🎬 Director", "📅 Año", "⭐ Rating"]
        )
        
        if tipo_busqueda == "🎭 Género":
            todos_generos = set()
            for generos in recomendador.df['genre'].dropna():
                todos_generos.update(generos.split('/'))
            genero_seleccionado = st.selectbox("Selecciona un género:", sorted(todos_generos))
            
            if st.button("🔍 Buscar"):
                resultados = recomendador.obtener_peliculas_por_genero(genero_seleccionado)
                st.success(f"✅ Se encontraron {len(resultados)} películas")
                
                for idx, pelicula in resultados.iterrows():
                    with st.expander(f"🎬 {pelicula['title']} ({pelicula['year']}) - ⭐ {pelicula['rating']}/10"):
                        st.write(f"**Director:** {pelicula['director']}")
                        st.write(f"**Género:** {pelicula['genre']}")
                        st.write(f"**Sinopsis:** {pelicula['description']}")
        
        elif tipo_busqueda == "🎬 Director":
            todos_directores = sorted(recomendador.df['director'].dropna().unique())
            director_seleccionado = st.selectbox("Selecciona un director:", todos_directores)
            
            if st.button("🔍 Buscar"):
                resultados = recomendador.obtener_peliculas_por_director(director_seleccionado)
                st.success(f"✅ Se encontraron {len(resultados)} películas")
                
                for idx, pelicula in resultados.iterrows():
                    with st.expander(f"🎬 {pelicula['title']} ({pelicula['year']}) - ⭐ {pelicula['rating']}/10"):
                        st.write(f"**Género:** {pelicula['genre']}")
                        st.write(f"**Sinopsis:** {pelicula['description']}")
        
        elif tipo_busqueda == "📅 Año":
            anio_min = int(recomendador.df['year'].min())
            anio_max = int(recomendador.df['year'].max())
            rango_anios = st.slider("Rango de años:", anio_min, anio_max, (anio_min, anio_max))
            
            if st.button("🔍 Buscar"):
                resultados = recomendador.df[
                    (recomendador.df['year'] >= rango_anios[0]) & 
                    (recomendador.df['year'] <= rango_anios[1])
                ]
                st.success(f"✅ Se encontraron {len(resultados)} películas")
                
                resultados_ordenados = resultados.sort_values('rating', ascending=False)
                for idx, pelicula in resultados_ordenados.iterrows():
                    with st.expander(f"🎬 {pelicula['title']} ({pelicula['year']}) - ⭐ {pelicula['rating']}/10"):
                        st.write(f"**Director:** {pelicula['director']}")
                        st.write(f"**Género:** {pelicula['genre']}")
        
        elif tipo_busqueda == "⭐ Rating":
            rating_min = float(recomendador.df['rating'].min())
            rating_max = float(recomendador.df['rating'].max())
            rango_rating = st.slider("Rango de rating:", rating_min, rating_max, (7.0, rating_max), 0.1)
            
            if st.button("🔍 Buscar"):
                resultados = recomendador.df[
                    (recomendador.df['rating'] >= rango_rating[0]) & 
                    (recomendador.df['rating'] <= rango_rating[1])
                ]
                st.success(f"✅ Se encontraron {len(resultados)} películas")
                
                resultados_ordenados = resultados.sort_values('rating', ascending=False)
                for idx, pelicula in resultados_ordenados.iterrows():
                    with st.expander(f"🎬 {pelicula['title']} ({pelicula['year']}) - ⭐ {pelicula['rating']}/10"):
                        st.write(f"**Director:** {pelicula['director']}")
                        st.write(f"**Género:** {pelicula['genre']}")
    
    elif pagina == "⚖️ Comparar Películas":
        st.header("⚖️ Comparar Películas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pelicula1 = st.text_input("🎬 Película 1:", placeholder="Ej: El Padrino")
        
        with col2:
            pelicula2 = st.text_input("🎬 Película 2:", placeholder="Ej: Goodfellas")
        
        if st.button("⚖️ Comparar", type="primary", use_container_width=True):
            if pelicula1 and pelicula2:
                with st.spinner("🔄 Comparando películas..."):
                    resultado = recomendador.comparar_peliculas(pelicula1, pelicula2)
                    
                    if resultado and resultado[0] and resultado[1]:
                        datos_pelicula1, datos_pelicula2, comparacion = resultado
                        
                        st.success("✅ Comparación realizada")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"### 🎬 {datos_pelicula1['title']}")
                            st.metric("⭐ Rating", f"{datos_pelicula1['rating']}/10")
                            st.write(f"**Año:** {datos_pelicula1['year']}")
                            st.write(f"**Director:** {datos_pelicula1['director']}")
                            st.write(f"**Género:** {datos_pelicula1['genre']}")
                            st.write(f"**País:** {datos_pelicula1['country']}")
                        
                        with col2:
                            st.markdown(f"### 🎬 {datos_pelicula2['title']}")
                            st.metric("⭐ Rating", f"{datos_pelicula2['rating']}/10")
                            st.write(f"**Año:** {datos_pelicula2['year']}")
                            st.write(f"**Director:** {datos_pelicula2['director']}")
                            st.write(f"**Género:** {datos_pelicula2['genre']}")
                            st.write(f"**País:** {datos_pelicula2['country']}")
                        
                        st.markdown("---")
                        st.subheader("📊 Análisis de Similitud")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("🎯 Similitud", f"{comparacion['similitud']}%")
                            st.progress(comparacion['similitud'] / 100)
                        with col2:
                            st.metric("⭐ Diferencia de Rating", f"{comparacion['diferencia_rating']}")
                        with col3:
                            st.metric("📅 Diferencia de Años", f"{comparacion['diferencia_anios']} años")
                    else:
                        st.error("❌ No se pudieron encontrar una o ambas películas")
            else:
                st.warning("⚠️ Por favor, ingresa ambas películas")

if __name__ == "__main__":
    main()
