# 🏛️ Sentinel LAI/LGPD  
 Classificação Automática de Pedidos de Acesso à Informação com Dados Pessoais

1º Hackathon em Controle Social – Desafio Participa DF  
Edital nº 10/2025 – Controladoria-Geral do Distrito Federal (CGDF)  
Categoria: Acesso à Informação

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![LGPD](https://img.shields.io/badge/Conformidade-LGPD-critical?style=flat-square)
![Auditabilidade](https://img.shields.io/badge/Modelo-Auditável-success?style=flat-square)

---

 📌 Contexto Institucional

No âmbito da Lei de Acesso à Informação (Lei nº 12.527/2011), pedidos classificados como públicos não podem conter dados pessoais, sob pena de violação à Lei Geral de Proteção de Dados – LGPD (Lei nº 13.709/2018).

Na prática, órgãos públicos lidam diariamente com grandes volumes de pedidos textuais, muitos dos quais são marcados como públicos de forma automática ou manual, sem verificação sistemática da presença de dados pessoais.

Este projeto propõe uma solução automatizada de apoio à decisão, capaz de identificar pedidos de acesso à informação que contenham dados pessoais, permitindo sua correta reclassificação como não públicos.

---

 🎯 Objetivo da Solução

Desenvolver um modelo de classificação automática que:

- Receba pedidos de acesso à informação em formato textual  
- Identifique a presença de dados pessoais, conforme definido no edital  
- Classifique o pedido como:
- Contém dados pessoais  
- Não contém dados pessoais  

O sistema foi projetado para execução via linha de comando (CLI), conforme o padrão esperado para avaliação técnica automatizada.

---

 🧾 Definição de Dados Pessoais (Escopo do Modelo)

De acordo com o edital, o modelo considera como dados pessoais:

- Nome de pessoa natural  
- CPF  
- RG  
- Telefone  
- Endereço de e-mail  
- Informações que permitam identificação direta ou indireta de pessoa natural  

⚠️ Todos os dados utilizados no projeto são sintéticos, gerados exclusivamente para fins de teste e demonstração.

---

 🧠 Arquitetura da Solução

A solução adota uma arquitetura híbrida, priorizando recall elevado, explicabilidade e auditabilidade, características essenciais para uso em contexto governamental.

# 🔹 Camada 1 — Regras Determinísticas (Regex)
Identificação direta de padrões sensíveis, como:
- CPF  
- RG  
- Telefones  
- Endereços de e-mail  
- Matrículas funcionais  

Esta camada reduz falsos negativos críticos.

# 🔹 Camada 2 — Classificação Probabilística (NLP)
- Vetorização textual via TF-IDF (n-grams)  
- Classificador linear explicável (Regressão Logística)  
- Análise de contexto semântico para reduzir falsos positivos  

# 🔹 Estratégia Geral
- Classificação conservadora  
- Penalização explícita de falsos negativos  
- Decisões rastreáveis e justificáveis

---

 📊 Métricas de Avaliação

O desempenho do modelo é medido conforme o edital, utilizando:

- Precisão
- Recall (Sensibilidade)
- F1-score

> Estratégia adotada: priorizar Recall, reduzindo o risco de exposição indevida de dados pessoais.

---

 🚀 Execução do Projeto (CLI)

# 🔧 Pré-requisitos
- Python 3.9 ou superior
- Ambiente virtual recomendado

# 📦 Instalação

pip install -r requirements.txt
