# Software utilizado

Os nomes e as versões abaixo foram tirados dos próprios arquivos do trabalho. Onde a versão não aparece no material, isso está indicado.

## AutoDock Vina

Os arquivos de docking foram gerados com o **AutoDock Vina 1.2.7** (Linux, x86_64), junto com o utilitário `vina_split` da mesma versão. Os binários não estão neste repositório, por serem programas de terceiros. Para reproduzir, obtenha a versão oficial em https://github.com/ccsb-scripps/AutoDock-Vina/releases e confira o MD5 do arquivo usado no trabalho:

| Arquivo usado no trabalho | MD5 |
|---|---|
| `vina_1.2.7_linux_x86_64` | `0c5d02550bdb3e661a77ee0badcfbe78` |
| `vina_split_1.2.7_linux_x86_64` | `99d87222be16fbd6800c7624d1811f77` |
| `vina_1.2.5_win.exe` (Windows, versão 1.2.5, aparece só na pasta 6N4B) | `39ff27d9b1f29b4a8e7a1f35e3186861` |

Se o MD5 da versão baixada for diferente, o resultado pode não ser idêntico ao original.

## Preparação de estruturas e ligantes

Os receptores preparados têm o sufixo `_prep_maestro`, e os derivados trazem `maestro` no nome (`filtered_molecules_enumeration_bergenin_maestro_...`). Isso sugere o uso do Schrödinger Maestro. Alguns ligantes têm `MGLTools_prepared` no nome, o que sugere o uso do MGLTools. São indicações pelos nomes dos arquivos, não registros de execução. Versões não registradas no material.

## Dinâmica molecular

Os relatórios `desmond_md_200ns_*.pdf` indicam simulações de 200 ns no Desmond (Schrödinger). Versão não registrada. Os arquivos de entrada da simulação não estão no material (ver `problemas_conhecidos.md`).

## Caixa de grid

O script `scripts/third_party/LaBOX.py` calcula as dimensões da caixa de grid a partir de um arquivo de ligante. Ele é de terceiros (https://github.com/RyanZR/LaBOX), e a licença original deve ser conferida antes de redistribuir. A versão usada não está registrada.
