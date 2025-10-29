# Como Configurar o Token do GitHub

## 1. Gerando o Token de Acesso

1. Acesse o GitHub e faça login
2. Vá para **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Clique em **"Generate new token (classic)"**
4. Configure o token:
   - **Note**: Lab03 - Code Review Analysis
   - **Expiration**: 90 days (ou conforme sua preferência)
   - **Scopes** necessários:
     - ✅ `public_repo` (acesso a repositórios públicos)
     - ✅ `read:org` (leitura de informações de organizações)

## 2. Configurando no Projeto

1. Copie o token gerado (algo como `ghp_xxxxxxxxxxxx`)
2. Renomeie o arquivo `.env.example` para `.env`
3. Edite o arquivo `.env` e cole seu token:
   ```
   GITHUB_TOKEN=ghp_seu_token_real_aqui
   ```

## 3. Testando a Configuração

Execute o teste rápido:
```bash
python quick_test.py
```

Se tudo estiver correto, você verá uma lista dos 10 repositórios mais populares do GitHub.

## 4. Rate Limits

- Token autenticado: 5,000 requests/hora
- Sem token: 60 requests/hora

O sistema inclui gerenciamento automático de rate limiting com pausas apropriadas.

## 5. Segurança

⚠️ **IMPORTANTE**: 
- Nunca compartilhe seu token
- Não faça commit do arquivo `.env`
- O arquivo `.env` já está no `.gitignore`