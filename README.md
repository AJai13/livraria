# Sistema de Gerenciamento de Livraria

Um sistema completo de gerenciamento de livraria desenvolvido em Python, que integra SQLite, manipulação de arquivos CSV, backup automático e validação de dados.

## Funcionalidades

### Operações CRUD Completas
- **Adicionar livros** com validação de dados
- **Listar todos os livros** cadastrados
- **Atualizar preços** de livros existentes
- **Remover livros** do sistema
- **Buscar livros por autor**

### Gerenciamento de Dados
- **Exportar dados** para arquivos CSV
- **Importar dados** de arquivos CSV
- **Backup automático** antes de modificações
- **Limpeza automática** de backups antigos (mantém 5 mais recentes)

### Validações Implementadas
- **Título**: 2-200 caracteres, caracteres válidos
- **Autor**: 2-100 caracteres, apenas letras e caracteres especiais permitidos
- **Ano**: Entre 1450 e ano atual
- **Preço**: Valores positivos até R$ 9.999,99 com formatação automática
- **Nomes de arquivo**: Caracteres válidos para sistema de arquivos

## Estrutura de Arquivos

```
meu_sistema_livraria/
├── main.py                 # Sistema principal com menu interativo
├── database_manager.py     # Gerenciamento do banco SQLite
├── file_manager.py         # Operações de arquivo e backup
├── validator.py           # Validações de entrada
├── backups/               # Backups automáticos do banco
│   ├── backup_livraria_2024-09-19_10-30-00.db
│   └── backup_livraria_2024-09-19_11-15-30.db
├── data/                  # Banco de dados principal
│   └── livraria.db
├── exports/               # Arquivos CSV exportados
│   ├── livros_exportados.csv
│   └── exemplo_importacao.csv
└── livraria_system.log    # Arquivo de log do sistema
```

## Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Bibliotecas: sqlite3, csv, pathlib, datetime, logging (todas incluídas no Python padrão)

### Execução
```bash
cd meu_sistema_livraria
python main.py
```

## Menu Principal

```
==================================================
    SISTEMA DE GERENCIAMENTO DE LIVRARIA
==================================================
1. Adicionar novo livro
2. Exibir todos os livros
3. Atualizar preço de um livro
4. Remover um livro
5. Buscar livros por autor
6. Exportar dados para CSV
7. Importar dados de CSV
8. Fazer backup do banco de dados
9. Sair
==================================================
```

## Exemplos de Uso

### Adicionando um Livro
```
 ADICIONAR NOVO LIVRO
------------------------------
Digite o título do livro: 1984
Digite o nome do autor: George Orwell
Digite o ano de publicação: 1949
Digite o preço (ex: 29.99): R$ 29,90

   Livro adicionado com sucesso! ID: 1
   Título: 1984
   Autor: George Orwell
   Ano: 1949
   Preço: R$ 29,90
```

### Importando de CSV
O sistema aceita arquivos CSV no formato:
```csv
Título,Autor,Ano de Publicação,Preço
1984,George Orwell,1949,29.90
Dom Casmurro,Machado de Assis,1899,25.50
```

### Backup Automático
- Backup é criado automaticamente antes de:
  - Adicionar livros
  - Atualizar preços
  - Remover livros
  - Importar dados CSV
- Mantém automaticamente os 5 backups mais recentes
- Formato: `backup_livraria_YYYY-MM-DD_HH-MM-SS.db`

## Recursos Técnicos

### Banco de Dados SQLite
- Tabela `livros` com campos: id, titulo, autor, ano_publicacao, preco
- Chave primária auto-incremental
- Operações CRUD completas com tratamento de erros

### Manipulação de Arquivos
- Uso de `pathlib` para operações de arquivo multiplataforma
- Criação automática de diretórios quando necessário
- Backup com timestamp para versionamento
- Limpeza automática de arquivos antigos

### Validação de Dados
- Regex para validação de formatos
- Conversão segura de tipos de dados
- Mensagens de erro descritivas
- Suporte a diferentes formatos de entrada (vírgula/ponto decimal)

### Sistema de Logs
- Registro de todas as operações importantes
- Logs salvos em `livraria_system.log`
- Diferentes níveis: INFO, WARNING, ERROR, CRITICAL

## Tratamento de Erros

O sistema implementa tratamento robusto de erros:
- **Validação de entrada**: Dados inválidos são rejeitados com mensagens claras
- **Erros de banco**: SQLite errors são capturados e logados
- **Problemas de arquivo**: Arquivos não encontrados ou permissões
- **Interrupção do usuário**: Ctrl+C tratado graciosamente
- **Backup de segurança**: Sistema continua funcionando mesmo se backup falhar

## Fluxo de Backup

1. **Antes de qualquer modificação** → Backup automático criado
2. **Operação executada** → Mudanças aplicadas no banco
3. **Limpeza automática** → Mantém apenas 5 backups mais recentes
4. **Log registrado** → Operação documentada em arquivo de log

## Recursos Extras Implementados

- **Contador de livros** em tempo real
- **Formatação de preços** brasileira (R$ XX,XX)
- **Timestamps** em backups e exports
- **Arquivo CSV de exemplo** para facilitar importações
- **Menu interativo** com emojis e formatação
- **Confirmação para operações destrutivas**
- **Suporte a caracteres especiais** (acentos, etc.)

## Conceitos Demonstrados

Este projeto demonstra o uso prático de:
- **SQLite e CRUD**: Operações completas de banco de dados
- **Manipulação de Arquivos**: pathlib, os.makedirs, shutil
- **CSV**: Exportação/importação de dados estruturados
- **Backup e Versionamento**: Gestão automática de arquivos
- **Validação de Dados**: Regex, conversão de tipos, tratamento de erros
- **Logging**: Registro de operações e debugging
- **Orientação a Objetos**: Classes bem estruturadas e modulares
- **Interface de Usuário**: Menu interativo e feedback visual

---

**Desenvolvido para a disciplina de Tópicos Especiais em Software** 

Demonstra integração completa entre banco de dados, manipulação de arquivos e boas práticas de desenvolvimento Python.