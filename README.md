# Queimadas INPE — Análise Estratégica de Focos de Incêndio no Brasil

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
<img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
<img src="https://img.shields.io/badge/FIAP-Global%20Solution-red" />

Plataforma de coleta, processamento e visualização estratégica de dados de queimadas do INPE, desenvolvida como projeto da Global Solution da FIAP.

---

## Problema

As queimadas são um problema recorrente no Brasil e afetam diretamente o meio ambiente, a biodiversidade, a qualidade do ar e a saúde da população. Embora parte dos eventos ocorra por causas naturais, a maior parte dos focos de incêndio está relacionada à ação humana — desmatamento, expansão agropecuária, limpeza de terrenos e uso inadequado do fogo.

O INPE disponibiliza dados sobre focos de calor em todo o território nacional, mas essas informações exigem análises complementares para identificar padrões, tendências e possíveis causas dos incêndios em cada região.

**Como transformar dados brutos do INPE em informações estratégicas que apoiem órgãos ambientais, pesquisadores e gestores públicos na prevenção e fiscalização de queimadas?**

---

## Solução Proposta

Desenvolvimento de uma plataforma de análise de dados com dashboards e visualizações interativas que permitem:

- Identificar **padrões temporais e geográficos** de focos de incêndio
- Comparar a **incidência entre regiões** do Brasil
- Indicar se a origem dos eventos está relacionada a **causas naturais ou à ação humana**
- Apoiar decisões de **monitoramento, prevenção e fiscalização** ambiental

---

## Fontes de Dados

| Fonte | Datasets utilizados |
|---|---|
| **INPE Queimadas** *(principal)* | Focos ativos, risco de fogo, áreas queimadas, histórico de focos |
| **IBGE** | Estados, municípios, malhas geográficas |
| **MapBiomas** | Uso e cobertura do solo |
| **INMET** | Chuva, temperatura, umidade |

Os dados brutos anuais de focos (2020–2025) são baixados diretamente do servidor do INPE e salvos em `data/raw/`. O pipeline os converte para Parquet em `data/interim/`.

> **Os dados não são versionados no repositório** — use o script de ingestão para obtê-los localmente (veja [Como executar](#como-executar)).

---

## Estrutura do Projeto

```
queimadas_inpe_bi/
│
├── data/
│   ├── external/       <- Dados de fontes externas (IBGE, MapBiomas, INMET)
│   ├── interim/        <- Dados intermediários convertidos para Parquet
│   ├── processed/      <- Dados finais prontos para modelagem e visualização
│   └── raw/            <- Dados brutos originais do INPE (ZIPs e CSVs)
│
├── docs/               <- Documentação do projeto (MkDocs)
│
├── models/             <- Modelos treinados e predições
│
├── notebooks/          <- Jupyter Notebooks exploratórios
│
├── reports/
│   └── figures/        <- Gráficos e visualizações geradas
│
├── queimadas_inpe/     <- Código-fonte principal
│   ├── data/
│   │   └── ingest.py   <- Pipeline de download e conversão dos dados do INPE
│   ├── modeling/
│   │   ├── train.py    <- Treinamento de modelos
│   │   └── predict.py  <- Inferência com modelos treinados
│   ├── config.py       <- Configurações e variáveis globais
│   ├── dataset.py      <- Carregamento e preparação dos datasets
│   ├── features.py     <- Engenharia de features
│   └── plots.py        <- Geração de visualizações
│
├── tests/              <- Testes automatizados
├── .env.example        <- Template de variáveis de ambiente
├── pyproject.toml      <- Dependências e configuração do projeto
└── Makefile            <- Comandos de conveniência
```

---

## Como Executar

### Pré-requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)

### 1. Clonar o repositório

```bash
git clone https://github.com/joaoadamii/queimadas_inpe_bi.git
cd queimadas_inpe_bi
```

### 2. Criar o ambiente virtual e instalar dependências

```bash
uv sync
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
# edite o .env se necessário
```

### 4. Baixar os dados do INPE

```bash
uv run python -m queimadas_inpe.data.ingest
```

Isso irá baixar os arquivos anuais de focos (2020–2025) do servidor do INPE, extrair os CSVs dos ZIPs e convertê-los para Parquet em `data/interim/`.

### 5. Abrir os notebooks

```bash
uv run jupyter lab
```

---

## Tecnologias

| Categoria | Ferramentas |
|---|---|
| Linguagem | Python 3.12 |
| Dados | Pandas, DuckDB, PyArrow |
| Geoespacial | GeoPandas, Folium, Shapely |
| Visualização | Plotly, Matplotlib |
| Dashboard | Streamlit |
| ML | Scikit-learn |
| Qualidade | Ruff, Pytest |
| Docs | MkDocs |

---

## Time

Projeto desenvolvido pelo grupo da Global Solution — FIAP.
