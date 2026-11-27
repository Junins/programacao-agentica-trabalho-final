---
name: ensinar
description: Ensina um código legado por perguntas do tipo "o que acontece se...". A pessoa responde com uma confiança de 0 a 100, sem executar; a skill confere executando e explica o erro. Use quando a pessoa já leu o mapa e quer saber se entendeu de verdade.
---

# Ensinar por perguntas conferidas

> RASCUNHO do agente (26/11/2026). Reescrito por mim em: ___
> Generaliza o que `experimento/conferir.py` faz para as rodadas A e B.

## Fase 0

1. Pergunte qual parte do código e quantas perguntas (sugestão: 5).
2. Pergunte se já houve uma rodada de perguntas antes: não repita as dela.

## Passos (uma pergunta por vez)

1. Escreva **uma** situação concreta: estado inicial e ação. Ex.: "com X já feito, o que
   acontece se Y?". Misture caminho principal e casos de borda.
2. **Antes** de responder, escreva para você como vai conferir (teste, script, requisição).
3. Peça a resposta e a confiança (0 a 100). Espere. Não dê dicas.
4. Execute a conferência e mostre a saída real.
5. Se errou, classifique com a pessoa: **linguagem** (não entendeu a construção),
   **tecnologia** (SQL, HTTP...), ou **regra** (o código decide algo que não dava para
   saber). Explique só o que causou o erro, com `arquivo:linha`.
6. Anote em `onboarding/aulas.md`: pergunta, resposta, confiança, acertou, causa.
7. Depois de todas: compare confiança e acerto. Proponha a próxima pergunta na área
   onde errou com confiança alta.

## Não faça

- Não responda por ela nem aceite "não sei" sem pedir um palpite.
- Não confira só lendo o código: a resposta é a que a execução der.

## Lições

| Sintoma | Correção |
|---|---|
| pergunta entrega a resposta no enunciado | reescrever sem nomear a regra |
| ___ | ___ |
