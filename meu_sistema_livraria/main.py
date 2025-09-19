"""
Sistema de Gerenciamento de Livraria
Sistema completo para gerenciar livros com banco de dados SQLite,
backup automático e operações de importação/exportação CSV.
"""

import sys
from database_manager import DatabaseManager
from file_manager import FileManager
from validator import ValidadorDados
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('livraria_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SistemaLivraria:
    """Classe principal do sistema de gerenciamento de livraria."""
    
    def __init__(self):
        """Inicializa o sistema com os componentes necessários."""
        try:
            self.db_manager = DatabaseManager("data/livraria.db")
            self.file_manager = FileManager(".")
            self.validator = ValidadorDados()
            logger.info("Sistema de livraria inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {e}")
            sys.exit(1)
    
    def exibir_menu(self) -> None:
        """Exibe o menu principal do sistema."""
        print("\n" + "="*50)
        print("    SISTEMA DE GERENCIAMENTO DE LIVRARIA")
        print("="*50)
        print("1. Adicionar novo livro")
        print("2. Exibir todos os livros")
        print("3. Atualizar preço de um livro")
        print("4. Remover um livro")
        print("5. Buscar livros por autor")
        print("6. Exportar dados para CSV")
        print("7. Importar dados de CSV")
        print("8. Fazer backup do banco de dados")
        print("9. Sair")
        print("="*50)
    
    def adicionar_livro(self) -> None:
        """Adiciona um novo livro ao sistema."""
        print("\n📖 ADICIONAR NOVO LIVRO")
        print("-" * 30)
        
        try:
            # Fazer backup antes de modificar
            self._fazer_backup_automatico("adição")
            
            # Solicitar e validar dados
            titulo = self.validator.solicitar_entrada_validada(
                "Digite o título do livro: ",
                self.validator.validar_titulo
            )
            
            autor = self.validator.solicitar_entrada_validada(
                "Digite o nome do autor: ",
                self.validator.validar_autor
            )
            
            ano = self.validator.solicitar_entrada_validada(
                "Digite o ano de publicação: ",
                self.validator.validar_ano_publicacao
            )
            
            preco = self.validator.solicitar_entrada_validada(
                "Digite o preço (ex: 29.99): R$ ",
                self.validator.validar_preco
            )
            
            # Adicionar ao banco de dados
            livro_id = self.db_manager.adicionar_livro(titulo, autor, ano, preco)
            
            print(f"\n✅ Livro adicionado com sucesso! ID: {livro_id}")
            print(f"   Título: {titulo}")
            print(f"   Autor: {autor}")
            print(f"   Ano: {ano}")
            print(f"   Preço: {self.validator.formatar_preco(preco)}")
            
        except Exception as e:
            print(f"\n❌ Erro ao adicionar livro: {e}")
            logger.error(f"Erro ao adicionar livro: {e}")
    
    def listar_livros(self) -> None:
        """Lista todos os livros cadastrados."""
        print("\n📚 TODOS OS LIVROS CADASTRADOS")
        print("-" * 40)
        
        try:
            livros = self.db_manager.listar_livros()
            
            if not livros:
                print("Nenhum livro cadastrado.")
                return
            
            print(f"Total de livros: {len(livros)}")
            print()
            
            for livro in livros:
                id_livro, titulo, autor, ano, preco = livro
                print(f"ID: {id_livro}")
                print(f"Título: {titulo}")
                print(f"Autor: {autor}")
                print(f"Ano: {ano}")
                print(f"Preço: {self.validator.formatar_preco(preco)}")
                print("-" * 40)
                
        except Exception as e:
            print(f"\n❌ Erro ao listar livros: {e}")
            logger.error(f"Erro ao listar livros: {e}")
    
    def atualizar_preco(self) -> None:
        """Atualiza o preço de um livro."""
        print("\n💰 ATUALIZAR PREÇO DE LIVRO")
        print("-" * 30)
        
        try:
            # Primeiro, mostrar livros disponíveis
            livros = self.db_manager.listar_livros()
            if not livros:
                print("Nenhum livro cadastrado.")
                return
            
            print("Livros disponíveis:")
            for livro in livros:
                id_livro, titulo, autor, ano, preco = livro
                print(f"ID: {id_livro} - {titulo} - {self.validator.formatar_preco(preco)}")
            
            print()
            
            # Solicitar ID do livro
            livro_id = self.validator.solicitar_entrada_validada(
                "Digite o ID do livro para atualizar: ",
                self.validator.validar_id
            )
            
            # Verificar se o livro existe
            livro = self.db_manager.buscar_livro_por_id(livro_id)
            if not livro:
                print(f"❌ Livro com ID {livro_id} não encontrado.")
                return
            
            # Mostrar dados atuais
            _, titulo, autor, ano, preco_atual = livro
            print("\nLivro selecionado:")
            print(f"Título: {titulo}")
            print(f"Autor: {autor}")
            print(f"Preço atual: {self.validator.formatar_preco(preco_atual)}")

            # Fazer backup antes de modificar
            self._fazer_backup_automatico("atualização")

            # Solicitar novo preço
            novo_preco = self.validator.solicitar_entrada_validada(
                "Digite o novo preço: R$ ",
                self.validator.validar_preco
            )

            # Atualizar no banco
            if self.db_manager.atualizar_preco(livro_id, novo_preco):
                print("\n✅ Preço atualizado com sucesso!")
                print(f"   Preço anterior: {self.validator.formatar_preco(preco_atual)}")
                print(f"   Novo preço: {self.validator.formatar_preco(novo_preco)}")
            else:
                print("❌ Erro ao atualizar preço.")
                
        except Exception as e:
            print(f"\n❌ Erro ao atualizar preço: {e}")
            logger.error(f"Erro ao atualizar preço: {e}")
    
    def remover_livro(self) -> None:
        """Remove um livro do sistema."""
        print("\n🗑️  REMOVER LIVRO")
        print("-" * 20)
        
        try:
            # Primeiro, mostrar livros disponíveis
            livros = self.db_manager.listar_livros()
            if not livros:
                print("Nenhum livro cadastrado.")
                return
            
            print("Livros disponíveis:")
            for livro in livros:
                id_livro, titulo, autor, ano, preco = livro
                print(f"ID: {id_livro} - {titulo} - {autor}")
            
            print()
            
            # Solicitar ID do livro
            livro_id = self.validator.solicitar_entrada_validada(
                "Digite o ID do livro para remover: ",
                self.validator.validar_id
            )
            
            # Verificar se o livro existe
            livro = self.db_manager.buscar_livro_por_id(livro_id)
            if not livro:
                print(f"❌ Livro com ID {livro_id} não encontrado.")
                return
            
            # Mostrar dados do livro
            _, titulo, autor, ano, preco = livro
            print("\nLivro selecionado:")
            print(f"Título: {titulo}")
            print(f"Autor: {autor}")
            print(f"Ano: {ano}")
            print(f"Preço: {self.validator.formatar_preco(preco)}")

            # Confirmar remoção
            confirmacao = input("\n⚠️  Tem certeza que deseja remover este livro? (s/N): ").lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                return

            # Fazer backup antes de remover
            self._fazer_backup_automatico("remoção")

            # Remover do banco
            if self.db_manager.remover_livro(livro_id):
                print("\n✅ Livro removido com sucesso!")
            else:
                print("❌ Erro ao remover livro.")
                
        except Exception as e:
            print(f"\n❌ Erro ao remover livro: {e}")
            logger.error(f"Erro ao remover livro: {e}")
    
    def buscar_por_autor(self) -> None:
        """Busca livros por autor."""
        print("\n🔍 BUSCAR LIVROS POR AUTOR")
        print("-" * 30)
        
        try:
            autor = input("Digite o nome do autor (busca parcial): ").strip()
            
            if not autor:
                print("Nome do autor não pode estar vazio.")
                return
            
            livros = self.db_manager.buscar_livros_por_autor(autor)
            
            if not livros:
                print(f"Nenhum livro encontrado para o autor '{autor}'.")
                return
            
            print(f"\n📖 Encontrados {len(livros)} livro(s) para o autor '{autor}':")
            print("-" * 50)
            
            for livro in livros:
                id_livro, titulo, autor_nome, ano, preco = livro
                print(f"ID: {id_livro}")
                print(f"Título: {titulo}")
                print(f"Autor: {autor_nome}")
                print(f"Ano: {ano}")
                print(f"Preço: {self.validator.formatar_preco(preco)}")
                print("-" * 40)
                
        except Exception as e:
            print(f"\n❌ Erro ao buscar livros: {e}")
            logger.error(f"Erro ao buscar livros: {e}")
    
    def exportar_csv(self) -> None:
        """Exporta dados para arquivo CSV."""
        print("\n📤 EXPORTAR DADOS PARA CSV")
        print("-" * 30)
        
        try:
            livros = self.db_manager.listar_livros()
            
            if not livros:
                print("Nenhum livro cadastrado para exportar.")
                return
            
            # Solicitar nome do arquivo
            nome_arquivo = input("Digite o nome do arquivo (sem extensão) ou pressione Enter para usar padrão: ").strip()
            
            if nome_arquivo:
                # Validar nome do arquivo
                valido, erro = self.validator.validar_nome_arquivo(nome_arquivo)
                if not valido:
                    print(f"❌ {erro}")
                    return
                nome_arquivo += ".csv"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"livros_exportados_{timestamp}.csv"
            
            # Exportar
            caminho_arquivo = self.file_manager.exportar_para_csv(livros, nome_arquivo)

            print("\n✅ Dados exportados com sucesso!")
            print(f"   Arquivo: {caminho_arquivo}")
            print(f"   Total de livros: {len(livros)}")
            
        except Exception as e:
            print(f"\n❌ Erro ao exportar dados: {e}")
            logger.error(f"Erro ao exportar dados: {e}")
    
    def importar_csv(self) -> None:
        """Importa dados de arquivo CSV."""
        print("\n📥 IMPORTAR DADOS DE CSV")
        print("-" * 25)
        
        try:
            # Listar arquivos CSV disponíveis
            csv_files = self.file_manager.listar_exports()
            
            if csv_files:
                print("Arquivos CSV disponíveis:")
                for i, arquivo in enumerate(csv_files, 1):
                    tamanho = self.file_manager.obter_tamanho_arquivo(arquivo)
                    print(f"{i}. {arquivo.name} ({tamanho})")
                
                print(f"{len(csv_files) + 1}. Digitar nome de arquivo manualmente")
                print(f"{len(csv_files) + 2}. Criar arquivo de exemplo")
                
                opcao = input(f"\nEscolha uma opção (1-{len(csv_files) + 2}): ").strip()
                
                if opcao.isdigit():
                    opcao = int(opcao)
                    if 1 <= opcao <= len(csv_files):
                        nome_arquivo = csv_files[opcao - 1].name
                    elif opcao == len(csv_files) + 1:
                        nome_arquivo = input("Digite o nome do arquivo CSV: ").strip()
                    elif opcao == len(csv_files) + 2:
                        self.file_manager.criar_arquivo_exemplo_csv()
                        print("✅ Arquivo de exemplo criado: exemplo_importacao.csv")
                        return
                    else:
                        print("Opção inválida.")
                        return
                else:
                    print("Opção inválida.")
                    return
            else:
                print("Nenhum arquivo CSV encontrado.")
                opcao = input("1. Digitar nome de arquivo\n2. Criar arquivo de exemplo\nEscolha: ").strip()
                
                if opcao == "1":
                    nome_arquivo = input("Digite o nome do arquivo CSV: ").strip()
                elif opcao == "2":
                    self.file_manager.criar_arquivo_exemplo_csv()
                    print("✅ Arquivo de exemplo criado: exemplo_importacao.csv")
                    return
                else:
                    print("Opção inválida.")
                    return
            
            if not nome_arquivo.endswith('.csv'):
                nome_arquivo += '.csv'
            
            # Importar dados
            print(f"\nImportando dados de: {nome_arquivo}")
            livros_importados = self.file_manager.importar_de_csv(nome_arquivo)
            
            if not livros_importados:
                print("Nenhum dado válido encontrado no arquivo CSV.")
                return
            
            # Fazer backup antes de importar
            self._fazer_backup_automatico("importação")
            
            # Adicionar livros ao banco
            livros_adicionados = 0
            for titulo, autor, ano, preco in livros_importados:
                try:
                    self.db_manager.adicionar_livro(titulo, autor, ano, preco)
                    livros_adicionados += 1
                except Exception as e:
                    print(f"⚠️  Erro ao adicionar livro '{titulo}': {e}")
            
            print("\n✅ Importação concluída!")
            print(f"   Livros processados: {len(livros_importados)}")
            print(f"   Livros adicionados: {livros_adicionados}")
            
        except Exception as e:
            print(f"\n❌ Erro ao importar dados: {e}")
            logger.error(f"Erro ao importar dados: {e}")
    
    def fazer_backup_manual(self) -> None:
        """Faz backup manual do banco de dados."""
        print("\n💾 FAZER BACKUP DO BANCO DE DADOS")
        print("-" * 35)
        
        try:
            db_path = self.db_manager.get_database_path()
            backup_path = self.file_manager.fazer_backup(db_path)
            
            if backup_path:
                print("\n✅ Backup criado com sucesso!")
                print(f"   Arquivo: {backup_path}")
                
                # Mostrar informações sobre backups
                backups = self.file_manager.listar_backups()
                print(f"   Total de backups: {len(backups)}")
                
                if backups:
                    print("\n📋 Backups disponíveis:")
                    for backup in backups[:5]:  # Mostrar apenas os 5 mais recentes
                        tamanho = self.file_manager.obter_tamanho_arquivo(backup)
                        data_mod = datetime.fromtimestamp(backup.stat().st_mtime)
                        print(f"   - {backup.name} ({tamanho}) - {data_mod.strftime('%d/%m/%Y %H:%M')}")
            else:
                print("❌ Erro ao criar backup.")
                
        except Exception as e:
            print(f"\n❌ Erro ao fazer backup: {e}")
            logger.error(f"Erro ao fazer backup: {e}")
    
    def _fazer_backup_automatico(self, operacao: str) -> None:
        """Faz backup automático antes de operações que modificam dados."""
        try:
            db_path = self.db_manager.get_database_path()
            if db_path.exists():
                backup_path = self.file_manager.fazer_backup(db_path)
                if backup_path:
                    print(f"🔄 Backup automático realizado antes da {operacao}")
                    logger.info(f"Backup automático criado para {operacao}: {backup_path}")
        except Exception as e:
            logger.warning(f"Falha no backup automático para {operacao}: {e}")
    
    def executar(self) -> None:
        """Executa o loop principal do sistema."""
        print("🚀 Sistema de Livraria iniciado com sucesso!")
        print(f"📊 Total de livros cadastrados: {self.db_manager.contar_livros()}")
        
        while True:
            try:
                self.exibir_menu()
                opcao = input("\nEscolha uma opção (1-9): ").strip()
                
                if opcao == "1":
                    self.adicionar_livro()
                elif opcao == "2":
                    self.listar_livros()
                elif opcao == "3":
                    self.atualizar_preco()
                elif opcao == "4":
                    self.remover_livro()
                elif opcao == "5":
                    self.buscar_por_autor()
                elif opcao == "6":
                    self.exportar_csv()
                elif opcao == "7":
                    self.importar_csv()
                elif opcao == "8":
                    self.fazer_backup_manual()
                elif opcao == "9":
                    print("\n👋 Obrigado por usar o Sistema de Livraria!")
                    print("📊 Estatísticas finais:")
                    print(f"   Total de livros: {self.db_manager.contar_livros()}")
                    backups = self.file_manager.listar_backups()
                    print(f"   Total de backups: {len(backups)}")
                    logger.info("Sistema encerrado pelo usuário")
                    break
                else:
                    print("\n❌ Opção inválida. Digite um número entre 1 e 9.")
                
                input("\nPressione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Sistema interrompido pelo usuário.")
                logger.info("Sistema interrompido com Ctrl+C")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                logger.error(f"Erro inesperado no loop principal: {e}")
                input("\nPressione Enter para continuar...")


def main():
    """Função principal do programa."""
    try:
        sistema = SistemaLivraria()
        sistema.executar()
    except Exception as e:
        print(f"❌ Erro crítico ao inicializar sistema: {e}")
        logger.critical(f"Erro crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()