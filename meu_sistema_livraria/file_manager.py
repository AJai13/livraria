"""
Módulo para gerenciamento de arquivos, backups e operações CSV.
Implementa funcionalidades de backup automático, exportação/importação CSV
e limpeza de backups antigos.
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import logging

# Configuração de logging
logger = logging.getLogger(__name__)


class FileManager:
    """Classe responsável por gerenciar operações de arquivo e backup."""
    
    def __init__(self, base_dir: str = "."):
        """
        Inicializa o gerenciador de arquivos.
        
        Args:
            base_dir: Diretório base do projeto
        """
        self.base_dir = Path(base_dir)
        self.backups_dir = self.base_dir / "backups"
        self.data_dir = self.base_dir / "data"
        self.exports_dir = self.base_dir / "exports"
        
        # Criar diretórios se não existirem
        self._criar_diretorios()
    
    def _criar_diretorios(self) -> None:
        """Cria os diretórios necessários se não existirem."""
        try:
            self.backups_dir.mkdir(parents=True, exist_ok=True)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.exports_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Diretórios criados/verificados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar diretórios: {e}")
            raise
    
    def fazer_backup(self, source_db_path: Path) -> str:
        """
        Cria um backup do banco de dados com timestamp.
        
        Args:
            source_db_path: Caminho do banco de dados a ser copiado
            
        Returns:
            Caminho do arquivo de backup criado
        """
        try:
            if not source_db_path.exists():
                logger.warning(f"Arquivo de origem não existe: {source_db_path}")
                return None
            
            # Gerar nome do backup com timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"backup_livraria_{timestamp}.db"
            backup_path = self.backups_dir / backup_filename
            
            # Copiar o arquivo
            shutil.copy2(source_db_path, backup_path)
            logger.info(f"Backup criado: {backup_path}")
            
            # Limpar backups antigos
            self._limpar_backups_antigos()
            
            return str(backup_path)
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            raise
    
    def _limpar_backups_antigos(self, max_backups: int = 5) -> None:
        """
        Remove backups antigos, mantendo apenas os mais recentes.
        
        Args:
            max_backups: Número máximo de backups a manter
        """
        try:
            # Listar todos os backups ordenados por data de modificação
            backup_files = [f for f in self.backups_dir.glob("backup_livraria_*.db")]
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remover backups excedentes
            for backup_file in backup_files[max_backups:]:
                backup_file.unlink()
                logger.info(f"Backup antigo removido: {backup_file}")
                
            logger.info(f"Limpeza de backups concluída. {len(backup_files[:max_backups])} backups mantidos.")
        except Exception as e:
            logger.error(f"Erro ao limpar backups antigos: {e}")
    
    def exportar_para_csv(self, livros: List[Tuple], filename: str = "livros_exportados.csv") -> str:
        """
        Exporta dados de livros para um arquivo CSV.
        
        Args:
            livros: Lista de tuplas com dados dos livros
            filename: Nome do arquivo CSV a ser criado
            
        Returns:
            Caminho do arquivo CSV criado
        """
        try:
            csv_path = self.exports_dir / filename
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escrever cabeçalho
                writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
                
                # Escrever dados
                for livro in livros:
                    writer.writerow(livro)
            
            logger.info(f"Dados exportados para CSV: {csv_path}")
            return str(csv_path)
        except Exception as e:
            logger.error(f"Erro ao exportar para CSV: {e}")
            raise
    
    def importar_de_csv(self, filename: str) -> List[Tuple]:
        """
        Importa dados de livros de um arquivo CSV.
        
        Args:
            filename: Nome do arquivo CSV para importar
            
        Returns:
            Lista de tuplas com dados dos livros (sem ID)
        """
        try:
            csv_path = self.exports_dir / filename
            
            if not csv_path.exists():
                raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")
            
            livros = []
            with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                # Pular cabeçalho
                next(reader, None)
                
                for row in reader:
                    if len(row) >= 4:  # Mínimo de campos necessários (sem ID)
                        # Converter tipos de dados
                        try:
                            if len(row) == 5:  # Com ID
                                titulo = row[1]
                                autor = row[2]
                                ano = int(row[3])
                                preco = float(row[4])
                            else:  # Sem ID
                                titulo = row[0]
                                autor = row[1]
                                ano = int(row[2])
                                preco = float(row[3])
                            
                            livros.append((titulo, autor, ano, preco))
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Linha inválida ignorada: {row} - Erro: {e}")
                            continue
            
            logger.info(f"Importados {len(livros)} livros do CSV: {csv_path}")
            return livros
        except Exception as e:
            logger.error(f"Erro ao importar CSV: {e}")
            raise
    
    def listar_backups(self) -> List[Path]:
        """
        Lista todos os arquivos de backup disponíveis.
        
        Returns:
            Lista de caminhos dos arquivos de backup
        """
        try:
            backup_files = list(self.backups_dir.glob("backup_livraria_*.db"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return backup_files
        except Exception as e:
            logger.error(f"Erro ao listar backups: {e}")
            return []
    
    def listar_exports(self) -> List[Path]:
        """
        Lista todos os arquivos CSV de exportação disponíveis.
        
        Returns:
            Lista de caminhos dos arquivos CSV
        """
        try:
            csv_files = list(self.exports_dir.glob("*.csv"))
            csv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return csv_files
        except Exception as e:
            logger.error(f"Erro ao listar exports: {e}")
            return []
    
    def obter_tamanho_arquivo(self, file_path: Path) -> str:
        """
        Obtém o tamanho de um arquivo formatado.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Tamanho formatado do arquivo
        """
        try:
            if file_path.exists():
                size_bytes = file_path.stat().st_size
                if size_bytes < 1024:
                    return f"{size_bytes} B"
                elif size_bytes < 1024**2:
                    return f"{size_bytes/1024:.1f} KB"
                else:
                    return f"{size_bytes/(1024**2):.1f} MB"
            return "N/A"
        except Exception as e:
            logger.error(f"Erro ao obter tamanho do arquivo: {e}")
            return "Erro"
    
    def criar_arquivo_exemplo_csv(self) -> str:
        """
        Cria um arquivo CSV de exemplo para importação.
        
        Returns:
            Caminho do arquivo CSV de exemplo criado
        """
        try:
            exemplo_path = self.exports_dir / "exemplo_importacao.csv"
            
            dados_exemplo = [
                ['Título', 'Autor', 'Ano de Publicação', 'Preço'],
                ['1984', 'George Orwell', 1949, 29.90],
                ['Dom Casmurro', 'Machado de Assis', 1899, 25.50],
                ['O Cortiço', 'Aluísio Azevedo', 1890, 22.80],
                ['O Alquimista', 'Paulo Coelho', 1988, 32.00],
                ['Capitães da Areia', 'Jorge Amado', 1937, 28.70]
            ]
            
            with open(exemplo_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(dados_exemplo)
            
            logger.info(f"Arquivo CSV de exemplo criado: {exemplo_path}")
            return str(exemplo_path)
        except Exception as e:
            logger.error(f"Erro ao criar arquivo de exemplo: {e}")
            raise