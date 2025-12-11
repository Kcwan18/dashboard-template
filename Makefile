.PHONY: install run clean reset-db

install:
	pip install -r requirements.txt

run:
	python app.py

clean:
	rm -rf __pycache__
	rm -rf *.pyc

reset-db:
	rm -f db.sqlite
	@echo "Database deleted. Restart the app to recreate it."
