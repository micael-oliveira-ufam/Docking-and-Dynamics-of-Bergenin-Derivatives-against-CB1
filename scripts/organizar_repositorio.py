#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organizar_repositorio.py

Reconstrói, de forma determinística, a organização do repositório a partir
dos arquivos originais (zip do TCC e zip dos relatórios de dinâmica).

Cada decisão é registrada:
  - MANIFEST.csv : origem -> destino, MD5 e tamanho de cada arquivo copiado
  - EXCLUIDOS.csv: arquivos descartados e o motivo

Regras aplicadas
  1. Cada alvo (5TGZ, 6KPG, 6N4B, 8GHV) vira targets/<PDB>/ e a estrutura
     interna é preservada, pois os arquivos de configuração usam caminhos
     relativos (ex.: Receptor/...).
  2. Nomes são convertidos para ASCII (remove escapes '#U00xx' do zip e acentos).
  3. ZIPs aninhados cujos membros são idênticos (CRC32 + tamanho) a arquivos já
     presentes são descartados como redundantes.
  4. ZIPs aninhados com conteúdo exclusivo são extraídos no lugar.
  5. Binários do AutoDock Vina e arquivos temporários (.ipynb_checkpoints,
     locks do LibreOffice, .DS_Store) são excluídos.
  6. LaBOX.py (software de terceiros) vai para scripts/third_party/.

Uso
  python3 organizar_repositorio.py \
      --tcc "Larissa__TCC_.zip" \
      --relatorios "Relatórios_da_dinâmica.zip" \
      --destino repo_saida
"""

import argparse
import csv
import hashlib
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
import zlib
from pathlib import Path

PDB_RE = re.compile(r"(5TGZ|6KPG|6N4B|8GHV)", re.IGNORECASE)
BINARY_RE = re.compile(r"^vina.*(_linux_x86_64|\.exe)$", re.IGNORECASE)
SKIP_DIRS = {".ipynb_checkpoints", "__MACOSX"}
THIRD_PARTY = {"LaBOX.py": ("scripts", "third_party", "LaBOX.py")}


def ascii_name(name: str) -> str:
    """Converte um nome de arquivo/pasta para ASCII seguro."""
    name = re.sub(r"#U([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), name)
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = re.sub(r"[()]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"[^A-Za-z0-9._\-]", "_", name)
    return name


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def skip_reason(parts) -> str | None:
    name = parts[-1]
    if any(p in SKIP_DIRS for p in parts):
        return "arquivo temporario/macOS"
    if name.startswith(".~lock") or name.endswith("#") or name == ".DS_Store":
        return "arquivo de lock/temporario"
    if BINARY_RE.match(name):
        return "binario do AutoDock Vina (nao redistribuido; ver docs/software.md)"
    return None


def zip_is_redundant(zpath: Path) -> bool:
    """True se todo membro do zip já existe identico (tamanho + CRC32) na mesma pasta."""
    search_root = zpath.parent
    index: dict[str, list[Path]] = {}
    for dp, _, fs in os.walk(search_root):
        for f in fs:
            if f.lower().endswith(".zip"):
                continue
            index.setdefault(f, []).append(Path(dp) / f)
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            base = os.path.basename(info.filename)
            ok = False
            for cand in index.get(base, []):
                if cand.stat().st_size != info.file_size:
                    continue
                with open(cand, "rb") as fh:
                    if (zlib.crc32(fh.read()) & 0xFFFFFFFF) == info.CRC:
                        ok = True
                        break
            if not ok:
                return False
    return True


def extract_zip(zpath: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(dest)


def resolve_nested_zips(raw_root: Path, excluded: list) -> None:
    """Descobre zips aninhados, descarta redundantes e extrai os que têm conteúdo novo."""
    handled: set[Path] = set()
    while True:
        pending = [p for p in sorted(raw_root.rglob("*.zip")) if p not in handled]
        if not pending:
            break
        for zp in pending:
            handled.add(zp)
            rel = zp.relative_to(raw_root).parts
            if zip_is_redundant(zp):
                excluded.append((Path(*rel).as_posix(), "zip aninhado redundante (todos os membros ja presentes, CRC32 identico)"))
            else:
                target = zp.parent / ascii_name(zp.stem)
                extract_zip(zp, target)
                excluded.append((Path(*rel).as_posix(), f"zip aninhado com conteudo exclusivo: extraido em '{target.relative_to(raw_root).as_posix()}'"))


def collect(root: Path, source_label: str, rel_is_relatorios: bool):
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = Path(dp) / f
            if p.suffix.lower() == ".zip":
                continue
            yield p, p.relative_to(root).parts, source_label, rel_is_relatorios


def destination_for(parts, rel_is_relatorios: bool):
    name = parts[-1]
    if name in THIRD_PARTY:
        return THIRD_PARTY[name]
    if rel_is_relatorios:
        m = PDB_RE.search(name)
        pdb = m.group(1).upper() if m else "GERAL"
        return ("targets", pdb, "Relatorios_dinamica", ascii_name(name))
    idx = next((i for i, p in enumerate(parts) if PDB_RE.search(p)), None)
    if idx is None:
        return ("targets", "GERAL", *[ascii_name(x) for x in parts])
    pdb = PDB_RE.search(parts[idx]).group(1).upper()
    rest = [ascii_name(x) for x in parts[idx + 1:]]
    return ("targets", pdb, *rest)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tcc", required=True, help="zip com os alvos (Larissa__TCC_.zip)")
    ap.add_argument("--relatorios", required=True, help="zip com os relatorios de dinamica")
    ap.add_argument("--destino", required=True, help="pasta de saida do repositorio")
    ap.add_argument("--force", action="store_true", help="sobrescreve destino existente")
    args = ap.parse_args()

    dest_root = Path(args.destino)
    if dest_root.exists():
        if not args.force:
            print(f"ERRO: '{dest_root}' já existe. Use --force para recriar.", file=sys.stderr)
            return 1
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True)

    excluded: list[tuple[str, str]] = []
    manifest: list[tuple[str, str, str, int]] = []
    seen: dict[str, str] = {}
    seen_ci: dict[str, str] = {}  # chave em minusculas: evita colisao em macOS/Windows

    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp)
        tcc_dir = raw / "tcc"
        rel_dir = raw / "relatorios"
        extract_zip(Path(args.tcc), tcc_dir)
        extract_zip(Path(args.relatorios), rel_dir)

        resolve_nested_zips(raw, excluded)

        sources = [(tcc_dir, False), (rel_dir, True)]
        for root, is_rel in sources:
            for p, parts, _, rel_flag in collect(root, root.name, is_rel):
                src_label = f"{root.name}/" + "/".join(parts)
                reason = skip_reason(parts)
                if reason:
                    excluded.append((src_label, reason))
                    continue
                dest_parts = destination_for(parts, rel_flag)
                dest_rel = Path(*dest_parts).as_posix()
                if dest_rel in seen:
                    raise SystemExit(f"COLISAO de destino: {dest_rel}\n  origem1: {seen[dest_rel]}\n  origem2: {src_label}")
                if dest_rel.lower() in seen_ci:
                    raise SystemExit(f"COLISAO sem diferenca de maiusculas: {dest_rel} x {seen_ci[dest_rel.lower()]}")
                seen_ci[dest_rel.lower()] = dest_rel
                out = dest_root / Path(*dest_parts)
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, out)
                seen[dest_rel] = src_label
                manifest.append((dest_rel, src_label, md5_of(out), out.stat().st_size))

    with open(dest_root / "MANIFEST.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["destino", "origem_original", "md5", "tamanho_bytes"])
        w.writerows(sorted(manifest))

    with open(dest_root / "EXCLUIDOS.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["origem_original", "motivo"])
        w.writerows(sorted(excluded))

    total = sum(m[3] for m in manifest)
    by_target: dict[str, int] = {}
    for d, *_ in manifest:
        t = d.split("/")[1] if d.startswith("targets/") else d.split("/")[0]
        by_target[t] = by_target.get(t, 0) + 1
    print(f"Arquivos copiados : {len(manifest)}  ({total/1e6:.1f} MB)")
    for t in sorted(by_target):
        print(f"  {t:<8} {by_target[t]:>5}")
    print(f"Excluidos/registrados : {len(excluded)}  (ver EXCLUIDOS.csv)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
