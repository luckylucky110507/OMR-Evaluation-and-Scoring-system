# 📊 OMR Evaluation System

A lightweight OMR (Optical Mark Recognition) evaluation project with a Streamlit frontend and command-line helper scripts.

## 🌟 What’s Included

- `app.py` — Streamlit user interface for OMR processing and reporting
- `config.py` — runtime settings, environment overrides, and directory helpers
- `run.py` — entry point for starting the backend, frontend, or both
- `runner.py` — install, test, and status helper script
- `requirements.txt` — runtime dependencies
- `sample_answer_key.csv` — demo answer key data

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- `pip` available

### Install dependencies and create folders
```bash
python runner.py install
```

### Run the frontend only
```bash
python run.py web
```

### Run the backend only
```bash
python run.py api
```

### Run both frontend and backend
```bash
python run.py both
```

### Optional runner commands
```bash
python runner.py frontend
python runner.py backend
python runner.py both
python runner.py status
```

## 🧩 Project Layout

```
./
├── app.py
├── config.py
├── run.py
├── runner.py
├── requirements.txt
├── pyproject.toml
├── setup.py
├── README.md
├── LICENSE
├── sample_answer_key.csv
├── sample_answer_key.json
├── sample_answer_key.xlsx
├── simple_test.py
├── test_excel_processing.py
├── test_omr_system.py
├── test_system.py
└── test_teacher_system.py
```

## 🔧 Configuration

The project reads several settings from environment variables. Default values are defined in `config.py`.

Common variables:
- `DATABASE_URL` — database connection string
- `UPLOAD_DIR` — upload folder
- `RESULTS_DIR` — results folder
- `EXPORTS_DIR` — export folder
- `ANSWER_KEYS_DIR` — answer key folder
- `LOGS_DIR` — logging folder
- `API_HOST` / `API_PORT` — backend host and port
- `STREAMLIT_HOST` / `STREAMLIT_PORT` — Streamlit host and port
- `MAX_FILE_SIZE_MB` — maximum upload file size
- `PROCESSING_TIMEOUT_SECONDS` — processing timeout

Example `.env` values:
```env
DATABASE_URL=sqlite:///./omr_evaluation.db
UPLOAD_DIR=uploads
RESULTS_DIR=results
LOGS_DIR=logs
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_HOST=localhost
STREAMLIT_PORT=8501
MAX_FILE_SIZE_MB=50
PROCESSING_TIMEOUT_SECONDS=300
```

## 📌 Notes

- `app.py` is the Streamlit frontend entry point.
- `run.py` can start the backend API, web interface, or both.
- `runner.py` is a convenience script for install, status, and test workflows.
- The repository currently contains only the core runtime files and test scripts.

## 🧪 Testing

Run tests with:
```bash
python runner.py test
```

If you want to run a single test file directly:
```bash
python test_omr_system.py
```

## 💡 Recommended Workflow

1. Install dependencies
2. Run `python runner.py install`
3. Start the full system with `python runner.py both`
4. Open `http://localhost:8501` in your browser

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
