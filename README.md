# 📚 CRUD de Livros com Sockets em Python

Este projeto implementa uma aplicação cliente-servidor para gerenciamento de livros (CRUD) utilizando sockets TCP em Python e armazenamento com SQLite.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x  
- Sockets TCP (módulo `socket`)
- SQLite3

---

## 📁 Estrutura de Arquivos

- `bd.py` → Responsável pela criação do banco de dados SQLite e operações CRUD na tabela `teste`.
- `crudServer.py` → Servidor que escuta conexões de clientes e processa as requisições de inserção, busca, remoção e atualização.
- `crudCliente.py` → Interface em linha de comando para o usuário interagir com o sistema via socket TCP.

---

## ▶️ Como Executar

### 1. Execute o servidor

```bash
python crudServer.py
```

> O servidor ficará escutando na porta `50000`.

### 2. Em outro terminal, execute o cliente

```bash
python crudCliente.py
```

---

## 📚 Funcionalidades Disponíveis (cliente)

Ao rodar o cliente, o usuário verá o menu:

- **1 - Inserir**  
  Solicita dados do livro e envia para o servidor.  
  Retorna o ID gerado.

- **2 - Buscar**  
  Solicita o ID do livro e exibe os dados se encontrado.

- **3 - Remover**  
  Solicita o ID e tenta remover o livro.

- **4 - Atualizar**  
  Verifica se o ID existe e permite modificar os dados do livro.

- **5 - Sair**  
  Encerra a conexão com o servidor.

---

## 🗃 Estrutura da Tabela

O banco de dados `biblioteca.db` possui uma única tabela chamada `teste`, com os seguintes campos:

- `id` (INTEGER PRIMARY KEY)
- `nome` (TEXT)
- `autor` (TEXT)
- `edicao` (INTEGER)
- `idioma` (TEXT)

---

## 📌 Observações

- O banco de dados é criado automaticamente na primeira execução do servidor.
- Todos os dados são trocados em bytes entre cliente e servidor.
- Os tamanhos das strings são enviados explicitamente para garantir leitura correta no lado receptor.

---

👨‍💻 Projeto simples para fins didáticos sobre comunicação com sockets e persistência de dados em Python.
