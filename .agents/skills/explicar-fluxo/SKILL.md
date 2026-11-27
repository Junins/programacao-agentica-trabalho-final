---
name: explicar-fluxo
description: Explica um caso de uso de ponta a ponta (do clique ou da requisição até o banco e de volta), citando arquivo e linha em cada passo, e escreve onboarding/fluxo-<nome>.md. Use depois de mapear, quando a pessoa precisa entender um caminho específico.
---

# Explicar um fluxo

> RASCUNHO do agente (26/11/2026). Reescrito por mim em: ___

## Fase 0

1. Pergunte qual caso de uso, em palavras da pessoa ("alguém se inscreve", "sai o
   relatório"). Se ela não souber, ofereça a lista dos pontos de entrada do mapa.
2. Pergunte o nível: só o caminho feliz, ou também os erros.

## Passos

1. Ache onde o caso começa (rota, comando, botão). Cite `arquivo:linha`.
2. Siga chamada por chamada até o dado ser gravado ou lido, e depois até a resposta.
   Em cada passo: `arquivo:linha`, o que entra, o que sai, em uma ou duas frases.
3. Em cada trecho na linguagem que a pessoa conhece pouco, explique a construção da
   linguagem (por exemplo, `with`, decorador, exceção) separada da regra de negócio.
4. Marque com **[decisão]** todo lugar onde o código escolhe algo que o pedido original
   não dizia. Não justifique a decisão; só aponte.
5. **Confirme executando**: monte uma situação mínima (teste, script ou requisição) que
   passe pelo fluxo e mostre a saída. Se não conseguir executar, diga.
6. Escreva `onboarding/fluxo-<nome>.md`. No fim, peça à pessoa que conte o fluxo de volta
   com as palavras dela e aponte o que ficou errado.

## Não faça

- Não pule passos "óbvios": o óbvio para quem escreveu é o que falta para quem herda.
- Não afirme comportamento que só deduziu lendo; separe "li" de "executei".

## Lições

| Sintoma | Correção |
|---|---|
| ___ | ___ |
