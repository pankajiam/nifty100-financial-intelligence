load:
	python src/etl/loader.py

ratios:
	python src/etl/compute_ratios.py

test:
	pytest tests/ --html=reports/pytest_report.html --self-contained-html

report:
	python src/reports/generate_reports.py

dashboard:
	streamlit run src/dashboard/app.py

api:
	uvicorn src.api.main:app --reload --port 8000

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf reports/pytest_report.html .pytest_cache