import streamlit as st
import joblib
import pandas as pd

# 1. Carregar o novo modelo otimizado
try:
    modelo = joblib.load('random_forest_otimizado.joblib')
except:
    st.error("Erro: O ficheiro 'random_forest_otimizado.joblib' não foi encontrado na pasta.")

# Mapeamentos de Classes e Cores
class_mapping = {
    0: "Peso Insuficiente", 1: "Peso Normal", 2: "Sobrepeso Nível I",
    3: "Sobrepeso Nível II", 4: "Obesidade Tipo I", 5: "Obesidade Tipo II", 6: "Obesidade Tipo III"
}

color_mapping = {
    0: "#3498db", 1: "#27ae60", 2: "#f1c40f", 3: "#f39c12", 4: "#e67e22", 5: "#e74c3c", 6: "#c0392b"
}

st.set_page_config(page_title="Hospit-AI", layout="wide")
st.title("🩺 Assistente de Diagnóstico Preditivo - Hospit-AI")
st.markdown("---")

aba1, aba2 = st.tabs(["🎯 Simulador de Risco", "📊 Visão de Negócio & Insights"])

with aba1:
    st.subheader("Entrada de Dados do Paciente (Números Inteiros)")
    
    with st.form("form_clinico"):
        col1, col2 = st.columns(2)
        
        with col1:
            sexo = st.selectbox("1. Sexo Biológico", [0, 1], format_func=lambda x: "Feminino" if x == 0 else "Masculino")
            idade = st.number_input("2. Idade em anos", 14, 80, 25)
            familia = st.selectbox("3. Histórico familiar de excesso de peso", [0, 1], format_func=lambda x: "Não" if x == 0 else "Sim")
            vegetais = st.slider("4. Frequência de consumo de vegetais (1 a 3)", 1, 3, 2)
            refeicoes = st.slider("5. Número de refeições principais (1 a 4)", 1, 4, 3)

        with col2:
            lanches = st.selectbox("6. Consumo de lanches entre refeições", [0, 1, 2, 3], format_func=lambda x: ["Não", "Às vezes", "Frequentemente", "Sempre"][x])
            agua = st.slider("7. Consumo diário de água (1 a 3)", 1, 3, 2)
            atividade = st.slider("8. Frequência semanal de atividade física (0 a 3)", 0, 3, 1)
            eletronicos = st.slider("9. Tempo diário de uso de eletrônicos (0 a 2)", 0, 2, 1)
            alcool = st.selectbox("10. Consumo de bebida alcoólica", [0, 1, 2, 3], format_func=lambda x: ["Não", "Às vezes", "Frequentemente", "Sempre"][x])

        enviar = st.form_submit_button("Gerar Laudo Preditivo")

    if enviar:
        entrada = pd.DataFrame([[sexo, idade, familia, vegetais, refeicoes, lanches, agua, atividade, eletronicos, alcool]], 
                             columns=['Sexo biológico', 'Idade em anos', 'Histórico familiar de excesso de peso', 
                                      'Frequência de consumo de vegetais', 'Número de refeições principais', 
                                      'Consumo de lanches entre refeições', 'Consumo diário de água', 
                                      'Frequência semanal de atividade física', 'Tempo diário de uso de eletrônicos', 
                                      'Consumo de bebida alcoólica'])
        
        resultado_num = modelo.predict(entrada)[0]
        st.markdown(f"""
            <div style="padding:30px; border-radius:15px; background-color:{color_mapping[resultado_num]}; margin-top: 20px;">
                <h2 style="color:white; text-align:center; margin:0;">
                    Diagnóstico Estimado: {class_mapping[resultado_num]}
                </h2>
            </div>
        """, unsafe_allow_html=True)

with aba2:
    st.subheader("📊 Análise Exploratória de Dados")
    
    try:
        df = pd.read_csv("Obesity.csv")
        
        # Métricas de Negócio
        m1, m2, m3 = st.columns(3)
        m1.metric("Pacientes Analisados", len(df))
        # Ajuste de nomes de colunas comum no dataset de obesidade (Age e CH2O)
        if 'Age' in df.columns:
            m2.metric("Média de Idade", f"{df['Age'].mean():.1f} anos")
        if 'CH2O' in df.columns:
            m3.metric("Média Consumo Água", f"{df['CH2O'].mean():.1f} L")

        st.markdown("---")

        # Gráfico de Distribuição
        st.markdown("**Distribuição por Nível de Obesidade na Base**")
        # Procura a coluna alvo (NObeyesdad é o padrão do dataset)
        col_alvo = 'NObeyesdad' if 'NObeyesdad' in df.columns else 'Obesity'
        
        if col_alvo in df.columns:
            st.bar_chart(df[col_alvo].value_counts())
        else:
            st.warning("Coluna de diagnóstico não encontrada no ficheiro CSV.")

    except Exception as e:
        st.error(f"Erro ao carregar os insights: {e}")