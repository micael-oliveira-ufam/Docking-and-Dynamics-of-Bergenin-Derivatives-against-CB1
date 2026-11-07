#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar.py

Duas verificações rápidas do repositório:

  1. Integridade: recalcula o MD5 de cada arquivo listado em MANIFEST.csv
     e confirma que ele existe e não foi alterado.
  2. Configs: para cada config_*.txt do AutoDock Vina, confirma que o
     arquivo indicado em 'receptor =' existe relativamente à pasta do alvo.

Uso (a partir da raiz do repositório):
  python3 scripts/verificar.py

Código de saída: 0 se tudo estiver OK; 1 se houver qualquer falha.
"""

import csv
import hashlib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TARGETS = RAIZ / "targets"


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def checar_integridade() -> list[str]:
    erros: list[str] = []
    manifesto = RAIZ / "MANIFEST.csv"
    if not manifesto.exists():
        return [f"MANIFEST.csv nao encontrado em {RAIZ}"]
    with open(manifesto, encoding="utf-8") as fh:
        linhas = list(csv.DictReader(fh))
    for r in linhas:
        arq = RAIZ / r["destino"]
        if not arq.exists():
            erros.append(f"AUSENTE: {r['destino']}")
            continue
        if md5_of(arq) != r["md5"]:
            erros.append(f"MD5 DIFERENTE: {r['destino']}")
    print(f"[integridade] {len(linhas)} arquivos verificados, {len(erros)} problema(s)")
    return erros


def ler_receptor(config: Path) -> str | None:
    for linha in config.read_text(encoding="utf-8", errors="replace").splitlines():
        if linha.strip().lower().startswith("receptor"):
            return linha.split("=", 1)[1].strip()
    return None


def checar_configs() -> list[str]:
    erros: list[str] = []
    total = 0
    for config in sorted(TARGETS.glob("*/config_*.txt")) + sorted(TARGETS.glob("*/*/config_*.txt")):
        total += 1
        alvo = config.parent
        receptor = ler_receptor(config)
        rel = config.relative_to(RAIZ).as_posix()
        if receptor is None:
            erros.append(f"SEM 'receptor =': {rel}")
            continue
        if not (alvo / receptor).exists():
            erros.append(f"RECEPTOR AUSENTE: {rel} -> '{receptor}' nao existe em {alvo.relative_to(RAIZ).as_posix()}/")
    print(f"[configs] {total} config(s) verificado(s), {len(erros)} problema(s)")
    return erros


def main() -> int:
    erros = checar_integridade() + checar_configs()
    if erros:
        print("\nProblemas encontrados:")
        for e in erros:
            print("  -", e)
        print("\nVer docs/problemas_conhecidos.md para o contexto de cada item.")
        return 1
    print("Tudo OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
