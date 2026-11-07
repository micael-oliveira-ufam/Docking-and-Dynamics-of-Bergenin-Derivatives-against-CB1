# Docking e dinâmica molecular de derivados da bergenina frente ao CB1

Dados de docking molecular (AutoDock Vina) e relatórios de dinâmica molecular (Desmond, 200 ns) de derivados da bergenina contra o receptor canabinoide CB1. São quatro estruturas de partida, identificadas pelo código PDB: **5TGZ**, **6KPG**, **6N4B** e **8GHV**.

Este repositório reúne os arquivos de entrada e de saída organizados por alvo, com um manifesto de auditoria (MD5 de cada arquivo) e scripts para verificar a integridade e reconstruir a organização a partir dos arquivos originais.

## Estrutura

```
.
├── README.md
├── MANIFEST.csv              # 3.949 arquivos: destino, origem original, MD5, tamanho
├── EXCLUIDOS.csv             # 23 itens descartados ou registrados, com o motivo
├── docs/
│   ├── software.md           # programas, versões e como obter o AutoDock Vina
│   └── problemas_conhecidos.md
├── scripts/
│   ├── organizar_repositorio.py   # reconstrói targets/ a partir dos zips originais
│   ├── verificar.py               # integridade (MD5) e caminhos dos configs
│   └── third_party/LaBOX.py       # cálculo de caixa de grid (software de terceiros)
└── targets/
    ├── 5TGZ/
    ├── 6KPG/
    ├── 6N4B/
    └── 8GHV/
```

Cada pasta em `targets/` é autocontida e mantém a estrutura original do trabalho. Isso importa porque os arquivos de configuração usam caminhos relativos (por exemplo, `Receptor/...`), que só funcionam se o Vina for executado a partir da pasta do alvo.

Dentro de cada alvo aparecem, em geral, as seguintes partes: o receptor (`Receptor/` e arquivos `*_prep_maestro.pdbqt`), os ligantes de referência (`Ligantes/` ou `Ligantes_originais/`), os derivados gerados no Maestro (`Derivado_gerados_por_AI_no_Maestro/` e variantes), os configs de docking (`config_*.txt`), as saídas de *blind docking* e *site docking* (pastas `Screening*`), e as figuras e análises de interação (`Analises*/` e imagens `*.png`).

No alvo 6N4B estão também `Dinamica_molecular/`, com os complexos de entrada para dinâmica, e `Relatorios_dinamica/`, com os oito relatórios em PDF das simulações de 200 ns. Há ainda uma triagem de docking que, pelos parâmetros e pelo identificador de job, parece ter sido executada em servidor web (`triagem_6n4b_..._bergenina_...`), com os parâmetros do algoritmo genético e o identificador do job.

| Alvo | Arquivos | Observação |
|---|---:|---|
| 5TGZ | 756 | blind e site docking, triagens 1 a 3 |
| 6KPG | 684 | ver pendência no config de site docking |
| 6N4B | 1.568 | inclui dinâmica molecular e triagem em servidor web |
| 8GHV | 940 | blind e site docking |

## Como reproduzir

**1. Software.** As versões e as formas de obtenção estão em `docs/software.md`. O ponto mais importante é o AutoDock Vina 1.2.7, que não foi redistribuído aqui.

**2. Reconstruir a organização.** Com os dois zips originais em mãos:

```bash
python3 scripts/organizar_repositorio.py \
    --tcc "Larissa__TCC_.zip" \
    --relatorios "Relatórios_da_dinâmica.zip" \
    --destino repo_reconstruido
```

O script é determinístico. Ele descarta os 9 zips aninhados que são cópias idênticas dos arquivos já presentes (checagem por CRC32 e tamanho), extrai os 2 que têm conteúdo próprio, remove binários e temporários, converte nomes para ASCII e grava `MANIFEST.csv` e `EXCLUIDOS.csv`.

**3. Verificar.** A partir da raiz do repositório:

```bash
python3 scripts/verificar.py
```

O script recalcula o MD5 de todos os arquivos listados no manifesto e checa se o receptor de cada config existe. Hoje ele passa na integridade e aponta uma falha de configuração, descrita em `docs/problemas_conhecidos.md`.

**4. Exemplo de docking.** Os configs não registram o comando completo. Este é um exemplo que segue a convenção de nomes dos arquivos, a ser ajustado conforme a execução original:

```bash
cd targets/5TGZ
vina --config config_5tgz_CB1_blind_docking.txt \
     --ligand Ligantes/THC.pdbqt \
     --out Screening1_results_blind_docking_CB1_5TGZ/THC_out.pdbqt
```

As caixas de grid usadas estão nos próprios configs (`center_x/y/z`, `size_x/y/z`) e o `exhaustiveness` é 96 em todos.

## Limitações

A pasta contém os resultados e as entradas, mas não o registro completo de cada execução. Faltam os comandos exatos, as versões de vários programas e os arquivos de entrada da dinâmica molecular no Desmond (`.cms` e `.msj`). Os relatórios em PDF existem, mas a simulação não pode ser refeita a partir deste repositório. Os detalhes e o que fazer em cada caso estão em `docs/problemas_conhecidos.md`.

## Licença e citação

Licença e forma de citação ainda não definidas pelos autores. Antes de tornar o repositório público, é preciso escolher uma licença e preencher esta seção.
