import socket
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 50000))

opcao = None
while opcao != 5:
    
    opcao = int(input('Digite 1 para inserir, 2 para buscar, 3 para remover, 4 para atualizar, 5 para sair: '))
    match opcao:
        
        case 1:
            clear()
            nome = input('Digite o nome do livro: ')
            autor = input('Digite o nome do autor: ')
            edicao = int(input('Digite a edição do livro: '))
            idioma = input('Digite o idioma do livro: ')

            msg = opcao.to_bytes(1, 'big')
            msg += len(nome.encode()).to_bytes(1, 'big') + nome.encode()
            msg += len(autor.encode()).to_bytes(1, 'big') + autor.encode()
            msg += edicao.to_bytes(1, 'big')  # edicao como inteiro de 1 byte
            msg += len(idioma.encode()).to_bytes(1, 'big') + idioma.encode()

            cliente.send(msg)
            opcode = cliente.recv(1)
            id = cliente.recv(1)
            id = int.from_bytes(id, 'big', signed=True)
            print("Livro inserido com ID:", id)

        case 2:
            clear()
            id = int(input('Digite o ID do livro para busca: '))
            msg = opcao.to_bytes(1, 'big') + id.to_bytes(1, 'big')
            cliente.send(msg)

            opcode = cliente.recv(1)
            opcode = int.from_bytes(opcode, 'big')

            if opcode == 6:
                print('Livro não encontrado.')
            else:
                id = int.from_bytes(cliente.recv(1), 'big')

                tam_nome = int.from_bytes(cliente.recv(1), 'big')
                nome = cliente.recv(tam_nome).decode()

                tam_autor = int.from_bytes(cliente.recv(1), 'big')
                autor = cliente.recv(tam_autor).decode()

                edicao = int.from_bytes(cliente.recv(1), 'big')

                tam_idioma = int.from_bytes(cliente.recv(1), 'big')
                idioma = cliente.recv(tam_idioma).decode()

                print(f'Dados encontrados:\nID: {id}\nNome: {nome}\nAutor: {autor}\nEdição: {edicao}\nIdioma: {idioma}')

        case 3:
            clear()
            id = int(input('Digite o ID do livro para remover: '))
            msg = opcao.to_bytes(1, 'big') + id.to_bytes(1, 'big')
            cliente.send(msg)

            resposta = cliente.recv(2)
            opcode = resposta[0]
            status = resposta[1]

            if status == 1:
                print("Livro removido com sucesso.")
            else:
                print("Livro não encontrado.")

        case 4:
            clear()
            id = int(input('Digite o ID do livro para atualizar: '))

            # --- VERIFICAÇÃO PRÉVIA DO ID ANTES DE PEDIR NOVOS DADOS ---
            msg_verifica = (2).to_bytes(1, 'big') + id.to_bytes(1, 'big')
            cliente.send(msg_verifica)

            opcode = int.from_bytes(cliente.recv(1), 'big')

            if opcode == 6:
                print("Livro não encontrado para atualização.")
                continue  # Volta para o menu

            # --- Se chegou aqui, o ID existe ---
            # Recebe os dados do livro atual só para limpar o buffer (ou opcionalmente mostrar ao usuário)
            cliente.recv(1)  # ID (descarta)
            tam_nome = int.from_bytes(cliente.recv(1), 'big')
            cliente.recv(tam_nome)
            tam_autor = int.from_bytes(cliente.recv(1), 'big')
            cliente.recv(tam_autor)
            cliente.recv(1)  # edição
            tam_idioma = int.from_bytes(cliente.recv(1), 'big')
            cliente.recv(tam_idioma)

            # Agora pede os novos dados
            nome = input('Digite o novo nome do livro: ')
            autor = input('Digite o novo nome do autor: ')
            edicao = int(input('Digite a nova edição do livro: '))
            idioma = input('Digite o novo idioma do livro: ')

            msg = opcao.to_bytes(1, 'big')
            msg += id.to_bytes(1, 'big')
            msg += len(nome.encode()).to_bytes(1, 'big') + nome.encode()
            msg += len(autor.encode()).to_bytes(1, 'big') + autor.encode()
            msg += edicao.to_bytes(1, 'big')
            msg += len(idioma.encode()).to_bytes(1, 'big') + idioma.encode()

            cliente.send(msg)

            resposta = cliente.recv(2)
            status = resposta[1]

            if status == 1:
                print("Livro atualizado com sucesso.")
            else:
                print("Erro inesperado ao atualizar.")

        case 5:
            print("Encerrando conexão...")

cliente.close()
