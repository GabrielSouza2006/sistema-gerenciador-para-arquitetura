# =============================================================================
# ESTÁCIO CARAPICUIBA - CURSO: Análise e Desenvolvimento de Sistemas
# DISCIPLINA: Desenvolvimento Rápido de Aplicações em Python
# ALUNO: Gabriel Santos de Souza
# PROJETO: SISTEMA DE GERENCIAMENTO DE ATIVOS DIGITAIS PARA ARQUITETURA
# REFERÊNCIAS: 
# - MENEZES, Nilo Ney C. Introdução à programação com Python. 3. ed.
# - Documentação Flask: https://flask.palletsprojects.com/
# - Material de Aula: SAVA
# =============================================================================

from flask import Flask, render_template_string, request, redirect, url_for, send_file
import os
import io
import base64
from datetime import datetime

app = Flask(__name__)

# ------------------------------- BANCO DE DADOS EM MEMÓRIA -------------------------------
portfolio_digital = [
    {
        "registro": "IMG001",
        "projeto": "Residencial Horizonte",
        "tecnica": "HDR High-End",
        "data": "2026-03-15",
        "status": "Aprovado"
    },
    {
        "registro": "IMG002",
        "projeto": "Corporativo Office",
        "tecnica": "Renderização V-Ray",
        "data": "2026-03-20",
        "status": "Em Edição"
    }
]

# ------------------------------- BLOCO DE TEMPLATES -------------------------------
# Como mostrado em aula os tamplates são strings para manter o projeto em um único arquivo.
layout_base_estilo = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; }
    
    /* Header Estilizado */
    .header-topo { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: white; padding: 40px 20px; text-align: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .header-topo h1 { font-size: 24px; letter-spacing: 1px; text-transform: uppercase; }
    
    /* Menu estilo App */
    .menu-nav { background: #ffffff; padding: 15px; text-align: center; border-bottom: 1px solid #e2e8f0; sticky: top; }
    .menu-nav a { color: #64748b; margin: 0 15px; text-decoration: none; font-weight: 600; font-size: 14px; transition: 0.3s; padding: 8px 15px; border-radius: 6px; }
    .menu-nav a:hover { background: #f1f5f9; color: #2563eb; }

    /* Container Card */
    .container { width: 95%; max-width: 1100px; margin: 30px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); min-height: 450px; }
    
    h2 { color: #1e293b; margin-bottom: 20px; font-weight: 700; }

    /* Tabela Estilizada */
    .tabela-v3 { width: 100%; border-collapse: separate; border-spacing: 0 10px; margin-top: 10px; }
    .tabela-v3 th { background-color: #f8fafc; color: #64748b; padding: 15px; text-align: center; font-size: 13px; text-transform: uppercase; border-bottom: 2px solid #e2e8f0; }
    .tabela-v3 td { background-color: #ffffff; padding: 15px; text-align: center; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
    .tabela-v3 tr:hover td { background-color: #f8fafc; }

    /* Botões e Icones */
    .status-badge { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }

    .btn-acao { background-color: #ef4444; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: 0.2s; }
    .btn-acao:hover { background-color: #dc2626; transform: translateY(-1px); }
    
    .btn-confirmar { background-color: #2563eb; color: white; width: 100%; padding: 12px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; margin-top: 10px; }
    .btn-confirmar:hover { background-color: #1d4ed8; }

    /* Rodapé */
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
                        <th>AÇÃO</th>
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
                        <td><a href="/excluir/{{{{ item.registro }}}}"><button class="btn-acao">REMOVER</button></a></td>
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

html_form = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CADASTRO</title>
    {layout_base_estilo}
</head>
<body>
    {menu_navegacao}

    <div class="header-topo">
        <h1>INSERIR NOVO ATIVO</h1>
    </div>
    <div class="container">
        <center>
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

# ------------------------------- ROTAS -------------------------------

@app.route('/')
def rota_inicial():
    # Passando a lista (simulando o banco de dados) para o template
    return render_template_string(html_principal, dados=portfolio_digital)

# Rota para exibir o formulário de cadastro
@app.route('/novo_item')
def tela_adicionar():
    return render_template_string(html_form)

# Rota para adicionar um novo item a lista (simulando inserção no banco de dados) via POST
@app.route('/adicionar', methods=['POST'])
def processa_adicao():
    # Coleta de dados manual via formulário
    reg = request.form.get('reg')
    proj = request.form.get('proj')
    tec = request.form.get('tec')
    st = request.form.get('st')
    dt = datetime.now().strftime("%Y-%m-%d")
    
    # Criando dicionário para inserir na lista
    novo_objeto = {
        "registro": reg,
        "projeto": proj,
        "tecnica": tec,
        "data": dt,
        "status": st
    }
    
    # Adicionando na lista global
    portfolio_digital.append(novo_objeto)
    
    # Redirecionamento para a página inicial para mostrar o novo item adicionado
    return redirect(url_for('rota_inicial'))

# Rota para remover um item da lista (simulando remoção no banco de dados)
@app.route('/excluir/<string:id_reg>')
def remover_projeto(id_reg):
    # Lógica de remoção manual percorrendo a lista
    global portfolio_digital
    for i in range(len(portfolio_digital)):
        if portfolio_digital[i]['registro'] == id_reg:
            portfolio_digital.pop(i)
            break
    return redirect(url_for('rota_inicial'))

# Rota para gerar um relatório simples dos ativos cadastrados
@app.route('/relatorio')
def gerar_relatorio():
    total = len(portfolio_digital)
    corpo = f"<h1>RELATÓRIO DE ATIVOS</h1><p>Total de itens: {total}</p><hr>"
    for p in portfolio_digital:
        corpo += f"<p><b>Projeto:</b> {p['projeto']} | <b>Status:</b> {p['status']}</p>"
    corpo += "<br><a href='/'>Voltar</a>"
    return render_template_string(corpo)

# Rota para exibir informações sobre o projeto e bibliografia
@app.route('/sobre')
def info_projeto():
    # Seção para bibliografia exigida pelo professor
    conteudo = """
    <div style="padding: 30px;">
        <h2>DADOS DO TRABALHO</h2>
        <p><b>Disciplina:</b> Desenvolvimento Rápido de Aplicações em Python</p>
        <p><b>TEMA:</b> Gerenciamento de Ativos Imobiliários</p>
        <hr>
        <h3>REFERÊNCIAS BIBLIOGRÁFICAS (ABNT2):</h3>
        <ul>
            <li>MENEZES, Nilo Ney Coutinho. <b>Introdução à programação com Python:</b> algoritmos e lógica de programação para iniciantes. 3. ed. São Paulo: Novatec, 2019.</li>
            <li>FLASK. <b>Pallets Projects:</b> Documentation. Disponível em: https://flask.palletsprojects.com/. Acesso em: 12 abr. 2026.</li>
            <li>ESTÁCIO. <b>Material de Apoio SAVA:</b> Programação com Python.</li>
        </ul>
        <br><br>
        <a href="/">[ VOLTAR PARA O SISTEMA ]</a>
    </div>
    """
    return render_template_string(conteudo)

# ------------------------------- EXECUÇÃO FINAL -------------------------------

if __name__ == '__main__':
    # Mantendo o padrão solicitado de host e port para servidor local
    print("Iniciando servidor de Portfólio de Imóveis...")
    app.run(debug=True, host='0.0.0.0', port=5000)

# -----------------------------------------------------------------
# Este bloco serve para documentar a lógica de manutenção do sistema
# conforme o padrão de estudo do material fornecido.
# 1. O sistema utiliza listas globais para persistência temporária.
# 2. As rotas Flask gerenciam o fluxo de requisição (Request/Response).
# 3. O HTML é renderizado via string para garantir arquivo único (Single File).
# 4. Implementado o método POST para segurança de envio de dados.
# 5. Adicionado loop de busca para remoção de registros.
# 6. Estilização CSS inline para facilitar a visualização sem arquivos externos.
# -----------------------------------------------------------------