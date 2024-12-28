# Sistema de Carrinho de Compras - Banco de Dados

Este projeto consiste em um banco de dados para um sistema de carrinho de compras, onde um cliente pode adicionar itens ao carrinho, finalizar a compra, e visualizar o histórico de pedidos. O banco de dados foi modelado usando SQL e foi projetado para armazenar dados de clientes, produtos, carrinho de compras, pedidos e itens de pedidos.

## Estrutura do Banco de Dados

### Tabelas

1. **Clientes**  
   A tabela `clientes` armazena as informações básicas dos clientes.
   - `id_cliente` (INTEGER): Chave primária, identificador único do cliente.
   - `nome` (TEXT): Nome do cliente.
   - `email` (TEXT): Email do cliente (único).
   - `endereco` (TEXT): Endereço do cliente.
   - `telefone` (TEXT): Telefone do cliente.

   ```sql
   CREATE TABLE clientes (
       id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
       nome TEXT NOT NULL,
       email TEXT UNIQUE NOT NULL,
       endereco TEXT,
       telefone TEXT
   );
   ```

2. **Produtos**  
   A tabela `produtos` armazena o catálogo de produtos disponíveis para compra.
   - `id_produto` (INTEGER): Chave primária, identificador único do produto.
   - `nome` (TEXT): Nome do produto.
   - `descricao` (TEXT): Descrição do produto.
   - `preco` (DECIMAL): Preço do produto.

   ```sql
   CREATE TABLE produtos (
       id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
       nome TEXT NOT NULL,
       descricao TEXT,
       preco DECIMAL(10, 2) NOT NULL
   );
   ```

3. **Carrinho de Compras**  
   A tabela `carrinho` mantém os produtos que o cliente adicionou ao carrinho antes de finalizar a compra.
   - `id_carrinho` (INTEGER): Chave primária, identificador único do carrinho.
   - `id_cliente` (INTEGER): Chave estrangeira referenciando o cliente que está fazendo a compra.
   - `id_produto` (INTEGER): Chave estrangeira referenciando o produto adicionado ao carrinho.
   - `quantidade` (INTEGER): Quantidade do produto no carrinho.

   ```sql
   CREATE TABLE carrinho (
       id_carrinho INTEGER PRIMARY KEY AUTOINCREMENT,
       id_cliente INTEGER,
       id_produto INTEGER,
       quantidade INTEGER NOT NULL,
       FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
       FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
   );
   ```

4. **Pedidos**  
   A tabela `pedidos` armazena os pedidos finalizados pelos clientes, incluindo a data e hora da compra.
   - `id_pedido` (INTEGER): Chave primária, identificador único do pedido.
   - `id_cliente` (INTEGER): Chave estrangeira referenciando o cliente que fez o pedido.
   - `data_compra` (DATETIME): Data e hora da compra.

   ```sql
   CREATE TABLE pedidos (
       id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
       id_cliente INTEGER,
       data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
   );
   ```

5. **Itens de Pedido**  
   A tabela `itens_pedido` mantém os produtos comprados dentro de um pedido.
   - `id_item_pedido` (INTEGER): Chave primária, identificador único do item do pedido.
   - `id_pedido` (INTEGER): Chave estrangeira referenciando o pedido.
   - `id_produto` (INTEGER): Chave estrangeira referenciando o produto.
   - `quantidade` (INTEGER): Quantidade do produto comprada.
   - `preco` (DECIMAL): Preço do produto no momento da compra.

   ```sql
   CREATE TABLE itens_pedido (
       id_item_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
       id_pedido INTEGER,
       id_produto INTEGER,
       quantidade INTEGER NOT NULL,
       preco DECIMAL(10, 2) NOT NULL,
       FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
       FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
   );
   ```

## Como Configurar o Banco de Dados

### Requisitos

- SQLite 3.x ou superior
- Um editor de SQL ou ferramenta de administração para executar os comandos SQL

### Passos para Configuração

1. **Baixe o arquivo SQL** com os scripts de criação das tabelas, ou copie os comandos fornecidos neste documento.

2. **Abra o SQLite**:
   - No terminal, navegue até o diretório onde você deseja armazenar o banco de dados e execute o comando `sqlite3`:
     ```bash
     sqlite3 nome_do_banco.db
     ```

3. **Crie o banco de dados**:
   - Dentro do terminal do SQLite, cole os scripts de criação das tabelas. Isso criará as tabelas necessárias para o seu sistema de carrinho de compras.

4. **Popule o banco de dados com alguns dados iniciais** (opcional):
   - Insira dados fictícios de clientes e produtos para testar o funcionamento do sistema.
   ```sql
   INSERT INTO clientes (nome, email, endereco, telefone) 
   VALUES ('João Silva', 'joao@email.com', 'Rua A, 123', '1234-5678');
   
   INSERT INTO produtos (nome, descricao, preco) 
   VALUES ('Produto 1', 'Descrição do produto 1', 10.00),
          ('Produto 2', 'Descrição do produto 2', 20.00);
   ```


## Como Testar o Sistema

1. **Adicionar um item ao carrinho**:
   - Primeiro, adicione um produto ao carrinho de um cliente:
     ```sql
     INSERT INTO carrinho (id_cliente, id_produto, quantidade)
     VALUES (1, 1, 2); -- Cliente 1 adiciona 2 unidades do Produto 1
     ```

2. **Finalizar o pedido**:
   - Crie um novo pedido e mova os itens do carrinho para a tabela de pedidos:
     ```sql
     INSERT INTO pedidos (id_cliente) 
     VALUES (1); -- Cria um pedido para o Cliente 1

     INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco) 
     SELECT (SELECT id_pedido FROM pedidos WHERE id_cliente = 1 ORDER BY data_compra DESC LIMIT 1),
            id_produto, quantidade, preco
     FROM carrinho
     WHERE id_cliente = 1;
     ```

3. **Visualizar o histórico de pedidos do cliente**:
   - Consulte o histórico de pedidos de um cliente:
     ```sql
     SELECT p.id_pedido, p.data_compra, ip.id_produto, ip.quantidade, ip.preco
     FROM pedidos p
     JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
     WHERE p.id_cliente = 1;
     ```


## Conclusão

Esse modelo de banco de dados atende aos requisitos de um sistema de carrinho de compras básico, permitindo que os clientes adicionem itens ao carrinho, finalizem a compra e vejam o histórico de pedidos. O relacionamento entre as tabelas foi cuidadosamente projetado para garantir que os dados de clientes, produtos, carrinho e pedidos sejam armazenados de forma eficiente e que as relações entre essas entidades sejam bem estabelecidas.

