# =====================================================================
#  Makefile — compila todo o material do curso
#
#  make aula N=01      slides, handout, notas, lista e gabarito da aula 01
#  make all            todas as aulas + apostila
#  make apostila       apostila completa (notas de todas as aulas)
#  make figs           regenera as figuras a partir de src/tml/figuras.py
#  make diagramas      renderiza aulas/*/diagramas/*.mmd (Mermaid) em figs/*.pdf
#  make notebooks      sincroniza .ipynb <-> .py (jupytext)
#  make clean          apaga build/ de todas as pastas
#  make distclean      clean + dist/
#
#  PDFs finais vão para dist/ com nomes padronizados (aula01-slides.pdf ...)
# =====================================================================
SHELL   := /bin/bash
LATEXMK := latexmk -r $(CURDIR)/.latexmkrc -cd
PYTHON  ?= python3
DIST    := dist

AULAS   := $(sort $(wildcard aulas/[0-9][0-9]-*))
N       ?=

.PHONY: all aula apostila figs diagramas notebooks clean distclean help

# Mermaid: requer `npm install -g @mermaid-js/mermaid-cli`.
# Se o Chromium do puppeteer não for encontrado, passe um config:
#   make diagramas MMDC_FLAGS="-p puppeteer.json"
MMDC       ?= mmdc
MMDC_FLAGS ?=
MMD        := $(wildcard aulas/*/diagramas/*.mmd)

help:
	@sed -n '2,15p' Makefile

all: $(AULAS:%=%.aula) apostila

aula:
	@test -n "$(N)" || (echo "Uso: make aula N=01" && exit 1)
	@$(MAKE) --no-print-directory $(wildcard aulas/$(N)-*).aula

# Regra genérica: aulas/01-xxx.aula
%.aula:
	@mkdir -p $(DIST)
	$(eval D := $*)
	$(eval K := $(shell basename $* | cut -c1-2))
	$(LATEXMK) $(D)/slides.tex
	$(LATEXMK) -pretex='\PassOptionsToClass{handout}{beamer}' -jobname=slides-handout $(D)/slides.tex
	$(LATEXMK) $(D)/notas.tex
	$(LATEXMK) $(D)/lista.tex
	$(LATEXMK) -jobname=lista-solucao $(D)/lista.tex
	@cp $(D)/build/slides.pdf         $(DIST)/aula$(K)-slides.pdf
	@cp $(D)/build/slides-handout.pdf $(DIST)/aula$(K)-slides-handout.pdf
	@cp $(D)/build/notas.pdf          $(DIST)/aula$(K)-notas.pdf
	@cp $(D)/build/lista.pdf          $(DIST)/aula$(K)-lista.pdf
	@cp $(D)/build/lista-solucao.pdf  $(DIST)/aula$(K)-lista-solucao.pdf
	@echo ">> Aula $(K) pronta em $(DIST)/"

apostila:
	@mkdir -p $(DIST)
	$(LATEXMK) apostila/main.tex
	@cp apostila/build/main.pdf $(DIST)/apostila.pdf

figs:
	PYTHONPATH=src $(PYTHON) -m tml.figuras

# aulas/NN/diagramas/x.mmd -> aulas/NN/figs/x.pdf (só refaz o que mudou)
diagramas:
	@for f in $(MMD); do \
	  o=$$(dirname $$f)/../figs/$$(basename $${f%.mmd}).pdf; \
	  if [ $$f -nt $$o ] || [ tex/mermaid.json -nt $$o ]; then \
	    echo "mmdc $$f"; \
	    $(MMDC) -q $(MMDC_FLAGS) -c tex/mermaid.json -i $$f -o $$o || exit 1; \
	  fi; \
	done

notebooks:
	jupytext --sync aulas/*/notebooks/*.ipynb

clean:
	@for d in $(AULAS) apostila; do rm -rf $$d/build; done

distclean: clean
	rm -rf $(DIST)
