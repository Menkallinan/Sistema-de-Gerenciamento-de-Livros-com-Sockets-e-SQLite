import socket
import bd  

class CRUD:

    def __init__(self):
        self.banco = bd.Banco()
        self.escutador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.escutador.bind(('', 50000))

    def esperarConexao(self):
        self.escutador.listen(1)
        socket_cliente, dados_cliente = self.escutador.accept()
        self.processarPedidos(socket_cliente)

    def processarPedidos(self, socket_cliente: socket.socket):
        cliente_conectado = True
        while cliente_conectado:
            opcode = socket_cliente.recv(1)
            if not opcode:
                cliente_conectado = False
            else:
                opcode = int.from_bytes(opcode, 'big')
                match opcode:
                    case 1:  # Inserção
                        # Recebe nome
                        tam_nome = int.from_bytes(socket_cliente.recv(1), 'big')
                        nome = socket_cliente.recv(tam_nome).decode()

                        # Recebe autor
                        tam_autor = int.from_bytes(socket_cliente.recv(1), 'big')
                        autor = socket_cliente.recv(tam_autor).decode()

                        # Recebe edicao (agora como inteiro)
                        edicao = int.from_bytes(socket_cliente.recv(1), 'big')

                        # Recebe idioma
                        tam_idioma = int.from_bytes(socket_cliente.recv(1), 'big')
                        idioma = socket_cliente.recv(tam_idioma).decode()

                        id = self.adicionar(nome, autor, edicao, idioma)

                        if id is None:
                            id = -1

                        msg = opcode.to_bytes(1, 'big') + id.to_bytes(1, 'big', signed=True)
                        socket_cliente.send(msg)

                    case 2:  # Busca
                        id = int.from_bytes(socket_cliente.recv(1), 'big')
                        retorno = self.banco.buscar(id)
                        if retorno is None:
                            opcode = 6
                            msg = opcode.to_bytes(1, 'big')
                            socket_cliente.send(msg)
                        else:
                            nome = retorno[1]
                            autor = retorno[2]
                            edicao = retorno[3]
                            idioma = retorno[4]

                            msg = opcode.to_bytes(1, 'big')
                            msg += id.to_bytes(1, 'big')
                            msg += len(nome.encode()).to_bytes(1, 'big') + nome.encode()
                            msg += len(autor.encode()).to_bytes(1, 'big') + autor.encode()
                            msg += edicao.to_bytes(1, 'big')
                            msg += len(idioma.encode()).to_bytes(1, 'big') + idioma.encode()

                            socket_cliente.send(msg)

                    case 3:  # Remoção
                        id = int.from_bytes(socket_cliente.recv(1), 'big')
                        sucesso = self.banco.remover(id)
                        
                        if sucesso:
                            resposta = opcode.to_bytes(1, 'big') + b'\x01'  # 1 para sucesso
                        else:
                            resposta = opcode.to_bytes(1, 'big') + b'\x00'  # 0 para falha
                        
                        socket_cliente.send(resposta)

                    case 4:  # Atualização completa

                        id = int.from_bytes(socket_cliente.recv(1), 'big')

                        # Verifica se o ID existe antes de continuar
                        registro = self.banco.buscar(id)
                        if not registro:
                            resposta = opcode.to_bytes(1, 'big') + b'\x00'  # Falha: ID não encontrado
                            socket_cliente.send(resposta)
                            continue  # Continua ouvindo pedidos do cliente, não encerra a conexão

                        tam_nome = int.from_bytes(socket_cliente.recv(1), 'big')
                        nome = socket_cliente.recv(tam_nome).decode()

                        tam_autor = int.from_bytes(socket_cliente.recv(1), 'big')
                        autor = socket_cliente.recv(tam_autor).decode()

                        edicao = int.from_bytes(socket_cliente.recv(1), 'big')

                        tam_idioma = int.from_bytes(socket_cliente.recv(1), 'big')
                        idioma = socket_cliente.recv(tam_idioma).decode()

                        sucesso = self.banco.atualizar(id, nome, autor, edicao, idioma)

                        resposta = opcode.to_bytes(1, 'big') + (b'\x01' if sucesso else b'\x00')
                        socket_cliente.send(resposta)


    def adicionar(self, nome, autor, edicao, idioma):
        id = self.banco.adicionar(None, nome, autor, edicao, idioma)
        return id

def main():
    c = CRUD()
    while True:
        c.esperarConexao()

if __name__ == '__main__':
    main()
