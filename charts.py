import plotly.graph_objects as go

def grafico_projecao(df, titulo="Projeção de Renda Mensal"):
    fig = go.Figure()

    # Linha base (renda atual sem crescimento)
    fig.add_trace(go.Scatter(
        x=df["mes"],
        y=df["renda_base"],
        mode="lines",
        name="Renda Atual",
        line=dict(color="#E10600", width=2, dash="dash"),
        hovertemplate="Mês %{x}<br>R$ %{y:,.2f}<extra></extra>"
    ))

    # Linha projetada
    fig.add_trace(go.Scatter(
        x=df["mes"],
        y=df["renda_projetada"],
        mode="lines+markers",
        name="Renda Projetada",
        line=dict(color="#00C853", width=3),
        marker=dict(size=6),
        hovertemplate="Mês %{x}<br>R$ %{y:,.2f}<extra></extra>"
    ))

    fig.update_layout(
        title=titulo,
        template="plotly_dark",
        height=480,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            title="Renda Mensal",
            tickprefix="R$ ",
            tickformat=",.0f",
            gridcolor="#222"
        ),
        xaxis=dict(
            title="Mês",
            showgrid=False
        )
    )

    return fig
