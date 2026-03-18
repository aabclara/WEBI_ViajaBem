# Spec: Modelagem Visual de Interface e Componentes (UI/UX)

## Requirement: Padronização Visual Estrita
A interface de usuário MUST respeitar rigorosamente a identidade visual definida para a agência ("Viaje Bem"), ancorada no uso oficial do ecossistema de componentes `shadcn/ui` e padronizações estabelecidas no Design System oficial.

### Cenário: Estrutura Base e Identidade Visual (Cores)
- **Dado** o processo de renderização global da aplicação web perante o usuário final,
- **Quando** elementos foliares base de estrutura e navegação carregarem de forma interativa,
- **Então** o fundo global da aplicação MUST respeitar o código e tom unificado do domínio (Fundo Creme/`#F7F2E8`).
- **E** os elementos interativos, chamadas âncora, ou hyperlinks de navegação SHALL implementar reatividade de foco ou hover expressando coloração Ciano (`#0DBDC2`), operando navegação ágil provida essencialmente por roteamento Single Page Application (SPA).
- **E** a interface MUST exibir identificação vetorial clássica restrita à biblioteca `lucide-react`, proibindo Emojis ou SVGs randômicos descolados do grid nativo.

### Cenário: Representação Visual de Viagens no Catálogo
- **Dado** que a interface recebeu dados ativos de expedições ou pacotes de viagens e de métricas de lotação/escassez,
- **Quando** processar o mapeamento destes elementos na página de catálogo visual (Home),
- **Então** cada ocorrência MUST gerar um componente modularizado (Card Component) apresentando formatações com arredondamento explícito.
- **E** a UI MUST instanciar para os Cards o componente nativo de preenchimento em barra exibindo proporção real (`<Progress />`), imperativamente na cor Laranja de Advertência (`#FFA915`) reforçando gamificação e escassez do Estoque no negócio.
- **E** zonas designadas para processamento de rotinas principais MUST assegurar dimensões acessíveis ao toque (no mínimo limites recomendados mobile-first) integrados junto à estilização complementar de destaque direcional (Ciano Acionável).
