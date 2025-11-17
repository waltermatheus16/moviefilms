# 🎬 IA Recomendadora de Películas

Una aplicación inteligente de recomendación de películas construida con Python y Streamlit que utiliza técnicas de machine learning para sugerir películas similares basadas en contenido.

## ✨ Características

### 🎯 Sistema de Recomendación Principal
- **Búsqueda inteligente**: Encuentra películas por nombre (búsqueda exacta, parcial o por palabras clave)
- **Recomendaciones basadas en contenido**: Utiliza TF-IDF y similitud de coseno para encontrar películas similares
- **Métricas de similitud**: Muestra el porcentaje de similitud entre películas

### 📊 Estadísticas y Visualizaciones
- Dashboard con estadísticas generales de la base de datos
- Gráficos interactivos de géneros, directores y ratings
- Distribución de películas por año
- Visualizaciones creadas con Plotly

### 🔍 Búsqueda Avanzada
- Búsqueda por género
- Búsqueda por director
- Filtrado por rango de años
- Filtrado por rango de ratings

### ⚖️ Comparación de Películas
- Compara dos películas lado a lado
- Muestra similitud entre películas
- Análisis de diferencias en rating y año

### 📝 Análisis de Sentimientos
- Analiza el sentimiento de textos (descripciones, reseñas, comentarios)
- Mide polaridad y subjetividad
- Clasifica sentimientos como Positivo, Neutral o Negativo
- Análisis de descripciones de películas

## 🚀 Instalación

1. **Clonar o descargar el repositorio**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**:
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
ia peliculas/
├── app.py                 # Aplicación principal Streamlit
├── movie_recommender.py   # Lógica de recomendación
├── requirements.txt       # Dependencias
├── README.md             # Documentación
└── data/
    └── movies.csv        # Base de datos de películas
```

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para la interfaz web
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas
- **Scikit-learn**: Machine learning (TF-IDF, similitud de coseno)
- **TextBlob**: Análisis de sentimientos
- **Plotly**: Visualizaciones interactivas

## 🎓 Cómo Funciona

### Sistema de Recomendación

1. **Preprocesamiento**: Combina características de películas (género, director, reparto, descripción) en un solo texto
2. **Vectorización**: Utiliza TF-IDF para convertir el texto en vectores numéricos
3. **Cálculo de Similitud**: Calcula la similitud de coseno entre todas las películas
4. **Recomendación**: Encuentra las películas más similares a la película de entrada

### Análisis de Sentimientos

Utiliza TextBlob para analizar:
- **Polaridad**: Sentimiento positivo/negativo (-1 a 1)
- **Subjetividad**: Qué tan subjetivo es el texto (0 a 1)

## 📝 Uso

1. **Recomendaciones**: Ingresa el nombre de una película y obtén recomendaciones similares
2. **Estadísticas**: Explora estadísticas generales y visualizaciones de la base de datos
3. **Búsqueda Avanzada**: Filtra películas por diferentes criterios
4. **Comparar**: Compara dos películas y ve su similitud
5. **Análisis**: Analiza el sentimiento de textos relacionados con películas

## 🎨 Características de la Interfaz

- Diseño moderno y responsive
- Navegación intuitiva con sidebar
- Visualizaciones interactivas
- Feedback visual con colores y badges
- Búsqueda flexible y tolerante a errores

## 🔮 Posibles Mejoras Futuras

- Integración con APIs de películas (TMDB, OMDB)
- Sistema de recomendación colaborativo
- Base de datos más grande
- Sistema de usuarios y favoritos
- Recomendaciones personalizadas basadas en historial
- Análisis de reseñas de usuarios

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

---

¡Disfruta explorando y descubriendo nuevas películas! 🎬✨

