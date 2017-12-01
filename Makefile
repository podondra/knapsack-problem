TARGET = Analysis\ of\ Methods\ for\ Solving\ the\ Knapsack\ Problem.ipynb
OUT = podszond-report
KNAPGEN_DIR = knapgen-src
.PHONY: pdf all archive knapgen clean

pdf: $(TARGET)
	jupyter nbconvert --to PDF --output $(OUT)\
	 --PDFExporter.exclude_code_cell=True '$^'

all: archive pdf

archive:
	git archive -o $(OUT).zip --prefix=podszond-code/ HEAD

knapgen: $(KNAPGEN_DIR)/knapgen.c $(KNAPGEN_DIR)/knapcore.c
	$(CC) $^ -lm -o $@

clean:
	$(RM) $(OUT).pdf $(OUT).zip knapgen
