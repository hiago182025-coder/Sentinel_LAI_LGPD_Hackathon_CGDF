# 🏛️ Sentinel LAI/LGPD  
## Classificação Automática de Pedidos de Acesso à Informação com Dados Pessoais

**1º Hackathon em Controle Social – Desafio Participa DF**  
**Edital nº 10/2025 – Controladoria-Geral do Distrito Federal (CGDF)**  
**Categoria: Acesso à Informação**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![LGPD](https://img.shields.io/badge/Conformidade-LGPD-critical?style=flat-square)
![Auditabilidade](https://img.shields.io/badge/Modelo-Auditável-success?style=flat-square)

---

## 📌 Contexto Institucional

No âmbito da **Lei de Acesso à Informação (Lei nº 12.527/2011)**, pedidos classificados como públicos não podem conter dados pessoais, sob pena de violação à **Lei Geral de Proteção de Dados (LGPD – Lei nº 13.709/2018)**.

Este projeto propõe uma solução automatizada de apoio à decisão capaz de identificar pedidos de acesso à informação que contenham dados pessoais, permitindo sua correta reclassificação como não públicos.

---

## 🎯 Objetivo da Solução

Desenvolver um **modelo automático de classificação** que receba pedidos de acesso à informação em formato textual e indique a presença ou ausência de dados pessoais, conforme os critérios definidos no edital.

A solução é executável via **linha de comando (CLI)** e foi projetada para avaliação técnica automatizada.

---

## 🧾 Escopo de Dados Pessoais

O modelo considera como dados pessoais:
- Nome de pessoa natural
- CPF
- RG
- Telefone
- Endereço de e-mail
- Informações que permitam identificação direta ou indireta

Todos os dados utilizados neste projeto são **sintéticos**, gerados exclusivamente para fins de teste.

---

## 🧠 Arquitetura da Solução

A solução adota uma **arquitetura híbrida**, composta por:
- **Camada determinística**: identificação de padrões sensíveis via expressões regulares
- **Camada probabilística**: análise contextual por NLP (TF-IDF + Regressão Logística)

A estratégia prioriza **alto recall**, reduzindo o risco de falsos negativos.

---

## 📊 Métricas de Avaliação

O modelo é avaliado utilizando:
- Precisão
- Recall (Sensibilidade)
- F1-score

---

## 🚀 Execução do Projeto (CLI)

### 🔧 Pré-requisitos
- Python 3.9 ou superior
- Recomendado: ambiente virtual

---

### 📦 Instalação

```bash
pip install -r requirements.txt

🧪 Geração de Dados Sintéticos (Opcional)

Para facilitar testes locais, o projeto inclui um gerador de dados sintéticos realistas baseado na biblioteca Faker (pt_BR).

Este passo é opcional e não substitui o dataset oficial fornecido pela CGDF.

python generate_data.py


Ao executar este comando:

Um arquivo CSV de pedidos de acesso à informação é gerado

O arquivo é salvo na pasta data/raw/

O dataset contém textos com e sem dados pessoais simulados

▶️ Execução do Modelo de Classificação

Após a instalação (e opcionalmente a geração dos dados), execute:

python evaluate.py


Este comando realiza automaticamente:

Carregamento dos dados

Pré-processamento textual

Treinamento do modelo

Inferência dos resultados

Cálculo das métricas (Precisão, Recall e F1-score)

Geração dos artefatos de saída

📤 Saídas Geradas

Os resultados são gerados na pasta data/processed/:

🖥️ Relatório no Terminal

Progresso de execução

Métricas finais

Amostra de pedidos classificados como contendo dados pessoais

📑 Relatório de Auditoria (Excel)

Arquivo .xlsx contendo:

Texto do pedido

Classificação final

Indicação de risco

Estrutura organizada para análise humana

📂 Estrutura do Repositório
acesso-informacao-lgpd/
├── data/
│   ├── raw/                 # Dados brutos (sintéticos ou fornecidos)
│   └── processed/           # Resultados e relatórios gerados
├── src/
│   ├── preprocessing.py     # Limpeza e normalização textual
│   ├── rules.py             # Padrões regex de dados pessoais
│   ├── model.py             # Pipeline híbrido (Regras + NLP)
│   └── reporter.py          # Geração de relatórios
├── generate_data.py         # Geração de dados sintéticos (opcional)
├── evaluate.py              # Script principal (CLI)
├── requirements.txt
└── README.md

⚖️ Conformidade Legal e Ética

Não são utilizados dados pessoais reais

O modelo atua exclusivamente como apoio à decisão humana

Nenhuma decisão automatizada definitiva é tomada pelo sistema

📌 Observações Finais

Este projeto foi desenvolvido exclusivamente para fins de participação no
1º Hackathon em Controle Social – Desafio Participa DF, respeitando integralmente as diretrizes do edital.
