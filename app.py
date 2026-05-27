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
st.title("🩺 Assistente de Diagnóstico Preditivo")
st.markdown("---")

st.subheader("Entrada de Dados do Paciente")
    
with st.form("form_clinico"):
    col1, col2 = st.columns(2)
    
    with col1:
        sexo = st.selectbox("1. Sexo Biológico", [0, 1], format_func=lambda x: "Feminino" if x == 0 else "Masculino")
        idade = st.number_input("2. Idade em anos", 14, 80, 25)
        familia = st.selectbox("3. Histórico familiar de excesso de peso", [0, 1], format_func=lambda x: "Não" if x == 0 else "Sim")
        
        # Alterado de Slider para Selectbox
        vegetais = st.selectbox("4. Frequência de consumo de vegetais", [1, 2, 3], index=1, 
                               format_func=lambda x: {1: "Raramente", 2: "Às vezes", 3: "Sempre"}[x])
        
        refeicoes = st.selectbox("5. Número de refeições principais", [1, 2, 3, 4], index=2,
                                format_func=lambda x: "1 refeição" if x == 1 else (f"{x} refeições" if x < 4 else "Mais de 3 refeições"))

    with col2:
        lanches = st.selectbox("6. Consumo de lanches entre refeições", [0, 1, 2, 3], 
                              format_func=lambda x: ["Não", "Às vezes", "Frequentemente", "Sempre"][x])
        
        # Alterado de Slider para Selectbox
        agua = st.selectbox("7. Consumo diário de água", [1, 2, 3], index=1,
                           format_func=lambda x: {1: "Menos de 1L", 2: "Entre 1L e 2L", 3: "Mais de 2L"}[x])
        
        atividade = st.selectbox("8. Frequência semanal de atividade física", [0, 1, 2, 3], 
                                format_func=lambda x: {0: "Nenhuma", 1: "1 a 2 dias", 2: "2 a 4 dias", 3: "5 ou mais dias"}[x])
        
        eletronicos = st.selectbox("9. Tempo diário de uso de eletrônicos", [0, 1, 2], 
                                  format_func=lambda x: {0: "0-2 horas", 1: "3-5 horas", 2: "Mais de 5 horas"}[x])
        
        alcool = st.selectbox("10. Consumo de bebida alcoólica", [0, 1, 2, 3], 
                             format_func=lambda x: ["Não", "Às vezes", "Frequentemente", "Sempre"][x])

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
