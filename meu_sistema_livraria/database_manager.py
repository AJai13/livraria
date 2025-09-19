"""
Módulo para gerenciamento do banco de dados SQLite da livraria.
Implementa as operações CRUD para a entidade Livros.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Classe responsável por gerenciar as operações do banco de dados SQLite."""
    
    def __init__(self, db_path: str = "data/livraria.db"):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._criar_tabela()
    
    def _criar_tabela(self) -> None:
        """Cria a tabela de livros se ela não existir."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS livros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        autor TEXT NOT NULL,
                        ano_publicacao INTEGER NOT NULL,
                        preco REAL NOT NULL
                    )
                ''')
                conn.commit()
                logger.info("Tabela 'livros' criada/verificada com sucesso")
        except sqlite3.Error as e:
            logger.error(f"Erro ao criar tabela: {e}")
            raise
    
    def adicionar_livro(self, titulo: str, autor: str, ano_publicacao: int, preco: float) -> int:
        """
        Adiciona um novo livro ao banco de dados.
        
        Args:
            titulo: Título do livro
            autor: Autor do livro
            ano_publicacao: Ano de publicação
            preco: Preço do livro
            
        Returns:
            ID do livro inserido
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                    VALUES (?, ?, ?, ?)
                ''', (titulo, autor, ano_publicacao, preco))
                conn.commit()
                livro_id = cursor.lastrowid
                logger.info(f"Livro '{titulo}' adicionado com ID: {livro_id}")
                return livro_id
        except sqlite3.Error as e:
            logger.error(f"Erro ao adicionar livro: {e}")
            raise
    
    def listar_livros(self) -> List[Tuple]:
        """
        Lista todos os livros cadastrados.
        
        Returns:
            Lista de tuplas com informações dos livros
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM livros ORDER BY titulo')
                livros = cursor.fetchall()
                logger.info(f"Listados {len(livros)} livros")
                return livros
        except sqlite3.Error as e:
            logger.error(f"Erro ao listar livros: {e}")
            raise
    
    def buscar_livro_por_id(self, livro_id: int) -> Optional[Tuple]:
        """
        Busca um livro específico pelo ID.
        
        Args:
            livro_id: ID do livro
            
        Returns:
            Tupla com informações do livro ou None se não encontrado
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
                livro = cursor.fetchone()
                if livro:
                    logger.info(f"Livro encontrado: ID {livro_id}")
                else:
                    logger.warning(f"Livro com ID {livro_id} não encontrado")
                return livro
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar livro: {e}")
            raise
    
    def buscar_livros_por_autor(self, autor: str) -> List[Tuple]:
        """
        Busca livros por autor.
        
        Args:
            autor: Nome do autor (busca parcial)
            
        Returns:
            Lista de tuplas com informações dos livros
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM livros WHERE autor LIKE ? ORDER BY titulo', 
                             (f'%{autor}%',))
                livros = cursor.fetchall()
                logger.info(f"Encontrados {len(livros)} livros do autor '{autor}'")
                return livros
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar livros por autor: {e}")
            raise
    
    def atualizar_preco(self, livro_id: int, novo_preco: float) -> bool:
        """
        Atualiza o preço de um livro.
        
        Args:
            livro_id: ID do livro
            novo_preco: Novo preço do livro
            
        Returns:
            True se a atualização foi bem-sucedida, False caso contrário
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE livros SET preco = ? WHERE id = ?', 
                             (novo_preco, livro_id))
                conn.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Preço do livro ID {livro_id} atualizado para R$ {novo_preco:.2f}")
                    return True
                else:
                    logger.warning(f"Livro com ID {livro_id} não encontrado para atualização")
                    return False
        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar preço: {e}")
            raise
    
    def remover_livro(self, livro_id: int) -> bool:
        """
        Remove um livro do banco de dados.
        
        Args:
            livro_id: ID do livro a ser removido
            
        Returns:
            True se a remoção foi bem-sucedida, False caso contrário
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Livro ID {livro_id} removido com sucesso")
                    return True
                else:
                    logger.warning(f"Livro com ID {livro_id} não encontrado para remoção")
                    return False
        except sqlite3.Error as e:
            logger.error(f"Erro ao remover livro: {e}")
            raise
    
    def contar_livros(self) -> int:
        """
        Conta o total de livros cadastrados.
        
        Returns:
            Número total de livros
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM livros')
                total = cursor.fetchone()[0]
                return total
        except sqlite3.Error as e:
            logger.error(f"Erro ao contar livros: {e}")
            raise
    
    def get_database_path(self) -> Path:
        """
        Retorna o caminho do banco de dados.
        
        Returns:
            Objeto Path do banco de dados
        """
        return self.db_path