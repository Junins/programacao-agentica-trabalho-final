---
name: mapear
description: Descreve um repositório desconhecido para quem vai ficar responsável por ele - camadas, pontos de entrada, como rodar e testar - e escreve um mapa curto em onboarding/mapa.md. Use no primeiro contato com um código legado, antes de explicar qualquer regra.
---

# Mapear o repositório

> RASCUNHO do agente (26/11/2026). Reescrito por mim em: ___

Objetivo: a pessoa sair sabendo **onde está cada coisa** e **como fazer o sistema rodar**,
sem ainda saber o que cada regra decide.

## Fase 0: perguntar antes de ler

1. Pergunte à pessoa o que ela já sabe (linguagens, banco, web) e o que ela vai ter de
   fazer no código. O mapa é escrito para esse nível.
2. Pergunte se há partes que ela **não** quer ver explicadas ainda (por exemplo, por
   causa de um teste de compreensão). Respeite isso em todos os passos.

## Passos

1. Liste a árvore de arquivos (sem dependências, sem gerados). Para cada pasta, uma frase.
2. Ache os pontos de entrada: o que se executa para subir o sistema, para testar, scripts
   avulsos. Mostre o comando exato.
3. **Rode** o comando de testes e o de subir o sistema. Registre o que aconteceu, mesmo
   se falhar. Não descreva comportamento que você não viu.
4. Desenhe as camadas em texto (quem chama quem), citando `arquivo:linha` da função de
   entrada de cada camada.
5. Liste dependências externas e onde ficam os dados.
6. Escreva `onboarding/mapa.md` com no máximo uma página. No fim, três perguntas que a
   pessoa deveria conseguir responder depois de ler o mapa.

## Não faça

- Não explique o que as regras aceitam ou recusam: isso é das outras skills.
- Não corrija nada que encontrar; anote em "Estranhezas" no fim do mapa.

## Lições

| Sintoma | Correção |
|---|---|
| mapa vira explicação do código inteiro | cortar para uma página; detalhe vai para `explicar-fluxo` |
| ___ | ___ |
