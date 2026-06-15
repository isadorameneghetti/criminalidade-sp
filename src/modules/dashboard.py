"""
===============================================================================
MODULO: DASHBOARD - VISUALIZACAO INTERATIVA COM PLOTLY
===============================================================================
Autor: Isadora Meneghetti
Versao: 2.1 (Layout Formal e Espacado)
Data: Junho 2026
Contexto: FIAP - Engenharia de Software - Data Science and Statistical Computing
===============================================================================
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DashboardCriminalidade:
    """
    Dashboard interativo com layout profissional e espaçamento adequado.
    """
    
    def __init__(self, df):
        self.df = df
        self.meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                           'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        self.cores = {
            'primary': '#1a73e8',
            'secondary': '#e8710a',
            'success': '#0d7c3f',
            'danger': '#d93025',
            'purple': '#9334e6',
            'dark': '#2c3e50',
            'light': '#f8f9fa',
            'gray': '#7f8c8d'
        }
    
    def criar_dashboard_completo(self, output_file="outputs/dashboard/dashboard_criminalidade.html"):
        """
        Cria dashboard interativo com layout formal e bem espaçado.
        """
        print("\nCriando dashboard interativo (layout formal)...")
        
        # Métricas para o cabeçalho
        total_ocorrencias = self.df['ocorrencias'].sum()
        periodo_inicio = self.df['data'].min().year
        periodo_fim = self.df['data'].max().year
        total_crimes = self.df['natureza'].nunique()
        media_mensal = self.df['ocorrencias'].mean()
        
        crime_principal = self.df.groupby('natureza')['ocorrencias'].sum().idxmax()
        total_crime_principal = self.df.groupby('natureza')['ocorrencias'].sum().max()
        
        # Subplots com maior espaçamento vertical/horizontal
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                '<b>Total de Ocorrências por Ano</b>',
                '<b>Top 10 Crimes</b>',
                '<b>Evolução Temporal - Top 5 Crimes</b>',
                '<b>Sazonalidade - Média Mensal</b>',
                '<b>Mapa de Calor Temporal</b>',
                '<b>Distribuição das Ocorrências</b>'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'scatter'}, {'type': 'bar'}],
                [{'type': 'heatmap'}, {'type': 'histogram'}]
            ],
            vertical_spacing=0.15,    # Mais espaço entre linhas
            horizontal_spacing=0.12    # Mais espaço entre colunas
        )
        
        # Ajustar fonte dos títulos dos subplots
        for annotation in fig['layout']['annotations']:
            annotation['font'] = dict(size=14, color=self.cores['dark'])
        
        # =========================================================
        # GRÁFICO 1: Total por ano (barras)
        # =========================================================
        total_ano = self.df.groupby('ano')['ocorrencias'].sum().reset_index()
        fig.add_trace(
            go.Bar(
                x=total_ano['ano'],
                y=total_ano['ocorrencias'],
                marker=dict(color=self.cores['primary'], line=dict(width=1, color='white')),
                text=total_ano['ocorrencias'].apply(lambda x: f'{x:,.0f}'),
                textposition='outside',
                textfont=dict(size=11, color=self.cores['dark']),
                hovertemplate='<b>Ano: %{x}</b><br>Total: %{y:,.0f} ocorrências<extra></extra>'
            ),
            row=1, col=1
        )
        
        # =========================================================
        # GRÁFICO 2: Top 10 crimes (barras horizontais)
        # =========================================================
        top_crimes = self.df.groupby('natureza')['ocorrencias'].sum().nlargest(10).reset_index()
        fig.add_trace(
            go.Bar(
                x=top_crimes['ocorrencias'],
                y=top_crimes['natureza'],
                orientation='h',
                marker=dict(color=self.cores['secondary'], line=dict(width=1, color='white')),
                text=top_crimes['ocorrencias'].apply(lambda x: f'{x:,.0f}'),
                textposition='outside',
                textfont=dict(size=10),
                hovertemplate='<b>%{y}</b><br>Total: %{x:,.0f} ocorrências<extra></extra>'
            ),
            row=1, col=2
        )
        
        # =========================================================
        # GRÁFICO 3: Evolução top 5 crimes
        # =========================================================
        top5 = top_crimes['natureza'].head(5).tolist()
        cores_linhas = [self.cores['primary'], self.cores['secondary'], 
                        self.cores['success'], self.cores['danger'], self.cores['purple']]
        for i, crime in enumerate(top5):
            df_crime = self.df[self.df['natureza'] == crime].groupby('data')['ocorrencias'].sum().reset_index()
            fig.add_trace(
                go.Scatter(
                    x=df_crime['data'],
                    y=df_crime['ocorrencias'],
                    name=crime[:40],
                    mode='lines+markers',
                    line=dict(color=cores_linhas[i % len(cores_linhas)], width=2),
                    marker=dict(size=5),
                    hovertemplate='<b>%{x|%b %Y}</b><br>' + f'{crime[:30]}: %{{y:,.0f}}<extra></extra>'
                ),
                row=2, col=1
            )
        
        # =========================================================
        # GRÁFICO 4: Sazonalidade
        # =========================================================
        sazonalidade = self.df.groupby('mes_num')['ocorrencias'].mean().reset_index()
        cores_meses = [
            self.cores['danger'] if m in [12,1,2] else
            self.cores['success'] if m in [3,4,5] else
            self.cores['primary'] if m in [6,7,8] else
            self.cores['secondary'] for m in range(1,13)
        ]
        fig.add_trace(
            go.Bar(
                x=self.meses_nomes,
                y=sazonalidade['ocorrencias'],
                marker=dict(color=cores_meses, line=dict(width=1, color='white')),
                text=sazonalidade['ocorrencias'].round(0),
                textposition='outside',
                textfont=dict(size=11),
                hovertemplate='<b>%{x}</b><br>Média: %{y:.0f} ocorrências<extra></extra>'
            ),
            row=2, col=2
        )
        # Linha da média anual
        media_anual = sazonalidade['ocorrencias'].mean()
        fig.add_hline(y=media_anual, line_dash="dash", line_color=self.cores['gray'],
                      annotation_text=f"Média anual: {media_anual:.0f}",
                      annotation_position="top right", row=2, col=2)
        
        # =========================================================
        # GRÁFICO 5: Heatmap temporal
        # =========================================================
        matriz = self.df.groupby(['ano', 'mes_num'])['ocorrencias'].sum().unstack()
        fig.add_trace(
            go.Heatmap(
                z=matriz.values,
                x=self.meses_nomes,
                y=matriz.index,
                colorscale='Reds',
                hovertemplate='<b>Ano: %{y}</b><br><b>Mês: %{x}</b><br>Ocorrências: %{z:,.0f}<extra></extra>',
                colorbar=dict(title="Ocorrências")
            ),
            row=3, col=1
        )
        
        # =========================================================
        # GRÁFICO 6: Distribuição (histograma)
        # =========================================================
        fig.add_trace(
            go.Histogram(
                x=self.df['ocorrencias'],
                nbinsx=40,
                marker=dict(color=self.cores['purple'], line=dict(width=1, color='white')),
                opacity=0.8,
                hovertemplate='<b>Intervalo: %{x}</b><br>Frequência: %{y}<extra></extra>'
            ),
            row=3, col=2
        )
        
        # =========================================================
        # LAYOUT GERAL - Ajustes finos
        # =========================================================
        fig.update_layout(
            title=dict(
                text=f"<b>Dashboard de Criminalidade - Estado de São Paulo</b><br>" +
                     f"<sup>Período: {periodo_inicio} – {periodo_fim} | Total de ocorrências: {total_ocorrencias:,.0f}</sup>",
                font=dict(size=22, color=self.cores['dark']),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            height=1200,          # Altura maior para melhor espaçamento
            width=1400,           # Largura maior
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial, Helvetica, sans-serif", size=12),
            hoverlabel=dict(bgcolor="white", font_size=12),
            margin=dict(l=60, r=60, t=100, b=60)   # Margens externas generosas
        )
        
        # Estilo dos eixos (grid leve)
        grid_cor = '#e0e0e0'
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_cor, title_font=dict(size=12))
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_cor, title_font=dict(size=12))
        
        # Ajustes específicos por subplot (títulos de eixo)
        fig.update_xaxes(title_text="Ano", row=1, col=1)
        fig.update_xaxes(title_text="Total de Ocorrências", row=1, col=2)
        fig.update_xaxes(title_text="Data", row=2, col=1)
        fig.update_xaxes(title_text="Mês", row=2, col=2)
        fig.update_xaxes(title_text="Mês", row=3, col=1)
        fig.update_xaxes(title_text="Ocorrências", row=3, col=2)
        
        fig.update_yaxes(title_text="Ocorrências", row=1, col=1)
        fig.update_yaxes(title_text="Crime", row=1, col=2)
        fig.update_yaxes(title_text="Ocorrências", row=2, col=1)
        fig.update_yaxes(title_text="Ocorrências", row=2, col=2)
        fig.update_yaxes(title_text="Ano", row=3, col=1)
        fig.update_yaxes(title_text="Frequência", row=3, col=2)
        
        # =========================================================
        # HTML FINAL COM CARDS DE MÉTRICAS E LAYOUT LIMPO
        # =========================================================
        plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        html_completo = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Criminalidade - São Paulo</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5;
            padding: 30px 20px;
        }}
        .container {{
            max-width: 1500px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            padding: 24px 32px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            color: #475569;
            font-size: 14px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 10px;
        }}
        .metric-card {{
            background: #ffffff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            transition: all 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        .metric-card .value {{
            font-size: 32px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }}
        .metric-card .label {{
            font-size: 13px;
            font-weight: 500;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .metric-card.primary .value {{ color: #1a73e8; }}
        .metric-card.secondary .value {{ color: #e8710a; }}
        .metric-card.success .value {{ color: #0d7c3f; }}
        .metric-card.purple .value {{ color: #9334e6; }}
        .dashboard-wrapper {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            overflow-x: auto;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
            padding: 20px;
            border-top: 1px solid #e2e8f0;
        }}
        @media (max-width: 1000px) {{
            .metrics {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .card {{
                padding: 16px;
            }}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="card header">
        <h1>Análise da Criminalidade – Estado de São Paulo</h1>
        <div class="subtitle">
            Dados oficiais da Secretaria de Segurança Pública | Período: {periodo_inicio} – {periodo_fim} (dados até abril/2026)
        </div>
        <div class="metrics">
            <div class="metric-card primary">
                <div class="value">{total_ocorrencias:,.0f}</div>
                <div class="label">Total de Ocorrências</div>
            </div>
            <div class="metric-card secondary">
                <div class="value">{media_mensal:.0f}</div>
                <div class="label">Média Mensal</div>
            </div>
            <div class="metric-card success">
                <div class="value">{total_crimes}</div>
                <div class="label">Tipos de Crime</div>
            </div>
            <div class="metric-card purple">
                <div class="value">{total_crime_principal:,.0f}</div>
                <div class="label">Principal Crime</div>
            </div>
        </div>
    </div>
    <div class="dashboard-wrapper">
        {plot_html}
    </div>
    <div class="footer">
        <p>Desenvolvido por <strong>Isadora Meneghetti</strong> | Engenharia de Software – FIAP | Disciplina: Data Science and Statistical Computing</p>
        <p style="margin-top: 8px;">Fonte: Governo do Estado de São Paulo | Dashboard interativo – clique, arraste e explore</p>
    </div>
</div>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_completo)
        
        print(f"Dashboard formal salvo: {output_file}")
        print(f"Abra o arquivo no navegador para visualizar.")
        return fig