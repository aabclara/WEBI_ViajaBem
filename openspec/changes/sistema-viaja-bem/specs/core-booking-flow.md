# Spec: Core Booking Flow & Gamification

## Contexto
O cliente líder explora a Vitrine, sendo impactado pelo fluxo gamificado de vagas e preços, e cadastra sua "intenção" ou "combo" de lugares no ônibus via um fluxo minimamente friccionado.

### Requirement: Vitrine Gamificada
A aplicação SSR deve prover os dados reativos de ocupação da viagem em tempo real.

#### Scenario: Visualização de escassez
- **WHEN** usuário acessa os detalhes da excursão X.
- **AND** a excursão possui 40 lugares e constam 35 Intentions nas fases `CREATED`, `BLOCKED` ou `CONFIRMED`.
- **THEN** a barra de progresso visual deve renderizar 87.5% completa sob cor estética madura.
- **AND** o texto lateral deve enfatizar "5 Vagas Restantes".

#### Scenario: Desbloqueio progressivo de Tiers
- **WHEN** os bloqueios confirmados atinjam a meta de N pessoas declarada na viagem.
- **THEN** a interface de Vitrine deverá atualizar o Status de Bônus Coletivo, exibindo à todos (potenciais novos compradores) que "A excursão obteve o upgrade VIP".

### Requirement: Captura de Intenção e "Fricção Progressiva"
Bloqueio instantâneo do carrinho de combos para não perder a venda impulsiva, delegando a burocracia do nome completo e RG para depois.

#### Scenario: Submissão rápida do Combo
- **WHEN** cliente seleciona quantidade N de assentos (O Combo).
- **AND** informa exclusivamente seus dados primários (Email ou Telefone e Nome da Conta).
- **THEN** o Back-End cria a entidade `Reservation` com status `CREATED` e salva o `combo_size` como N.
- **AND** o sistema subtrai N das vagas temporariamente disponíveis no pool daquela Viagem.

#### Scenario: Autenticação Limpa (Passwordless)
- **WHEN** usuário submete o Combo gerando a `Reservation` pela primeira vez na plataforma.
- **THEN** o sistema envia um link (Magic Link) simulado para autenticação contínua, permitindo ao líder voltar posteriormente no mesmo dispositivo para checagem do painel, sem exigir senha clássica complexa.
