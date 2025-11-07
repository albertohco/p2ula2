# Projeto Fundamento Python 2 Aula 2
## padronização de nomes e email

Este é um projeto prático para ensino de conceitos de strings e seus métodos em Python, utilizando FastAPI e SQLite.

## Conceitos de Strings Abordados

1. Manipulação básica de strings:
   - Capitalização (`title()`, `lower()`)
   - Remoção de espaços (`split()`, `join()`)
   - Substituição de caracteres (`replace()`)

2. Expressões regulares (RegEx):
   - Remoção de caracteres especiais
   - Substituição de padrões
   - Validação de formato

3. Normalização de texto:
   - Remoção de acentos
   - Padronização de formato

## Funcionalidades

1. Padronização de nomes:
   - Capitaliza cada palavra
   - Trata preposições (de, da, do) adequadamente
   - Remove espaços extras

2. Padronização de emails:
   - Converte nome para formato de email
   - Remove acentos e caracteres especiais
   - Adiciona domínio padrão

3. Armazenamento em SQLite:
   - Salva dados padronizados
   - Evita duplicatas de email
   - Permite consulta dos registros

## Como Executar

1. Instale as dependências:
   ```bash
   pip install fastapi uvicorn sqlalchemy regex python-multipart email-validator
   ```

2. Execute a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Acesse a documentação da API:
   - http://localhost:8000/docs

## Exemplos de Uso

### Criando um novo usuário:
```bash
curl -X POST "http://localhost:8000/usuarios/" \
-H "Content-Type: application/json" \
-d '{"nome": "João da Silva Santos", "email": "teste@teste.com"}'
```

### Listando usuários:
```bash
curl "http://localhost:8000/usuarios/"
```

## Exemplos de Padronização

1. Nome: "JOÃO da SILVA santos"
   - Padronizado: "João da Silva Santos"
   - Email: joao.da.silva.santos@empresa.com.br

2. Nome: "Maria    das   Dores"
   - Padronizado: "Maria das Dores"
   - Email: maria.das.dores@empresa.com.br

3. Nome: "José dos SANTOS Filho"
   - Padronizado: "José dos Santos Filho"
   - Email: jose.dos.santos.filho@empresa.com.br