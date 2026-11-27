# Proposta: quem ainda entende este código?

Trabalho individual. Escrita em 25/11/2026, antes de qualquer código.

> **Quem escreveu.** Este texto foi redigido pelo agente (Claude Code) a partir do
> pedido "Faça o trabalho. Ele pode ser feito individualmente.". A pergunta e a
> hipótese só passam a ser minhas quando eu as ler, corrigir e assinar no fim desta
> página. Se eu mudar algo, escrevo a versão nova embaixo da antiga, com data e motivo.

**Pergunta:** consigo explicar e manter um código que um agente escreveu quase
sozinho, a partir de um pedido curto?

**Hipótese:** espero conseguir explicar o caminho principal (inscrição, presença,
certificado) e errar nas regras que o agente decidiu sem me perguntar, porque um
pedido curto deixa buracos e quem preenche é ele. Espero também que a primeira
manutenção sem agente leve mais tempo do que eu prever, e que a previsão da segunda
erre menos, porque nessa altura já terei lido o código.

**Cenário.** A coordenação de um curso organiza a semana acadêmica. O pedido:

> "Oi! Todo ano na semana acadêmica é a mesma correria: o pessoal se inscreve num
> formulário, eu passo pra planilha, na porta rola uma lista de papel e depois fico uma
> semana fazendo certificado no Word, um por um. Queria inscrição, presença e
> certificado num lugar só. Ah, e o certificado só pode sair pra quem veio mesmo.
> Consegue pra esse ano?"

**O que será construído.** Um sistema web pequeno, sem dependências externas e sem IA
dentro: inscrição em atividades, chamada pela coordenação, certificado imprimível e
conferência do certificado. Dados fictícios.

**Como observar.**
1. O agente constrói e mantém um diário com previsão antes e resultado depois de cada
   etapa. Os commits dele saem com autor "Claude Code (agente)", para o `git blame`
   separar o que é dele do que é meu.
2. Sem rodar o programa, respondo a perguntas do tipo "o que acontece se...", com a
   minha confiança em cada uma; um script executa as situações e mostra a resposta.
   Uma rodada antes das manutenções (A) e outra, com perguntas diferentes, depois (B).
3. Duas manutenções que só abro na hora: a primeira sem agente; a segunda com agente,
   e só aceito o que eu conseguir explicar. Antes de cada uma anoto a previsão.

**Onde aperta.** Sou uma pessoa só, então o resultado vale para mim. Quem escreveu as
perguntas e as manutenções foi o mesmo agente que escreveu o código.

**Teto de gasto:** o valor de uma mensalidade da assinatura Claude Pro, sem nenhum gasto além dela (sem API paga e sem uso extra). Definido por mim em 26/11/2026, registrado pelo agente a meu pedido.

---

**Combinado com o professor:** sem conversa à parte; vale a orientação dele por mensagem, repassada em 26/11/2026 (diário do agente, etapa 10). Pendências descartadas em 27/11/2026 a pedido da pessoa. ·
**Li e assumo a pergunta e a hipótese:** _nome e data_

---

## Ajuste de 25/11/2026 (redigido pelo agente)

Motivo: avisos do professor. A pergunta e a hipótese acima não mudam.

- O artigo pode ser um por grupo, com relato individualizado em arquivo separado
  (`relatos/`). Como sou uma pessoa só, há um artigo e um relato.
- 27/11/2026 é a primeira entrega, de acompanhamento. A entrega final é na semana seguinte.
- As medições (rodada A em diante) só começam depois da conversa de 27/11, porque a
  versão da hipótese combinada com o professor é a que vale como original.
- Se o tempo não der, corto a manutenção 2, e a parte da hipótese sobre a segunda
  previsão fica sem resposta. O corte é registrado.

**Segundo ajuste de 25/11/2026** (redigido pelo agente a partir do que a pessoa informou):
trabalho individual confirmado; apresentação em 04/12/2026. Pergunta e hipótese não mudam.

---

## Hipótese revista em 26/11/2026

**Quem escreveu.** Redigida pelo agente a meu pedido, a partir das minhas respostas de
26/11 (registradas na etapa 9 do diário do agente). A pergunta não muda. A hipótese
de 25/11 fica acima, como estava.

**Motivo.** A de 25/11 foi escrita pelo agente sem saber nada de mim. A parte sobre
prazo contrariava a minha experiência, e o "porquê" não era meu.

**De onde parto.** Sei pouco de Python e bastante de SQL e HTTP. Já usei agentes para
programar e na maioria das vezes lia o código que eles escreviam. Já mantive código de
outra pessoa, e as minhas estimativas de prazo não erraram.

**Hipótese:**

1. Nas rodadas de perguntas, espero errar nas regras que o agente decidiu sem me
   perguntar, e não por causa da linguagem. Mesmo sabendo pouco de Python, espero
   entender o que cada trecho faz, porque já li código Python antes; o que não dá para deduzir
   lendo é o que o agente escolheu quando o pedido não dizia.
2. Espero que a minha confiança acompanhe os meus acertos: alta onde acerto, baixa onde
   erro, porque costumo ler o código que um agente escreve.
3. Na manutenção 1, sem agente, espero levar mais tempo do que vou prever, embora as
   minhas estimativas costumem acertar. O motivo: ler Python é diferente de escrever, e
   para mudar o código terei de escrever numa linguagem que conheço pouco.
4. Na manutenção 2, com agente, espero que a previsão erre menos, porque quem escreve o
   Python é o agente, e o meu tempo vai para entender e conferir.

O motivo do item 1 é meu. Os motivos dos itens 3 e 4 foram deduzidos pelo agente e
confirmados por mim em 26/11/2026.

---

**Combinado com o professor:** sem conversa à parte; vale a orientação dele por mensagem, repassada em 26/11/2026 (diário do agente, etapa 10). Pendências descartadas em 27/11/2026 a pedido da pessoa. ·
**Li e assumo a hipótese de 26/11:** Junins, 26/11/2026 (pedido feito por mim ao agente, que registrou)

---

## Ajuste de 26/11/2026: skills de onboarding (adotado em 27/11)

**Quem escreveu.** Redigida pelo agente a meu pedido, em 26/11. Adotada em 27/11/2026,
antes da rodada A: não há o que combinar com o professor além das mensagens dele.
Nada foi medido até aqui.

**Motivo.** Orientação do professor: usar IA agêntica para me apropriar de um
repositório a ponto de fazer coisa nova nele, e apresentar as ferramentas que me
ajudaram a entender. Ele indicou como exemplo o voicebox
(https://github.com/jamiepine/voicebox), que tem skills de agente em `.agents/skills/`.
Resumo dele: skills ou metodologia que descrevam, expliquem e ensinem um código legado
a quem vai ficar responsável por ele.

**Pergunta nova:** como uso IA agêntica, com skills e uma metodologia, para me apropriar
de um código legado que um agente escreveu, a ponto de fazer algo novo nele? A pergunta
antiga ("consigo explicar e manter?") vira a medida, e a hipótese de 26/11 continua.

**O que muda.**
- Cinco skills em `.agents/skills/` (`mapear`, `explicar-fluxo`, `ensinar`,
  `decisoes-implicitas`, `preparar-mudanca`). Rascunhadas pelo agente; eu reescrevo
  cada uma antes de usar, em commit meu.
- A rodada A continua sem IA, como linha de base, e vem antes de qualquer skill rodar em
  `produto/`.
- Para cada skill usada, anoto: tempo, o que aprendi, o que ela errou ou inventou, se
  usaria de novo. Isso vira a tabela de ferramentas do artigo e da apresentação.
- Na manutenção 1 eu escrevo o código; as skills só ajudam a entender e preparar.
- Opcional, se sobrar tempo: rodar `mapear` e `explicar-fluxo` no voicebox, só leitura,
  para ver se servem fora deste projeto.

**Item 5 da hipótese** (respostas minhas de 27/11/2026, dadas antes de usar qualquer
skill; redação do agente, a meu pedido): espero que a skill que mais me ajude a me
apropriar do código seja `ensinar`, porque ela ataca o meu ponto fraco, que é o Python.
Vou saber que ajudou se, depois de usá-la, eu entender onde errei na rodada A. Não tenho
expectativa sobre as skills reescritas por mim em relação ao rascunho do agente; vou só
registrar o que acontecer.

**Sequência proposta.**

| Quando | O quê |
|---|---|
| sex 27/11 | conversa com o professor; rodada A sem IA |
| sáb 28/11 | reescrever as skills; ler `registro/decisoes-do-agente.md` só depois de rodar `decisoes-implicitas` |
| dom 29/11 | usar as skills em `produto/` e anotar cada uso |
| seg 30/11 | manutenção 1 (eu escrevo; skills para entender) |
| ter 1/12 | manutenção 2 (agente escreve) e rodada B |
| qua 2 a qui 3/12 | relato, artigo e ensaio, com a tabela de skills no centro |
| sex 4/12 | apresentação |

**Combinado com o professor:** sem conversa à parte; vale a orientação dele por mensagem, repassada em 26/11/2026 (diário do agente, etapa 10). Pendências descartadas em 27/11/2026 a pedido da pessoa. ·
**Li e assumo este ajuste:** Junins, 27/11/2026 (pedido feito por mim ao agente, que registrou)
