# Problemas conhecidos e pendências

Esta lista registra o que foi encontrado ao organizar os arquivos, o que não pôde ser resolvido sem o autor e o que fazer em cada caso. Nada foi corrigido silenciosamente: os arquivos estão como foram entregues.

### 1. Config de site docking do 6KPG aponta para um receptor de outro alvo

O arquivo `targets/6KPG/config_6kpg_CB1_site_docking.txt` indica `receptor = Receptor/6n4b_CB1_prep_maestro.pdbqt`. Esse arquivo não existe na pasta 6KPG, que só tem `6kpg_prep_maestro.pdbqt`. Além disso, o centro (92.223, 131.930, 120.478) e o tamanho da caixa (21.360, 11.716, 17.428) são exatamente os do site docking do 6N4B. O mais provável é que o config tenha sido copiado do 6N4B e não ajustado. Não é possível afirmar, pelo material, qual receptor e qual grid foram de fato usados nas saídas de site docking do 6KPG. A verificação `scripts/verificar.py` acusa essa falha. Ação recomendada: confirmar com o autor; se o site docking do 6KPG precisar ser refeito, usar o receptor 6KPG e uma caixa calculada para o sítio do 6KPG com o LaBOX.

### 2. Comandos de execução não registrados

Os configs trazem receptor, centro, tamanho da caixa e `exhaustiveness`, mas não trazem o ligante, o caminho de saída nem a pasta de execução. Esses dados não estão em nenhum outro arquivo. O exemplo de comando em `README.md` segue a convenção de nomes e deve ser tratado como reconstrução, não como registro do que foi rodado. Ação: se houver scripts ou históricos de terminal, incluí-los em `scripts/`.

### 3. Entradas da dinâmica molecular ausentes

Os relatórios `Relatorios_dinamica/` são oito PDFs de simulações de 200 ns no Desmond, todos do alvo 6N4B. A pasta `Dinamica_molecular/` contém complexos em PDB, que são estruturas de docking e não sistemas preparados para simulação. Não há arquivos de sistema do Desmond (`.cms`, `.msj`), nem a descrição da preparação (campo de força, solvatação, íons, protocolo de equilibração). Sem isso, a dinâmica não pode ser refeita a partir deste repositório. Ação: incluir os arquivos do Desmond, se existirem, ou documentar o protocolo.

### 4. Complexo de um ligante não relacionado ao restante

`targets/6N4B/Dinamica_molecular/complex_6NIG_alpha_amyrenone.pdb` contém a alfa-amirenona, e o código 6NIG não aparece nos demais arquivos de análise. Pode ser um controle ou um resíduo de outro projeto. Ação: confirmar com o autor e, se for o caso, separar ou remover.

### 5. Zips aninhados: o que foi descartado e por que

Havia onze zips dentro das pastas. Nove foram descartados, porque todos os seus arquivos são idênticos (mesmo tamanho e mesmo CRC32) a arquivos já presentes. Eles estão em `EXCLUIDOS.csv` com o motivo. Dois foram extraídos. Um é o zip `Screening_14_05_25_derivados_originais_bergenina-...` da 6N4B. Ele tem arquivos com os mesmos nomes da pasta de docking, mas com tamanhos e conteúdos diferentes, ou seja, outra rodada de resultados. Uma verificação feita só pelo nome teria descartado esse zip e perdido dados, por isso a comparação é feita por CRC32. O outro é o zip `triagem_6n4b_..._bergenina_...`, que contém arquivos que não existem em nenhum outro lugar.

### 6. Triagem em servidor web (6N4B)

A pasta `triagem_6n4b_CB1_derivados_AI_bergenina_...` contém os parâmetros de um job de docking com algoritmo genético: um milhão de avaliações, população de 750, 24 execuções e 88 ligantes. O centro e o tamanho da caixa coincidem com os do site docking do 6N4B. Não está claro se a lista de ligantes corresponde à pasta `Derivado_gerados_por_AI_no_Maestro` do mesmo alvo. Ação: confirmar essa correspondência.

### 7. Versões de software não registradas

Maestro, MGLTools, Desmond, LaBOX e Python não têm versão registrada no material. Ver `docs/software.md`. Ação: registrar as versões.

### 8. Licenças de componentes de terceiros

O AutoDock Vina não foi redistribuído, por isso não há o que licenciar aqui. O `LaBOX.py` foi incluído, com atribuição ao projeto de origem, mas a licença original precisa ser verificada antes da publicação. Os relatórios e figuras são produção do próprio trabalho.

### 9. Publicação de trabalho acadêmico e metadados de terceiros

O conjunto inclui resultados de um trabalho acadêmico, possivelmente ainda não publicado. Antes de tornar o repositório público, confirmar com a autora e com o orientador que a publicação está autorizada. Nos nomes de arquivos e pastas não foram encontrados dados pessoais, e o nome do zip original não entra nos caminhos do repositório. Já os oito PDFs de relatório de dinâmica trazem nos metadados o campo `Author: Dmitry Lupyan`, provavelmente gerado pelo modelo do Schrödinger. Os PDFs não foram alterados, para preservar os arquivos originais. Ação: decidir se o campo de autor deve ser removido antes da publicação.
