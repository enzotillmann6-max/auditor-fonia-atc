"""Captura contínua de um stream MP3 (Icecast) em blocos de N segundos.

Uso:
    python capture.py

Le a URL e a duracao do bloco em config.yaml.
Duração medida pelo relógio (time.monotonic), nunca pelo tamanho do arquivo.
Se o stream cair, reconecta com espera crescente (1s, 2s, 4s... máx 30s).
"""
import time
import datetime
import pathlib

import requests
import yaml

OUT_DIR = pathlib.Path("audio")


def carrega_config():
    with open("config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def new_block_file():
    OUT_DIR.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUT_DIR / f"bloco_{ts}.mp3"
    return path, open(path, "wb")


def capture_forever(url, block_seconds=60):
    backoff = 1
    while True:
        path, f = new_block_file()
        try:
            print(f"[conectando] {url}")
            with requests.get(url, stream=True, timeout=(10, 15)) as r:
                r.raise_for_status()
                print("[conectado]")
                backoff = 1
                block_start = time.monotonic()
                for chunk in r.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    f.write(chunk)
                    if time.monotonic() - block_start >= block_seconds:
                        f.close()
                        print(f"[ok] {path.name}")
                        path, f = new_block_file()
                        block_start = time.monotonic()
        except (requests.RequestException, OSError) as e:
            print(f"[queda] {e!r} - reconectando em {backoff}s")
        finally:
            f.close()
        time.sleep(backoff)
        backoff = min(backoff * 2, 30)


if __name__ == "__main__":
    cfg = carrega_config()
    url = cfg["frequencia"]
    secs = cfg.get("duracao_bloco_segundos", 60)
    try:
        capture_forever(url, secs)
    except KeyboardInterrupt:
        print("\n[encerrado]")