# Spec: Autenticação do Administrador (Admin Auth)

## Requirement: Proteção de Acesso ao Painel Administrativo

O sistema MUST restringir o acesso a todas as rotas `/admin/*` exclusivamente a usuários autenticados com `role=ADMIN`. O mecanismo de autenticação MUST operar via JWT Bearer Token obtido por login com `email` e `password`.

---

### Cenário: Login bem-sucedido com credenciais válidas

- **Dado** que existe um usuário com `role=ADMIN` cadastrado no banco de dados,
- **Quando** o administrador enviar uma requisição `POST /admin/auth/login` com `email` e `password` corretos,
- **Então** o sistema MUST retornar HTTP 200 com um `access_token` JWT válido no corpo da resposta.
- **E** o token MUST conter o identificador do admin e o campo `role=ADMIN` nos claims.
- **E** o token MUST ter expiração de 8 horas a partir do momento de geração.

---

### Cenário de Erro: Credenciais inválidas (email ou senha incorretos)

- **Dado** que o endpoint `POST /admin/auth/login` está disponível,
- **Quando** o administrador enviar credenciais com email não cadastrado ou senha incorreta,
- **Então** o sistema MUST retornar HTTP 401 Unauthorized.
- **E** a mensagem de erro MUST ser genérica ("Credenciais inválidas") sem indicar qual campo está errado.
- **E** nenhum token MUST ser gerado ou retornado.

---

### Cenário de Erro: Payload de login incompleto ou malformado

- **Dado** que o endpoint `POST /admin/auth/login` recebe uma requisição,
- **Quando** o payload estiver ausente, sem o campo `email` ou sem o campo `password`,
- **Então** o sistema MUST retornar HTTP 422 Unprocessable Entity com descrição dos campos inválidos.

---

### Cenário: Acesso a rota protegida com token válido

- **Dado** que o administrador possui um JWT Bearer Token válido e não expirado,
- **Quando** ele enviar uma requisição a qualquer rota sob `/admin/*` com o header `Authorization: Bearer <token>`,
- **Então** o sistema MUST processar a requisição normalmente e retornar a resposta esperada da rota.

---

### Cenário de Erro: Acesso a rota protegida sem token

- **Dado** que existe uma rota protegida sob `/admin/*`,
- **Quando** uma requisição for enviada a essa rota sem o header `Authorization`,
- **Então** o sistema MUST retornar HTTP 403 Forbidden.
- **E** a resposta MUST informar que autenticação é necessária sem expor detalhes internos.

---

### Cenário de Erro: Acesso com token expirado

- **Dado** que o administrador possui um JWT Bearer Token cujo tempo de expiração (`exp`) já foi ultrapassado,
- **Quando** ele enviar uma requisição a qualquer rota sob `/admin/*` com esse token,
- **Então** o sistema MUST retornar HTTP 403 Forbidden.
- **E** a mensagem MUST indicar que o token expirou e que um novo login é necessário.

---

### Cenário de Erro: Acesso com token adulterado ou assinatura inválida

- **Dado** que um token com assinatura inválida ou payload adulterado é enviado,
- **Quando** o middleware de autenticação processar esse token,
- **Então** o sistema MUST retornar HTTP 403 Forbidden sem processar a requisição subjacente.
- **E** MUST NOT expor qual parte da validação falhou.

---

### Cenário de Erro: Usuário com role diferente de ADMIN tenta acessar rotas admin

- **Dado** que existe um token JWT válido pertencente a um usuário com `role=CUSTOMER`,
- **Quando** esse token for utilizado para acessar qualquer rota sob `/admin/*`,
- **Então** o sistema MUST retornar HTTP 403 Forbidden.
- **E** o acesso MUST ser negado independentemente da validade da assinatura do token.
