import json
import re
import unicodedata

IN = "transcricoes.jsonl"
OUT = "ocorrencias.jsonl"


def normaliza(t):
    t = t.lower()
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t


REGRAS = [
    ("EMERGENCIA", "critica", r"\bmayday\b|\bemergencia\b"),
    ("URGENCIA", "critica", r"\bpan\s*pan\b"),
    ("TRANSPONDER_7500", "critica", r"\b7\s*5\s*0\s*0\b|transponder.{0,15}7500"),
    ("TRANSPONDER_7600", "critica", r"\b7\s*6\s*0\s*0\b|transponder.{0,15}7600"),
    ("TRANSPONDER_7700", "critica", r"\b7\s*7\s*0\s*0\b|transponder.{0,15}7700"),
    ("FUSAO", "critica", r"\bfusao\b|perda de separacao"),
    ("TCAS_RA", "critica", r"\bresolution\b|\btcas\b"),
    ("QUASE_COLISAO", "critica", r"passou perto|passou proximo"),
    ("INCURSAO", "critica", r"\bincursao\b"),
    ("ARREMETIDA", "alta", r"arremet(a|endo|ida)"),
    ("PRIORIDADE_POUSO", "alta", r"prioridade.{0,10}pouso"),
    ("COMBUSTIVEL", "alta", r"pouco combustivel|minimum fuel"),
    ("CONTA_E_RISCO", "alta", r"por conta e risco"),
    ("INFRACAO", "alta", r"\binfracao\b"),
    ("DRONE", "alta", r"\bdrone\b|\bvant\b|nao tripulada"),
    ("OBJETO_NAO_IDENTIFICADO", "alta", r"\bbalao\b|\bbaloes\b|\bpipa\b|\bpipas\b|nao identificad"),
    ("FAUNA", "media", r"\bave\b|\baves\b|urubu|quero-?quero|\bcao\b|\bcaes\b|capivara"),
    ("RECLAMACAO", "media", r"\babsurdo\b|inaceitavel|vou reportar"),
    ("CONTINGENCIA", "media", r"falha de equipamento|pista interditada|\bfod\b"),
    ("DESVIO_CAMBIO_OVER", "media", r"\bcambio\b|\bover\b"),
    ("DESVIO_COLOQUIAL", "baixa", r"\bbeleza\b|\bvaleu\b|brigadao"),
]

REGRAS_COMPILADAS = [(cat, sev, re.compile(pat)) for cat, sev, pat in REGRAS]


def checa(texto_norm):
    achados = []
    for cat, sev, pat in REGRAS_COMPILADAS:
        if pat.search(texto_norm):
            achados.append((cat, sev))
    return achados


def main():
    ocorrencias = []
    with open(IN, encoding="utf-8") as f:
        for linha in f:
            rec = json.loads(linha)
            arquivo = rec["arquivo"]
            for seg in rec["segmentos"]:
                texto = seg["texto"]
                norm = normaliza(texto)
                for cat, sev in checa(norm):
                    ocorrencias.append({
                        "arquivo": arquivo,
                        "inicio": seg["inicio"],
                        "fim": seg["fim"],
                        "categoria": cat,
                        "severidade": sev,
                        "trecho": texto,
                        "justificativa": f"gatilho da regra '{cat}' encontrado no texto",
                        "norma": "MCA 100-16",
                    })

    with open(OUT, "w", encoding="utf-8") as f:
        for oc in ocorrencias:
            f.write(json.dumps(oc, ensure_ascii=False) + "\n")

    print(f"[ok] {len(ocorrencias)} ocorrencias salvas em {OUT}")
    contagem = {}
    for oc in ocorrencias:
        contagem[oc["categoria"]] = contagem.get(oc["categoria"], 0) + 1
    for cat, n in sorted(contagem.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()