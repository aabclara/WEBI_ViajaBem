# Spec: Core Booking Flow e Fricção Progressiva

## Requirement: Gerenciamento de Vagas e Fricção Mínima
O sistema MUST minimizar a fricção inicial durante a reserva. O fluxo principal solicitará apenas "Número de Assentos" e "Dados de Contato", registrando a intenção de compra sem exigir cadastro completo ou pagamento imediato na plataforma. 

### Cenário: Criação de Reserva com Fricção Mínima
- **Dado** que há vagas suficientes disponíveis para uma viagem específica,
- **Quando** o usuário preencher o formulário informando a quantidade desejada e seus dados de contato básicos,
- **Então** a interface MUST exibir um indicador de carregamento e desabilitar o botão de envio.
- **E** o backend MUST registrar a reserva com status `CREATED` vinculada ao contato informado.
- **E** o sistema MUST retornar HTTP 201 e redirecionar o usuário para o painel de acompanhamento da reserva.

### Cenário de Erro: Falha por Overbooking (Vagas Insuficientes)
- **Dado** que a viagem possui apenas 2 vagas disponíveis,
- **Quando** o usuário tentar reservar 3 ou mais vagas,
- **Então** o backend MUST recusar a transação para impedir overbooking.
- **E** a API MUST retornar HTTP 422 (Unprocessable Entity).
- **E** a interface MUST interceptar a falha e exibir uma mensagem de erro clara informando a disponibilidade atual, sem recarregar a página.

### Cenário de Erro: Payload Inválido ou Incompleto
- **Dado** que o usuário tente enviar o formulário via API contendo dados estruturais incorretos ou faltantes,
- **Quando** o backend receber a requisição,
- **Então** o sistema MUST rejeitar o payload retornando HTTP 400 ou 422.
- **E** o frontend SHALL realizar validação local prévia para evitar o envio de dados inválidos ao servidor.

### Cenário: Expiração do prazo de pagamento do sinal (24h)
- **Dado** que o líder realizou uma reserva com status `CREATED`,
- **Quando** o prazo de 24 horas vencer sem confirmação de pagamento do sinal pela agência,
- **Então** o sistema MUST manter a reserva visível no Kanban
- **E** a agência MUST decidir manualmente entre cancelar a reserva ou estender o prazo — o sistema NÃO cancela automaticamente.

### Cenário: Autenticação do líder via OTP por email
- **Dado** que o líder forneceu apenas seu email na vitrine ao garantir a vaga,
- **Quando** ele tentar acessar o painel "Minhas Viagens",
- **Então** o sistema MUST enviar um código OTP para o email cadastrado e MUST conceder acesso somente após validação bem-sucedida do código.
- **E** caso o código expire ou seja inválido, o sistema MUST permitir reenvio e MUST exibir mensagem de erro clara sem expor detalhes técnicos.

### Cenário: Geração do voucher viral
- **Dado** que a reserva do líder teve o sinal confirmado pela agência e o status mudou para `BLOCKED`,
- **Quando** o sistema processar essa transição,
- **Então** o sistema MUST gerar automaticamente um link único e exclusivo para o líder compartilhar com seus acompanhantes.
- **E** o link MUST ser exibido no painel do líder e MUST permitir que os acompanhantes visualizem os dados da viagem sem precisar de autenticação.

### Cenário de Erro: Falha de conexão com o banco de dados
- **Dado** que o usuário tentou realizar qualquer operação que exija persistência,
- **Quando** o banco de dados estiver indisponível,
- **Então** o sistema MUST retornar HTTP 503 e a interface MUST exibir mensagem de indisponibilidade temporária sem expor detalhes técnicos ao usuário.

### Cenário de Erro: Timeout de resposta da API
- **Dado** que o usuário clicou em confirmar uma ação,
- **Quando** a API demorar além do tempo aceitável para responder,
- **Então** a interface MUST exibir o componente de loading padrão, desabilitar o botão de envio e após o timeout MUST notificar o usuário com mensagem de erro sem recarregar a página.
