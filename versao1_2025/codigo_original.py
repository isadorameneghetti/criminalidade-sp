"""
================================================================================
PROJETO: ANALISE DE CRIMINALIDADE - ESTADO DE SAO PAULO
================================================================================
Autor: Isadora Meneghetti
Versao: 1.0
Data: 2025
Contexto: FIAP - Engenharia de Software - Data Science and Statistical Computing

Descricao:
    Esta e a primeira versao do projeto de analise de criminalidade.
    O codigo foi desenvolvido como trabalho para a disciplina, priorizando
    a obtencao dos resultados basicos. A estrutura reflete o aprendizado
    inicial da linguagem Python e das bibliotecas de ciencia de dados.
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

print("="*50)
print("ANALISE DE CRIMINALIDADE SP - VERSAO 1.0")
print("="*50)
print("Autora: Isadora Meneghetti")
print("FIAP - Engenharia de Software")
print("Disciplina: Data Science and Statistical Computing")
print("Ano: 2025")
print("="*50)

# =============================================================================
# CARREGAMENTO DOS DADOS
# =============================================================================

print("\n[1] CARREGAMENTO DOS DADOS")

arquivo = "OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx"

# Leitura das abas anuais
df_2023 = pd.read_excel(arquivo, sheet_name="2023")
df_2023['ano'] = 2023

df_2024 = pd.read_excel(arquivo, sheet_name="2024")
df_2024['ano'] = 2024

df_2025 = pd.read_excel(arquivo, sheet_name="2025")
df_2025['ano'] = 2025

df_2026 = pd.read_excel(arquivo, sheet_name="2026")
df_2026['ano'] = 2026

# Consolidacao
df_raw = pd.concat([df_2023, df_2024, df_2025, df_2026], ignore_index=True)
print(f"Registros carregados: {df_raw.shape[0]} linhas, {df_raw.shape[1]} colunas")

# =============================================================================
# PREPARACAO DOS DADOS
# =============================================================================

print("\n[2] PREPARACAO DOS DADOS")

# Remocao de linhas vazias
df_raw.dropna(how='all', inplace=True)

# Padronizacao dos nomes das colunas
df_raw.columns = df_raw.columns.str.lower().str.replace(' ', '_')

# Lista de meses
meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho',
         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

# Conversao para formato longo
registros = []

for idx in range(len(df_raw)):
    crime = df_raw.iloc[idx, 0]
    ano = df_raw.iloc[idx, -1]
    
    for i, mes in enumerate(meses):
        valor = df_raw.iloc[idx, i+1]
        if pd.notna(valor) and valor != '...':
            registros.append({
                'crime': crime,
                'ano': ano,
                'mes': i+1,
                'nome_mes': mes,
                'ocorrencias': float(valor)
            })

df_long = pd.DataFrame(registros)
print(f"Registros processados: {len(df_long)}")

# =============================================================================
# ESTATISTICAS DESCRITIVAS
# =============================================================================

print("\n[3] ESTATISTICAS DESCRITIVAS")

# Total por ano
total_ano = {}
anos = [2023, 2024, 2025, 2026]

for ano in anos:
    mask = df_long['ano'] == ano
    total_ano[ano] = df_long[mask]['ocorrencias'].sum()

print("\nTotal de ocorrencias por ano:")
for ano in anos:
    print(f"  {ano}: {total_ano[ano]:,.0f}")

# Grafico: Total por ano
plt.figure(figsize=(10, 6))
plt.bar(total_ano.keys(), total_ano.values(), color='steelblue', edgecolor='black')
plt.title('Total de Ocorrencias por Ano', fontsize=14)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Ocorrencias', fontsize=12)
plt.grid(axis='y', alpha=0.3)

for i, (ano, valor) in enumerate(total_ano.items()):
    plt.text(i, valor + 500, f'{valor:,.0f}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('output_ano.png', dpi=150)
plt.show()

# =============================================================================
# RANKING DE CRIMES
# =============================================================================

print("\n[4] RANKING DE CRIMES")

ranking = df_long.groupby('crime')['ocorrencias'].sum().sort_values(ascending=False)
top10 = ranking.head(10)

print("\nTop 10 crimes:")
for i, (crime, total) in enumerate(top10.items(), 1):
    print(f"  {i}. {crime}: {total:,.0f}")

# Grafico: Top 10
plt.figure(figsize=(12, 8))
plt.barh(range(len(top10)), top10.values, color='coral', edgecolor='black')
plt.yticks(range(len(top10)), top10.index, fontsize=9)
plt.xlabel('Total de Ocorrencias', fontsize=12)
plt.title('Top 10 Crimes - Periodo 2023-2026', fontsize=14)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('output_ranking.png', dpi=150)
plt.show()

# =============================================================================
# ANALISE DO CRIME PRINCIPAL
# =============================================================================

print("\n[5] ANALISE DO CRIME PRINCIPAL")

crime_principal = ranking.index[0]
print(f"Crime selecionado: {crime_principal}")

# Filtro para o crime principal
df_crime = df_long[df_long['crime'] == crime_principal].copy()
df_crime = df_crime.sort_values(['ano', 'mes'])

# Criacao de data para serie temporal
df_crime['data'] = pd.to_datetime(df_crime['ano'].astype(str) + '-' + 
                                   df_crime['mes'].astype(str) + '-01')

# Grafico da serie temporal
plt.figure(figsize=(14, 6))
plt.plot(df_crime['data'], df_crime['ocorrencias'], 'o-', markersize=5, linewidth=2)
plt.title(f'Evolucao Temporal - {crime_principal[:60]}', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Ocorrencias', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output_temporal.png', dpi=150)
plt.show()

# =============================================================================
# REGRESSAO LINEAR
# =============================================================================

print("\n[6] REGRESSAO LINEAR")

# Preparacao para regressao
X = np.arange(len(df_crime)).reshape(-1, 1)
y = df_crime['ocorrencias'].values

# Modelo
modelo = LinearRegression()
modelo.fit(X, y)
y_pred = modelo.predict(X)
r2 = modelo.score(X, y)

print(f"Coeficiente angular: {modelo.coef_[0]:+.2f} ocorrencias/mes")
print(f"Coeficiente R²: {r2:.3f}")

# Grafico com tendencia
plt.figure(figsize=(14, 6))
plt.plot(df_crime['data'], y, 'o-', label='Dados reais', markersize=5)
plt.plot(df_crime['data'], y_pred, '--', label=f'Tendencia linear (R²={r2:.3f})', 
         color='red', linewidth=2)
plt.title(f'Tendencia - {crime_principal[:60]}', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Ocorrencias', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output_tendencia.png', dpi=150)
plt.show()

# =============================================================================
# SAZONALIDADE
# =============================================================================

print("\n[7] SAZONALIDADE")

# Media por mes
sazonalidade = df_long.groupby('nome_mes')['ocorrencias'].mean()
ordem_meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho',
               'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
sazonalidade = sazonalidade.reindex(ordem_meses)

meses_abrev = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

print("\nMedia de ocorrencias por mes:")
for mes, media in sazonalidade.items():
    print(f"  {mes.capitalize()}: {media:.0f}")

# Grafico
plt.figure(figsize=(12, 6))
plt.bar(meses_abrev, sazonalidade.values, color='seagreen', edgecolor='black')
plt.title('Media de Ocorrencias por Mes', fontsize=14)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Media de Ocorrencias', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('output_sazonalidade.png', dpi=150)
plt.show()

# =============================================================================
# RESULTADOS
# =============================================================================

print("\n" + "="*50)
print("RESULTADOS DA ANALISE")
print("="*50)

print(f"\nTotal de ocorrencias no periodo: {sum(total_ano.values()):,.0f}")
print(f"Media mensal: {df_long['ocorrencias'].mean():.0f}")

print(f"\nCrime mais frequente: {crime_principal}")
print(f"  Total: {ranking.iloc[0]:,.0f} ocorrencias")
print(f"  Tendencia: {modelo.coef_[0]:+.2f} ocorrencias/mes")

mes_max = sazonalidade.idxmax()
mes_min = sazonalidade.idxmin()
print(f"\nMes com maior incidencia: {mes_max.capitalize()} ({sazonalidade[mes_max]:.0f})")
print(f"Mes com menor incidencia: {mes_min.capitalize()} ({sazonalidade[mes_min]:.0f})")

print("\nArquivos gerados:")
print("  - output_ano.png")
print("  - output_ranking.png")
print("  - output_temporal.png")
print("  - output_tendencia.png")
print("  - output_sazonalidade.png")

print("\n" + "="*50)
print("ANALISE CONCLUIDA")
print("="*50)