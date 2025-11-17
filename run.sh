#!/bin/bash

# Script para ejecutar la aplicación de recomendación de películas

echo "🎬 Iniciando IA Recomendadora de Películas..."
echo ""

# Verificar si las dependencias están instaladas
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    echo ""
fi

# Descargar datos de TextBlob si es necesario
echo "📥 Configurando TextBlob..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True); nltk.download('movie_reviews', quiet=True)" 2>/dev/null || echo "TextBlob ya está configurado"

echo ""
echo "🚀 Iniciando aplicación Streamlit..."
echo ""

streamlit run app.py

