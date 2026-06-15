
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

Como engenheira de software e estudiosa de ciência de dados, considero que a produção de evidências quantitativas é um primeiro passo necessário, mas não suficiente. Os dados obtidos neste projeto revelam um fenômeno que não pode ser tratado apenas como estatística.

### 4.1 Sobre os números de estupro de vulnerável

Os dados oficiais mostram que o **Estupro de Vulnerável** foi o tipo de crime mais frequente no período analisado, representando quase um quarto do total de ocorrências. Essa posição de liderança no ranking não é um acidente amostral – é o reflexo de uma violência estrutural que atinge, sobretudo, crianças e adolescentes.

De acordo com boletins da Secretaria de Segurança Pública, em 2026 os casos de estupro contra menores de 13 anos chegaram a representar **75,3%** de todos os estupros registrados no estado. Ainda no primeiro trimestre de 2026, foram contabilizadas **2.942 ocorrências** apenas dessa natureza, com crescimento mês a mês (892 em janeiro, 915 em fevereiro, 1.135 em março).

Esses números são alarmantes, mas sabe-se que a subnotificação é grave. A pandemia de Covid-19 escancarou o isolamento de vítimas e a dificuldade de denúncia, e ainda hoje muitos casos não chegam às estatísticas.

### 4.2 Avanço legal e desafios persistentes

A promulgação da **Lei nº 15.353/2026** representou um avanço civilizatório ao positivar a **presunção absoluta de vulnerabilidade** para menores de 14 anos, vedando argumentos defensivos baseados na suposta “experiência sexual prévia” da vítima. A lei é uma resposta necessária à impunidade histórica.

Todavia, o arcabouço legal não opera no vácuo. Persistem gargalos operacionais graves:

- **São Paulo continua sendo o único estado brasileiro sem Delegacias Especializadas de Proteção à Criança e ao Adolescente (DPCA)**, apesar de previsão legal desde 2017.
- A falta de estrutura especializada compromete o acolhimento humanizado, a coleta de provas e a celeridade investigativa.
- A sensação de impunidade, alimentada por anos de relativização judicial, não se dissipa com a edição de uma lei – exige mudança cultural e investimento contínuo.

### 4.3 Responsabilidade da análise de dados

Diante desse contexto, minha posição como profissional de dados é:

1. **Produzir evidência rigorosa e acessível** – os dados devem ser públicos, reproduzíveis e compreensíveis, servindo de base para o debate informado.
2. **Exigir transparência e efetividade** – não basta que os dados existam; é necessário que o poder público os utilize para gestão, alocação de recursos e avaliação de políticas.
3. **Cobrar ação coordenada** – a existência de uma lei robusta e de evidências estatísticas inequívocas é condição necessária, mas não suficiente. A ausência de delegacias especializadas e a subnotificação são falhas que a tecnologia pode ajudar a mitigar (integração de bases de saúde, educação e segurança), mas que dependem de decisão política.

Acredito que o papel da ciência de dados não se limita a descrever a realidade. Quando aplicada a temas sensíveis como a violência sexual contra vulneráveis, ela deve também **instrumentalizar a cobrança por resultados** e contribuir para a construção de políticas públicas baseadas em evidências.

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