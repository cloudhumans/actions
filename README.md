# CloudHumans Reusable GitHub Actions

Monorepo de actions reutilizáveis da organização CloudHumans. Cada action vive em um subdiretório na raiz e pode ser versionada via tags (`v1`, `v2`, etc.).

## Objetivo
Padronizar lógica repetitiva de pipelines (versão, processamento de templates, etc.) reduzindo boilerplate e risco de divergência entre repositórios.

## Estrutura

```
actions/
  app-version/        # Action que gera APP_VERSION + (opcional) processa templates
  .github/workflows/  # Testes automatizados das actions
  README.md           # Este arquivo
```

Cada pasta de action contém:
- `action.yml` (definição composite)
- `README.md` específico
- Scripts auxiliares

## Actions Disponíveis

| Action | Caminho | Descrição |
|--------|---------|-----------|
| app-version | `app-version/` | Calcula versão baseada em arquivo/override + metadata do commit e opcionalmente expande variáveis em templates. |

## Como Consumir

Referencie usando `uses: cloudhumans/actions/<pasta>@v1` após publicar a tag:

```yaml
- name: Compute version
  uses: cloudhumans/actions/app-version@v1
  with:
    version_file: version
    format: "{base}-{sha7}"
```

## Desenvolvimento

1. Adicione/edite a action em um novo diretório.
2. Crie/atualize testes em `.github/workflows/*` garantindo cobertura mínima (happy path + edge cases).
3. Abra PR.
4. Após merge: crie/atualize tag major (`git tag v1 && git push origin v1`).

## Versionamento

Siga SemVer sempre que possível. Ao quebrar compatibilidade, incremente major (`v2`). Mantenha a tag major apontando para a última minor patch estável.

## Boas Práticas
- Evite dependências desnecessárias (ações composite puras em bash/python simples).
- Saídas (outputs) claras e documentadas.
- Falhar cedo com mensagens (`::error`).
- Testes rápidos (< 1 min) para feedback contínuo.

## Roadmap Geral
- Action para build/publish Docker padronizado
- Action para validação de manifests
- Action para bump semver automático

## Contribuições
PRs e issues são bem-vindos. Descreva claramente a motivação e impacto.

---
CloudHumans Engineering