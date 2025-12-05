# Guia de Configuração do Token GitHub

## Por que preciso de um token?

O GitHub limita o número de requisições que você pode fazer sem autenticação (60 por hora). Com um token, você pode fazer até 5.000 requisições por hora, essencial para experimentos que fazem múltiplas chamadas à API.

## Como criar um token

### Passo 1: Acesse as configurações do GitHub
1. Faça login no [GitHub](https://github.com)
2. Clique na sua foto de perfil (canto superior direito)
3. Clique em **Settings**

### Passo 2: Gerar um Personal Access Token (Classic)
1. No menu lateral, role até o final e clique em **Developer settings**
2. Clique em **Personal access tokens**
3. Clique em **Tokens (classic)**
4. Clique no botão **Generate new token** → **Generate new token (classic)**

### Passo 3: Configurar o token
1. **Note**: Dê um nome descritivo (ex: "Lab Experimentação")
2. **Expiration**: Escolha um prazo (recomendado: 30 dias)
3. **Scopes**: Marque as seguintes permissões:
   - ✅ `public_repo` (acesso a repositórios públicos)
   - ✅ `read:org` (leitura de dados de organizações)
   - ✅ `read:user` (leitura de perfil de usuário)

4. Role até o final e clique em **Generate token**

### Passo 4: Copiar o token
⚠️ **IMPORTANTE**: O token só será mostrado UMA VEZ!

1. Copie o token (começa com `ghp_`)
2. Cole no arquivo `experiment/main.py`:

```python
GITHUB_TOKEN = "ghp_seu_token_aqui"
```

## Segurança

- ❌ **NUNCA** compartilhe seu token
- ❌ **NUNCA** faça commit do token em repositórios públicos
- ✅ Use `.gitignore` para ignorar arquivos de configuração
- ✅ Revogue tokens antigos que não está mais usando

## Testando o token

Depois de configurar, execute:

```bash
python experiment/main.py
```

Se tudo estiver correto, o experimento iniciará sem erros de autenticação.

## Problemas Comuns

### "Você esqueceu de colocar seu Token"
→ Certifique-se de que substituiu `"TOKEN"` pelo seu token real.

### "Rate limit exceeded"
→ Você atingiu o limite de requisições. Aguarde 1 hora ou use um token válido.

### "Bad credentials"
→ O token está incorreto ou expirado. Gere um novo token.

## Revogar um token

Se você expôs acidentalmente seu token:

1. Vá em **Settings** → **Developer settings** → **Personal access tokens**
2. Encontre o token comprometido
3. Clique em **Delete**
4. Gere um novo token

---

**Data**: Dezembro de 2025
