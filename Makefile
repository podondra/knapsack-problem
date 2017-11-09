TARGET = Analysis\ of\ Methods\ for\ Solving\ the\ Knapsack\ Problem.ipynb
OUT = podszond-report

pdf: $(TARGET)
	jupyter nbconvert --to PDF --output $(OUT)\
	 --PDFExporter.exclude_code_cell=True '$^'

all: archive pdf

archive:
	git archive -o $(OUT).zip --prefix=podszond-code/ HEAD

clean:
	$(RM) $(OUT).pdf $(OUT).zip
