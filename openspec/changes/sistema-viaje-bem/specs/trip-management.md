# Spec: Gestão de Pacotes de Viagem (Trip Management)

## Requirement: Criação e Manutenção de Pacotes pelo Administrador
O administrador da agência MUST ter controle total sobre a publicação e edição dos pacotes de viagem expostos na vitrine pública. Toda alteração MUST ser refletida imediatamente na interface do usuário final.

### Cenário: Criação de novo pacote de viagem
- **Dado** que o administrador está autenticado no painel administrativo,
- **Quando** ele preencher todos os campos obrigatórios (título, descrição, data de início, data de término, vagas totais, preço por pessoa e imagem de capa) e clicar em "Publicar Viagem",
- **Então** o sistema MUST persistir o pacote no banco de dados com status ativo.
- **E** o sistema MUST tornar o pacote imediatamente visível na vitrine pública.

### Cenário de Erro: Campos obrigatórios ausentes
- **Dado** que o administrador está preenchendo o formulário de novo pacote,
- **Quando** ele tentar publicar sem preencher todos os campos obrigatórios,
- **Então** o sistema MUST bloquear a submissão.
- **E** a interface MUST destacar os campos faltantes com mensagem explicativa sem apagar os campos já preenchidos.

### Cenário de Erro: Formato de data inválido
- **Dado** que o administrador está preenchendo as datas do pacote,
- **Quando** ele informar uma data de término anterior à data de início,
- **Então** o sistema MUST rejeitar a submissão.
- **E** a interface MUST exibir mensagem de erro indicando a inconsistência nas datas.

### Cenário de Erro: Imagem de capa com formato ou tamanho inválido
- **Dado** que o administrador está fazendo upload da imagem de capa,
- **Quando** o arquivo enviado não for PNG ou JPG, ou ultrapassar 10MB,
- **Então** o sistema MUST rejeitar o arquivo.
- **E** a interface MUST informar os formatos aceitos (PNG, JPG) e o tamanho máximo (10MB) sem apagar os outros campos já preenchidos.

### Cenário: Edição de pacote existente
- **Dado** que o administrador acessa um pacote já publicado,
- **Quando** ele alterar qualquer campo e salvar,
- **Então** o sistema MUST atualizar os dados no banco de dados e MUST refletir as alterações imediatamente na vitrine pública.
- **E** se o pacote já tiver reservas ativas, o sistema MUST impedir a redução do número de vagas totais abaixo do total já reservado.

### Cenário de Erro: Falha de conexão com o banco de dados
- **Dado** que o administrador tentou publicar ou editar um pacote,
- **Quando** o banco de dados estiver indisponível,
- **Então** o sistema MUST exibir mensagem de indisponibilidade temporária sem apagar os dados do formulário.
