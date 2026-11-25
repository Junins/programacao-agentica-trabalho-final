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
