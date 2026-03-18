---
page: Dashboard Kanban Admin
source_directory: docs/stitch_showcase_viaje_bem/admin_kanban_viaje_bem/
---

# Design Override: Kanban CRM

> **REGRA DE HERANÇA:** Este documento anula a regra global do Master que exige fundos claros. Para diminuir fadiga visual, componentes de fundo operacionais recebem overrides em tons Slate/Dark.

## Estrutura Topológica (Baseada no HTML Original)

Quando traduzirmos o arquivo `code.html` estático do diretório `admin_kanban_viaje_bem` para o Next.js, a IA MUST realizar a seguinte transição cirúrgica para garantir reatividade sem ferir a Identidade Visual corporativa:

### 1. Setup do Board (Colunas)
- O Container `flex overflow-x-auto gap-6` que embala as 4 colunas MUST ser atrelado a um estado isolado com `"use client"`.
- Cada uma das colunas (Novos, Aguardando Sinal, etc) listadas no arquivo original perde sua rigidez e vira o container alvo das bibliotecas modernas (ex: `@dnd-kit/core`).

### 2. Cards Interativos (As Reservas)
A renderização dos crachás com nomes dos clientes que o Stitch montou como `div`s brancas soltas MUST sofrer Parse para o Shadcn:
- **Corpo:** `<Card className="cursor-grab active:cursor-grabbing border-slate-200 shadow-sm">`
- O Hover effect de `translate-y-1` original é migrado para classe do `Card` mantendo o aspecto lúdico ao encostar o mouse.

### 3. A Central do WhatsApp (Atrito PIX)
A grande âncora originada pelo designer na UI (*O botão verde solto ou os CTAs do Zap*):
- MUST ser invocado usando `<Button variant="outline" className="text-green-600 border-green-200 hover:bg-green-50">`.
- O Ícone MUST ser `import { MessageCircle } from "lucide-react"` caso o `lucide` oficial não porte o path nativo do whatsapp para mantermos BDD neutro, ou `<IconBrandWhatsapp>` usando pacote unificado da empresa caso aprovado no tech lead. (Proibido SVG `<svg>` jogadas inline soltas como o Stitch faz no rodapé do `code.html` pra economizar sujeira no DOM).
