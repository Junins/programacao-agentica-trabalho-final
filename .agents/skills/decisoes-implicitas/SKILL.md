---
name: decisoes-implicitas
description: Procura no código regras e escolhas que ninguém pediu explicitamente (limites, recusas, formatos, valores fixos, ordem de operações) e escreve onboarding/decisoes.md, comparando com o pedido original. Use quando a pessoa vai assumir um código e precisa saber o que foi decidido por quem escreveu.
---

# Achar decisões implícitas

> RASCUNHO do agente (26/11/2026). Reescrito por mim em: ___

## Fase 0

1. Peça o pedido original (mensagem, issue, especificação). Sem ele, não há como saber
   o que "não foi pedido"; diga isso e siga marcando tudo como "a confirmar".
2. Pergunte se existe registro das decisões feito por quem escreveu. Se existir, **não
   leia antes** de terminar a sua lista: o valor está em comparar as duas.

## Passos

1. Procure: constantes e números fixos; `if` que recusam ou lançam erro; restrições do
   banco (UNIQUE, NOT NULL, chaves); normalizações (maiúsculas, minúsculas, corte);
   ordem obrigatória entre ações; o que acontece com dado repetido.
2. Para cada uma: `arquivo:linha`, o que o código faz, trecho do pedido que a justifica
   (ou "nenhum"), e uma situação executável que mostra a decisão.
3. **Execute** cada situação e registre a saída.
4. Classifique: **pedida**, **dedutível** (consequência razoável do pedido),
   **escolha de quem escreveu**.
5. Escreva `onboarding/decisoes.md` como tabela. Só então compare com o registro de
   quem escreveu, se houver: o que só você achou, o que só ele anotou.
6. Para as "escolha de quem escreveu", sugira a pergunta a fazer a quem pediu o sistema.

## Não faça

- Não julgue se a decisão é boa; isso é com a pessoa e com quem pediu.
- Não invente justificativa no lugar de quem escreveu.

## Lições

| Sintoma | Correção |
|---|---|
| ___ | ___ |
