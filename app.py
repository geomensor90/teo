import streamlit as st
import pandas as pd



# Dados fornecidos
dados = {
    "Ano": [2021, 2022, 2023, 2024, 2025, 2026],
    "Coluna 2": [1.8, 2, 2.12, 2.2, 2.31, 2.31],
    "Coluna 3": [0.24, 0.27, 0.29, 0.3, 0.31, 0.31]
}

df = pd.DataFrame(dados)

# Título do app
st.subheader("Taxa de Execução de Obras (TEO)")

opcao = st.radio(
    "Escolha o cálculo:",
    ["Cálculo da TEO", "Cálculo da Área"],
    horizontal=True
)

if opcao == "Cálculo da TEO": 
        
    # Entrada da área
    campo1 = st.number_input(
        "Insira a área da construção em m²:",
        min_value=0.0,
        step=1.0,
        format="%.2f"
    )

    # Seleção dos anos
    anos_selecionados = []

    st.subheader("Selecione os anos:")

    for ano in df["Ano"]:
        if st.checkbox(str(ano), key=f"ano_{ano}"):
            anos_selecionados.append(ano)

    # Checkbox para Art. 28
    artigo_28 = st.checkbox(
        "Texto Padrão no caso de multa"
    )

    # Verifica se anos foram selecionados
    if anos_selecionados:

        dados_filtrados = df[
            df["Ano"].isin(anos_selecionados)
        ]

        # =====================================================
        # RESULTADOS
        # =====================================================

        for _, row in dados_filtrados.iterrows():

            ano = int(row["Ano"])
            valor_col2 = row["Coluna 2"]
            valor_col3 = row["Coluna 3"]

            # Cálculo
            if campo1 <= 1000:

                valor_ate_1000 = campo1 * valor_col2
                area_excedente = 0
                valor_excedente = 0

            else:

                valor_ate_1000 = 1000 * valor_col2
                area_excedente = campo1 - 1000
                valor_excedente = area_excedente * valor_col3

            valor_total = valor_ate_1000 + valor_excedente

            # =================================================
            # CABEÇALHO DO ANO
            # =================================================

            st.markdown(f"### Ano {ano}")

            # =================================================
            # TEXTO DA AUTUAÇÃO
            # =================================================

            if artigo_28:

                st.write(
                    f"Fica o contribuinte **AUTUADO** por não efetuar "
                    f"a declaração da Taxa de Execução de Obras - TEO, "
                    f"referente ao exercício {ano}"
                )

            else:

                st.write(
                    f"Taxa de Execução de Obras - TEO, "
                    f"referente ao exercício {ano}"
                )

            # =================================================
            # MEMÓRIA DE CÁLCULO
            # =================================================

            st.write("**Memória de Cálculo:**")

            st.write(
                f"Metro quadrado até áreas de 1000m² = "
                f"R$ {valor_col2:.2f}"
            )

            st.write(
                f"Valor excedente = R$ {valor_col3:.2f}"
            )

            st.write(
                f"Área (m²): {campo1:.2f}"
            )

            st.write(
                f"Valor até 1000m² = "
                f"{min(campo1, 1000):.2f} X {valor_col2:.2f} = "
                f"R$ {valor_ate_1000:.2f}"
            )

            st.write(
                f"Valor excedente = "
                f"{area_excedente:.2f} X {valor_col3:.2f} = "
                f"R$ {valor_excedente:.2f}"
            )

            st.write(
                f"**Valor total para {ano}: R$ {valor_total:.2f}**"
            )

            # =================================================
            # PRAZO
            # =================================================

            st.write("**Prazo: 30 dias**")

            # =================================================
            # OBSERVAÇÃO LEGAL
            # =================================================

            if artigo_28:

                st.write(
                    "LC 783/2008, art. 20, § 1º: Na hipótese de "
                    "recolhimento integral da taxa, o valor da multa "
                    "prevista no caput será reduzido em 80% (oitenta "
                    "por cento) se o pagamento for efetuado no prazo "
                    "de até 20 (vinte) dias contados da data em que "
                    "o contribuinte ou responsável for notificado "
                    "da exigência."
                )

            # Separação entre anos
            if len(dados_filtrados) > 1:
                st.markdown("---")

    else:

        st.warning("Por favor, selecione ao menos um ano.")


    # =========================================================
# OPÇÃO 2 — CÁLCULO REVERSO
# =========================================================

    # =========================================================
# OPÇÃO 2 — CÁLCULO REVERSO
# =========================================================

if opcao == "Cálculo da Área":

    st.header("Cálculo Reverso")
    st.caption(
        "Informe o valor pago para descobrir a área (m²) da construção."
    )

    valor_pago = st.number_input(
        "Valor pago (R$):",
        min_value=0.0,
        step=1.0,
        format="%.2f",
        key="valor_pago_reverso"
    )

    # Anos em ordem decrescente
    anos_reverso = [2026, 2025, 2024, 2023, 2022, 2021]

    ano_reverso = st.selectbox(
        "Selecione o ano:",
        anos_reverso,
        key="ano_reverso"
    )

    # =========================================================
    # SELEÇÃO DO PERÍODO
    # =========================================================

    ano_inteiro = st.checkbox(
        "Ano inteiro",
        value=True,
        key="ano_inteiro_reverso"
    )

    meses_nomes = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    if not ano_inteiro:

        col_mes1, col_mes2 = st.columns(2)

        with col_mes1:
            mes_inicio = st.selectbox(
                "Mês de início:",
                meses_nomes,
                index=0,
                key="mes_inicio_reverso"
            )

        with col_mes2:
            mes_fim = st.selectbox(
                "Mês de fim:",
                meses_nomes,
                index=11,
                key="mes_fim_reverso"
            )

        idx_inicio = meses_nomes.index(mes_inicio) + 1
        idx_fim = meses_nomes.index(mes_fim) + 1

    else:

        idx_inicio = 1
        idx_fim = 12

    # =========================================================
    # VERIFICAÇÃO DO PERÍODO
    # =========================================================

    if idx_fim < idx_inicio:

        st.error(
            "O mês final não pode ser anterior ao mês de início."
        )

    else:

        num_meses = idx_fim - idx_inicio + 1

        # =====================================================
        # BUSCA DOS VALORES DO ANO
        # =====================================================

        linha_ano = df[df["Ano"] == ano_reverso]

        if linha_ano.empty:

            st.error(
                f"Os valores para o ano {ano_reverso} ainda não estão "
                "cadastrados na tabela."
            )

        else:

            linha_ano = linha_ano.iloc[0]

            valor_col2 = linha_ano["Coluna 2"]
            valor_col3 = linha_ano["Coluna 3"]

            # =================================================
            # PRORRATEAMENTO PELO NÚMERO DE MESES
            # =================================================

            fator = num_meses / 12

            # Taxas proporcionais ao período
            teo_ate_1000 = valor_col2 * fator
            teo_excedente = valor_col3 * fator

            # =================================================
            # CÁLCULO REVERSO
            # =================================================

            if valor_pago > 0:

                # Valor correspondente aos primeiros 1.000 m²
                valor_limite_1000 = 1000 * teo_ate_1000

                # -------------------------------------------------
                # ATÉ 1.000 m²
                # -------------------------------------------------

                if valor_pago <= valor_limite_1000:

                    area_calculada = valor_pago / teo_ate_1000

                    valor_excedente = 0
                    area_excedente = 0

                # -------------------------------------------------
                # ACIMA DE 1.000 m²
                # -------------------------------------------------

                else:

                    # Valor que ultrapassa os primeiros 1.000 m²
                    valor_excedente = valor_pago - valor_limite_1000

                    # Área correspondente ao excedente
                    area_excedente = (
                        valor_excedente / teo_excedente
                    )

                    # Área total
                    area_calculada = 1000 + area_excedente

                # =================================================
                # RESULTADO
                # =================================================

                st.subheader("Resultado do Cálculo Reverso")

                if ano_inteiro:

                    st.write(
                        f"Período considerado: ano {ano_reverso} inteiro "
                        f"(12 meses)"
                    )

                else:

                    texto_meses = (
                        "1 mês"
                        if num_meses == 1
                        else f"{num_meses} meses"
                    )

                    st.write(
                        f"Período considerado: {mes_inicio} a {mes_fim} "
                        f"de {ano_reverso} ({texto_meses})"
                    )

                st.write(
                    f"TEO até 1.000 m²: "
                    f"R$ {teo_ate_1000:.2f}/m²"
                )

                st.write(
                    f"TEO excedente: "
                    f"R$ {teo_excedente:.2f}/m²"
                )

                st.write(
                    f"Valor correspondente a 1.000 m²: "
                    f"R$ {valor_limite_1000:.2f}"
                )

                st.write(
                    f"Valor pago: "
                    f"R$ {valor_pago:.2f}"
                )

                if area_excedente > 0:

                    st.write(
                        f"Valor excedente: "
                        f"R$ {valor_excedente:.2f}"
                    )

                    st.write(
                        f"Área excedente: "
                        f"{area_excedente:.2f} m²"
                    )

                st.write(
                    f"Área estimada da construção: "
                    f"**{area_calculada:.2f} m²**"
                )

            else:

                st.info(
                    "Informe o valor pago para calcular a área."
                )

    
