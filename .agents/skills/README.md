# Skills de onboarding em código legado (PROPOSTA)

Rascunho do agente (Claude Code), 26/11/2026, a meu pedido. Eu vou reescrever cada uma;
a versão que valer é a minha, num commit meu. Nada aqui foi usado ainda.

Motivo: orientação do professor de usar IA agêntica para me apropriar de um repositório
e fazer coisa nova nele, com skills ou uma metodologia que descrevam, expliquem e ensinem
um código legado a quem vai ficar responsável por ele. O formato imita o das skills do
repositório de exemplo indicado por ele (https://github.com/jamiepine/voicebox, pasta
`.agents/skills/`): frontmatter com `name` e `description`, passos numerados, um
levantamento escrito antes de mexer e uma tabela de lições.

| Skill | Para quê | Produz |
|---|---|---|
| `mapear` | descrever o repositório por fora: camadas, entradas, como rodar e testar | `onboarding/mapa.md` |
| `explicar-fluxo` | seguir um caso de uso de ponta a ponta, com arquivo e linha | `onboarding/fluxo-<nome>.md` |
| `ensinar` | perguntar "o que acontece se...", receber resposta e confiança, conferir executando | `onboarding/aulas.md` |
| `decisoes-implicitas` | achar regras que o código impõe e que ninguém pediu | `onboarding/decisoes.md` |
| `preparar-mudanca` | levantamento antes de uma manutenção: arquivos, riscos, testes | `onboarding/mudanca-<nome>.md` |

**Regra deste repositório:** nenhuma skill roda em `produto/` antes de eu conferir a
rodada A (`experimento/perguntas-a.md`), porque elas entregariam as respostas.
`decisoes-implicitas` também não roda antes de eu ler `registro/decisoes-do-agente.md`
por conta própria, senão não dá para comparar.

Para cada uso, anoto no meu diário: qual skill, quanto tempo, o que aprendi que não
sabia, o que ela errou ou inventou, e se eu usaria de novo.
