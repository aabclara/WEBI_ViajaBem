# Design System Master File (Strict Viaje Bem SDD)

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** Viaje Bem (MVP)
**Category:** Travel/Tourism Agency
**Aesthetic:** Minimalist Classic

---

## Global Rules

### 1. Color Palette (Variáveis Tailwind Obrigatórias)

A aplicação deve restringir seu gamut visual a estes exatos Hexadecimais no `tailwind.config.ts`:

| Role | Hex | Tailwind Class Name | Uso Semântico |
|------|-----|-------------------|---------------|
| Primary / Urgency | `#ffa914` | `bg-primary` | Barras de Gamificação (`Progress`), Botão Hero de Descoberta. |
| Secondary / Action | `#0DBDC2` | `text-accent-teal` / `bg-accent-teal`| Botões de transação garantida ("Reservar Agora"), Âncoras e Links. |
| Background Light | `#F7F2E8` | `bg-background-light` | Fundo base global da Aplicação HTTP. |
| Background Dark | `#231c0f` | `bg-background-dark` | Suporte a Dark Mode foliar (Header/Footer). |
| Cards & Containers | `#ffffff` | `bg-card-white` | Fundo de vitrines, cartões e modais elevados. |
| Text Main | `#1F1F1F` | `text-text-main` | Tipografia massiva de alto contraste (WCAG AAA). |

### 2. Typography

A interface bane fontes serifadas ou cursivas randômicas. A espinha dorsal tipográfica provê clareza mecânica.

- **Global Font Family:** `Inter` (sans-serif).
- **Weights:** Regular (400), Medium (500), Bold (700) e Black (900).
- **Google Fonts Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
```

### 3. Spacing, Sizing e Acessibilidade Tátil

- **Touch Targets Base:** `h-14` (56px) para todos os `<Button>`s e inputs centrais. Interfaces com falhas de clique em telas mobile estão vetadas.
- **Borders (Rounded):** Componentes pai (`Card`, `Dialog`) usam classe estrita `rounded-xl` (12px). `<Button>`s podem chegar a `rounded-full` ou `rounded-xl`.
- **Shadows:** A estruturação de eixo Z baseia-se em `shadow-md` para repouso, ascendendo a `shadow-xl` / `shadow-2xl` em *Hover States* (Elevação tátil na Vitrine).

---

## Governança Estrutural UI (shadcn/ui e Lucide)

Para aniquilar invenções de UI (`UI Drift`), **NENHUM** componente deverá ser escrito usando blocos crús de `<button>` ou `<div>`s de formulários com CSS arbitrário. O Ecossistema React será construído encapsulado.

### Componentes Obrigatórios (Shadcn CLI)
- **Ações:** `<Button variant="default">` (herdará o Laranja `#ffa914`) e variações secudárias.
- **Containers de Destinos:** `<Card>`, `<CardHeader>`, `<CardContent>`.
- **Atrito Progressivo (Checkout):** Apenas invocáveis via `<Sheet>` (painel lateral) ou `<Dialog>` (Modal central). Proíbe-se roteamento destrutivo `/checkout`.
- **Dashboards:** A listagem "Minhas Viagens" e CRM dão-se estritamente através do `<Table>` nativo providenciando semântica de linhas, ou Grid Layout em Kanban com Optimistic UI.
- **Pressão de Vendas (Gamificação):** Obrigatório injetar o `<Progress value={X} />` pintando sua barra indicadora secundária na cor primária alaranjada.

### Iconografia Restringida
- ❌ **Proibido Emojis (👎 ✈️ 🚌).**
- ✅ **Aprovado:** Pacote mandatário NPM `lucide-react`. Renderizar como `<Icons.mapPin />`, `<Icons.clock />`, `<Icons.users />`.

---

## Anti-Patterns (Violações de SDD UI)

- ❌ Escrever CSS puro (ex: `.btn-primary { background: red; }`). **(Apenas Tailwind e Shadcn permitidos).**
- ❌ Omitir estados de `Hover` ou `Focus-visible`. (A11Y é mandatória).
- ❌ Componentes transacionais (CTAs de compra) menores que 48px de altura celular.
- ❌ Renderizar toda a lista de viagens num `Client Component`. SEO exige `Server Component` na `page.tsx` base injetando componentes de cliente só nas folhas (Ex: o Botão em si).
- ❌ Submeter requisições cegas sem bloqueio tátil de `<Button disable={pending}>` ou Loader em andamento.
