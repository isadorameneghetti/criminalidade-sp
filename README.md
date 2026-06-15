
# Análise da Criminalidade no Estado de São Paulo

**Autora:** Isadora Meneghetti  
**Versão:** 2.0 (2026)  
**Curso:** Engenharia de Software – FIAP  
**Disciplina:** Data Science and Statistical Computing  
**Repositório:** [github.com/isadorameneghetti/criminalidade-sp](https://github.com/isadorameneghetti/criminalidade-sp)

---

## 1. Apresentação do Projeto

Este projeto consiste na análise exploratória e estatística de dados públicos de criminalidade do Estado de São Paulo, abrangendo o período de 2023 a 2026 (parcial). Os dados foram disponibilizados pela Secretaria de Segurança Pública do Estado de São Paulo.

O trabalho foi desenvolvido originalmente em 2025 como atividade acadêmica da disciplina *Data Science and Statistical Computing*. Em 2026, o código foi completamente refatorado, adotando boas práticas de engenharia de software, modularização, testes automatizados e técnicas avançadas de análise de séries temporais.

### 1.1 Objetivos

- Identificar os tipos de crime mais frequentes no estado.
- Analisar a evolução temporal da criminalidade.
- Detectar padrões sazonais e tendências.
- Identificar outliers e anomalias.
- Gerar previsões de curto prazo usando modelos estatísticos.
- Produzir relatórios automáticos (PDF, Markdown) e um dashboard interativo.

### 1.2 Tecnologias Utilizadas

| Ferramenta | Finalidade |
|------------|------------|
| Python 3.9+ | Linguagem principal |
| Pandas / NumPy | Manipulação e processamento de dados |
| Matplotlib / Seaborn | Visualização estática |
| Plotly | Dashboard interativo |
| Scikit-learn | Regressão linear e polinomial |
| SciPy / Statsmodels | Testes estatísticos, Holt-Winters, decomposição sazonal |
| Pytest | Testes unitários |
| Openpyxl | Leitura de arquivos Excel |

---

## 2. Metodologia e Estrutura do Projeto

### 2.1 Organização dos diretórios

```
criminalidade-sp/
├── data/
│   ├── raw/                     # Dados originais (Excel)
│   └── processed/               # Dados limpos (CSV)
├── outputs/
│   ├── graficos/                # Gráficos estáticos (PNG)
│   ├── relatorio/               # PDF, Markdown e CSVs de ranking
│   └── dashboard/               # Dashboard HTML interativo
├── src/modules/
│   ├── data_loader.py           # Carga e limpeza
│   ├── trend_analysis.py        # Tendências, outliers, previsões
│   ├── dashboard.py             # Construção do dashboard
│   └── analise_criminalidade.py # Classe orquestradora
├── tests/                       # Testes unitários
├── versao1_2025/                # Código original (versão 1.0)
├── docs/                        # Documentação complementar
├── notebooks/                   # Jupyter notebook exploratório
├── main.py                      # Script principal
├── run_tests.py                 # Script alternativo de testes
├── requirements.txt
└── README.md
```

### 2.2 Fluxo de análise

1. **Carregamento** – leitura das abas anuais (2023–2026).
2. **Limpeza** – remoção de linhas vazias, padronização de colunas, conversão para formato longo.
3. **Transformação** – criação de coluna de data, remoção de outliers extremos.
4. **Análise exploratória** – estatísticas descritivas, totais por ano, ranking de crimes.
5. **Análise avançada** – regressão linear/polinomial, modelo Holt-Winters, decomposição sazonal, detecção de outliers (IQR e Z‑score).
6. **Visualização** – geração de gráficos estáticos e dashboard interativo.
7. **Geração de relatórios** – PDF, Markdown e CSV.

---

## 3. Resultados Obtidos

### 3.1 Panorama geral (2023 – abril/2026)

| Indicador | Valor |
|-----------|-------|
| Total de ocorrências | 114.454 |
| Média mensal | 136 |
| Tipos de crime distintos | 23 |

### 3.2 Ranking dos cinco crimes mais frequentes

| Posição | Tipo de crime | Total | % do total |
|---------|---------------|-------|-------------|
| 1º | ESTUPRO DE VULNERÁVEL | 27.902 | 24,4% |
| 2º | ROUBO DE CARGA | 15.111 | 13,2% |
| 3º | HOMICÍDIO CULPOSO POR ACIDENTE DE TRÂNSITO | 13.046 | 11,4% |
| 4º | TENTATIVA DE HOMICÍDIO | 12.291 | 10,7% |
| 5º | ESTUPRO | 11.419 | 10,0% |

### 3.3 Evolução anual

| Ano | Total de ocorrências | Variação |
|-----|---------------------|----------|
| 2023 | 27.825 | – |
| 2024 | 28.076 | +0,9% |
| 2025 | 26.332 | -6,2% |
| 2026* | 32.221 | +22,4%* |

> *Dados parciais (apenas os quatro primeiros meses).

### 3.4 Sazonalidade

| Mês | Média de ocorrências | Desvio em relação à média anual |
|-----|---------------------|--------------------------------|
| Dezembro | 136 | +0,0% (pico) |
| Março | 110 | -19,1% (vale) |

A amplitude entre o mês de maior e menor incidência é de **24,1%**, indicando sazonalidade relevante.

### 3.5 Análise do crime principal: Estupro de Vulnerável

| Indicador | Valor |
|-----------|-------|
| Tendência mensal (linear) | –2,03 ocorrências/mês |
| R² do modelo linear | 0,004 (correlação muito fraca) |
| Melhor modelo | Polinomial (grau 2) com R² = 0,068 |
| Contribuição da sazonalidade na variância | 26,9% |
| Contribuição do ruído | 52,6% |

A baixa qualidade dos ajustes lineares indica que outros fatores (econômicos, sociais, operacionais) têm maior poder explicativo sobre a variação mensal.

### 3.6 Previsão para os próximos meses (modelo Holt-Winters)

| Mês/Ano | Ocorrências previstas |
|---------|----------------------|
| Maio 2026 | 580 |
| Junho 2026 | 831 |
| Julho 2026 | 832 |
| Agosto 2026 | 601 |
| Setembro 2026 | 275 |
| Outubro 2026 | 603 |

---

## 4. Posicionamento e Compromisso Ético

Como estudante de Engenharia de Software e pesquisadora em Ciência de Dados, acredito que a produção de evidências quantitativas é um passo fundamental para compreender problemas complexos da sociedade. Entretanto, quando analisamos temas sensíveis, os dados não podem ser tratados apenas como estatísticas: eles representam pessoas, realidades e desafios concretos que exigem atenção.

### 4.1 Sobre os números de estupro de vulnerável

Os dados oficiais analisados neste projeto mostram que o **Estupro de Vulnerável** foi o tipo de crime mais frequente no período estudado, representando aproximadamente **24,4%** do total de ocorrências registradas.

A magnitude desses números evidencia a relevância do tema dentro do cenário da segurança pública paulista. Mais do que um resultado estatístico, esse indicador aponta para um problema persistente que afeta principalmente crianças e adolescentes e que demanda atenção contínua por parte da sociedade e das instituições responsáveis.

De acordo com boletins da Secretaria de Segurança Pública, em 2026 os casos de estupro contra menores de 13 anos representaram **75,3%** dos estupros registrados no estado. Apenas no primeiro trimestre de 2026 foram contabilizadas **2.942 ocorrências**, com crescimento mês a mês.

É importante destacar que os registros analisados representam apenas os casos oficialmente notificados. Diversos estudos nacionais e internacionais apontam que crimes dessa natureza apresentam índices relevantes de subnotificação, o que reforça a necessidade de interpretar os dados com cautela e reconhecer suas limitações.

### 4.2 Avanços institucionais e desafios persistentes

A promulgação da **Lei nº 15.353/2026** representou um avanço importante ao consolidar a presunção absoluta de vulnerabilidade para menores de 14 anos, fortalecendo a proteção jurídica das vítimas.

Ao mesmo tempo, a análise dos dados e da literatura sobre o tema sugere que o enfrentamento da violência sexual contra vulneráveis depende de uma atuação integrada que vai além da legislação. Estruturas especializadas de acolhimento, investigação, prevenção e atendimento às vítimas continuam sendo elementos fundamentais para a efetividade das políticas públicas.

Nesse contexto, desafios relacionados à capacidade institucional, à subnotificação e ao acesso das vítimas aos mecanismos de proteção permanecem relevantes para a compreensão do fenômeno e para a formulação de respostas mais eficazes.

### 4.3 Responsabilidade da análise de dados

Diante desse cenário, entendo que o papel da Ciência de Dados não deve se limitar à descrição de padrões estatísticos.

Como profissional da área, considero essencial:

1. **Produzir análises rigorosas, transparentes e reproduzíveis**, permitindo que resultados sejam verificados e debatidos de forma aberta.
2. **Transformar dados em informação acessível**, contribuindo para uma compreensão mais clara dos problemas públicos.
3. **Apoiar decisões baseadas em evidências**, fornecendo subsídios para pesquisadores, gestores públicos e sociedade civil.
4. **Reconhecer as limitações dos dados**, especialmente em fenômenos marcados por subnotificação e elevada complexidade social.

Acredito que a Ciência de Dados possui um papel relevante na construção de diagnósticos mais precisos da realidade. Quando aplicada a temas sensíveis, como a violência sexual contra crianças e adolescentes, sua contribuição vai além da análise estatística: ela pode auxiliar na identificação de prioridades, na avaliação de políticas públicas e na promoção de discussões fundamentadas em evidências.

---

## 5. Comparação entre versões (2025 → 2026)

| Característica | Versão 1.0 (2025) | Versão 2.0 (2026) |
|----------------|-------------------|-------------------|
| Estrutura | Script único | 4 módulos + classe principal |
| Linhas de código | ~280 | ~1500 |
| Tratamento de erros | Ausente | Presente |
| Testes unitários | Não | 12 testes |
| Dashboard | Não | Interativo (Plotly) |
| Modelos de tendência | Linear | Linear, polinomial |
| Previsão | Regressão linear | Holt‑Winters com sazonalidade |
| Decomposição de série | Não | Tendência + sazonalidade + ruído |
| Detecção de outliers | Não | IQR e Z‑score |
| Relatórios | Apenas gráficos PNG | PDF, Markdown, CSV, dashboard HTML |

A refatoração de 2026 buscou aplicar os princípios de **modularidade, reusabilidade, testabilidade e clareza documental** – competências centrais da engenharia de software aplicada à ciência de dados.

---

## 6. Instruções de Execução

### 6.1 Pré‑requisitos

- Python 3.9 ou superior
- Pip instalado

### 6.2 Instalação

```bash
git clone https://github.com/isadorameneghetti/criminalidade-sp.git
cd criminalidade-sp
pip install -r requirements.txt
```

### 6.3 Execução da análise

```bash
python main.py
```

### 6.4 Execução dos testes

```bash
pytest tests/test_limpeza.py -v
# ou
python run_tests.py
```

### 6.5 Visualização dos resultados

- Dashboard interativo: `outputs/dashboard/dashboard_criminalidade.html`
- Relatório executivo: `outputs/relatorio/relatorio_executivo.md`
- Relatório completo (PDF): `outputs/relatorio/relatorio_criminalidade_sp.pdf`
- Gráficos estáticos: `outputs/graficos/`

---

## 7. Licença

Distribuído sob licença MIT. Consulte o arquivo `LICENSE` para mais informações.

---

## 8. Contato e Agradecimentos

**Isadora Meneghetti**  
- GitHub: [isadorameneghetti](https://github.com/isadorameneghetti)  
- E‑mail: isadorameneghetti@gmail.com  

Agradecimentos à **FIAP**, ao **professor da disciplina Data Science and Statistical Computing** e ao **Governo do Estado de São Paulo** pela disponibilização dos dados públicos.