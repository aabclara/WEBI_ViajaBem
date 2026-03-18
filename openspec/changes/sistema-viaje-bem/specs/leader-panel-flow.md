# Spec: Fluxo do Painel do Líder (Leader Panel Flow)

## Requirement: Autogestão e Cadastro de Acompanhantes
O sistema MUST gerenciar as interações do usuário criador (Líder) na área autenticada por OTP, permitindo a finalização documental do grupo conforme o status da reserva for atualizado.

### Cenário: Acesso ao painel após autenticação OTP bem-sucedida
- **Dado** que o líder forneceu seu email na vitrine ao garantir a vaga,
- **Quando** ele validar o código OTP recebido por email,
- **Então** o sistema MUST conceder acesso à área do painel.
- **E** a interface MUST listar todas as reservas do líder com seus status atualizados (`CREATED`, `BLOCKED`, `CONFIRMED`).

### Cenário: Cadastro dos dados dos acompanhantes
- **Dado** que a reserva do líder possui status `BLOCKED`,
- **Quando** o líder preencher os dados documentais dos acompanhantes (Nome Completo e RG),
- **Então** o sistema MUST salvar os dados vinculados à reserva no banco de dados.
- **E** a interface MUST exibir um alerta de sucesso confirmando o cadastro.
- **E** enquanto o status da reserva for `CREATED`, o formulário de acompanhantes MUST permanecer bloqueado e inacessível.

### Cenário: Congelamento do combo após BLOCKED
- **Dado** que a reserva possui status `BLOCKED`,
- **Quando** o líder tentar alterar o número de acompanhantes do seu combo,
- **Então** o sistema MUST bloquear essa alteração.
- **E** a interface MUST exibir uma mensagem orientando o líder a contatar a agência via WhatsApp para qualquer ajuste no número de vagas.

### Cenário de Erro: Dados de acompanhante inválidos
- **Dado** que o líder está preenchendo os dados dos acompanhantes,
- **Quando** ele submeter dados incompletos ou com formato inválido,
- **Então** o sistema MUST rejeitar a submissão.
- **E** a interface MUST destacar os campos inválidos com uma mensagem explicativa sem apagar os dados já preenchidos corretamente.

### Cenário: Visualização do voucher de compartilhamento
- **Dado** que a reserva possui status `BLOCKED`,
- **Quando** o líder acessar o painel,
- **Então** a interface MUST exibir o link do voucher exclusivo com uma opção de copiar.
- **E** o sistema MUST informar quantos acompanhantes já visualizaram o link do voucher.

### Cenário de Erro: Falha de conexão com o banco de dados
- **Dado** que o líder tentou acessar ou atualizar qualquer informação no painel,
- **Quando** o banco de dados estiver indisponível,
- **Então** o sistema MUST exibir uma mensagem de indisponibilidade temporária sem expor detalhes técnicos.
- **E** o sistema MUST preservar os dados já preenchidos nos formulários da sessão atual.
