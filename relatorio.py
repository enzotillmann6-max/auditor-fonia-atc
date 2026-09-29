import json
import os

IN = "ocorrencias.jsonl"
OUT_DIR = "relatorios"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(IN):
        print(f"[erro] {IN} nao encontrado. Rode rules.py primeiro.")
        return

    total = 0
    with open(IN, encoding="utf-8") as f:
        for i, linha in enumerate(f, start=1):
            oc = json.loads(linha)
            nome = f"{i:04d}_{oc['categoria']}.md"
            caminho = os.path.join(OUT_DIR, nome)
            conteudo = f"""# Ocorrencia {i:04d}

- Arquivo de audio: {oc['arquivo']}
- Trecho no bloco: {oc['inicio']}s ate {oc['fim']}s
- Categoria: {oc['categoria']}
- Severidade: {oc['severidade']}
- Norma de referencia: {oc['norma']}

## Transcricao do trecho

{oc['trecho']}

## Justificativa

{oc['justificativa']}
"""
            with open(caminho, "w", encoding="utf-8") as out:
                out.write(conteudo)
            total += 1

    print(f"[ok] {total} relatorios gerados em {OUT_DIR}/")


if __name__ == "__main__":
    main()