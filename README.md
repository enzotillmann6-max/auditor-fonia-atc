# Auditor de fonia ATC — Torre de Congonhas (SBSP)

Agente que escuta a fonia publica da Torre de Congonhas, transcreve o audio
e sinaliza desvios de fraseologia e situacoes de risco, gerando relatorios
que um auditor humano pode conferir contra o audio original.

## Módulos

- `config.yaml` — parametros: URL do stream, duracao do bloco, modelo do Whisper.
- `capture.py` — conecta no stream de audio da Torre, grava blocos de 60s
  em MP3 na pasta `audio/`, reconecta sozinho se a conexao cair.
- `transcribe.py` — le os blocos de `audio/`, transcreve com faster-whisper
  (modelo local, sem API paga), filtra alucinacoes (silencio, repeticao,
  vinheta) e grava tudo em `transcricoes.jsonl`.
- `rules.py` — le `transcricoes.jsonl`, procura os gatilhos de severidade
  critica e alta (emergencia, arremetida, transponder 7500/7600/7700 etc.)
  e grava as ocorrencias em `ocorrencias.jsonl`.
- `relatorio.py` — le `ocorrencias.jsonl` e gera um arquivo `.md` por
  ocorrencia na pasta `relatorios/`, com categoria, severidade, trecho e
  norma de referencia.
- `avulso.py` — modo avulso: transcreve e audita um unico arquivo de audio
  local, sem depender do stream. Util para testar sem esperar a captura.

## Instalação

Requer Python 3 instalado.

pip install requests pyyaml faster-whisper


## Execução

1. Editar `config.yaml` se quiser mudar a URL do stream, a duração do
   bloco ou o modelo do Whisper.
2. Rodar a captura (deixa rodando continuamente):

python capture.py

3. Em outra janela, rodar a transcrição (roda em paralelo, pega os blocos
   novos conforme eles ficam prontos):

python transcribe.py

4. Quando quiser gerar as ocorrências e os relatórios (pode rodar a
   qualquer momento, nao precisa esperar a captura terminar):

python rules.py
python relatorio.py



### Modo avulso

Para testar com um arquivo de audio local, sem depender do stream:

python avulso.py "caminho/do/arquivo.mp3"


## Limitações conhecidas

- O motor de regras atual cobre os gatilhos de texto fixo (emergência,
  arremetida, transponder, fauna, reclamação, etc.). Desvios que exigem
  contexto (cotejamento incompleto, indicativo omitido) ainda nao sao
  cobertos — ficariam a cargo de uma analise por LLM (diferencial nao
  implementado nesta entrega).
- A transcrição erra mais em números e indicativos de chamada, por isso
  o áudio de cada bloco fica guardado como evidência; o relatório e
  triagem, não veredito.
- Os relatórios ajudam a auditoria e não substituem os canais oficiais
  de reporte (CENIPA e DECEA).
