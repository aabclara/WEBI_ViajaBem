# Spec: UI/UX & Design System (Minimalist Classic)

## Contexto
Para garantir que o produto atinja a máxima confiabilidade financeira e seja utilizável por um público diversificado (jovens ao público sênior 50+), a interface do **Sistema Viaja Bem** deve seguir preceitos inegociáveis do design rigoroso, herdando estritamente as características extraídas da identidade visual (logo) da agência. Não haverá espaço para exibições visuais lúdicas em telas transacionais.

### Requirement: O Design System Rigoroso ("Minimalist Classic")
As páginas e os componentes React/Tailwind devem limitar-se à paleta matemática da marca, garantindo aprovação absoluta no contraste WCAG AA.

#### Scenario: Aplicação das Cores Oficiais
- **WHEN** um componente estiver sendo estruturado pelo desenvolvedor.
- **THEN** ele só deve utilizar os Hexadecimais oficiais:
  - **Fundo Global/Containers Externos:** Creme / Off-White (`#F7F2E8`). Protege a visão e aquece a percepção.
  - **Contêineres Internos/Cartões (Cards):** Branco Absoluto (`#FFFFFF`).
  - **Foco e Descoberta Inicial (Hero):** Laranja / Âmbar vibrante (`#FFA915`). Usado para o botão primário de descoberta "Explorar Destinos" e para a barra de "Vagas Restantes" dentro dos cartões, transmitindo escassez e impacto visual primário.
  - **Ação Transacional (Cards e Login):** Ciano / Teal (`#0DBDC2`). Oficializado como o botão de reserva ("Reservar Agora") dentro das Vitrines, botões de acesso à agência e navegação. Transmite segurança e estabilidade no momento do clique de compra.
  - **Carga de Texto:** Chumbo Estrito (`#1F1F1F`).

#### Scenario: Tipografia e Acessibilidade Tátil
- **WHEN** renderizando textos descritivos ou formulários.
- **THEN** a interface **nunca** utilizará fontes cursivas (presentes na marca). A UI deverá ser sustentada unicamente por Sans-Serif modulares (`Inter` ou `Roboto`), para transparecer eficiência bancária.
- **AND** botões e áreas de input deverão possuir "touch-targets" imensos (Mínimo de 48px a 56px de altura) prevenindo "miss-clicks" em ambientes Mobile.

### Requirement: Mapeamento de Telas (O Flow Front-end)
A aplicação condensará todo o negócio do MVP em 5 visões estritas e 2 modais acoplados.

#### Scenario: A Visão Pública e Captura Emocional
- **Vitrine de Destinos (Home):** Ponto de SEO (Server-Side Rendered). Fundo creme. A página inicia com um "Split Hero Section": lado esquerdo apresentando a proposta de valor "Viagens rápidas. Lotação coletiva." com os dois CTAs principais (Laranja e Ciano), e o lado direito apresentando uma imagem em grande destaque (proporção 4/3). Abaixo do Hero, entra o Grid fotográfico de destinos (`Próximas Saídas`). A presença forte da "Barra Laranja de Gamificação" indicará a escassez das vagas do ônibus em todos os cartões do grid. O Header será estrito: contendo a Logo e o botão simples de Login, focado inteiramente na conversão.
- **Modal de Checkout Rápido:** Abre sobre a Home. Fundo branco puro. Oculta menus. Permite ao "Líder" salvar *apenas* a quantidade do Combo e seu Email, enviando os ingressos para o estado `CREATED` instantaneamente.
- **Página de Itinerário Público (Vírus):** Link lido de forma orgânica gerado ao final do funil. Modo read-only blindado contendo CTA chamativo para "captar leads amigos" que também queiram ir.

#### Scenario: A Visão da Burocracia Privada
- **Painel "Minhas Viagens" (Líder / Cliente):** Interface de utilidade bancária. Cartões horizontais dividindo viagens futuras/passadas. Ação central em Ciano para: "Cadastrar Passageiros (RG)" caso as vagas já estejam pagas no Whatsapp, ou botão em Laranja caso o Sinal não tenha sido reconhecido.
- **Tela de Login Simples:** Painel estilo "Magic Link" ou OTP, fugindo ativamente de senhas pesadas que aumentam abandono. Tela em formato "Split" isolada por fundo claro.

#### Scenario: A Visão do Gerenciador de Operações da Agência
- **Login B2B Admin:** Tela seca e utilitária, sem fotos turísticas de fundo. Foco estrito em segurança.
- **Dashboard Kanban CRM:** Sistema denso baseado em Grid Trello. Quatro Colunas verticais (`Novos`, `Sinal Pago`, `Confirmados`, `Cancelados`). 
  - Um click sobre um *Card* do Kanban aciona um **Management Modal**.
  - Esse modal permite que o atendente mude o status do usuário, acione cobrança enviando o link do PIX automático por API pro Zap Web e verifique os convidados cadastrados sem ferir o Overbooking matemático do banco de dados (que engessa transições equivocadas).
