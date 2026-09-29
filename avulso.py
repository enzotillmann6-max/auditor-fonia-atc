import sys
import json

from faster_whisper import WhisperModel

import rules

MODEL = "small"
INITIAL_PROMPT = "Torre Congonhas, QNH, cotejamento"


def main():
    if len(sys.argv) < 2:
        print('Uso: python avulso.py "caminho_do_audio"')
        return

    caminho = sys.argv[1]
    print(f"[carregando modelo]")
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")

    print(f"[transcrevendo] {caminho}")
    segs, _ = model.transcribe(
        caminho,
        language="pt",
        vad_filter=True,
        initial_prompt=INITIAL_PROMPT,
        condition_on_previous_text=False,
    )

    ocorrencias = []
    texto_completo = []
    for s in segs:
        texto = s.text.strip()
        if not texto:
            continue
        texto_completo.append(texto)
        norm = rules.normaliza(texto)
        for cat, sev in rules.checa(norm):
            ocorrencias.append({
                "inicio": round(s.start, 2),
                "fim": round(s.end, 2),
                "categoria": cat,
                "severidade": sev,
                "trecho": texto,
            })

    print("\n[transcricao completa]")
    print(" ".join(texto_completo) or "(nenhuma fala detectada)")

    print(f"\n[ocorrencias] {len(ocorrencias)}")
    for oc in ocorrencias:
        print(f"  {oc['inicio']}s-{oc['fim']}s [{oc['severidade']}] {oc['categoria']}: {oc['trecho']}")


if __name__ == "__main__":
    main()