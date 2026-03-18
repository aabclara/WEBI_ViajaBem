---
page: Vitrine Home (Catálogo)
source_directory: docs/stitch_showcase_viaje_bem/showcase_bot_es_empilhados/
---

# Design Override: Vitrine Home

> **REGRA DE HERANÇA:** Este documento anula o MASTER.md apenas nas especificidades layout/geométricas abaixo. Cores e tipologia (Inter, Creme, Ciano, Laranja) seguem o Master.

## Estrutura Topológica (Baseada no HTML Original)

Ao codificar o componente `app/page.tsx`, o Desenvolvedor/IA MUST importar o HTML estático do diretório `source_directory` e converter obrigatoriamente para as seguintes árvores do **shadcn/ui**:

### 1. Header Corporativo (Sticky)
- Converter a `<header>` tailwind livre para o design pattern do componente fixo.
- A âncora de `Login` originada do HTML cru (`<button>Login</button>`) MUST ser substituída por `<Button variant="link" className="text-accent-teal font-bold">`.

### 2. O Split-Hero ("Viagens rápidas. Lotação coletiva")
- O contêiner pai `@[864px]:flex-row` MUST ser respeitado no Grid do Tailwind para separar o texto à esquerda da van à direita.
- Os CTAs originais de estilo em HTML (*Explorar Destinos* e *Conheça nossa agência*):
  - Primário (Explorar): `<Button size="lg" className="bg-primary rounded-xl h-14 w-full">`
  - Secundário (Conhecer): `<Button size="lg" className="bg-accent-teal rounded-xl h-14 w-full">`

### 3. O Grid de Viagens (Cards)
A seção `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">` detectada no arquivo original MUST ser refatorada assim:
- **Card Mestre:** Substituir a `div` vazia original de `bg-card-white` por `<Card className="rounded-xl shadow-md border-slate-100 hover:shadow-xl">`.
- **Preço e Destino:** Passam para dentro de `<CardHeader>` e `<CardTitle>`.
- **A Barra de Gamificação:** A div `<div class="w-full bg-slate-200...">` com width percentual MUST ser aniquilada e substituída exclusivamente pelo componente React `<Progress value={80} className="[&>div]:bg-primary h-3" />` do Shadcn.
- **Botão de Reserva:** MUST usar `<Button className="bg-accent-teal w-full h-14 rounded-xl"> Reservar Agora </Button>`.

Essa blindagem assegura que a geometria das fotos do Stitch seja mantida intacta, mas o "motor de renderização" web passe a ser 100% componentes blindados do ecossistema Shadcn App Router.
