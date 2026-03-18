# Spec: Fluxo do Painel do Líder (Leader Panel Flow)

## Requirement: Autogestão e Cadastramento de Grupo Restrito
O sistema MUST gerenciar as interações do usuário criador (Líder) na área autenticada por OTP, permitindo a finalização documental do grupo mediante a liberação e alteração do status da transação.

### Cenário: Acesso ao painel após autenticação OTP bem-sucedida
- **Dado** que o líder forneceu seu email na vitrine ao garantir a vaga,
- **Quando** ele validar ativamente o código numérico OTP recebido por email,
- **Então** o sistema MUST conceder acesso autorizado à interface do painel unificado.
- **E** a página web inicial MUST listar todas as reservas do líder englobando seu status atualizado correspondente (`CREATED`, `BLOCKED`, `CONFIRMED`).

### Cenário: Cadastro dos dados dos acompanhantes
- **Dado** que qualquer reserva referenciada do líder atingiu o status transacional validado `BLOCKED`,
- **Quando** o líder for munido da área de cadastro preenchendo os dados documentais base dos acompanhantes (Nome Completo e RG),
- **Então** os controladores lógicos MUST salvar e persistir os inputs referenciados à reserva estritamente no banco relacional.
- **E** a UI MUST confirmar a gravação integral dos dados com um alerta de sucesso proeminente.
- **E** as engrenagens de acesso MUST assegurar que enquanto o status for `CREATED`, as ferramentas de submissão do formulário de acompanhantes permaneçam bloqueadas e inacessivelmente seladas.

### Cenário: Congelamento do combo (Tamanho Original) após BLOCKED
- **Dado** que a reserva possui integridade selada correspondente ao status `BLOCKED`,
- **Quando** o líder atuar sobre a interface na intenção de mudar o número bruto e matematicamente alocado dos acompanhantes (Tamanho Original do Combo/Overbooking),
- **Então** todas as rotas ativas MUST interceptar o evento e bloquear categoricamente a alteração.
- **E** a renderização folhear no navegador MUST exibir alerta de proibição indicando contatar a agência base via chamada WhatsApp para ajustes manuais na capacidade estipulada em transação inicial.

### Cenário de Erro: Dados de acompanhante inválidos
- **Dado** a presença de dados formativos pelo Líder na respectiva inserção documental dos viajantes do combo,
- **Quando** ocorrer o evento de salvar sobrepondo envios de payloads imprecisos ou vazios contra a regex do sistema,
- **Então** a API retentora MUST rechaçar a inserção.
- **E** o fluxo frontend MUST mapear a resposta sublinhando ou destacando categoricamente em cor de advertência as seções/campos faltantes portando uma diretriz de correção simplificada sem deletar ou reiniciar blocos lógicos das views previamente adequadas.

### Cenário: Visualização do voucher de compartilhamento
- **Dado** a permissão adquirida quando um ingresso reserva tem status evoluído para `BLOCKED` ou similarmente faturado,
- **Quando** o cliente Líder focar na interface de veredito da sua viagem contida no painel,
- **Então** os blocos reativos MUST destacar de modo isolado à tela inteira um link único identificador (o Voucher Criptografado Exclusivo).
- **E** o sistema MUST renderizar componente utilitário de Cópia ágil (Copiar URL para Transferência) explicitando e enumerando a quantidade contabilizada dos acompanhantes subscritos na viagem que já perfizeram o tráfego do view neste convite eletrônico do ticket.

### Cenário de Erro: Falha de conexão com o banco de dados
- **Dado** qualquer navegação rotineira como verificação de painel lista ou envios documentais do cliente,
- **Quando** a via lógica servidora romper acesso com sua matriz de persistência e recusando o processo vital em base PostgreSQL,
- **Então** o sistema limitador MUST retornar alerta visível assinalando indisponibilidade emergencial temporária sem emitir logs brutos.
- **E** MUST proibir o extermínio/reinicio compulsivo dos bytes/informações de formulários presentemente preenchidos pelo titular mantendo cópia intocada do session-state na porta Client-Side.
