# VaR_Calculation

This project provides a modular implementation of Value at Risk (VaR) calculation for foreign exchange instruments. It supports portfolio allocation, time series ingestion, return computation, and risk estimation using standard statistical models.

---

## 🚀 Features

- Modular architecture for ease of testing and scalability
- Supports time series-based VaR computation
- Configurable input and return calculation logic
- Clean separation of concerns using Python packages
- Unit tests for core components

---

## 🗂 Folder Structure

```
VaR_Calculation/
├── handler.py                # Main entry point
├── requirements.txt          # Project dependencies
├── data/                     # Sample FX rate data
├── src/
│   ├── config/               # Configuration files
│   ├── ingestion/            # Data loading logic
│   ├── instrument/           # Instrument allocation
│   ├── processing/           # Data preprocessing
│   ├── returns/              # Return calculation
│   ├── risk_model/           # VaR model implementation
│   └── utils/                # Validators and helpers
└── test/                     # Unit tests
```

---

## 🛠️ Setup Instructions

1. Clone the repository:
```bash
git clone "https://github.com/Semanti2019/var_calculation_project.git"
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Run the main handler to trigger the full VaR pipeline:

```bash
python handler.py
```

Ensure the config and data files are correctly placed.

---

## ✅ Running Tests

Use `pytest` to execute unit tests:

```bash
pytest test/
```

---

## 🧪 Sample Configuration

Configuration files can be found under `src/config/config.py` and may include:
- Time horizon (days)
- Portfolio values
- FX instruments and weights
- Return function used (e.g. log returns)

---

## 📄 License

This project is intended for internal or educational use only unless stated otherwise.
