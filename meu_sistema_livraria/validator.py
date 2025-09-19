"""
Módulo para validação de entradas de dados.
Implementa validações para todos os campos de entrada do sistema de livraria.
"""

import re
from datetime import datetime
from typing import Tuple, Optional
import logging

# Configuração de logging
logger = logging.getLogger(__name__)


class ValidadorDados:
    """Classe responsável por validar entradas de dados do sistema."""
    
    @staticmethod
    def validar_titulo(titulo: str) -> Tuple[bool, str]:
        """
        Valida o título de um livro.
        
        Args:
            titulo: Título a ser validado
            
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if not titulo or not titulo.strip():
            return False, "O título não pode estar vazio."
        
        titulo = titulo.strip()
        
        if len(titulo) < 2:
            return False, "O título deve ter pelo menos 2 caracteres."
        
        if len(titulo) > 200:
            return False, "O título não pode ter mais de 200 caracteres."
        
        # Verificar se contém apenas caracteres válidos
        if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-\.\,\:\;\!\?\'\"\(\)]+$', titulo):
            return False, "O título contém caracteres inválidos."
        
        return True, ""
    
    @staticmethod
    def validar_autor(autor: str) -> Tuple[bool, str]:
        """
        Valida o nome do autor.
        
        Args:
            autor: Nome do autor a ser validado
            
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if not autor or not autor.strip():
            return False, "O nome do autor não pode estar vazio."
        
        autor = autor.strip()
        
        if len(autor) < 2:
            return False, "O nome do autor deve ter pelo menos 2 caracteres."
        
        if len(autor) > 100:
            return False, "O nome do autor não pode ter mais de 100 caracteres."
        
        # Verificar se contém apenas letras, espaços e alguns caracteres especiais
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\.\']+$', autor):
            return False, "O nome do autor deve conter apenas letras, espaços, hífens, pontos e apóstrofos."
        
        return True, ""
    
    @staticmethod
    def validar_ano_publicacao(ano_str: str) -> Tuple[bool, str, Optional[int]]:
        """
        Valida o ano de publicação.
        
        Args:
            ano_str: Ano como string a ser validado
            
        Returns:
            Tupla (é_válido, mensagem_erro, ano_convertido)
        """
        if not ano_str or not ano_str.strip():
            return False, "O ano de publicação não pode estar vazio.", None
        
        try:
            ano = int(ano_str.strip())
        except ValueError:
            return False, "O ano de publicação deve ser um número inteiro.", None
        
        ano_atual = datetime.now().year
        
        if ano < 1:
            return False, "O ano de publicação deve ser maior que zero.", None
        
        if ano > ano_atual:
            return False, f"O ano de publicação não pode ser maior que {ano_atual}.", None
        
        # Verificar se é um ano razoável (depois da invenção da imprensa)
        if ano < 1450:
            return False, "O ano de publicação deve ser posterior a 1450.", None
        
        return True, "", ano
    
    @staticmethod
    def validar_preco(preco_str: str) -> Tuple[bool, str, Optional[float]]:
        """
        Valida o preço do livro.
        
        Args:
            preco_str: Preço como string a ser validado
            
        Returns:
            Tupla (é_válido, mensagem_erro, preco_convertido)
        """
        if not preco_str or not preco_str.strip():
            return False, "O preço não pode estar vazio.", None
        
        # Limpar a string (remover espaços e aceitar vírgula como separador decimal)
        preco_str = preco_str.strip().replace(',', '.')
        
        # Remover símbolo de moeda se presente
        preco_str = re.sub(r'[R$\s]', '', preco_str)
        
        try:
            preco = float(preco_str)
        except ValueError:
            return False, "O preço deve ser um número válido.", None
        
        if preco < 0:
            return False, "O preço não pode ser negativo.", None
        
        if preco == 0:
            return False, "O preço deve ser maior que zero.", None
        
        if preco > 9999.99:
            return False, "O preço não pode ser maior que R$ 9.999,99.", None
        
        # Arredondar para 2 casas decimais
        preco = round(preco, 2)
        
        return True, "", preco
    
    @staticmethod
    def validar_id(id_str: str) -> Tuple[bool, str, Optional[int]]:
        """
        Valida um ID.
        
        Args:
            id_str: ID como string a ser validado
            
        Returns:
            Tupla (é_válido, mensagem_erro, id_convertido)
        """
        if not id_str or not id_str.strip():
            return False, "O ID não pode estar vazio.", None
        
        try:
            id_valor = int(id_str.strip())
        except ValueError:
            return False, "O ID deve ser um número inteiro.", None
        
        if id_valor <= 0:
            return False, "O ID deve ser um número positivo.", None
        
        return True, "", id_valor
    
    @staticmethod
    def validar_nome_arquivo(nome_arquivo: str) -> Tuple[bool, str]:
        """
        Valida um nome de arquivo.
        
        Args:
            nome_arquivo: Nome do arquivo a ser validado
            
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if not nome_arquivo or not nome_arquivo.strip():
            return False, "O nome do arquivo não pode estar vazio."
        
        nome_arquivo = nome_arquivo.strip()
        
        if len(nome_arquivo) < 1:
            return False, "O nome do arquivo deve ter pelo menos 1 caractere."
        
        if len(nome_arquivo) > 100:
            return False, "O nome do arquivo não pode ter mais de 100 caracteres."
        
        # Verificar caracteres inválidos para nomes de arquivo
        caracteres_invalidos = r'[<>:"/\\|?*]'
        if re.search(caracteres_invalidos, nome_arquivo):
            return False, "O nome do arquivo contém caracteres inválidos: < > : \" / \\ | ? *"
        
        return True, ""
    
    @staticmethod
    def formatar_preco(preco: float) -> str:
        """
        Formata um preço para exibição.
        
        Args:
            preco: Preço a ser formatado
            
        Returns:
            Preço formatado como string
        """
        return f"R$ {preco:.2f}".replace('.', ',')
    
    @staticmethod
    def solicitar_entrada_validada(prompt: str, validador_func, *args) -> any:
        """
        Solicita entrada do usuário com validação até obter valor válido.
        
        Args:
            prompt: Mensagem a ser exibida
            validador_func: Função de validação a ser aplicada
            *args: Argumentos adicionais para a função validadora
            
        Returns:
            Valor validado
        """
        while True:
            entrada = input(prompt).strip()
            
            # Se a função retorna tupla com 3 elementos (bool, str, valor)
            resultado = validador_func(entrada, *args)
            if len(resultado) == 3:
                valido, erro, valor = resultado
                if valido:
                    return valor
                else:
                    print(f"❌ Erro: {erro}")
            # Se a função retorna tupla com 2 elementos (bool, str)
            elif len(resultado) == 2:
                valido, erro = resultado
                if valido:
                    return entrada.strip()
                else:
                    print(f"❌ Erro: {erro}")
            
            print("Tente novamente.\n")