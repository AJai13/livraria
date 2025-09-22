"""
Módulo para gerenciamento do banco de dados SQLite da livraria.
Implementa as operações CRUD para a entidade Livros.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DatabaseManager:
    
    def __init__(self, db_path: str = "data/livraria.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._criar_tabela()
    
    def _criar_tabela(self) -> None:
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
        return self.db_path