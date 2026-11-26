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

**Teto de gasto:** _a definir por mim antes de continuar._

---

**Combinado com o professor em:** _data_ · **Ajustes:** _ ·
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
   entender o que cada trecho faz, porque a lógica passa por SQL e HTTP, que conheço;
   o que não dá para deduzir lendo é o que o agente escolheu quando o pedido não dizia.
2. Espero que a minha confiança acompanhe os meus acertos: alta onde acerto, baixa onde
   erro, porque estou acostumado(a) a ler o código que um agente escreve.
3. Na manutenção 1, sem agente, espero levar mais tempo do que vou prever, embora as
   minhas estimativas costumem acertar. O motivo: ler Python é diferente de escrever, e
   para mudar o código terei de escrever numa linguagem que conheço pouco.
4. Na manutenção 2, com agente, espero que a previsão erre menos, porque quem escreve o
   Python é o agente, e o meu tempo vai para entender e conferir.

---

**Combinado com o professor em:** _data_ · **Ajustes:** _ ·
**Li e assumo a hipótese de 26/11:** _nome e data_
