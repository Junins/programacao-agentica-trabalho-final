# Diário do agente

Escrito pelo agente durante o trabalho. Horários tirados do relógio da máquina (`date`).
Harness: Claude Code 2.1.332. Modelo: claude-opus-5-5. Sistema: Windows 10, Python 3.13.15.
Gasto: não é visível para o agente; a pessoa deve anotar o valor mostrado por `/cost`.

## 25/11/2026 16:44 — início

- Pedido recebido, na íntegra: "Faça o trabalho. Ele pode ser feito individualmente."
- A pergunta, o cenário e a hipótese da proposta foram escolhidos pelo agente.
- Não há Flask, pytest, LaTeX nem Docker na máquina.

## Etapa 1: regras e banco — previsão

- Tempo: 10 min. Espero que os testes achem 1 ou 2 erros meus.
- Onde acho que vai dar problema: conflito de horário entre atividades e contagem de vagas.

### Etapa 1 — o que aconteceu (16:47)

- Primeira tentativa de gravar os arquivos por um comando único do shell foi recusada
  (`unexpected EOF while looking for matching`); nada foi gravado. Reescrevi com a
  ferramenta de escrita de arquivos. Não investiguei a causa.
- 10 testes, todos passaram na primeira execução. Previsão errada nos dois pontos:
  levou cerca de 1 min e meio, e os testes não acharam erro.
- Ressalva: os testes foram escritos por quem escreveu o código, na mesma hora. Passar
  de primeira pode significar só que os dois têm o mesmo ponto cego.

## Etapa 2: servidor e páginas — previsão (antes de escrever)

- Tempo: 5 min. Delegação: total; ninguém revisou a etapa 1 ainda.
- Onde acho que vai dar problema: senha da coordenação e escape de HTML. Vou testar
  com o servidor de verdade, por HTTP, e não só com testes de função.

### Etapa 2 — o que aconteceu (16:48)

- 16 testes (6 por HTTP, com o servidor no ar), todos passaram na primeira execução.

## Etapa 3: verificar a verificação — previsão (antes de executar)

- Vou usar o sistema num Chrome de verdade e estragar o código de propósito, uma linha
  por vez, para ver se os testes percebem (mutação).
- Mutação: espero que 1 ou 2 de 10 escapem.
- Navegador: suspeito que o envio de formulário falhe. O servidor manda
  `Referrer-Policy: no-referrer` e recusa `Origin` diferente do próprio host; acho que
  com essa política o navegador envia `Origin: null`. Os testes não mandam `Origin` e
  por isso não veriam.

### Etapa 3a: navegador — o que aconteceu (16:49)

- Confirmado com `registro/navegador.mjs` no Chrome 158: `POST /inscrever` → 403
  "Origem não permitida". Com 16 de 16 testes verdes, o sistema não servia para ninguém.
- Defeito meu, causado por duas proteções que escrevi e que se anulavam. Se eu tivesse
  entregue ao fim da etapa 2, teria dito "pronto, 16 testes passando".
- Ainda sem correção neste commit.

### Etapa 3 — o que aconteceu

- Correção de 3a: `Referrer-Policy: same-origin`. No Chrome, a inscrição passou a chegar
  em `/minha`. Teste de regressão acrescentado.
- Mutação: planejei 10, escrevi 16; 11 percebidas e 5 escaparam
  (`registro/mutacao-resultado.txt`). A previsão (1 ou 2 de 10) errou para menos.
- Das 5: a nº 2 é equivalente (a lista já vem ordenada por início); a nº 5 (`BEGIN`)
  depende de corrida entre threads e o meu teste de corrida não a reproduz com certeza;
  as nº 8, 12 e 16 eram falta de teste, e acrescentei um para cada.
- Correção sobre este diário: os horários nos títulos das etapas 1, 2 e 3a foram
  arredondados por mim, não copiados do relógio; o de 3a (16:49) está adiantado. Valem
  as datas dos commits.
- Cortado: cancelar inscrição, editar atividade, presença por QR code, reabrir o evento,
  envio de e-mail, hospedagem. Motivo: o produto não entra na nota e precisa caber na
  cabeça de uma pessoa só.
