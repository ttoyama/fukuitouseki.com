# Makefile for LaTeX compilation
SOURCE = 透析実施困難施設対応チェックシート.tex
PDF = 透析実施困難施設対応チェックシート_20250903.pdf

.PHONY: all clean

all: $(PDF)

$(PDF): $(SOURCE)
	platex $(SOURCE)
	dvipdfmx -o $(PDF) 透析実施困難施設対応チェックシート.dvi

clean:
	rm -f *.aux *.log *.dvi *.pdf

# Test compilation
test:
	platex $(SOURCE)
	dvipdfmx -o $(PDF) 透析実施困難施設対応チェックシート.dvi
	@echo "PDF generated: $(PDF)"