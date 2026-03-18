# Proposal: Sistema Viaje Bem (MVP Agência Gamificada)

## Motivation

O processo de venda de viagens rápidas para grupos atualmente sofre com alto atrito e gestão caótica manual via WhatsApp ou planilhas. Clientes hesitam em organizar grupos devido à burocracia de cobrar amigos e coordenar dados, perdendo-se o senso de urgência inerente a viagens curtas. O "Sistema Viaje Bem" existe para automatizar a captação da intenção, gerar forte urgência ("FOMO" / Escassez) publicamente através de uma vitrine gamificada (onde os benefícios e o preço melhoram de acordo com o total de adesões) e organizar um CRM (Kanban) estruturado para o agente de viagens operar e confirmar vendas via WhatsApp sem precisar de um robusto gateway de pagamentos no MVP.

## What Changes

Criaremos uma plataforma web com duas grandes atuações, alinhadas às decisões de nossa Exploração de Design, rodando sob a arquitetura de **Clean Architecture, DDD, FastAPI e Next.js**:

*   **Vitrine Pública (The Funnel):** Catálogo de pacotes de viagem com foco em "Fricção Progressiva". O cliente vê uma Barra Dinâmica de Progresso de assentos e benefícios liberados (Gamificação Coletiva). Ele trava a intenção de vaga (o seu "Combo") fornecendo dados mínimos iniciais.
*   **Gestão de Líder ("Meu Painel"):** Um dashboard restrito para o comprador gerenciar o tempo (24h) de limite para pagamento do sinal da agência e adicionar os dados documentais completos dos seus acompanhantes (IDs) APÓS o sinal ser pago.
*   **CRM Kanban Administrativo:** Um painel para a agência gerenciar os contatos. Intents novas ("CREATED") caem para o admin cobrar 50% de sinal via WhatsApp. Uma vez bloqueada ("BLOCKED") a exclusividade das vagas de alteração migra do cliente Líder para o Admin, e finalmente "CONFIRMED".

## New Capabilities

- Visualização gamificada do progresso de lotação e liberação de "Tiers" em tempo real em Vitrine SSR (Server Side Rendering).
- Criação e Autenticação de Usuário (Líder) combinando senhas clássicas e tokens OTP.
- Gestão de ciclo de vida das Intenções de Compra ("Reservations") em fluxos restritos de CRUD Pós e Pré-Sinal pago.
- Emissão de link gerado (Voucher/Espelho de Leitura) exclusivo de compartilhamento viral aos passageiros Acompanhantes do líder.

## Changed Requirements

- **Comunicação e Pagamento Externo:** Por restrições de negócio e segurança do MVP, todo fechamento financeiro transcende o sistema. O software **não** executará rotinas transacionais via cartões ou API bancárias. O sistema reflete e acompanha status de Pagamento ("Sinal", "Concluído") orientados pela ação manual de um administrador atestando que recebeu o comprovante Pix via WhatsApp. E-mails transacionais não serão suportados inicialmente.

## Impact

- Impacta a Modelagem de Entidades do Banco (User, Trip, Reservation e Passengers).
- Exigência pesada de interfaces no Front-End Híbrido sob o "Classic Minimalist UX" para unificar o entendimento de leads jovens (Urgent buyers) a adultos que almejam credibilidade (Clean and Accessible UX).
- Reforça a modelagem de Cloud Infrastructure via Docker com FastAPI assíncrono pro Painel do Agente não sofra gargalo nos Picos Médios de acesso na Vitrine.
