# Spec: Core Booking Flow e Fricção Progressiva

## Requirement: Travamento Matemático de Carrinho
O sistema operante MUST providenciar atrito mínimo inicial durante intenções transacionais. A finalidade do Flow Core é solicitar "Número de Assentos e String de Contato", registrando o estado sem solicitar detalhes burocráticos massivos iniciais, respeitando o princípio prático de fricção progressiva validada pelo modelo de agência física.

### Cenário: Submissão Limpa de Pacote via Fricção Mínima
- **Dado** que um evento/viagem contém fisicamente na base 40 assentos no total, possuindo 24 blocos alocados com status viável de efetivação.
- **E** o utilizador final abre a interface de captação de pacote a partir do catálogo global.
- **Quando** ele fornece intenções válidas e informa quantidade simétrica de 4 ingressos/reservas, processando o disparo final.
- **Então** a Interface Web MUST desabilitar o gatilho principal acionando loader transicional temporário iminente.
- **E** a Interface Servidora MUST acomodar e alocar os espaços gravados no estado `CREATED` ou Pendente em log base de banco relacional e atrelados estritamente ao e-mail/celular remetido.
- **E** o Cliente Consumidor MUST ser notificado com Confirmação e Código 2XX positivo transicionando sessões diretamente ao painel final de faturamento do usuário logado.

### Cenário de Erro: Falha por Overbooking Abrupto (Gargalo Transacional)
- **Dado** que há o limite irredutível de meros 2 assentos na capacidade restante para a Viagem supramencionada no Banco.
- **Quando** a rotina de submissão do protocolo é violentada com manipulação ou envio em trânsito equivalendo compra em volume exigente de 3 ingressos.
- **Então** a engine de Validação do Core MUST suspender a persistência em recusa peremptória, de forma a preservar a inexistência de Overbooking e quebra material do Evento.
- **E** a requisição via rede MUST transbordar com erro semântico equivalente (`HTTP 422 Unprocessable` ou Payload de Falha).
- **E** as engrenagens de UI MUST interceptar completamente a falha de rede convertendo a recusa cega numa janela/alerta tangível "Toast de Destruição/Rechasso" na mesma folha visual, ordenando que o utilizador manipule menos vagas do inventário da Loja e abortar retentativas no server.

### Cenário de Erro: Payload Omisso ou Indisciplinado
- **Dado** que a formulação de entrada sofre ausências ou contornos na modelagem estrutural mínima requerida.
- **Quando** o Payload transmitido não contém vetores requerentes chaves do escopo inicial (Contatos errôneos de Liderança, ou Strings de volume nulificada).
- **Então** as camadas do Core MUST rejeitar de imediato a modelagem baseada em Regras com semântica legível (`HTTP 400` / `422`).
- **E** toda camada Frontend SHALL frear o tráfego nulo ativando os gatilhos preventivos nas bordas de imputação de formulários locais.
