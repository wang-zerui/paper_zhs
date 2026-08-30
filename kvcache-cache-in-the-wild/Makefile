MAIN ?= kvcache
DIFF ?= HEAD^
CODE := $(addsuffix .tex,$(filter-out %.tex,$(wildcard code/*)))
FIGS := $(patsubst %.svg,%.pdf,$(wildcard fig/*.svg))
FIG2 := $(patsubst %.eps,%.pdf,$(wildcard fig/*.eps))
PLOT := $(patsubst %.gp,%.eps,$(wildcard data/*.gp))
PLOT1 := $(patsubst %.gp,%.eps,$(wildcard data/ycsb-overall/*.gp) $(wildcard data/ycsbd-timeline/*.gp) \
	$(wildcard data/ycsbc-lat/*.gp) \
	$(wildcard data/motiv/*.gp) \
	$(wildcard data/app/*.gp) \
	$(wildcard data/datasets/*.gp) \
)

BTEX := --bibtex-args="-min-crossrefs=99"
#BTEX := --bibtex-args=""

all: $(DEPS)
#	@TEXINPUTS="sty:" bin/latexrun $(BTEX) $(MAIN)
#	mv latex.out/$(MAIN).pdf .
	latexmk -pdf -f $(MAIN).tex

data: $(DEPS)

diff: $(DEPS)
	@bin/diff.sh $(DIFF)

help:
	echo "..."


#code/%.tex: code/%
#	pygmentize -P tabsize=4 -P mathescape -f latex $^ > $@

#code/fmt.tex:
#pygmentize -f latex -S default > $@

fig/%.pdf: fig/%.svg
	inkscape --without-gui -f $^ -D -A $@

data/%.eps: data/%.gp
	gnuplot $^

data/ycsb-overall/%.eps : data/ycsb-overall/%.gp
	gnuplot $^

data/ycsb-timeline/%.eps : data/ycsbd-timeline/%.gp
	gnuplot $^

data/ycsbc-lat/%.eps : data/ycsbc-lat/%.gp
	gnuplot $^

data/app/%.eps : data/app/%.gp
	gnuplot $^

data/datasets/%.eps : data/datasets/%.gp
	gnuplot $^

data/motiv/%.eps : data/motiv/%.gp
	gnuplot $^

draft: $(DEPS)
	echo -e '\\newcommand*{\\DRAFT}{}' >> rev.tex
	@TEXINPUTS="sty:" bin/latexrun $(BTEX) $(MAIN)

watermark: $(DEPS)
	echo -e '\\usepackage[firstpage]{draftwatermark}' >> rev.tex
	@TEXINPUTS="sty:" bin/latexrun $(BTEX) $(MAIN)

spell:
	@for i in *.tex fig/*.tex; do bin/aspell.sh $$i; done
	@for i in *.tex; do bin/double.pl $$i; done
	@for i in *.tex; do bin/abbrv.pl  $$i; done
	@bin/hyphens.sh *.tex

clean:
#	@bin/latexrun --clean
	latexmk -c
	rm -f abs.txt

distclean: clean
	rm -f code/*.tex

init:
	rm -f {code,fig,data}/ex-*
	perl -pi -e 's/^\\input{ex}/% \\input{ex}/g' $(MAIN).tex

abs.txt: abs.tex $(MAIN).tex
	#@bin/mkabstract $(MAIN).tex $< > $@

.PHONY: all help FORCE draft clean spell distclean init
