"""
===============================================================================
MODULO: ANALISE CRIMINALIDADE - ORQUESTRACAO PRINCIPAL
===============================================================================
Autor: Isadora Meneghetti
Versao: 2.0
Data: Junho 2026
Contexto: FIAP - Engenharia de Software - Data Science and Statistical Computing
===============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from .data_loader import DataLoader
from .trend_analysis import TrendAnalyzer
from .dashboard import DashboardCriminalidade

# Configuracoes profissionais para graficos
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 100

class AnaliseCriminalidadeSP:
    """
    Classe principal para analise completa de criminalidade.
    """
    
    def __init__(self, file_path):
        """
        Inicializa a analise com o caminho do arquivo.
        """
        self.file_path = file_path
        self.data_loader = DataLoader(file_path)
        self.df_processed = None
        self.trend_analyzer = TrendAnalyzer()
        self.dashboard = None
        self._criar_diretorios()
    
    def _criar_diretorios(self):
        """Cria a estrutura de diretorios necessaria."""
        diretorios = [
            'data/processed',
            'outputs/graficos',
            'outputs/relatorio',
            'outputs/dashboard'
        ]
        for diretorio in diretorios:
            Path(diretorio).mkdir(parents=True, exist_ok=True)
    
    def _get_crime_principal(self):
        """Identifica o crime com maior numero de ocorrencias."""
        ranking = self.df_processed.groupby('natureza')['ocorrencias'].sum().sort_values(ascending=False)
        return ranking.index[0] if not ranking.empty else None
    
    def carregar_e_preparar_dados(self):
        """Carrega e prepara os dados para analise."""
        self.data_loader.carregar_dados()
        self.df_processed = self.data_loader.limpar_dados()
        self.data_loader.salvar_dados_processados("data/processed/dados_processados.csv")
        self.dashboard = DashboardCriminalidade(self.df_processed)
        return self
    
    def ranking_crimes(self, ano=None, top_n=10, salvar_csv=True):
        """Gera ranking de crimes por total de ocorrencias."""
        if ano:
            df_filtrado = self.df_processed[self.df_processed['ano'] == ano]
            titulo = f"Ranking de Crimes - {ano}"
            filename = f"ranking_crimes_{ano}.csv"
        else:
            df_filtrado = self.df_processed
            titulo = "Ranking de Crimes - Todos os Anos"
            filename = "ranking_crimes_completo.csv"
        
        ranking = df_filtrado.groupby('natureza')['ocorrencias'].sum().sort_values(ascending=False).head(top_n)
        
        # Criar grafico
        fig, ax = plt.subplots(figsize=(12, 8))
        cores = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(ranking)))
        bars = ax.barh(range(len(ranking)), ranking.values, color=cores)
        ax.set_yticks(range(len(ranking)))
        ax.set_yticklabels(ranking.index, fontsize=9)
        ax.set_xlabel('Total de ocorrencias', fontsize=12)
        ax.set_title(titulo, fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        for i, (bar, valor) in enumerate(zip(bars, ranking.values)):
            ax.text(valor + ranking.max()*0.01, bar.get_y() + bar.get_height()/2, 
                   f'{valor:,.0f}', va='center', fontsize=9)
        
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        save_path = f"outputs/graficos/{filename.replace('.csv', '.png')}"
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()
        
        if salvar_csv:
            ranking.to_csv(f"outputs/relatorio/{filename}", encoding='utf-8-sig')
            print(f"Ranking salvo em: outputs/relatorio/{filename}")
        
        return ranking
    
    def analise_avancada_completa(self):
        """Executa analises avancadas para o crime principal."""
        crime_principal = self._get_crime_principal()
        
        if not crime_principal:
            print("Nenhum crime encontrado")
            return
        
        print("\n" + "="*60)
        print(f" ANALISE AVANCADA: {crime_principal}")
        print("="*60)
        
        print("\n1. ANALISE DE TENDENCIA AVANCADA")
        resultado_tendencia = self.trend_analyzer.analisar_tendencia_avancada(
            self.df_processed, crime_principal,
            save_path=f"outputs/graficos/tendencia_{crime_principal[:30].replace(' ', '_')}"
        )
        
        print("\n2. PREVISAO SAZONAL (HOLT-WINTERS)")
        resultado_previsao = self.trend_analyzer.previsao_sazonal_holtwinters(
            self.df_processed, crime_principal, periodo_previsao=12,
            save_path=f"outputs/graficos/previsao_{crime_principal[:30].replace(' ', '_')}"
        )
        
        print("\n3. DECOMPOSICAO DA SERIE TEMPORAL")
        resultado_decomposicao = self.trend_analyzer.decompor_serie_temporal(
            self.df_processed, crime_principal,
            save_path=f"outputs/graficos/decomposicao_{crime_principal[:30].replace(' ', '_')}"
        )
        
        return {
            'crime': crime_principal,
            'tendencia': resultado_tendencia,
            'previsao': resultado_previsao,
            'decomposicao': resultado_decomposicao
        }
    
    def gerar_relatorio_markdown(self, output_file="outputs/relatorio/relatorio_executivo.md"):
        """Gera relatorio executivo em formato Markdown."""
        
        total_ano = self.df_processed.groupby('ano')['ocorrencias'].sum()
        crescimento = total_ano.pct_change() * 100
        ranking_geral = self.df_processed.groupby('natureza')['ocorrencias'].sum().nlargest(10)
        sazonalidade = self.df_processed.groupby('mes_num')['ocorrencias'].mean()
        
        meses_nomes = ['Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        media_total = sazonalidade.mean()
        total_geral = self.df_processed['ocorrencias'].sum()
        
        relatorio = f"""# RELATORIO EXECUTIVO - CRIMINALIDADE EM SAO PAULO

## Dados Gerais
| Indicador | Valor |
|-----------|-------|
| Periodo analisado | {self.df_processed['data'].min().year} a {self.df_processed['data'].max().year} |
| Total de ocorrencias | {total_geral:,.0f} |
| Media mensal | {self.df_processed['ocorrencias'].mean():,.0f} |
| Tipos de crime | {self.df_processed['natureza'].nunique()} |

## Top 10 Crimes
| Ranking | Crime | Total | Percentual |
|---------|-------|-------|------------|
"""
        for i, (crime, total) in enumerate(ranking_geral.items(), 1):
            pct = (total / total_geral) * 100
            relatorio += f"| {i} | {crime[:50]} | {total:,.0f} | {pct:.1f}% |\n"
        
        relatorio += f"""
## Evolucao Anual
| Ano | Total | Variacao |
|-----|-------|----------|
"""
        for ano in sorted(total_ano.index):
            var = crescimento.get(ano, 0)
            sinal = "+" if var > 0 else ""
            relatorio += f"| {ano} | {total_ano[ano]:,.0f} | {sinal}{var:.1f}% |\n"
        
        relatorio += f"""
## Sazonalidade
| Mes | Media | Variacao vs Media |
|-----|-------|-------------------|
"""
        for mes_num in range(1, 13):
            media = sazonalidade.get(mes_num, 0)
            variacao = ((media - media_total) / media_total * 100) if media_total > 0 else 0
            sinal = "+" if variacao > 0 else ""
            relatorio += f"| {meses_nomes[mes_num-1]} | {media:.0f} | {sinal}{variacao:.1f}% |\n"
        
        relatorio += f"""
## Recomendacoes
1. Reforcar policiamento nos meses de maior incidencia
2. Investigar causas do crime mais frequente
3. Monitorar tendencias de crescimento

---
*Relatorio gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        print(f"Relatorio Markdown salvo: {output_file}")
        return output_file
    
    def gerar_relatorio_pdf(self, output_file="outputs/relatorio/relatorio_criminalidade_sp.pdf"):
        """Gera relatorio completo em PDF."""
        from matplotlib.backends.backend_pdf import PdfPages
        
        print(f"\nGerando relatorio PDF: {output_file}")
        ranking_all = self.ranking_crimes(ano=None, top_n=15, salvar_csv=False)
        
        with PdfPages(output_file) as pdf:
            # Capa
            fig_capa = plt.figure(figsize=(11.69, 8.27))
            fig_capa.text(0.5, 0.7, 'RELATORIO DE ANALISE CRIMINAL', 
                         fontsize=28, ha='center', fontweight='bold')
            fig_capa.text(0.5, 0.6, 'Estado de Sao Paulo', fontsize=20, ha='center')
            fig_capa.text(0.5, 0.5, f'Periodo: {self.df_processed["data"].min().year} a {self.df_processed["data"].max().year}', 
                         fontsize=16, ha='center')
            fig_capa.text(0.5, 0.4, f'Data: {datetime.now().strftime("%d/%m/%Y")}', 
                         fontsize=12, ha='center')
            pdf.savefig(fig_capa)
            plt.close()
            
            # Ranking
            fig_rank, ax = plt.subplots(figsize=(11.69, 8.27))
            ax.barh(range(len(ranking_all)), ranking_all.values, color='steelblue')
            ax.set_yticks(range(len(ranking_all)))
            ax.set_yticklabels(ranking_all.index, fontsize=8)
            ax.set_xlabel('Total de ocorrencias')
            ax.set_title('Ranking Geral de Crimes')
            ax.invert_yaxis()
            pdf.savefig(fig_rank)
            plt.close()
        
        print(f"Relatorio PDF gerado: {output_file}")
        return output_file
    
    def executar_analise_completa(self):
        """Executa todas as etapas da analise."""
        print("INICIANDO ANALISE COMPLETA DE CRIMINALIDADE - VERSAO 2.0")
        print("="*60)
        print("Autora: Isadora Meneghetti")
        print("FIAP - Engenharia de Software")
        print("Disciplina: Data Science and Statistical Computing")
        print("="*60)
        
        self.carregar_e_preparar_dados()
        
        print("\n=== ANALISES PRINCIPAIS ===")
        self.ranking_crimes(ano=2025, top_n=10)
        self.ranking_crimes(ano=None, top_n=15)
        
        print("\n=== CRIANDO DASHBOARD INTERATIVO ===")
        self.dashboard.criar_dashboard_completo()
        
        print("\n=== ANALISE AVANCADA ===")
        self.analise_avancada_completa()
        
        print("\n=== DETECCAO DE OUTLIERS ===")
        self.trend_analyzer.detectar_outliers(
            self.df_processed, crime_name=None,
            save_path="outputs/graficos/outliers_total_geral.png"
        )
        
        print("\n=== GERANDO RELATORIOS ===")
        self.gerar_relatorio_markdown()
        self.gerar_relatorio_pdf()
        
        print("\n" + "="*60)
        print("ANALISE CONCLUIDA COM SUCESSO")
        print("="*60)
        print("\nArquivos gerados:")
        print("  - outputs/dashboard/dashboard_criminalidade.html")
        print("  - outputs/relatorio/relatorio_executivo.md")
        print("  - outputs/relatorio/relatorio_criminalidade_sp.pdf")
        print("  - outputs/graficos/")
        print("  - data/processed/dados_processados.csv")