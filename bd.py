import sqlite3

class Banco:

    def __init__(self):
        self.conexao = sqlite3.connect("biblioteca.db")
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS teste(id INTEGER PRIMARY KEY, nome TEXT, autor TEXT, edicao INTEGER, idioma TEXT)")
        self.conexao.commit()
        cursor.close()

    def adicionar(self, id, nome, autor, edicao, idioma):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO teste(nome, autor, edicao, idioma) VALUES(?, ?, ?, ?)', (nome, autor, edicao, idioma))
        if cursor.rowcount > 0:
            id = cursor.lastrowid
        else:
            id = None
        self.conexao.commit()
        cursor.close()
        return id
    
    def buscar(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM teste WHERE id = ?', (id,))
        retorno = cursor.fetchone()
        cursor.close()
        return retorno
    
    def remover(self, id):
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM teste WHERE id = ?', (id,))
        self.conexao.commit()
        sucesso = cursor.rowcount > 0
        cursor.close()
        return sucesso
    
    def atualizar(self, id, nome, autor, edicao, idioma):
        cursor = self.conexao.cursor()
        cursor.execute('''
            UPDATE teste 
            SET nome = ?, autor = ?, edicao = ?, idioma = ?
            WHERE id = ?
        ''', (nome, autor, edicao, idioma, id))
        
        sucesso = cursor.rowcount > 0
        self.conexao.commit()
        cursor.close()
        return sucesso
