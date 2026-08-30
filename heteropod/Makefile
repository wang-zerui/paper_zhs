PAPER = sidecore
RESUBMISSION = resubmission-summary
TEX = $(wildcard *.tex code/*.tex)
BIB = ref.bib
FIGS = $(wildcard figs/*.pdf figs/*.eps figs-eval/*.pdf figs-eval/*.eps figures/*.pdf figures/*.png graphs/*.pdf graphs/*.png)

.PHONY: all clean

$(PAPER).pdf: $(TEX) $(BIB) $(FIGS) acmart.cls	
	#echo $(FIGS)
	pdflatex -shell-escape $(PAPER)
	bibtex $(PAPER)
	pdflatex -shell-escape $(PAPER)
	pdflatex -shell-escape $(PAPER)

$(RESUBMISSION).pdf: $(RESUBMISSION).tex $(BIB) acmart.cls
	pdflatex -shell-escape $(RESUBMISSION)
	#bibtex $(RESUBMISSION)
	pdflatex -shell-escape $(RESUBMISSION)
	pdflatex -shell-escape $(RESUBMISSION)

clean:
#	rm -f *.ent *.aux *.bbl *.blg *.log *.out $(PAPER).pdf
	rm -f *.ent *.aux *.bbl *.blg *.log *.out 
	rm -rf comment.cut
	rm -f *.pdf

