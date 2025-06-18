# Loblaw Bio Immune Cell Analysis

This project helps Bob Loblaw analyze immune cell population data from a clinical trial. It enables loading and managing cytometry data, generating summary statistics, performing treatment response analysis, and visualizing immune signatures across patient samples.

---

## Features

- Load data from `cell-count.csv` into a SQLite database
- Add/remove samples programmatically
- Generate per-sample immune population frequencies
- Compare responders vs non-responders (melanoma, tr1, PBMC)
- Boxplot visualizations of population frequency distributions
- Subset analysis by treatment time, sex, and project

---

## Setup Instructions

### Python Version
Tested with: **Python 3.12.5**

---

### 1. Clone the Repository

```bash
git clone TODO add url
cd loblaw-analysis
```

---

### 2. Set Up a Virtual Environment

```bash
python3.12 -m venv venv      # Please use 3.12 for now as this has not been tested with other versions
source venv/bin/activate     # For Mac/Linux
venv\Scripts\activate        # For Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Place the CSV File

The required `cell-count.csv` file is already included in the `data/` directory. If you plan to use updated data, replace the file with your own:

```
loblaw-analysis/
└── data/
    └── cell-count.csv
```