# =============================================================================
# ESTÁCIO CARAPICUIBA - CURSO: Análise e Desenvolvimento de Sistemas
# DISCIPLINA: Desenvolvimento Rápido de Aplicações em Python
# ALUNO: Gabriel Santos de Souza
# PROJETO: SISTEMA DE GERENCIAMENTO DE ATIVOS DIGITAIS PARA ARQUITETURA
# REFERÊNCIAS: 
# - MENEZES, Nilo Ney C. Introdução à programação com Python. 3. ed.
# - Documentação Flask: https://flask.palletsprojects.com/
# - Documentação SQLite3: https://docs.python.org/3/library/sqlite3.html
# - Material de Aula: SAVA
# =============================================================================

from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ------------------------------- CONFIGURAÇÃO DO BANCO DE DADOS --------------------------------
# Nome do arquivo físico do banco de dados SQLite que será criado na pasta do projeto
DB_FILE = "portfolio_digital.db"

# ------------------------------- FUNÇÕES DE CONEXÃO ----------------------

# Função de conexão
def conectar_bd():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

def criar_tabela():
    """Cria a tabela 'ativos' no banco de dados se ela ainda não existir.
    
    É chamada uma única vez na inicialização do servidor para garantir
    que a estrutura do banco esteja pronta antes de qualquer requisição.
    """
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ativos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            registro  TEXT    UNIQUE NOT NULL,
            projeto   TEXT    NOT NULL,
            tecnica   TEXT,
            data      TEXT,
            status    TEXT
        )
    """)
    # Insere registros de exemplo apenas se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM ativos")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO ativos (registro, projeto, tecnica, data, status)
            VALUES
                ('IMG001', 'Residencial Horizonte', 'HDR High-End',       '2026-03-15', 'Aprovado')
        """)
    conn.commit()
    conn.close()

# ------------------------------- BLOCO DE TEMPLATES -------------------------------
# As chaves duplas {{ }} são usadas para escapar o Jinja2 dentro de f-strings Python.
layout_base_estilo = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; }

    .header-topo { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 40px 20px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .header-topo h1 { font-size: 24px; letter-spacing: 1px; text-transform: uppercase; }

    .menu-nav { background: #ffffff; padding: 15px; text-align: center; border-bottom: 1px solid #e2e8f0; }
    .menu-nav a { color: #64748b; margin: 0 15px; text-decoration: none; font-weight: 600; font-size: 14px; transition: 0.3s; padding: 8px 15px; border-radius: 6px; }
    .menu-nav a:hover { background: #f1f5f9; color: #2563eb; }

    .container { width: 95%; max-width: 1100px; margin: 30px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); min-height: 450px; }

    h2 { color: #1e293b; margin-bottom: 20px; font-weight: 700; }

    .tabela-v3 { width: 100%; border-collapse: separate; border-spacing: 0 10px; margin-top: 10px; }
    .tabela-v3 th { background-color: #f8fafc; color: #64748b; padding: 15px; text-align: center; font-size: 13px; text-transform: uppercase; border-bottom: 2px solid #e2e8f0; }
    .tabela-v3 td { background-color: #ffffff; padding: 15px; text-align: center; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
    .tabela-v3 tr:hover td { background-color: #f8fafc; }

    .btn-acao { background-color: #ef4444; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: 0.2s; }
    .btn-acao:hover { background-color: #dc2626; transform: translateY(-1px); }

    .btn-editar { background-color: #f59e0b; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: 0.2s; margin-right: 5px; }
    .btn-editar:hover { background-color: #d97706; transform: translateY(-1px); }

    .campo-readonly { background-color: #f1f5f9; color: #94a3b8; cursor: not-allowed; }

    .msg-erro    { background: #fee2e2; color: #991b1b; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .msg-sucesso { background: #dcfce7; color: #166534; padding: 12px; border-radius: 6px; margin-bottom: 15px; }

    .rodape { margin-top: 50px; padding-bottom: 30px; text-align: center; font-size: 12px; color: #94a3b8; }
</style>
"""

menu_navegacao = """
    <div class="header-topo">
        <h1>GERENCIADOR DE ATIVOS DIGITAIS</h1>
    </div>

    <div class="menu-nav">
        <a href="/">LISTAGEM</a>
        <a href="/novo_item">CADASTRAR ATIVO</a>
        <a href="/relatorio">RELATÓRIO</a>
        <a href="/sobre">SOBRE</a>
    </div>
"""

# Template da página principal — lista todos os ativos vindos do SELECT no banco
html_principal = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SISTEMA DE PORTFÓLIO</title>
    {layout_base_estilo}
</head>
<body>
    {menu_navegacao}

    <div class="container">
        <center>
            <h2>LISTAGEM DE PROJETOS ATIVOS</h2>
            <hr width="50%">
            <br>
            <table class="tabela-v3">
                <thead>
                    <tr>
                        <th>CÓDIGO</th>
                        <th>NOME DO PROJETO</th>
                        <th>TÉCNICA UTILIZADA</th>
                        <th>DATA</th>
                        <th>STATUS</th>
                        <th>AÇÕES</th>
                    </tr>
                </thead>
                <tbody>
                    {{% for item in dados %}}
                    <tr>
                        <td><b>{{{{ item.registro }}}}</b></td>
                        <td>{{{{ item.projeto }}}}</td>
                        <td>{{{{ item.tecnica }}}}</td>
                        <td>{{{{ item.data }}}}</td>
                        <td style="color: green;">{{{{ item.status }}}}</td>
                        <td>
                            <!-- Botão EDITAR: redireciona para o formulário de edição passando o registro na URL -->
                            <a href="/editar/{{{{ item.registro }}}}"><button class="btn-editar">EDITAR</button></a>
                            <!-- Botão REMOVER: executa o DELETE passando o registro como parâmetro na URL -->
                            <a href="/excluir/{{{{ item.registro }}}}"><button class="btn-acao">REMOVER</button></a>
                        </td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>
        </center>
    </div>

    <div class="rodape">
        <p>Desenvolvido conforme mostrado nas aulas e materiais de apoio.</p>
        <p>Desenvolvimento Rápido de Aplicações em Python - Fábio de Paula</p>
    </div>
</body>
</html>
"""

# Template do formulário de cadastro de novo ativo
# A variável 'erro' exibe mensagem de registro duplicado vinda da rota (IntegrityError)
html_form = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CADASTRO</title>
    {layout_base_estilo}
</head>
<body>
    {menu_navegacao}

    <div class="container">
        <center>
            <h2>INSERIR NOVO ATIVO</h2>
            <hr width="50%">
            <br>
            <!-- Exibe mensagem de erro se o registro já existir no banco (campo UNIQUE) -->
            {{% if erro %}}
            <div class="msg-erro" style="width: 50%;">{{{{ erro }}}}</div>
            {{% endif %}}
            <form action="/adicionar" method="POST" style="width: 50%; text-align: left; padding: 20px; border: 1px solid #eee;">
                <label>Registro (ID):</label><br>
                <input type="text" name="reg" style="width: 100%;" required><br><br>

                <label>Nome do Projeto:</label><br>
                <input type="text" name="proj" style="width: 100%;" required><br><br>

                <label>Técnica (8K, HDR, V-Ray):</label><br>
                <input type="text" name="tec" style="width: 100%;"><br><br>

                <label>Status:</label><br>
                <input type="text" name="st" style="width: 100%;"><br><br>

                <input type="submit" value="CONFIRMAR CADASTRO" style="width: 100%; background: #27ae60; color: white; padding: 10px; border: none;">
            </form>
            <br>
            <a href="/">CANCELAR E VOLTAR</a>
        </center>
    </div>
</body>
</html>
"""

# Template do formulário de edição, campos pré-preenchidos com os dados do SELECT
# O campo "Registro" é readonly pois é UNIQUE no banco
html_edicao = f"""
<!DOCTYPE html>
<html>
<head>
    <title>EDITAR ATIVO</title>
    {layout_base_estilo}
</head>
<body>
    {menu_navegacao}

    <div class="container">
        <center>
            <h2>EDITAR ATIVO: {{{{ item.registro }}}}</h2>
            <hr width="50%">
            <br>
            <!-- Exibe mensagem de erro se houver conflito de integridade no banco -->
            {{% if erro %}}
            <div class="msg-erro" style="width: 50%;">{{{{ erro }}}}</div>
            {{% endif %}}
            <!-- Formulário de edição com dados pré-preenchidos pelo Jinja2 -->
            <form action="/atualizar" method="POST" style="width: 50%; text-align: left; padding: 20px; border: 1px solid #eee;">

                <!-- Campo oculto: envia o registro original para o WHERE do UPDATE no banco -->
                <!-- Sem este campo, o UPDATE não saberia qual linha modificar -->
                <input type="hidden" name="reg_original" value="{{{{ item.registro }}}}">

                <label>Registro (ID) — não editável:</label><br>
                <!-- Readonly: registro é UNIQUE no banco, alterá-lo quebraria a integridade -->
                <input type="text" value="{{{{ item.registro }}}}" style="width: 100%;" class="campo-readonly" readonly><br><br>

                <label>Nome do Projeto:</label><br>
                <!-- value="..." pré-preenche o campo com o dado atual vindo do SELECT -->
                <input type="text" name="proj" value="{{{{ item.projeto }}}}" style="width: 100%;" required><br><br>

                <label>Técnica (8K, HDR, V-Ray):</label><br>
                <input type="text" name="tec" value="{{{{ item.tecnica }}}}" style="width: 100%;"><br><br>

                <label>Status:</label><br>
                <input type="text" name="st" value="{{{{ item.status }}}}" style="width: 100%;"><br><br>

                <input type="submit" value="SALVAR ALTERAÇÕES" style="width: 100%; background: #2563eb; color: white; padding: 10px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
            </form>
            <br>
            <a href="/">CANCELAR E VOLTAR</a>
        </center>
    </div>

    <div class="rodape">
        <p>Desenvolvido conforme mostrado nas aulas e materiais de apoio.</p>
        <p>Desenvolvimento Rápido de Aplicações em Python - Fábio de Paula</p>
    </div>
</body>
</html>
"""

# ------------------------------- ROTAS -------------------------------
# Rota principal, executa SELECT e passa os resultados para o template de listagem
@app.route('/')
def rota_inicial():
    conn = conectar_bd()
    cursor = conn.cursor()
    # SELECT para buscar todos os ativos cadastrados, ordenados pelo campo registro
    cursor.execute("SELECT registro, projeto, tecnica, data, status FROM ativos ORDER BY registro")
    # Converte cada sqlite3.Row para dicionário para o Jinja2 acessar por nome
    dados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template_string(html_principal, dados=dados)

# Rota para exibir o formulário de cadastro de novo ativo
@app.route('/novo_item')
def tela_adicionar():
    return render_template_string(html_form, erro=None)

# Rota para inserir um novo ativo no banco via POST
@app.route('/adicionar', methods=['POST'])
def processa_adicao():
    # Coleta dos dados enviados pelo formulário via método POST
    reg  = request.form.get('reg')
    proj = request.form.get('proj')
    tec  = request.form.get('tec')
    st   = request.form.get('st')
    dt   = datetime.now().strftime("%Y-%m-%d")

    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Insere o novo ativo na tabela do banco com os dados do formulário (INSERT)
        cursor.execute("""
            INSERT INTO ativos (registro, projeto, tecnica, data, status)
            VALUES (?, ?, ?, ?, ?)
        """, (reg, proj, tec, dt, st))
        # Os ? são parâmetros seguros que evitam SQL Injection
        conn.commit()
    except sqlite3.IntegrityError:
        # IntegrityError ocorre quando o campo UNIQUE já existe no banco
        # Mostra novamente o formulário com mensagem de erro ao invés de travar o sistema
        conn.close()
        erro = f"Erro: Já existe um ativo cadastrado com o registro '{reg}'."
        return render_template_string(html_form, erro=erro)
    finally:
        conn.close()

    return redirect(url_for('rota_inicial'))

# Rota para exibir o formulário de edição pré-preenchido com os dados do ativo
# Recebe o registro como parâmetro dinâmico na URL
@app.route('/editar/<string:id_reg>')
def tela_editar(id_reg):
    conn = conectar_bd()
    cursor = conn.cursor()
    # SELECT com WHERE para buscar apenas o ativo com o registro informado na URL
    cursor.execute(
        "SELECT registro, projeto, tecnica, data, status FROM ativos WHERE registro = ?",
        (id_reg,)
    )
    row = cursor.fetchone()
    conn.close()

    # Se o registro não existir no banco, redireciona para a listagem
    if row is None:
        return redirect(url_for('rota_inicial'))

    item = dict(row)
    return render_template_string(html_edicao, item=item, erro=None)

# Rota para processar as alterações enviadas pelo formulário de edição via POST
@app.route('/atualizar', methods=['POST'])
def processa_edicao():
    # Recupera o registro original para usar no WHERE do UPDATE
    reg_original = request.form.get('reg_original')

    # Recupera os novos valores enviados pelo formulário
    proj = request.form.get('proj')
    tec  = request.form.get('tec')
    st   = request.form.get('st')

    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # UPDATE com WHERE: atualiza apenas os campos editáveis da linha correspondente
        # O registro e a data originais são preservados
        cursor.execute("""
            UPDATE ativos
            SET projeto = ?, tecnica = ?, status = ?
            WHERE registro = ?
        """, (proj, tec, st, reg_original))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        item = {"registro": reg_original, "projeto": proj, "tecnica": tec, "status": st, "data": ""}
        erro = "Erro ao atualizar o ativo. Verifique os dados e tente novamente."
        return render_template_string(html_edicao, item=item, erro=erro)
    finally:
        conn.close()

    # Redireciona para a listagem após UPDATE bem-sucedido
    return redirect(url_for('rota_inicial'))

# Rota para remover um ativo do banco (DELETE)
@app.route('/excluir/<string:id_reg>')
def remover_projeto(id_reg):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Remove apenas o ativo com o registro informado na URL
    cursor.execute("DELETE FROM ativos WHERE registro = ?", (id_reg,))
    conn.commit()
    conn.close()
    return redirect(url_for('rota_inicial'))

# Rota para exibir um relatório simples dos ativos consultando o banco
@app.route('/relatorio')
def gerar_relatorio():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT projeto, status FROM ativos ORDER BY registro")
    ativos = cursor.fetchall()
    conn.close()

    total = len(ativos)
    corpo = f"<h1>RELATÓRIO DE ATIVOS</h1><p>Total de itens: {total}</p><hr>"
    for a in ativos:
        corpo += f"<p><b>Projeto:</b> {a['projeto']} | <b>Status:</b> {a['status']}</p>"
    corpo += "<br><a href='/'>Voltar</a>"
    return render_template_string(corpo)

# Rota para exibir informações sobre o projeto e bibliografia
@app.route('/sobre')
def info_projeto():
    conteudo = """
    <div style="padding: 30px;">
        <h2>DADOS DO TRABALHO</h2>
        <p><b>Disciplina:</b> Desenvolvimento Rápido de Aplicações em Python</p>
        <p><b>TEMA:</b> Gerenciamento de Ativos Digitais para Arquitetura</p>
        <hr>
        <h3>REFERÊNCIAS BIBLIOGRÁFICAS (ABNT2):</h3>
        <ul>
            <li>MENEZES, Nilo Ney Coutinho. <b>Introdução à programação com Python:</b> algoritmos e lógica de programação para iniciantes. 3. ed. São Paulo: Novatec, 2019.</li>
            <li>FLASK. <b>Pallets Projects:</b> Documentation. Disponível em: https://flask.palletsprojects.com/. Acesso em: 12 abr. 2026.</li>
            <li>PYTHON SOFTWARE FOUNDATION. <b>sqlite3 — DB-API 2.0 interface for SQLite databases.</b> Disponível em: https://docs.python.org/3/library/sqlite3.html. Acesso em: 12 abr. 2026.</li>
            <li>ESTÁCIO. <b>Material de Apoio SAVA:</b> Programação com Python.</li>
        </ul>
        <br><br>
        <a href="/">[ VOLTAR PARA O SISTEMA ]</a>
    </div>
    """
    return render_template_string(conteudo)

# ------------------------------- EXECUÇÃO FINAL -------------------------------

if __name__ == '__main__':
    # Garante que a tabela existe no banco antes de receber qualquer requisição
    criar_tabela()
    print("Iniciando servidor de Portfólio de Ativos Digitais...")
    app.run(debug=True, host='0.0.0.0', port=5000)

# -----------------------------------------------------------------
# Documentação da lógica de manutenção do sistema:
# 1. Banco de dados SQLite persistente substituiu a lista global em memória.
# 2. conectar_bd(): row_factory para acesso por nome.
# 3. criar_tabela() cria a estrutura do banco na inicialização do servidor.
# 4. Cada rota abre conexão, executa SQL e fecha no bloco finally.
# 5. try/except IntegrityError trata registros duplicados (campo UNIQUE no banco).
# 6. dict(row) converte sqlite3.Row para dicionário compatível com Jinja2.
# 7. Parâmetros ? nas queries SQL evitam SQL Injection.
# 8. O campo 'registro' é UNIQUE no banco: funciona como chave de negócio do ativo.
# -----------------------------------------------------------------
