---
name: preparar-mudanca
description: Antes de uma manutenção num código legado, faz um levantamento escrito - arquivos a mexer, regras afetadas, riscos, testes que devem continuar passando e testes novos - em onboarding/mudanca-<nome>.md, sem escrever o código. Use quando a pessoa recebe um pedido de mudança e ainda não começou.
---

# Preparar uma mudança

> RASCUNHO do agente (26/11/2026). Reescrito por mim em: ___
> Inspirada na "fase 0" da skill `add-tts-engine` do voicebox: levantar antes de codar.

## Fase 0

1. Peça o pedido de mudança, inteiro. Pergunte quem vai escrever o código: a pessoa ou
   o agente. Se for a pessoa, esta skill **não escreve código** nenhum.
2. Peça que a pessoa anote a **previsão de tempo** antes de ler o levantamento.

## Passos

1. Reescreva o pedido em uma frase e liste o que ele **não** diz (os buracos).
2. Ache os arquivos e funções a mexer, com `arquivo:linha`, e diga por quê.
3. Liste as regras existentes que a mudança toca e o que pode quebrar em cada uma.
4. Rode os testes atuais e anote o estado (todos verdes ou não) antes de qualquer mudança.
5. Proponha os testes novos, em palavras: situação e resultado esperado. Não escreva o
   código deles se for a pessoa quem vai fazer.
6. Para quem sabe pouco da linguagem: liste as construções que provavelmente vai
   precisar (com link para a documentação oficial), sem resolver o problema.
7. Escreva `onboarding/mudanca-<nome>.md`. Peça a previsão de tempo de novo, agora
   depois de ler.

## Não faça

- Não comece a implementar. Não faça commit nem push.
- Não resolva os buracos do pedido sozinho: liste como perguntas.

## Lições

| Sintoma | Correção |
|---|---|
| ___ | ___ |
