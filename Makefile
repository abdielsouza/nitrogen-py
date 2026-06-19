PYTHON = python3

.PHONY: run_excel_sample run_google_sample clean

run_excel_sample:
	$(PYTHON) examples/excel_sample.py

run_google_sample:
	$(PYTHON) examples/google_sheets_sample.py

clean:
	rm -rf __pycache__