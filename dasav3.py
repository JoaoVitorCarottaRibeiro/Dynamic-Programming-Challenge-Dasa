# Challenge Dasa - Sprint 3 

# João Vitor Carotta Ribeiro - RM 555187
# Arthur Bueno de Oliveira - RM 558396
# Victor Magdaleno Marcos - RM 556729

# Repositório no GitHub contendo a explicação detalhada do projeto, com referências e pré requisitos.

# Link do repositório: https://github.com/JoaoVitorCarottaRibeiro/Dynamic-Programming-Challenge-Dasa.git

# Importando todas as bibliotecas a serem usadas no projeto

import datetime
from collections import deque
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Criação de uma lista de dicionários denominada de remédios tendo alguns atributos em seus dicionários, sendo eles: nome, tipo, quantidade, validade e código, que serão utilizados para determinadas funcionalidades da aplicação.
remedios = [
    {"nome": "Aciclovir", "tipo": "Antiviral", "quantidade": 700, "validade": "2026-07", "codigo": "528374"},
    {"nome": "Ácido acetilsalicílico", "tipo": "Antitérmico", "quantidade": 150, "validade": "2026-02", "codigo": "671923"},
    {"nome": "Ácido fólico", "tipo": "Vitamina/Suplemento", "quantidade": 560, "validade": "2025-11", "codigo": "859607"},
    {"nome": "Amlodipino", "tipo": "Anti-hipertensivo", "quantidade": 240, "validade": "2026-04", "codigo": "071829"},
    {"nome": "Amoxicilina", "tipo": "Antibiótico", "quantidade": 500, "validade": "2026-01", "codigo": "102938"},
    {"nome": "Captopril", "tipo": "Anti-hipertensivo", "quantidade": 610, "validade": "2026-01", "codigo": "960718"},
    {"nome": "Cefalexina", "tipo": "Antibiótico", "quantidade": 600, "validade": "2025-10", "codigo": "564738"},
    {"nome": "Cetirizina", "tipo": "Antialérgico", "quantidade": 360, "validade": "2026-01", "codigo": "930172"},
    {"nome": "Cetoconazol", "tipo": "Antifúngico", "quantidade": 300, "validade": "2025-09", "codigo": "309182"},
    {"nome": "Cianocobalamina", "tipo": "Vitamina/Suplemento", "quantidade": 310, "validade": "2026-03", "codigo": "960718"},
    {"nome": "Clonazepam", "tipo": "Psicotrópico", "quantidade": 190, "validade": "2026-06", "codigo": "415263"},
    {"nome": "Codeína", "tipo": "Analgésico", "quantidade": 400, "validade": "2025-12", "codigo": "987646"},
    {"nome": "Diclofenaco", "tipo": "Anti-inflamatório", "quantidade": 800, "validade": "2025-08", "codigo": "192837"},
    {"nome": "Diazepam", "tipo": "Psicotrópico", "quantidade": 720, "validade": "2025-08", "codigo": "526374"},
    {"nome": "Dipirona monoidratada", "tipo": "Antitérmico", "quantidade": 550, "validade": "2026-04", "codigo": "738291"},
    {"nome": "Doxiciclina", "tipo": "Antibiótico", "quantidade": 700, "validade": "2026-03", "codigo": "837261"},
    {"nome": "Fexofenadina", "tipo": "Antialérgico", "quantidade": 610, "validade": "2025-11", "codigo": "102384"},
    {"nome": "Fluconazol", "tipo": "Antifúngico", "quantidade": 400, "validade": "2026-03", "codigo": "204859"},
    {"nome": "Gliclazida", "tipo": "Antidiabético", "quantidade": 450, "validade": "2026-02", "codigo": "293041"},
    {"nome": "Griseofulvina", "tipo": "Antifúngico", "quantidade": 200, "validade": "2025-12", "codigo": "418273"},
    {"nome": "Ibuprofeno", "tipo": "Analgésico", "quantidade": 300, "validade": "2025-09", "codigo": "765278"},
    {"nome": "Linagliptina", "tipo": "Antidiabético", "quantidade": 580, "validade": "2026-07", "codigo": "304152"},
    {"nome": "Loratadina", "tipo": "Antialérgico", "quantidade": 420, "validade": "2026-05", "codigo": "849302"},
    {"nome": "Losartana", "tipo": "Anti-hipertensivo", "quantidade": 320, "validade": "2025-10", "codigo": "859607"},
    {"nome": "Meloxicam", "tipo": "Anti-inflamatório", "quantidade": 200, "validade": "2026-06", "codigo": "460182"},
    {"nome": "Metamizol", "tipo": "Antitérmico", "quantidade": 950, "validade": "2026-07", "codigo": "509384"},
    {"nome": "Metformina", "tipo": "Antidiabético", "quantidade": 370, "validade": "2025-09", "codigo": "182930"},
    {"nome": "Nimesulida", "tipo": "Anti-inflamatório", "quantidade": 350, "validade": "2025-07", "codigo": "374920"},
    {"nome": "Oseltamivir", "tipo": "Antiviral", "quantidade": 900, "validade": "2026-06", "codigo": "638475"},
    {"nome": "Paracetamol", "tipo": "Analgésico", "quantidade": 100, "validade": "2025-11", "codigo": "346865"},
    {"nome": "Sertralina", "tipo": "Psicotrópico", "quantidade": 840, "validade": "2025-12", "codigo": "637485"},
    {"nome": "Vitamina D3", "tipo": "Vitamina/Suplemento", "quantidade": 630, "validade": "2025-07", "codigo": "748596"},
    {"nome": "Zanamivir", "tipo": "Antiviral", "quantidade": 1000, "validade": "2026-05", "codigo": "748596"},
]

# Lista onde será armazenado o histórico de mudanças feitas
remedios_historico = []
historico_acoes = []

# Estrutura de fila e pilha que futuramente vai receber suas respectivas funções. A fila vai registrar consumos diários em ordem cronológica e a pilha irá registrar as consultas dos remédios

fila_consumo = deque()
pilha_consultas = []     


# Função para registrar consumo, nela podemos observar o requisito de fila sendo utilizado. Ea também faz parte do histórico de ações do sistema. O registro é feito por meio de um dicionário, contendo as informações como data de adição, nome do remédio, quantidade e o tipo de operação.
def registrar_consumo(remedio_nome, quantidade, tipo_operacao):
    registro = {
        "data": datetime.datetime.now().strftime("%d/%m/%Y" + " | " "%H:%M:%S"),
        "remedio": remedio_nome,
        "quantidade": quantidade,
        "tipo_operacao": tipo_operacao
    }
    fila_consumo.append(registro)
    historico_acoes.append(f"{registro['data']} - {tipo_operacao} de {quantidade} unidades do remédio '{remedio_nome}'.")

# Função para registrar consulta de remédios
def registrar_consulta(remedio_nome):
    consulta = {
        "data": datetime.datetime.now().strftime("%d/%m/%Y" + " | " "%H:%M:%S"),
        "remedio": remedio_nome
    }
    pilha_consultas.append(consulta)

# Função para mostrar últimas consultas com base no registro e na data do registro sendo usada como parâmetro.
def mostrar_ultimas_consultas():
    print("\n----- Últimas Consultas -----")
    if not pilha_consultas:
        print("Nenhuma consulta registrada.")
    else:
        for registro in reversed(pilha_consultas):
            print(f"{registro['data']} - {registro['remedio']}")

# Função responsável por ordenar a lista de remédios em ordem alfabética com base no tipo, usando o algoritmo de seleção (selection sort), ignorando diferenças de maiúsculas e minúsculas.
def ordenar_por_tipo(lista):
    percorrer = len(lista)
    for i in range(percorrer):
        menor = i
        for k in range(i + 1, percorrer):
            if lista[k]['tipo'].lower() < lista[menor]['tipo'].lower():
                menor = k
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista


# Função que exibe o menu no terminal
def menu():
    print("\nBem-vindo ao Steve")
    print("1. Exibir remédios")
    print("2. Buscar remédio")  
    print("3. Atualizar informações")
    print("4. Inserir novo remédio")
    print("5. Remover remédio")
    print("6. Solicitar novo lote de remédios")
    print("7. Listar remédios próximos a validade")
    print("8. Histórico de ações")
    print("9. Alertas por e-mail")
    print("10. Consultar fila de consumos")
    print("11. Consultar pilha de últimas consultas")
    print("12. Ordenar remédios por validade (Merge Sort)")
    print("13. Gerar relatório PDF")
    print("14. Sair")

#Função que exibe os remédios presente na lista de dicionários. Um "for" simples foi usado para percorrer cada item dentro da lista, imprimindo os detalhes do remédio.
def exibir_remedios():
    print('\n----- Remédios -----')
    for remedio in remedios:
        print(f"{remedio['nome']} | Tipo: {remedio['tipo']} | Quantidade: {remedio['quantidade']} | Validade: {remedio['validade']} | Código: {remedio['codigo']}")

# Função que realiza uma busca binária pelo nome do remédio na lista previamente ordenada, retornando o remédio correspondente se encontrado.
remedios.sort(key=lambda r: r['nome'].lower())

def busca_binaria(remedio_procurado):
    remedio_procurado = remedio_procurado.lower()
    inicio, fim = 0, len(remedios) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        remedio_atual = remedios[meio]['nome'].lower()

        if remedio_atual == remedio_procurado:
            registrar_consulta(remedios[meio]['nome'])
            return remedios[meio]
        elif remedio_procurado < remedio_atual:
            fim = meio - 1
        else:
            inicio = meio + 1
    return None

# Função que solicita ao usuário o nome do remédio a ser buscado e exibe os detalhes do mesmo, utilizando a busca binária para localizá-lo.
def buscar_remedio():
    while True:
        remedio = input("Digite o nome do remédio para buscar (ou 'sair' para parar): ").strip()
        if remedio.lower() == 'sair':
            break

        resultado = busca_binaria(remedio)

        if resultado:
            print(f"\nRemédio: {resultado['nome']}")
            print(f"Tipo: {resultado['tipo']}")
            print(f"Quantidade: {resultado['quantidade']}")
            print(f"Validade: {resultado['validade']}")
            print(f"Código: {resultado['codigo']}")
        else:
            print("Remédio não encontrado")

# Função recursiva e memorização que permite atualizar a quantidade de um remédio (somar ou subtrair), evitando atualizações repetidas por meio do uso de memorização.
memoria = {}

def atualizar_informacoes(memoria={}):
    nome = input("Digite o nome do remédio a ser atualizado (ou 'sair' para encerrar): ").capitalize()
    if nome.lower() == "sair":
        return

    encontrado = None
    for remedio in remedios:
        if remedio["nome"].capitalize() == nome.capitalize():
            encontrado = remedio
            break
    
    if not encontrado:
        print("Remédio não encontrado")
        return atualizar_informacoes(memoria)
    
    operacao = str(input("Digite + para somar e - para subtrair da quantidade de um remédio: "))

    try:
        valor = int(input("Digite o valor: "))
    except ValueError:
        print("Valor inválido. Digite um número inteiro.")
        return atualizar_informacoes(memoria)

    if operacao == "+":
        nova_quantidade = encontrado["quantidade"] + valor
        tipo_op = "adição"
    elif operacao == "-":
        nova_quantidade = encontrado["quantidade"] - valor
        tipo_op = "consumo"
        if nova_quantidade < 0:
            print("A quantidade não pode ser negativa.")
            return atualizar_informacoes(memoria)
    else:
        print("Operação inválida.")
        return atualizar_informacoes(memoria)

    chave_memoria = (nome, "quantidade")
    if chave_memoria in memoria and memoria[chave_memoria] == nova_quantidade:
        print("Essa atualização já foi feita. Evitando repetição.")
    else:
        memoria[chave_memoria] = nova_quantidade
        encontrado["quantidade"] = nova_quantidade
        registrar_consumo(nome, valor, tipo_op)
        print(f"Quantidade atualizada para {nova_quantidade}.")

    return atualizar_informacoes(memoria)

# Função utilizada para inserir um novo remédio na lista, solicitando ao usuário os dados principais e validando o tipo e o código do medicamento. Nela há também uma verificação se o código possui 6 dígitos e cada inserção de remédio é adicionado no histórico.
def inserir_novo_remedio():
    nome = str(input("Digite o nome do remédio: "))
    quantidade = int(input("Digite a quantidade: "))
    validade = input("Digite a validade: ")

    tipos_permitidos = ["Vitamina/Suplemento", "Psicotrópico", "Antidiabético", "Anti-hipertensivo",
                        "Antiviral", "Antifúngico", "Antialérgico", "Antitérmico", "Anti-inflamatório",
                        "Antibiótico", "Analgésico"]

    while True:
        tipo = str(input("Digite o tipo do remédio: "))
        if tipo in tipos_permitidos:
            break
        print("Tipo inválido")

    while True:
        codigo = input("Digite o código do remédio (6 dígitos): ")
        if codigo.isdigit() and len(codigo) == 6:
            break
        print("Código inválido. Deve conter exatamente 6 dígitos numéricos.")

    remedios.append({
        "nome": nome,
        "tipo": tipo,
        "quantidade": quantidade,
        "validade": validade,
        "codigo": codigo
    })
    print('Remédio inserido com sucesso')

    historico_acoes.append(
        f"Novo remédio inserido: {nome} | Tipo: {tipo} | Quantidade: {quantidade} | Validade: {validade} | Código: {codigo}"
    )


# Função que permite remover um remédio da lista com base no código informado pelo usuário, validando a entrada e confirmando a exclusão. Cada exclusão é inserido no histórico de ações.
def remover_remedio():
    try:
        remover = input("Digite o código do remédio a ser removido: ")
    except ValueError:
        print("Código inválido")
        return

    for remedio in remedios:
        if remedio["codigo"] == remover:
            remedios.remove(remedio)
            print("Remédio removido com sucesso")

            historico_acoes.append(
                f"Remédio removido: {remedio['nome']} (Código: {remedio['codigo']})"
            )
            return

    print("Nenhum remédio com esse código foi encontrado")

    historico_acoes.append(f"Tentativa de remover remédio inexistente (Código: {remover})")


# Função que permite adicionar um novo lote a um remédio existente e registra essa ação no histórico.
def solicitar_novo_lote():
    nome = input("Digite o nome do remédio: ").capitalize()
    encontrado = next((r for r in remedios if r["nome"].capitalize() == nome), None)
    
    if encontrado:
        quantidade = int(input("Digite a quantidade do novo lote: "))
        encontrado["quantidade"] += quantidade
        registrar_consumo(nome, quantidade, "adição")
        print("Lote adicionado com sucesso!")
    else:
        print("Remédio não encontrado.")


# Função que lista os remédios cuja validade expira dentro de 6 meses, exibindo nome, validade e quantidade. Convertendo a String de mês e ano para a data do primeiro dia do mês e calculando a diferença entre o dia de hoje e os meses. Essa ação também é mostrada no histórico.
def listar_proximos_validade(meses=6):
    hoje = datetime.date.today()
    print(f"\n----- Remédios com validade nos próximos {meses} meses -----")
    
    for r in remedios:
        
        validade_data = datetime.datetime.strptime(r["validade"] + "-01", "%Y-%m-%d").date()

       
        diferenca = (validade_data.year - hoje.year) * 12 + (validade_data.month - hoje.month)

        if 0 <= diferenca <= meses:
            print(f"{r['nome']} | Validade: {r['validade']} | Quantidade: {r['quantidade']}")

    historico_acoes.append(f"{datetime.datetime.now().strftime("%d/%m/%Y" + " | " "%H:%M:%S")} - Listagem de remédios próximos à validade.")

# Função responsável por exibir todas as ações realizadas no sistema, armazenadas na lista de histórico.
def mostrar_historico():
    print("\n----- Histórico de Ações -----")
    if not historico_acoes:
        print("Nenhuma ação registrada ainda.")
    else:
        for acao in historico_acoes:
            print(acao)

#Função de enviar um email ao usuário, onde temos os dados do remetente como valor fixo (conta criada por nós do grupo no gmail para uso na aplicação), o destinatário de forma dinâmica através de um input, faz o corpo do email com o histórico de ações (função vista anteriormente), gera o PDF colocando-o em anexo no email e envia ao cliente Dasa. Nesse caso o envio é feito através de uma senha gerada no google password, que se comunica através do servidor SMTP para que o envio seja certo.
def alertas_email():
    
    email_remetente = "fiapespx1@gmail.com"
    senha_app = "gjdy gxjw tjnm efyn" 

    email_destino = input("Digite o e-mail do destinatário: ")

    if not historico_acoes:
        corpo_email = "Nenhuma ação registrada ainda."
    else:
        corpo_email = "Histórico de ações do Controle de Estoque:\n\n" + "\n".join(historico_acoes)

    
    datahora = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    nome_pdf = f"Relatorio_Acoes_{datahora}.pdf"

    c = canvas.Canvas(nome_pdf, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "Relatório de Ações do Sistema Steve")
    y = 780
    for acao in historico_acoes:
        c.drawString(50, y, f"- {acao}")
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 800
    c.save()

    
    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = email_destino
    msg['Subject'] = "Histórico de Ações - Controle de Estoque"
    msg.attach(MIMEText(corpo_email, 'plain'))

    
    with open(nome_pdf, "rb") as file:
        anexo = MIMEApplication(file.read(), _subtype="pdf")
    anexo.add_header("Content-Disposition", "attachment", filename=nome_pdf)
    msg.attach(anexo)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_remetente, senha_app)
        server.send_message(msg)
        server.quit()
        print(f"E-mail enviado com sucesso para {email_destino}!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Função que ordena uma lista de dicionários pelo campo validade, verifica se tem mais de um elemento, depois, separa a lista em duas metades, L (left) e R (right). A partir disso ele vai fazer uma verificação com base no índice, para ver qual lado possui o maior número, avançando-o.
def merge_sort_validade(lista):
    if len(lista) > 1:
        mid = len(lista) // 2
        L = lista[:mid]
        R = lista[mid:]

        merge_sort_validade(L)
        merge_sort_validade(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i]["validade"] <= R[j]["validade"]:
                lista[k] = L[i]
                i += 1
            else:
                lista[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            lista[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            lista[k] = R[j]
            j += 1
            k += 1


# Função que gera um pdf com o histórico de ações realizadas. Primeiramente ele verifica se há alguma alteração feita, caso tenha ele cria o PDF com base nas proporções escolhidas para a folha, colocando de maneira organizada o conteúdo.
def gerar_relatorio_pdf():
    if not historico_acoes:
        print("Nenhuma ação registrada para gerar relatório.")
        return
    
    nome_arquivo = f"Relatorio_Acoes.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "Relatório de Ações do Sistema Steve")
    
    y = 780
    for acao in historico_acoes:
        c.drawString(50, y, f"- {acao}")
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 800

    c.save()
    print(f"Relatório gerado com sucesso: {nome_arquivo}")

# Função que encerra o programa 
def sair():
    print("Saindo do sistema... Até mais!")
    exit()

# Função principal que fica rodando, permitindo que o usuário acesse as funções
def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            exibir_remedios()
        elif opcao == "2":
            buscar_remedio()
        elif opcao == "3":
            atualizar_informacoes()
        elif opcao == "4":
            inserir_novo_remedio()
        elif opcao == "5":
            remover_remedio()
        elif opcao == "6":
            solicitar_novo_lote()
        elif opcao == "7":
            listar_proximos_validade()
        elif opcao == "8":
            mostrar_historico()
        elif opcao == "9":
            alertas_email()
        elif opcao == "10":
            print("\n----- Fila de Consumso (Cronológico) -----")
            if not fila_consumo:
                print("Nenhum registro de consumo.")
            else:
                for registro in fila_consumo:
                    print(f"{registro['data']} - {registro['tipo_operacao']} de {registro['quantidade']} do remédio {registro['remedio']}")
        elif opcao == "11":
            mostrar_ultimas_consultas()
        elif opcao == "12":
            merge_sort_validade(remedios)
            print("Remédios ordenados por validade com Merge Sort:")
            exibir_remedios()
        elif opcao == "13":
            gerar_relatorio_pdf()
        elif opcao == "14":
            sair()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()