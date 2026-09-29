import glob
import json
import os
import time

from faster_whisper import WhisperModel

MODEL = "small"
AUDIO_DIR = "audio"
OUT = "transcricoes.jsonl"
INITIAL_PROMPT = "Torre Congonhas, QNH, cotejamento"
JUNK = ["obrigado por assistir", "legenda", "inscreva-se", "amara.org"]


def already_done():
    done = set()
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["arquivo"])
                except (ValueError, KeyError):
                    pass
    return done


def is_junk(seg):
    t = seg.text.strip().lower()
    if not t:
        return True
    if any(j in t for j in JUNK):
        return True
    if seg.no_speech_prob > 0.6 and seg.avg_logprob < -1.0:
        return True
    words = t.split()
    if len(words) >= 6 and len(set(words)) <= len(words) / 4:
        return True
    return False


def transcribe_file(model, path):
    segs, _ = model.transcribe(
        path,
        language="pt",
        vad_filter=True,
        initial_prompt=INITIAL_PROMPT,
        condition_on_previous_text=False,
    )
    out = []
    for s in segs:
        if is_junk(s):
            continue
        out.append({
            "inicio": round(s.start, 2),
            "fim": round(s.end, 2),
            "texto": s.text.strip(),
        })
    return out


def main():
    print("[carregando modelo]")
    model = WhisperModel(MODEL, device="cpu", compute_type="int8")
    print("[pronto] Ctrl+C para parar")
    while True:
        done = already_done()
        files = sorted(glob.glob(os.path.join(AUDIO_DIR, "*.mp3")))
        for path in files:
            name = os.path.basename(path)
            if name in done:
                continue
            if time.time() - os.path.getmtime(path) < 90:
                continue  # bloco ainda sendo gravado
            segmentos = transcribe_file(model, path)
            rec = {
                "arquivo": name,
                "transcrito_em": time.strftime("%Y-%m-%d %H:%M:%S"),
                "segmentos": segmentos,
            }
            with open(OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"[ok] {name}: {len(segmentos)} trechos")
        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[encerrado]")