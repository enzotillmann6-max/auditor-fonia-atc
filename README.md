# Auditor de fonia ATC — Torre de Congonhas (SBSP)

Agente que escuta a fonia pública da Torre de Congonhas, transcreve o áudio
e sinaliza desvios de fraseologia e situações de risco, gerando relatórios
que um auditor humano pode conferir contra o áudio original.

## Módulos

* `config.yaml` — parâmetros: URL do stream, duração do bloco, modelo do Whisper.
* `capture.py` — conecta no stream de áudio da Torre, grava blocos de 60s
  em MP3 na pasta `audio/`, reconecta sozinho se a conexão cair.
* `transcribe.py` — lê os blocos de `audio/`, transcreve com faster-whisper
  (modelo local, sem API paga), filtra alucinações (silêncio, repetição,
  vinheta) e grava tudo em `transcricoes.jsonl`.
* `rules.py` — lê `transcricoes.jsonl`, procura os gatilhos de severidade
  crítica e alta (emergência, arremetida, transponder 7500/7600/7700 etc.)
  e grava as ocorrências em `ocorrencias.jsonl`.
* `relatorio.py` — lê `ocorrencias.jsonl` e gera um arquivo `.md` por
  ocorrência na pasta `relatorios/`, com categoria, severidade, trecho e
  norma de referência.
* `avulso.py` — modo avulso: transcreve e audita um único arquivo de áudio
  local, sem depender do stream. Útil para testar sem esperar a captura.

## Instalação

Requer Python 3 instalado.

```bash
pip install requests pyyaml faster-whisper
```

## Execução

1. Editar `config.yaml` se quiser mudar a URL do stream, a duração do
   bloco ou o modelo do Whisper.
2. Rodar a captura (deixa rodando continuamente):

```bash
python capture.py
```

3. Em outra janela, rodar a transcrição (roda em paralelo, pega os blocos
   novos conforme eles ficam prontos):

```bash
python transcribe.py
```

4. Quando quiser gerar as ocorrências e os relatórios (pode rodar a
   qualquer momento, não precisa esperar a captura terminar):

```bash
python rules.py
python relatorio.py
```

### Modo avulso

Para testar com um arquivo de áudio local, sem depender do stream:

```bash
python avulso.py "caminho/do/arquivo.mp3"
```

## Limitações conhecidas

* O motor de regras atual cobre os gatilhos de texto fixo (emergência,
  arremetida, transponder, fauna, reclamação, etc.). Desvios que exigem
  contexto (cotejamento incompleto, indicativo omitido) ainda não são
  cobertos — ficariam a cargo de uma análise por LLM (diferencial não
  implementado nesta entrega).
* A transcrição erra mais em números e indicativos de chamada, por isso
  o áudio de cada bloco fica guardado como evidência; o relatório é
  triagem, não veredito.
* Os relatórios ajudam a auditoria e não substituem os canais oficiais
  de reporte (CENIPA e DECEA).
