PYTHON = python3
XMAKE = xmake

.PHONY: run_excel_sample run_google_sample compile_modules clean

run_excel_sample:
	$(PYTHON) examples/excel_sample.py

run_google_sample:
	$(PYTHON) examples/google_sheets_sample.py

compile_modules:
	$(XMAKE) build ./modules

clean:
	rm -rf __pycache__