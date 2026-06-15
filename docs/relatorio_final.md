# RELATORIO FINAL DE ANALISE CRIMINAL
## Estado de Sao Paulo - Periodo 2023-2026

---

**Autora:** Isadora Meneghetti  
**Curso:** Engenharia de Software - FIAP  
**Disciplina:** Data Science and Statistical Computing  
**Versao:** 2.0 (Refatorada e Melhorada)  
**Data:** Junho 2026  

---

## SUMARIO

1. [Introducao](#1-introducao)
2. [Metodologia](#2-metodologia)
3. [Fonte dos Dados](#3-fonte-dos-dados)
4. [Analise Exploratoria](#4-analise-exploratoria)
5. [Ranking de Crimes](#5-ranking-de-crimes)
6. [Evolucao Temporal](#6-evolucao-temporal)
7. [Analise de Sazonalidade](#7-analise-de-sazonalidade)
8. [Deteccao de Outliers](#8-deteccao-de-outliers)
9. [Analise de Tendencias](#9-analise-de-tendencias)
10. [Previsoes](#10-previsoes)
11. [Decomposicao da Serie Temporal](#11-decomposicao-da-serie-temporal)
12. [Principais Insights](#12-principais-insights)
13. [Recomendacoes](#13-recomendacoes)
14. [Conclusao](#14-conclusao)
15. [Limitacoes](#15-limitacoes)
16. [Trabalhos Futuros](#16-trabalhos-futuros)
17. [Referencias](#17-referencias)

---

## 1. INTRODUCAO

### 1.1 Contexto

A criminalidade e um dos principais desafios enfrentados pela sociedade contemporanea, afetando diretamente a qualidade de vida da populacao, o desenvolvimento economico e a eficiencia dos orgaos de seguranca publica. O Estado de Sao Paulo, sendo o mais populoso e economicamente mais importante do Brasil, concentra uma parcela significativa dos registros criminais do pais.

Este relatorio apresenta os resultados da analise de dados de criminalidade do Estado de Sao Paulo, abrangendo o periodo de 2023 a 2026. O estudo foi realizado com o objetivo de identificar padroes, tendencias e anomalias nos registros criminais, fornecendo subsidios para gestores publicos, forcas de seguranca, pesquisadores e a sociedade em geral.

### 1.2 Objetivos

**Objetivo Geral:**
- Desenvolver uma analise completa e aprofundada dos dados de criminalidade do Estado de Sao Paulo

**Objetivos Especificos:**
- Identificar os crimes mais frequentes no estado
- Analisar a evolucao temporal da criminalidade ao longo dos anos
- Detectar padroes sazonais nos registros criminais
- Identificar picos anormais (outliers) na serie temporal
- Gerar previsoes para os proximos 12 meses
- Fornecer recomendacoes baseadas em dados para orgaos de seguranca

### 1.3 Escopo

A analise contempla:
- Periodo: Janeiro de 2023 a Abril de 2026
- Tipos de crime: 23 categorias distintas
- Dados mensais desagregados por tipo de crime
- Analises estatisticas e graficas

---

## 2. METODOLOGIA

### 2.1 Abordagem Geral

O projeto seguiu uma abordagem estruturada de Ciencia de Dados, compreendendo as seguintes etapas:

| Etapa | Descricao |
|-------|-----------|
| Coleta de Dados | Importacao dos dados do arquivo Excel |
| Limpeza e Preprocessamento | Tratamento de valores ausentes, padronizacao |
| Analise Exploratoria | Estatisticas descritivas e visualizacoes iniciais |
| Analise Avancada | Modelagem de tendencias, deteccao de outliers |
| Geracao de Insights | Interpretacao dos resultados |

### 2.2 Ferramentas Utilizadas

| Categoria | Tecnologia | Finalidade |
|-----------|------------|------------|
| Linguagem | Python 3.9+ | Desenvolvimento do codigo |
| Manipulacao de Dados | Pandas, NumPy | Limpeza, transformacao e analise |
| Visualizacao | Matplotlib, Seaborn, Plotly | Graficos estaticos e interativos |
| Machine Learning | Scikit-learn | Regressao linear e polinomial |
| Estatistica | Scipy, Statsmodels | Testes estatisticos, Holt-Winters |

### 2.3 Tecnicas Utilizadas

#### 2.3.1 Regressao Linear
Utilizada para identificar tendencias de crescimento ou queda ao longo do tempo. O modelo assume uma relacao linear entre o tempo e o numero de ocorrencias.

#### 2.3.2 Regressao Polinomial (Grau 2)
Captura tendencias nao-lineares, como crescimento acelerado ou desaceleracao gradual.

#### 2.3.3 Modelo Holt-Winters
Modelo de previsao especifico para series temporais com:
- Tendencia (crescimento ou queda de longo prazo)
- Sazonalidade (padroes que se repetem anualmente)

#### 2.3.4 Decomposicao de Series Temporais
Separa a serie em tres componentes:
- **Tendencia:** Movimento de longo prazo
- **Sazonalidade:** Padrao que se repete anualmente
- **Residuo:** Variacao aleatoria (ruido)

#### 2.3.5 Deteccao de Outliers
- **IQR (Intervalo Interquartil):** Identifica valores fora de Q1-3*IQR ou Q3+3*IQR
- **Z-score:** Identifica valores com mais de 3 desvios padrao da media

---

## 3. FONTE DOS DADOS

### 3.1 Origem

Os dados utilizados neste projeto sao provenientes do **Governo do Estado de Sao Paulo**, disponibilizados publicamente pela Secretaria de Seguranca Publica.

### 3.2 Estrutura dos Dados

| Caracteristica | Descricao |
|----------------|-----------|
| Abas | 4 (2023, 2024, 2025, 2026) |
| Linhas por aba | 23 (tipos de crime) |
| Colunas | Natureza, Janeiro a Dezembro, Total |
| Total de registros apos processamento | 920 |

### 3.3 Tipos de Crime Analisados

1. HOMICIDIO DOLOSO
2. NUMERO DE VITIMAS EM HOMICIDIO DOLOSO
3. HOMICIDIO DOLOSO POR ACIDENTE DE TRANSITO
4. NUMERO DE VITIMAS EM HOMICIDIO DOLOSO POR ACIDENTE DE TRANSITO
5. HOMICIDIO CULPOSO POR ACIDENTE DE TRANSITO
6. HOMICIDIO CULPOSO OUTROS
7. TENTATIVA DE HOMICIDIO
8. LESAO CORPORAL SEGUIDA DE MORTE
9. LESAO CORPORAL DOLOSA
10. LESAO CORPORAL CULPOSA POR ACIDENTE DE TRANSITO
11. LESAO CORPORAL CULPOSA - OUTRAS
12. LATROCINIO
13. NUMERO DE VITIMAS EM LATROCINIO
14. TOTAL DE ESTUPRO
15. ESTUPRO
16. ESTUPRO DE VULNERAVEL
17. TOTAL DE ROUBO - OUTROS
18. ROUBO - OUTROS
19. ROUBO DE VEICULO
20. ROUBO A BANCO
21. ROUBO DE CARGA
22. FURTO - OUTROS
23. FURTO DE VEICULO

---

## 4. ANALISE EXPLORATORIA

### 4.1 Panorama Geral

| Indicador | Valor |
|-----------|-------|
| Periodo analisado | 2023 a 2026 (ate abril) |
| Total de ocorrencias | 114.454 |
| Media mensal | 136 |
| Tipos de crime | 23 |

### 4.2 Distribuicao dos Dados

A distribuicao das ocorrencias apresenta uma concentracao em valores baixos a medios, com alguns picos elevados correspondendo aos crimes mais frequentes (estupro de vulneravel e roubo de carga).

---

## 5. RANKING DE CRIMES

### 5.1 Top 10 Crimes (Periodo Completo)

| Ranking | Crime | Total | Percentual |
|---------|-------|-------|-------------|
| 1 | ESTUPRO DE VULNERAVEL | 27.902 | 24,4% |
| 2 | ROUBO DE CARGA | 15.111 | 13,2% |
| 3 | HOMICIDIO CULPOSO POR ACIDENTE DE TRANSITO | 13.046 | 11,4% |
| 4 | TENTATIVA DE HOMICIDIO | 12.291 | 10,7% |
| 5 | ESTUPRO | 11.419 | 10,0% |
| 6 | LESAO CORPORAL DOLOSA | 9.847 | 8,6% |
| 7 | HOMICIDIO DOLOSO | 8.908 | 7,8% |
| 8 | NUMERO DE VITIMAS EM HOMICIDIO DOLOSO | 8.696 | 7,6% |
| 9 | FURTO - OUTROS | 5.478 | 4,8% |
| 10 | ROUBO - OUTROS | 1.210 | 1,1% |

### 5.2 Analise do Ranking

**Principais Observacoes:**

1. **ESTUPRO DE VULNERAVEL** e o crime mais frequente, representando quase um quarto de todas as ocorrencias (24,4%). Este dado e particularmente alarmante, pois envolve vitimas vulneraveis (criancas, idosos, pessoas com deficiencia).

2. **ROUBO DE CARGA** ocupa a segunda posicao (13,2%), refletindo a importância economica do estado e os desafios logisticos enfrentados pelo setor de transporte.

3. **HOMICIDIO CULPOSO POR ACIDENTE DE TRANSITO** e o terceiro crime mais frequente (11,4%), indicando a gravidade dos acidentes de transito no estado.

4. Os **crimes violentos** (homicidios, tentativas, lesoes) aparecem com frequencia no topo do ranking.

---

## 6. EVOLUCAO TEMPORAL

### 6.1 Total de Ocorrencias por Ano

| Ano | Total | Variacao |
|-----|-------|----------|
| 2023 | 27.825 | - |
| 2024 | 28.076 | +0,9% |
| 2025 | 26.332 | -6,2% |
| 2026* | 32.221 | +22,4%* |

*Dados parciais (apenas 4 meses)

### 6.2 Analise da Evolucao

**Principais Observacoes:**

1. **Estabilidade entre 2023 e 2024:** Pequeno crescimento de 0,9%, sugerindo relativa estabilidade na criminalidade.

2. **Queda em 2025:** Reducao de 6,2% em relacao ao ano anterior. Possiveis causas incluem aumento do efetivo policial, implementacao de novas tecnologias de monitoramento e fatores socioeconomicos.

3. **Aumento em 2026:** Os primeiros 4 meses de 2026 ja registram 32.221 ocorrencias, um aumento significativo. Este dado deve ser interpretado com cautela, pois o ano esta incompleto.

---

## 7. ANALISE DE SAZONALIDADE

### 7.1 Media de Ocorrencias por Mes

| Mes | Media | Variacao vs Media Anual |
|-----|-------|------------------------|
| Janeiro | 126 | -7,4% |
| Fevereiro | 123 | -9,6% |
| Marco | 110 | -19,1% |
| Abril | 119 | -12,5% |
| Maio | 124 | -8,8% |
| Junho | 122 | -10,3% |
| Julho | 128 | -5,9% |
| Agosto | 131 | -3,7% |
| Setembro | 130 | -4,4% |
| Outubro | 131 | -3,7% |
| Novembro | 131 | -3,7% |
| Dezembro | 136 | 0,0% |

### 7.2 Analise da Sazonalidade

**Principais Observacoes:**

1. **Dezembro e o mes com maior incidencia** (136 ocorrencias), com variacao positiva em relacao a media.

2. **Marco e o mes com menor incidencia** (110 ocorrencias), com variacao negativa de -19,1%.

3. **Padrao observado:**
   - Queda nos meses de Marco a Junho
   - Aumento gradual a partir de Julho
   - Pico em Dezembro

4. **Variacao total:** 24,1% entre o mes de pico (Dezembro) e o mes de vale (Marco).

---

## 8. DETECCAO DE OUTLIERS

### 8.1 Metodologia

Foram aplicados dois metodos complementares para deteccao de outliers:
- **IQR (Intervalo Interquartil):** Mais robusto para distribuicoes assimetricas
- **Z-score:** Baseado em desvios padrao da media

### 8.2 Resultados

| Metodo | Outliers Detectados | Observacao |
|--------|--------------------|------------|
| IQR | 0 | Nenhum outlier significativo |
| Z-score | 0 | Nenhum outlier significativo |

### 8.3 Analise

A ausencia de outliers significativos indica que:
1. Os dados sao consistentes ao longo do periodo
2. Nao ha picos anormais que indiquem eventos extraordinarios
3. As variacoes observadas estao dentro do padrao esperado

---

## 9. ANALISE DE TENDENCIAS

### 9.1 Crime Principal: ESTUPRO DE VULNERAVEL

**Resultados da Regressao Linear:**

| Indicador | Valor |
|-----------|-------|
| R² (Coeficiente de Determinacao) | 0,004 |
| Tendencia mensal | -2,03 ocorrencias/mes |
| Projecao anual | -24 ocorrencias/ano |

### 9.2 Modelos Comparados

| Modelo | R² | Vantagem |
|--------|-----|----------|
| Linear | 0,004 | Simples, interpretavel |
| Polinomial | 0,068 | Captura nao-linearidades |
| Media Movel | - | Suavizacao do ruido |

**Melhor Modelo:** Polinomial (R² ligeiramente superior)

### 9.3 Interpretacao

- O R² de 0,004 (linear) indica uma correlacao muito fraca entre o tempo e as ocorrencias.
- O modelo polinomial (R²=0,068) apresenta desempenho ligeiramente melhor.
- A tendencia negativa sugere uma leve queda no numero de ocorrencias.
- No entanto, a baixa confiabilidade dos modelos indica que outros fatores (economicos, sociais, operacionais) tem maior poder explicativo.

---

## 10. PREVISOES

### 10.1 Modelo Holt-Winters

O modelo Holt-Winters foi aplicado considerando:
- Tendencia aditiva
- Sazonalidade anual (12 meses)
- Intervalo de confianca de 95%

### 10.2 Previsao para ESTUPRO DE VULNERAVEL

| Mes/Ano | Previsao (ponto) |
|---------|-----------------|
| Maio 2026 | 580 |
| Junho 2026 | 831 |
| Julho 2026 | 832 |
| Agosto 2026 | 601 |
| Setembro 2026 | 275 |
| Outubro 2026 | 603 |
| Novembro 2026 | 603 |
| Dezembro 2026 | 603 |

### 10.3 AIC do Modelo

O AIC (Akaike Information Criterion) do modelo Holt-Winters foi de **489,9**, indicando um ajuste razoavel.

---

## 11. DECOMPOSICAO DA SERIE TEMPORAL

### 11.1 Componentes da Serie para ESTUPRO DE VULNERAVEL

| Componente | Percentual da Variancia |
|------------|------------------------|
| Tendencia | 2,7% |
| Sazonalidade | 26,9% |
| Ruido | 52,6% |

### 11.2 Analise da Decomposicao

- **Sazonalidade explica 26,9%** da variacao dos dados, confirmando que ha um padrao anual relevante.
- **Ruido explica 52,6%** da variacao, indicando que fatores aleatorios ou nao modelados tem grande influencia.
- **Tendencia explica apenas 2,7%** da variacao, confirmando que nao ha uma direcao clara de longo prazo.

---

## 12. PRINCIPAIS INSIGHTS

### 12.1 Insight 1: Concentracao da Criminalidade

**Descoberta:** O crime "ESTUPRO DE VULNERAVEL" sozinho representa 24,4% de todas as ocorrencias registradas.

**Implicacao:** Politicas publicas de prevencao devem priorizar a protecao de grupos vulneraveis.

### 12.2 Insight 2: Sazonalidade Definida

**Descoberta:** Dezembro apresenta o maior indice criminal, enquanto Marco apresenta o menor. A variacao entre o mes de pico e o mes de vale e de 24,1%.

**Implicacao:** Recursos de seguranca podem ser alocados de forma mais eficiente, com reforco no final do ano e possivel realocacao no primeiro trimestre.

### 12.3 Insight 3: Queda na Criminalidade em 2025

**Descoberta:** Houve uma reducao de 6,2% no total de ocorrencias entre 2024 e 2025.

**Implicacao:** Investigar as causas dessa reducao (politicas publicas, mudancas socioeconomicas, operacoes policiais) pode fornecer aprendizados para futuras intervencoes.

### 12.4 Insight 4: Ausencia de Outliers Significativos

**Descoberta:** Nenhum outlier significativo foi detectado na serie temporal.

**Implicacao:** Os dados sao consistentes e nao ha eventos extraordinarios distorcendo a analise. As variacoes observadas sao padrao.

### 12.5 Insight 5: Fraca Correlacao Temporal

**Descoberta:** O modelo de tendencia para o crime principal apresentou R² de apenas 0,004, indicando que o tempo sozinho nao explica as variacoes nas ocorrencias.

**Implicacao:** Fatores adicionais (economia, clima, operacoes policiais) devem ser incorporados para melhor compreensao da dinamica criminal.

### 12.6 Insight 6: Ruido Predomina na Serie

**Descoberta:** O componente de ruido explica 52,6% da variacao da serie do crime principal.

**Implicacao:** Ha uma grande variabilidade aleatoria nos dados, o que torna previsoes precisas desafiadoras.

---

## 13. RECOMENDACOES

### 13.1 Acao Imediata

| Prioridade | Acao | Justificativa |
|------------|------|---------------|
| Alta | Reforcar policiamento nos meses de Dezembro e Janeiro | Sazonalidade indica pico no final do ano |
| Alta | Intensificar campanhas de prevencao ao estupro de vulneraveis | Crime mais frequente (24,4% do total) |
| Media | Investigar causas da queda em 2025 para replicar boas praticas | Reducao de 6,2% no periodo |

### 13.2 Medio Prazo

| Acao | Descricao |
|------|-----------|
| Implementar sistema de alerta precoce | Baseado nos padroes sazonais identificados |
| Desenvolver politicas integradas | Crimes correlacionados devem ser tratados em conjunto |
| Criar comite de monitoramento de tendencias | Acompanhamento mensal dos indicadores |

### 13.3 Longo Prazo

| Acao | Descricao |
|------|-----------|
| Estabelecer observatorio criminal permanente | Coleta continua de dados, analises regulares |
| Investir em tecnologias de analise preditiva | Modelos de machine learning para previsao |
| Desenvolver politicas publicas baseadas em evidencias | Utilizar os insights gerados para orientar decisoes |

---

## 14. CONCLUSAO

### 14.1 Resumo dos Principais Resultados

Este estudo analisou os dados de criminalidade do Estado de Sao Paulo entre 2023 e 2026, totalizando 114.454 ocorrencias distribuidas em 23 tipos de crime.

As principais conclusoes sao:

1. **O crime de ESTUPRO DE VULNERAVEL e o mais frequente**, representando quase um quarto de todas as ocorrencias. Este dado requer atencao especial de politicas publicas.

2. **A criminalidade apresenta sazonalidade definida**, com pico em Dezembro e vale em Marco. A variacao entre o mes de maior e menor incidencia e de 24,1%.

3. **Houve uma reducao de 6,2% na criminalidade entre 2024 e 2025**, indicando possivel eficacia de politicas implementadas no periodo.

4. **Nao foram detectados outliers significativos**, sugerindo consistencia nos dados e ausencia de eventos extraordinarios.

5. **O modelo de tendencia apresentou baixa correlacao (R²=0,004)** para o crime principal, indicando que outros fatores alem do tempo influenciam a criminalidade.

6. **O ruido explica 52,6% da variacao** da serie temporal, tornando previsoes precisas desafiadoras.

### 14.2 Contribuicoes do Projeto

- Dashboard interativo para exploracao dos dados
- Relatorio executivo em Markdown e PDF
- Analise de tendencias com multiplos modelos
- Deteccao robusta de outliers
- Previsoes sazonais com Holt-Winters
- Decomposicao da serie temporal

---

## 15. LIMITACOES

### 15.1 Dados

| Limitacao | Descricao |
|-----------|-----------|
| Subnotificacao | Os dados oficiais podem subestimar a criminalidade real |
| Periodo limitado | 4 anos podem nao ser suficientes para tendencias de longo prazo |
| Dados parciais em 2026 | Apenas os primeiros 4 meses estao disponiveis |

### 15.2 Analise

| Limitacao | Descricao |
|-----------|-----------|
| Fatores externos | Nao foram consideradas variaveis como desemprego, renda, escolaridade |
| Mudancas legislativas | Alteracoes nas leis podem afetar a comparabilidade |
| Falta de dados geograficos | Analise agregada por estado, sem detalhamento municipal |

### 15.3 Tecnicas

| Limitacao | Descricao |
|-----------|-----------|
| Modelos simples | Foram utilizados modelos classicos, nao redes neurais |
| Pressupostos estatisticos | Os modelos lineares assumem pressupostos que podem nao ser atendidos |

---

## 16. TRABALHOS FUTUROS

### 16.1 Expansao da Analise

| Area | Descricao |
|------|-----------|
| Variaveis socioeconomicas | Incorporar desemprego, renda per capita, escolaridade |
| Analise por municipio | Identificar regioes com maior incidencia |
| Modelos avancados | Redes neurais (LSTM), Random Forest, modelos Bayesianos |

### 16.2 Produtos

| Produto | Descricao |
|---------|-----------|
| API de previsao criminal | Endpoint para consulta de previsoes |
| Monitor em tempo real | Dashboard atualizado automaticamente |
| Aplicativo movel | Para cidadaos e orgaos publicos |

---

## 17. REFERENCIAS

### 17.1 Bibliograficas

1. HYNDMAN, R. J.; ATHANASOPOULOS, G. *Forecasting: Principles and Practice*. 3rd ed. OTexts, 2021.

2. JAMES, G. et al. *An Introduction to Statistical Learning*. Springer, 2013.

3. MCKINNEY, W. *Python for Data Analysis*. O'Reilly Media, 2017.

### 17.2 Documentacao Tecnica

- Pandas Documentation: https://pandas.pydata.org/
- Scikit-learn Documentation: https://scikit-learn.org/
- Plotly Documentation: https://plotly.com/python/
- Statsmodels Documentation: https://www.statsmodels.org/

### 17.3 Fontes dos Dados

- Secretaria de Seguranca Publica do Estado de Sao Paulo
- Governo do Estado de Sao Paulo - Dados Abertos

---

## ANEXOS

### A. Glossario

| Termo | Definicao |
|-------|-----------|
| Outlier | Valor que se desvia significativamente do padrao esperado |
| Sazonalidade | Padrao que se repete em intervalos regulares (ex: anual) |
| R² | Coeficiente de determinacao - mede qualidade do ajuste (0 a 1) |
| IQR | Intervalo Interquartil - medida de dispersao estatistica |
| Z-score | Numero de desvios padrao em relacao a media |
| Holt-Winters | Modelo de previsao para series com tendencia e sazonalidade |
| AIC | Akaike Information Criterion - medida de qualidade do modelo |

### B. Estrutura do Projeto

```
criminalidade_sp/
├── data/
│   ├── raw/                    # Dados brutos
│   └── processed/              # Dados processados
├── outputs/
│   ├── graficos/               # Graficos gerados
│   ├── relatorio/              # PDF e Markdown
│   └── dashboard/              # Dashboard interativo
├── src/
│   └── modules/
│       ├── data_loader.py
│       ├── trend_analysis.py
│       ├── dashboard.py
│       └── analise_criminalidade.py
├── tests/
│   └── test_limpeza.py
├── docs/
│   └── relatorio_final.md
├── versao1_2025/
│   └── codigo_original.py
├── main.py
├── requirements.txt
└── README.md
```

### C. Como Reproduzir

```bash
# 1. Clone o repositorio
git clone https://github.com/isadorameneghetti/criminalidade-sp.git

# 2. Instale as dependencias
pip install -r requirements.txt

# 3. Execute a analise
python main.py

# 4. Abra o dashboard
start outputs/dashboard/dashboard_criminalidade.html
```

---

**Fim do Relatorio**

---

*Relatorio gerado em Junho de 2026*  
*Isadora Meneghetti - Engenharia de Software - FIAP*  
*Data Science and Statistical Computing*
