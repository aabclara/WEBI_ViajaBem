# Registro de Decisões do Projeto: Sistema Viaje Bem (MVP)

Este documento registra o histórico do "Brainstorming" e do planejamento do sistema, documentando explicitamente por que algumas rotas arquiteturais e visuais foram adotadas (Sucessos) e por que outras foram abandonadas (Descartadas/Erros).

---

## ✅ Caminhos de Sucesso (Aprovados e Implementados)

### 1. Pagamentos e CRM Externo (WhatsApp)
*   **Decisão:** O MVP não terá gateway de pagamento interno (Stripe, Pagar.me). O Painel Administrativo apenas gerenciará os leads em um quadro Kanban, e as cobranças (Pix) ocorrerão manualmente via WhatsApp pela agência.
*   **Por que foi sucesso:** Cortou drasticamente o custo e a complexidade técnica do MVP de 60 horas. Reduziu o risco de chargebacks (estornos), dores de cabeça com compliance financeiro, e forçou o foco do sistema em ser uma máquina de "conversão e leads" exclusiva.

### 2. Funil de Fricção Progressiva
*   **Decisão:** Só pedir Nome e RG dos passageiros *após* o pagamento do sinal de 50%. No momento da intenção de compra, pede-se apenas a seleção do "Combo" (número de assentos e e-mail).
*   **Por que foi sucesso:** Destrava o bloqueio psicológico do cliente que desiste da viagem rápida por não ter os documentos dos amigos em mãos no ato do impulso de compra.

### 3. Gamificação Baseada em Escassez
*   **Decisão:** O uso de Tiers (Camadas) e uma barra de progresso visual mostrando quantas pessoas faltam para lotar a viagem ou atingir um upgrade no ônibus (ex: "Faltam 4 vagas para garantir Pousada VIP").
*   **Por que foi sucesso:** Transforma a viagem numa experiência social (Crowdfunding) acionando o FOMO (Medo de Ficar de Fora), incentivando os viajantes a chamarem mais amigos com o link público simplificado de acompanhantes.

### 4. UI/UX: Minimalist Classic (Com as Cores da Marca)
*   **Decisão:** Uso absoluto da paleta oficial da logo enviada (`#F7F2E8` Creme, `#0DBDC2` Ciano, `#FFA915` Laranja), combinada com muito "White Space" e tipografia Grotesca rigorosa (Inter/Roboto sem fontes manuscritas).
*   **Por que foi sucesso:** Resolvemos o problema com público de idades variadas. O foco nas especificações WCAG AA e botões massivos torna a plataforma madura e altamente confiável para uma conversão financeira para todas as idades.

---

## ❌ Caminhos Descartados (O que "deu errado" ou não sobreviveu)

### 1. Edição Livre do Combo Pós-Pagamento
*   **A Ideia Falha:** Permitir que o cliente líder alterasse o número de amigos do seu combo livremente pelo site a qualquer momento, mesmo depois de pagar.
*   **O Erro:** Criaria um pesadelo arquitetural de negócio (estado "zumbi"). Recalcular dinamicamente devoluções mataria a segurança do painel admin, correndo risco de gerar Overbookings pesados para a agência.
*   **A Solução Adotada:** Uma vez que o Admin muda a intenção para "BLOCKED" (Sinal 50%), os ingressos congelam numericamente. O cliente perdeu alguém do seu combo de 4 pessoas? Deve contatar a agência no Zap (Processo humano para mitigar erro de código e cancelamento coletivo).

### 2. Automação de E-mails Transacionais
*   **A Ideia Falha:** Configurar a API do SendGrid ou AWS SES para disparar recibos, aprovações automáticas ou campanhas de alerta sistêmicos.
*   **O Erro:** Além de fugir do orçamento restrito do MVP e do tempo (60 horas), quebrava a exigência principal do negócio do seu cliente, de que a comunicação deve ser artesanalmente operada no número comercial do WhatsApp porque este público responde e converte muito mais em chat direto humano.
*   **A Solução Adotada:** Transferência de 100% das comunicações financeiras para o esforço manual via Zap CRM guiado pelo painel Kanban.

### 3. Filosofia de Design "Organic Acceleration"
*   **A Ideia Falha:** A primeira sugestão visual do nosso modelo misturava estilos luxuosos com contrastes neon chocantes e formatos flutuantes orgânicos.
*   **O Erro:** Ignorou uma das premissas chave: *O público alvo é diversificado.* Aquele modelo seria visualmente cansativo para adultos (50+) ou não passaria a confiabilidade financeira e técnica ("Isso aqui é um banco ou um videogame?").
*   **A Solução Adotada:** O design foi brutalmente revisado para o "Classic Minimalist" pautado pela paleta do logo oficial da agência, utilizando apenas Creme, Ciano e Laranja sem neon e sem pontas flutuantes, trazendo solidez para a interface de viagens.

### 4. Checkout Completo (End-to-End)
*   **A Ideia Falha:** A visão teórica de criar um sistema genérico acoplando Stripe e gerador de faturas em PDF automático na mesma sprint.
*   **O Erro:** Em um MVC acadêmico focado em "Clean Architecture", mirar em um sistema genérico padrão faria os recursos serem gastos em meios de pagamento normais, abafando o *diferencial vital* do MVP: O Módulo de Gamificação Tática dos combos de vagas progressivas.
*   **A Solução Adotada:** Isolar a infraestrutura pesada (Backend Python e Next.js SSR) unicamente para turbinar o Domínio do Funil de Lotação Gamificada em Tiers, e empurrar o "pagamento" literal pra fora (Integração humana).
