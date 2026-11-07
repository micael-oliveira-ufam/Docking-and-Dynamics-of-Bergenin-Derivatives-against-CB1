# Docking and molecular dynamics of bergenin derivatives against the CB1 receptor

Molecular docking data (AutoDock Vina) and molecular dynamics reports (Desmond, 200 ns) for bergenin derivatives docked against the cannabinoid receptor CB1. Four starting structures, identified by their PDB codes, were used: **5TGZ**, **6KPG**, **6N4B** and **8GHV**.

This repository contains the input and output files for each target, organized in a self-contained folder per target. A manifest records the MD5 checksum of every file, and scripts verify file integrity and rebuild the layout from the original archives.

## Authors

- **Larissa Souza**, [Universidade Federal do Amazonas]. Student; molecular docking and analysis (undergraduate thesis, TCC).
- **Micael Oliveira**, [Universidade Federal do Amazonas]. Repository maintainer [aided at simulations].

Corresponding author: Clarice Veloso, [clariceveloso@ufam.edu.br].

## Repository structure

```
.
├── README.md
├── MANIFEST.csv                 # 3,949 files: destination, original source, MD5, size
├── EXCLUDED.csv                 # 23 items discarded or logged, with the reason
├── .gitignore
├── docs/
│   ├── software.md              # programs, versions, and how to obtain AutoDock Vina
│   └── known_issues.md          # open issues and items requiring the authors' input
├── scripts/
│   ├── organize_repository.py   # rebuilds targets/ from the original archives
│   ├── verify.py                # file integrity (MD5) and receptor paths in configs
│   └── third_party/LaBOX.py     # grid box calculation (third-party software)
└── targets/
    ├── 5TGZ/
    ├── 6KPG/
    ├── 6N4B/
    └── 8GHV/
```

Each folder in `targets/` is self-contained and keeps the internal structure of the original work. This matters because the configuration files use relative paths (for example `Receptor/...`), which only resolve when Vina is run from inside the target folder.

Most targets contain the following parts. `Receptor/` holds the prepared receptor (`*_prep_maestro.pdbqt`). `Ligands/` (or `Ligands_original/`) holds the reference ligands. `Derivative_generated_by_AI_in_Maestro/` and related folders hold the generated bergenin derivatives. `config_*.txt` files hold the docking configurations. The `Screening*` folders hold blind-docking and site-docking outputs. `Analyses*/` folders hold interaction figures and analyses.

The 6N4B target also contains `Molecular_dynamics/` (complex structures used as simulation inputs) and `MD_reports/` (eight PDF reports of the 200 ns simulations). It also contains a docking screening job, `screening_6n4b_CB1_derivatives_AI_bergenin_...`, whose parameters and job identifier suggest it was run on a web server.

| Target | Files | Notes |
|---|---:|---|
| 5TGZ | 756 | blind and site docking; screenings 1 to 3 |
| 6KPG | 684 | see the open issue on the site-docking configuration |
| 6N4B | 1,568 | includes molecular dynamics and a web-server screening job |
| 8GHV | 940 | blind and site docking |

## Reproducing the analysis

**1. Software.** Versions and sources are listed in `docs/software.md`. The key dependency is AutoDock Vina 1.2.7, which is not redistributed in this repository.

**2. Rebuilding the layout.** With the two original archives:

```bash
python3 scripts/organize_repository.py \
    --tcc "Larissa__TCC_.zip" \
    --reports "Relatórios_da_dinâmica.zip" \
    --dest rebuilt_repository
```

The script is deterministic: running it twice produces identical outputs. It discards the nine nested archives whose contents are identical to files already present (checked by CRC32 and size), extracts the two nested archives with unique content, removes binaries and temporary files, converts names to ASCII and English, and writes `MANIFEST.csv` and `EXCLUDED.csv`.

**3. Verification.** From the repository root:

```bash
python3 scripts/verify.py
```

The script recomputes the MD5 of every file in the manifest and checks that the receptor named in each configuration exists. All files pass the integrity check. One configuration fails the receptor check; see `docs/known_issues.md`, item 1.

**4. Example docking command.** Configuration files do not record the full command. The following reconstructs the naming convention and should be adjusted to the original run:

```bash
cd targets/5TGZ
vina --config config_5tgz_CB1_blind_docking.txt \
     --ligand Ligands/THC.pdbqt \
     --out Screening1_results_blind_docking_CB1_5TGZ/THC_out.pdbqt
```

The docking box is defined in each configuration file (`center_x/y/z`, `size_x/y/z`), and `exhaustiveness` is 96 in all of them.

## Known limitations

The repository contains the inputs and outputs, but not a complete record of each run. The exact commands, the versions of several programs, and the input files for the Desmond simulations (`.cms`, `.msj`) are missing. The MD reports are available as PDFs, but the simulations cannot be repeated from this repository alone. Details and suggested actions are in `docs/known_issues.md`.

## License and citation

A license has not yet been chosen, and citation information is pending. Both must be defined by the authors before public release.
