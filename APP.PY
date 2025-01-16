import streamlit as st
import pandas as pd

# Dados fornecidos
dados = {
    "Ano": [2020, 2021, 2022, 2023, 2024, 2025],
    "Coluna 2": [1.71, 1.8, 2, 2.12, 2.2, 2.31],
    "Coluna 3": [0.23, 0.24, 0.27, 0.29, 0.3, 0.31]
}

df = pd.DataFrame(dados)

# Título do app
st.title("Taxa de Execução de Obras (TEO)")

# Primeiro campo: entrada numérica
campo1 = st.number_input("Insira a área da construção em m²:", min_value=0.0, step=1.0, format="%.2f")

# Segundo campo: seleção dos anos (como checkboxes)
anos_selecionados = []
st.subheader("Selecione os anos:")
for ano in df["Ano"]:
    if st.checkbox(str(ano)):
        anos_selecionados.append(ano)

# Checkbox para Art. 28
artigo_28 = st.checkbox("Art. 28. Sujeitar-se-á à multa de 100% (cem por cento) sobre o valor atualizado da taxa devida o contribuinte que não prestar, no prazo estabelecido, a declaração prevista no art. 25, ou o fizer com omissão ou inexatidão.")

# Checkbox para Art. 27
artigo_27 = st.checkbox("Art. 27. Isentos do pagamento da Taxa de Execução de Obras")

if artigo_27:
    st.markdown("""
    <div style="text-align: center; font-size: 16px;">   
    <strong>I</strong> – a União, os Estados, o Distrito Federal e os Municípios;<br>
    <strong>II</strong> – as obras em prédios sedes de embaixadas;<br>
    <strong>III</strong> – as autarquias e fundações públicas, para as obras que realizarem em prédios destinados às suas finalidades específicas, excluídas as destinadas à revenda ou locação e as utilizadas para fins estranhos a essas pessoas jurídicas;<br>
    <strong>IV</strong> – as obras em imóveis reconhecidos em lei como de interesse histórico, cultural ou ecológico, desde que respeitem integralmente as características arquitetônicas originais das fachadas;<br>
    <strong>V</strong> – as obras executadas por imposição do Poder Público;<br>
    <strong>VI</strong> – as sedes de partidos políticos;<br>
    <strong>VII</strong> – as sedes das entidades sindicais;<br>
    <strong>VIII</strong> – templos de qualquer culto;<br>
    <strong>IX</strong> – o beneficiário de programa habitacional realizado pelo Poder Público, com área máxima de construção de 120m² em lote de uso residencial unifamiliar, que não seja possuidor de outro imóvel residencial no Distrito Federal;<br>
    <strong>X</strong> – as obras que independam de licença ou comunicação para serem executadas, de acordo com o Código de Edificações do Distrito Federal;<br>
    <strong>XI</strong> – as entidades associativas ou cooperativas de trabalhadores.<br>
    <strong>Parágrafo único:</strong> A efetivação do benefício de que trata este artigo se dará na forma do regulamento, mediante requerimento acompanhado de documentação comprobatória.
    </div>
    """, unsafe_allow_html=True)


# Verifica se anos foram selecionados
if anos_selecionados:
    # Filtra os dados pelos anos selecionados
    dados_filtrados = df[df["Ano"].isin(anos_selecionados)]

    # Calcula os resultados com base no valor do campo1
    resultados = []
    soma_total = 0
    for _, row in dados_filtrados.iterrows():
        if campo1 <= 1000:
            resultado = campo1 * row["Coluna 2"]
        else:
            resultado = campo1 * row["Coluna 2"] + campo1 * row["Coluna 3"]
        resultados.append((row["Ano"], resultado))
        soma_total += resultado

    # Aplica a multa de 100% se Art. 28 for selecionado
    if artigo_28:
        soma_total *= 2

    # Aplica a multa de 0% se Art. 27 for selecionado
    if artigo_27:
        soma_total *= 0

    # Exibe os resultados
    st.subheader("Resultados")
    for ano, resultado in resultados:
        st.write(f"Ano {ano:.0f}: R$ {resultado:.2f}")

    # Exibe a soma total
    st.subheader("Soma Total")
    st.write(f"R$ {soma_total:.2f}")
else:
    st.warning("Por favor, selecione ao menos um ano.")
