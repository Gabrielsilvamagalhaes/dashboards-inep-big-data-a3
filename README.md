# Dashboard INEP — Ensino Superior Brasileiro (A3)

Dashboard interativo de **análise de dados e Big Data** sobre o ensino superior no Brasil, desenvolvido a partir dos **microdados do Censo da Educação Superior 2024** (INEP/MEC).

O projeto simula o papel de analistas do Ministério da Educação (MEC), oferecendo indicadores táticos e estratégicos para apoiar a tomada de decisão por gestores públicos, universidades e instituições de ensino.

---

## Integrantes

| Nome                | RA          |
|---------------------|-------------|
| Gabriel Silva       | 1272313274  |
| Hanspeter Dietiker  | 1272313332  |
| Alexandre           | 12724123381 |

---

## Sobre o projeto

O dashboard permite explorar o cenário do ensino superior brasileiro em quatro áreas principais:

| Seção | Conteúdo |
|-------|----------|
| **Visão Nacional** | Matrículas, ingressantes, concluintes, cursos, instituições e distribuição por região e estado |
| **Perfil dos Estudantes** | Gênero, faixa etária, raça/cor e estudantes com deficiência |
| **Programas de Financiamento** | FIES, PROUNI e outras formas de apoio estudantil |
| **Análise de Cursos** | Demanda por curso, ingressantes, matrículas e taxa de conclusão |

**Fonte de dados:** [Microdados do Censo da Educação Superior 2024](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior) — INEP/MEC.

Para o escopo completo do trabalho acadêmico, consulte [SCOPE.md](SCOPE.md).

---

## Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|------------|----------------|
| **Python** | Linguagem principal |
| **Streamlit** | Interface web e navegação entre páginas |
| **Pandas** | Leitura, tratamento e agregação dos microdados (CSV) |
| **Plotly** | Gráficos interativos |
| **gdown** | Download e cache do arquivo CSV no Google Drive |
| **Colorama** | Logs coloridos no terminal durante a carga dos dados |

---

## Versões

### Requisitos mínimos (`requirements.txt`)

| Pacote | Versão mínima |
|--------|---------------|
| Python | **3.10+** (recomendado **3.11** ou superior) |
| streamlit | ≥ 1.28.0 |
| pandas | ≥ 2.0.0 |
| plotly | ≥ 5.0.0 |
| gdown | ≥ 5.2.0 |
| colorama | ≥ 0.4.6 |

### Ambiente de desenvolvimento testado

| Componente | Versão |
|------------|--------|
| Python | 3.13.7 |
| streamlit | 1.57.0 |
| pandas | 3.0.2 |
| plotly | 6.7.0 |
| gdown | 6.0.0 |
| colorama | 0.4.6 |

---

## Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado e disponível no `PATH`
- `pip` (geralmente incluso na instalação do Python)
- Conexão com a internet na **primeira execução** (download do CSV via Google Drive)
- Espaço em disco para cache local dos microdados (arquivo grande)

---

## Instalação na máquina

### 1. Clonar o repositório

```bash
git clone https://github.com/Gabrielsilvamagalhaes/dashboards-inep-big-data-a3.git
cd dashboards-inep-big-data-a3
```

Se você já possui o projeto localmente, entre na pasta raiz do repositório.

### 2. Criar e ativar um ambiente virtual (recomendado)

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## Como executar

Na raiz do projeto, com o ambiente virtual ativado:

```bash
streamlit run src/app.py
```

O Streamlit abrirá o dashboard no navegador (em geral em `http://localhost:8501`).

Na primeira execução, os dados são baixados do Google Drive e armazenados em cache local para as próximas aberturas. O carregamento pode levar alguns minutos, dependendo da conexão e do hardware.

### Dados locais (opcional)

É possível apontar para um CSV local em `samples/MICRODADOS_CADASTRO_CURSOS_2024.csv` (o arquivo não é versionado por tamanho). Consulte `src/app.py` e `src/services/extract_csv_service.py` para alterar a fonte dos dados.

---

## Estrutura do projeto

```
big-data-a3/
├── src/
│   ├── app.py                 # Entrada da aplicação Streamlit
│   ├── pages/                 # Páginas do dashboard
│   ├── dashboards/            # Componentes e gráficos por indicador
│   ├── services/              # Extração e cache do CSV
│   └── cache/                 # Utilitários de cache
├── requirements.txt
├── SCOPE.md                   # Escopo acadêmico do trabalho
├── .streamlit/config.toml     # Configuração do Streamlit
└── README.md
```

---

## Links úteis

- **Repositório GitHub:** [dashboards-inep-big-data-a3](https://github.com/Gabrielsilvamagalhaes/dashboards-inep-big-data-a3)
- **Notebook (Google Colab):** [Análise no Colab](https://colab.research.google.com/drive/1YjvgMnjOtm3wrT-GBRvv48UiZZD4rxyw?usp=sharing)

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
