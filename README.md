# Computação Aplicada à Economia: Tópicos em Aprendizado de Máquina

Material do curso (6 aulas × 2h): slides, notas de aula, listas de exercícios
e notebooks para o Google Colab. Professor: Kauê Lopes de Moraes.

| Aula | Tema | Notebooks |
|---|---|---|
| 1 | O que é Aprendizado de Máquina? | [demo](aulas/01-o-que-e-ml/notebooks/01_demo.ipynb) · [lab](aulas/01-o-que-e-ml/notebooks/01_lab.ipynb) |
| 2 | Computação aplicada: de Python ao aprendizado de máquina | [demo](aulas/02-python-numpy-jax/notebooks/02_demo.ipynb) · [lab](aulas/02-python-numpy-jax/notebooks/02_lab.ipynb) |
| 3 | Treino, Teste e Validação: Aprendendo ou Decorando? | — |
| 4 | Regressão Linear por Gradiente Descendente | — |
| 5 | Árvores Aleatórias e Redes Neurais: Aproximadores de Funções | — |
| 6 | Casos de Aprendizado de Máquina em Pesquisa Econômica | — |

Os PDFs (slides, notas e listas) ficam nas
[Releases](https://github.com/kauelopes/topicos-ml/releases). Os notebooks abrem
direto no Colab pelos links acima ou pelos botões nos slides.

## Estrutura

```
tex/                    compartilhado por todos os documentos
  topicosml.sty         notação, cores, caixas pedagógicas, minted, biblatex, metadados
  beamerthemeTML.sty    tema dos slides (hoje: metropolis + ajustes)
  tmlnotas.cls          classe das notas, listas e apostila
  exercicios.sty        ambientes exercicio/solucao (gabarito por jobname)
  refs.bib              bibliografia única
  mermaid.json          tema dos diagramas Mermaid (mesma paleta)
aulas/NN-tema/
  slides.tex            apresentação (beamer)
  conteudo.tex          texto das notas (incluído por notas.tex e pela apostila)
  notas.tex             invólucro que compila conteudo.tex sozinho
  lista.tex             exercícios + soluções num só arquivo
  diagramas/            fontes Mermaid (.mmd) dos diagramas
  figs/                 GERADO (figuras.py e make diagramas) — não editar à mão
  notebooks/            NN_demo (live coding) e NN_lab (laboratório)
apostila/main.tex       todas as notas num só PDF
src/tml/                pacote Python: dados (BCB/SGS), estilo e figuras
data/                   dados (raw/ fica fora do git)
admin/ementa/           ementa do curso
```

## Compilar

Requisitos: TeX Live recente com LuaLaTeX, `latexmk`, `biber` e Pygments
(`pip install pygments`) para o `minted`; Python com `numpy`, `matplotlib`, `jax`,
`scikit-learn`. Para regenerar diagramas: `npm install -g @mermaid-js/mermaid-cli`.
Os PDFs de `figs/` são versionados, então compilar o LaTeX não exige Python nem Node.

```bash
make figs           # gera figuras (matplotlib) de todas as aulas
make diagramas      # renderiza os .mmd que mudaram
make aula N=01      # slides, handout, notas, lista e gabarito da aula 01 -> dist/
make apostila       # dist/apostila.pdf
make all            # tudo
```

O `.latexmkrc` coloca `tex/` no caminho do TeX, então os arquivos usam
`\usepackage{topicosml}` sem caminhos relativos. Ao compilar por um editor
(VS Code/LaTeX Workshop), rode o `latexmk` a partir da raiz com `-cd`, ou
aponte `TEXINPUTS`/`BIBINPUTS` para `tex//`. É necessário `-shell-escape` (minted).

## Convenções

### Tom e didática
- Cada aula abre com uma **pergunta concreta** e fecha com **Para fixar** + ponte para a próxima.
- Conceito novo = intuição → formalização → exemplo econômico → armadilha comum (`atencao`).
- Sempre que possível, ligar ao que o aluno já sabe de econometria (`conexao`).
- **Diagramas Mermaid** quando o conteúdo é um fluxo, uma taxonomia ou uma
  composição; gráficos (matplotlib) quando são dados. Sem diagrama decorativo.
- Notebooks de laboratório com dados **simulados quando o objetivo é checar o que o modelo aprende**
  (sabemos o processo gerador) e reais quando o objetivo é o contato com a prática.

### Técnicas

- **Notação** sempre pelos macros de `topicosml.sty` (`\vbeta`, `\mX`, `\loss`, `\T`…).
  Vetores em negrito itálico, matrizes em negrito reto.
- **Figuras** com prefixo da aula (`a04_trajetoria_perda.pdf`) para não colidirem na apostila.
- **Caixas**: `conexao` (ponte com econometria), `definicao`, `intuicao`, `exemplo`, `atencao`.
- **Slides** seguem a dinâmica da aula: fundamentos → `\demo{...}` → `\lab{...}`.
- **Notebooks**: saídas limpas antes do commit (`nbstripout --install`); pares
  `.py` via `make notebooks` (jupytext) para diffs legíveis.
- **Links do Colab** usam `\tmlrepo` em `tex/topicosml.sty` — ajuste para `usuario/repositorio`.

## Utilitários no Colab

```python
!pip install -q git+https://github.com/kauelopes/topicos-ml.git
from tml import dados
ipca = dados.sgs(433, inicio="01/01/2015")   # IPCA mensal (BCB/SGS)
```
