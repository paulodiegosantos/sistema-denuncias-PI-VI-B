# Sistema de Denúncias de Segurança da Informação

Sistema web desenvolvido em Django para o registro e acompanhamento de denúncias relacionadas a vazamentos de dados, práticas inadequadas de segurança e atividades suspeitas.

O projeto foi desenvolvido como parte do Projeto Integrador VI-B do curso de Análise e Desenvolvimento de Sistemas.

## Objetivo

Oferecer um canal para que pessoas possam registrar denúncias de forma anônima ou identificada, preservando a confidencialidade das informações e permitindo o acompanhamento por meio de um protocolo individual.

## Funcionalidades

- Registro de denúncias anônimas ou identificadas.
- Classificação das denúncias por categoria.
- Geração automática de protocolo de acompanhamento.
- Consulta pública do andamento por protocolo.
- Painel administrativo restrito a usuários autorizados.
- Gerenciamento do status das denúncias.
- Registro de observações administrativas.
- Histórico de alterações e ações realizadas.
- Criptografia de informações confidenciais armazenadas no banco de dados.

## Páginas e rotas do sistema

O sistema possui páginas públicas, destinadas ao registro e acompanhamento de denúncias, e páginas administrativas, destinadas ao gerenciamento interno.

### Páginas públicas

| Página | Rota | Objetivo |
|---|---|---|
| Página inicial | `/` | Apresenta o sistema e oferece acesso às principais funcionalidades. |
| Registrar denúncia | `/denunciar/` | Permite registrar uma denúncia anônima ou identificada, informando sua categoria e descrição. |
| Confirmação | `/confirmacao/<protocolo>/` | Apresenta a confirmação do registro e o protocolo individual que será utilizado para acompanhar a denúncia. |
| Acompanhar denúncia | `/acompanhar/` | Permite consultar o andamento de uma denúncia utilizando seu protocolo, exibindo informações básicas como tipo, status e data de recebimento. |

### Páginas administrativas

| Página | Rota | Objetivo |
|---|---|---|
| Login administrativo | `/administracao/login/` | Permite a autenticação de usuários autorizados a administrar o sistema. |
| Painel administrativo | `/administracao/` | Apresenta as denúncias registradas e indicadores de acompanhamento, como quantidade total e distribuição por status. |
| Detalhes da denúncia | `/administracao/denuncia/<id>/` | Permite visualizar os detalhes confidenciais da denúncia, alterar seu status, registrar observações e consultar o histórico de alterações. |
| Sair da administração | `/administracao/sair/` | Encerra a sessão do usuário administrativo. |

**Observação:** as rotas administrativas são protegidas por controle de acesso. Usuários sem autorização não podem acessar o painel nem os detalhes internos das denúncias.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML e CSS
- Cryptography (Fernet)
- python-dotenv

## Segurança e privacidade

O sistema utiliza criptografia Fernet para proteger informações confidenciais armazenadas no banco de dados.

A chave criptográfica é gerada localmente durante a configuração inicial e armazenada em um arquivo `.env`, que não deve ser compartilhado ou publicado no repositório.

O acesso administrativo é restrito a usuários autorizados. A consulta pública por protocolo apresenta somente informações básicas sobre o andamento da denúncia.

O projeto aplica princípios relacionados à Lei Geral de Proteção de Dados (LGPD), como finalidade, necessidade, confidencialidade e segurança.

**Observação:** trata-se de um projeto acadêmico e demonstrativo. Sua utilização em ambiente de produção exige medidas adicionais de segurança, infraestrutura e governança.

## Requisitos

- Windows 10 ou superior.
- Python instalado e disponível no PATH.
- Conexão com a internet durante a instalação das dependências.

## Instalação e configuração

1. Baixe ou clone este repositório.
2. Entre na pasta principal do projeto.
3. Execute o arquivo `configurar.bat`.
4. Aguarde a criação do ambiente virtual, instalação das dependências, geração da chave criptográfica e preparação do banco de dados.

O script gera automaticamente uma chave Fernet e a salva localmente no arquivo `.env`, caso ele ainda não exista.

**Importante:** não exclua nem substitua o arquivo `.env` após cadastrar denúncias. A chave é necessária para descriptografar os dados existentes.

## Como executar

Após concluir a configuração, execute:

`iniciar.bat`

O sistema ficará disponível no endereço:

http://127.0.0.1:8000/

## Administração

Para acessar o painel administrativo, utilize a opção de administração disponível no sistema.

A criação do usuário administrador deve ser realizada pelo comando:

`venv\Scripts\python.exe manage.py createsuperuser`

Siga as instruções exibidas no terminal para cadastrar as credenciais.

## Estrutura de configuração

- `configurar.bat`: automatiza a instalação e preparação inicial.
- `iniciar.bat`: inicia o servidor Django.
- `.env.example`: modelo da variável de ambiente necessária.
- `.env`: arquivo local que armazena a chave criptográfica.
- `requirements.txt`: lista as dependências do projeto.

## Banco de dados

O projeto utiliza SQLite. O banco é criado e preparado automaticamente durante a configuração inicial por meio das migrações do Django.

Cada instalação possui sua própria chave criptográfica e seu próprio banco de dados.

## Autor

Projeto acadêmico desenvolvido por **Paulo Diego** individualmente para o Projeto Integrador VI-B.
