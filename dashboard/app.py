import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import plotly.express as px
import streamlit as st
from sql.query import (
    get_category,
    get_date_min_max,
    get_mark,
    get_states,
    query_filtro,
)

# 1. Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* ... seus outros estilos CSS aqui ... */

    /* CENTRALIZAR OS CONTEÚDOS DOS KPIS */
    [data-testid="stMetric"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    [data-testid="stMetricLabel"], 
    [data-testid="stMetricValue"], 
    [data-testid="stMetricDelta"] {
        justify-content: center !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BARRA LATERAL (SIDEBAR)
# ==========================================

with st.sidebar:
    st.title("⚙️ Filtros",text_alignment="justify")
    st.divider()

    data_inicio = get_date_min_max("min")
    data_fim = get_date_min_max("max")

    dt = st.date_input(
        "Período",
        value=(data_inicio, data_fim),
        format="DD/MM/YYYY",
        key="periodo_sidebar",
    )

    def resetar_filtros():
        st.session_state["periodo_sidebar"] = (data_inicio, data_fim)
        st.session_state["estado"] = "Todos"
        st.session_state["categoria"] = "Todos"
        st.session_state["marca"] = "Todos"

    states_options = ["Todos"] + get_states()
    category_options = ["Todos"] + get_category()
    mark_options = ["Todos"] + get_mark()

    state_filter = st.selectbox("Estado", states_options, key="estado")
    category_filter = st.selectbox(
        "Categoria", category_options, key="categoria"
    )
    mark_filter = st.selectbox("Marca", mark_options, key="marca")

    # Botão de limpar direto na sidebar (removidas as colunas não utilizadas)
    if st.button("Limpar 🔄", on_click=resetar_filtros, use_container_width=True):
        st.rerun()

    st.divider()

    st.subheader("Sobre o projeto")
    st.caption(
        """
        Dashboard desenvolvido com **Streamlit** para análise de vendas.
        
        Dados carregados via ETL a partir de arquivos CSV e armazenados no **MySQL**.
        """
    )

# ==========================================
# 3. BUSCA DOS DADOS E CABEÇALHO
# ==========================================

df = query_filtro(dt, state_filter, category_filter, mark_filter)

st.title("🛒 Dashboard de Vendas",text_alignment="center")
st.caption("Visão geral do desempenho de vendas",text_alignment="center")

st.divider()

# ==========================================
# 4. CARDS DE INDICADORES (KPIs)
# ==========================================
total_earnings = df["valor_total"].sum() if not df.empty else 0
sales_qtd = df["idVenda"].count() if not df.empty else 0
sales_product = df["quantidade"].sum() if not df.empty else 0
clients_qtd = df["idCliente"].nunique() if not df.empty else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap = "xxlarge") 

with kpi1:
    st.metric(
        label="💲 Faturamento Total",
        value=f"R$ {total_earnings:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
        border = True,
        width = "stretch"
    )

with kpi2:
    st.metric(
        label="🛒 Quantidade de Vendas",
        value=f"{sales_qtd:,}".replace(",", "."),
        border = True
    )

with kpi3:
    st.metric(
        label="📦 Produtos Vendidos",
        value=f"{sales_product:,}".replace(",", "."),
        border = True
    )

with kpi4:
    st.metric(
        label="👥 Clientes",
        value=f"{clients_qtd:,}".replace(",", "."),
        border = True
    )

st.divider()

# ==========================================
# 5. GRÁFICOS PRINCIPAIS
# ==========================================
col_graf1, col_graf2 = st.columns([1.4, 1],gap = "xlarge")

# --- Gráfico de Linha ---
with col_graf1:
    st.subheader("Faturamento por Período",text_alignment="center")

    if not df.empty and "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"])
        df_linha = (
            df.groupby(df["data"].dt.to_period("D"))["valor_total"]
            .sum()
            .reset_index()
        )
        df_linha["data"] = df_linha["data"].astype(str)

        fig_linha = px.line(
            df_linha,
            x="data",
            y="valor_total",
            markers=True,
            labels={"data": "Data", "valor_total": "Faturamento (R$)"},
            template="plotly_white",  # Força o fundo claro no Plotly
        )

        fig_linha.update_traces(
            line_color="#1f77b4", line_width=3, marker_size=8, fill="tozeroy"
        )
        fig_linha.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(tickprefix="R$ "),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#111827"),
        )

        st.plotly_chart(fig_linha, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para gerar o gráfico de período.")

# --- Gráfico de Rosca (Donut) ---
with col_graf2:
    st.subheader("Faturamento por Categoria",text_alignment="center",)

    if not df.empty and "categoria" in df.columns:
        df_cat = df.groupby("categoria")["valor_total"].sum().reset_index()

        fig_donut = px.pie(
            df_cat,
            values="valor_total",
            names="categoria",
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set1,
            template="plotly_white",
        )

        fig_donut.update_traces(textinfo="percent+label", showlegend=True)
        fig_donut.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#111827"),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.0,
            ),
        )

        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para gerar o gráfico de categorias.")

st.divider()

# ==========================================
# 6. OUTROS GRÁFICOS E ANÁLISES
# ==========================================
col_graf3, col_graf4 = st.columns([0.9, 1],gap="xlarge")

# --- Top 10 Produtos ---
with col_graf3:
    st.subheader("Top 10 Produtos", text_alignment= "center")

    if not df.empty and "nomeProduto" in df.columns:
        df_prod = (
            df.groupby("nomeProduto")["valor_total"]
            .sum()
            .reset_index()
            .sort_values(by="valor_total", ascending=True)
            .tail(10)
        )

        fig_bar = px.bar(
            df_prod,
            x="valor_total",
            y="nomeProduto",
            orientation="h",
            text_auto=".2s",
            labels={
                "valor_total": "Faturamento (R$)",
                "nomeProduto": "Produto",
            },
            color_discrete_sequence=["#1f77b4"],
            template="plotly_white",
        )

        fig_bar.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(tickprefix="R$ "),
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#111827"),
        )

        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Nenhum dado encontrado para gerar o ranking de produtos.")

# --- Vendas por Estado ---
with col_graf4:
    st.subheader("Vendas por Estado",text_alignment= "center")

    if not df.empty and "estado" in df.columns:
        df_estados = (
            df.groupby("estado")["valor_total"]
            .sum()
            .reset_index()
            .sort_values(by="valor_total", ascending=False)
        )

        col_mapa, col_tabela = st.columns([1.2, 0.45],gap="medium")

        with col_mapa:
            geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

            fig_map = px.choropleth(
                df_estados,
                geojson=geojson_url,
                locations="estado",
                featureidkey="properties.sigla",
                color="valor_total",
                color_continuous_scale="Blues",
                template="plotly_white",
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=300,
                coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#111827"),
            )

            st.plotly_chart(fig_map, use_container_width=True)

        with col_tabela:
            df_estados_tab = df_estados.copy()
            df_estados_tab["Faturamento"] = df_estados_tab[
                "valor_total"
            ].apply(
                lambda x: f"R$ {x:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            st.dataframe(
                df_estados_tab[["estado", "Faturamento"]],
                hide_index=True,
                use_container_width=True,
                height=300,
            )
    else:
        st.info("Nenhum dado encontrado para gerar as vendas por estado.")

st.markdown(
    """
    <style>
    .footer {
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #6B7280;
        text-align: center;
        padding: 20px 0 10px 0;
        font-size: 14px;
        margin-top: 40px;
        border-top: 1px solid #E5E7EB;
    }
    .footer a {
        color: #1F77B4 !important;
        text-decoration: none;
        font-weight: 600;
        margin: 0 8px;
        transition: color 0.2s ease;
    }
    .footer a:hover {
        color: #0056b3 !important;
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        Desenvolvido por <strong>João Victor Batista</strong> | 
        <a href="https://www.linkedin.com/in/joaobatista7/" target="_blank">🔗 LinkedIn</a> | 
        <a href="https://github.com/Joao-VictorRB" target="_blank">💻 GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)