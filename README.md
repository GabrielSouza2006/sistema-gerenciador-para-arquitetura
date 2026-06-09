# 🏛️ Arch-Asset Manager
**Sistema de Gerenciamento de Ativos Digitais para Arquitetura**

Uma aplicação web ágil desenvolvida para o controle de renders, plantas e metadados técnicos de projetos imobiliários, com persistência de dados via banco de dados SQLite.

---

## 📌 Sobre o Projeto

Este sistema foi desenvolvido como projeto prático para a disciplina de **Desenvolvimento Rápido de Aplicações em Python** na Estácio Carapicuíba. O foco principal é resolver a desorganização de arquivos digitais em escritórios de arquitetura, permitindo o rastreio rápido do status de cada visualização 3D ou planta baixa.

O projeto aplica o conceito de **RAD (Rapid Application Development)**, sendo estruturado como uma **Single-File Application** para demonstrar a eficiência do micro-framework Flask em prototipagem rápida. Os dados são persistidos em um banco de dados **SQLite** local, garantindo que os registros sobrevivam a reinicializações do servidor.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.x** — Linguagem base.
- **Flask** — Micro-framework para o back-end e gerenciamento de rotas HTTP.
- **SQLite3** — Banco de dados relacional embutido no Python para persistência dos ativos.
- **Jinja2** — Motor de renderização de templates dinâmicos.
- **HTML5 & CSS3** — Interface limpa e funcional.

---

## ⚙️ Funcionalidades

- [x] **Cadastro de Ativos** — Inserção de novos projetos com ID único, técnica (HDR, V-Ray, etc.) e status via formulário web (INSERT no banco).
- [x] **Dashboard de Listagem** — Visualização centralizada de todos os ativos armazenados no banco (SELECT).
- [x] **Edição de Ativos** — Formulário pré-preenchido para atualização de projeto, técnica e status sem perda de histórico (UPDATE no banco).
- [x] **Remoção de Ativos** — Exclusão individual de registros com confirmação visual (DELETE no banco).
- [x] **Relatório em Tempo Real** — Rota dedicada para resumo estatístico do portfólio, consultado diretamente do banco.
- [x] **Persistência de Dados** — Os registros são mantidos em `portfolio_digital.db` e não se perdem ao reiniciar o servidor.

---

## 🛠️ Como Executar

**1. Clone o repositório:**
```bash
git clone https://github.com/GabrielSouza2006/sistema-gerenciador-para-arquitetura.git
cd sistema-gerenciador-para-arquitetura
```

**2. Instale a dependência:**
```bash
pip install flask
```
> O módulo `sqlite3` já é nativo do Python — nenhuma instalação adicional é necessária.

**3. Execute o servidor:**
```bash
python app.py
```

**4. Acesse no navegador:** http://localhost:5000

> Na primeira execução, o arquivo `portfolio_digital.db` será criado automaticamente na pasta do projeto com dois registros de exemplo.

---

## 🗂️ Estrutura do Banco de Dados

A tabela `ativos` é criada automaticamente com a seguinte estrutura:

| Campo      | Tipo    | Descrição                          |
|------------|---------|------------------------------------|
| `id`       | INTEGER | Chave primária auto-incrementada   |
| `registro` | TEXT    | Identificador único do ativo (ex: IMG001) |
| `projeto`  | TEXT    | Nome do projeto arquitetônico      |
| `tecnica`  | TEXT    | Técnica utilizada (HDR, V-Ray...) |
| `data`     | TEXT    | Data de cadastro (gerada automaticamente) |
| `status`   | TEXT    | Status atual (Aprovado, Em Edição...) |

---

## 📖 Referências Acadêmicas

Fundamentado nos seguintes materiais:

- ESTÁCIO. **Material de Apoio SAVA:** Programação com Python. São Paulo: Estácio, 2026.
- FLASK. **Pallets Projects: Documentation.** Disponível em: https://flask.palletsprojects.com/. Acesso em: 12 abr. 2026.
- MENEZES, Nilo Ney Coutinho. **Introdução à programação com Python:** algoritmos e lógica de programação para iniciantes. 3. ed. São Paulo: Novatec, 2019.
- PYTHON SOFTWARE FOUNDATION. **sqlite3 — DB-API 2.0 interface for SQLite databases.** Disponível em: https://docs.python.org/3/library/sqlite3.html. Acesso em: 12 abr. 2026.

---

Desenvolvido por: **Gabriel Santos de Souza**
Curso: Análise e Desenvolvimento de Sistemas — Estácio 🎓
