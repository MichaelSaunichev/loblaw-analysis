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
git clone https://github.com/MichaelSaunichev/loblaw-analysis
cd loblaw-analysis
```

---

### 2. Set Up a Virtual Environment

```bash
python3.12 -m venv venv      # Please use 3.12 for now since compatibility with other versions has not been verified
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

---

## Running the Program

```bash
python main.py
```

You will be presented with an interactive CLI menu:

```
[1] Initialize database
[2] Load data from CSV
[3] Generate summary table
[4] Compare responders vs non-responders (melanoma + tr1 + PBMC)
[5] Visualize relative frequencies (boxplot)
[6] Run baseline subset analysis
[7] Add a sample
[8] Remove sample
[0] Exit
```

---

## Database Schema Design

The program uses a normalized SQLite relational database with the following schema:

### `samples` table:
Stores metadata for each biological sample.

| Column               | Type    | Description                            |
|----------------------|---------|----------------------------------------|
| `sample_id`          | TEXT    | Primary key                            |
| `project`            | TEXT    | Project name (e.g. prj1, prj2)         |
| `subject`            | TEXT    | Subject ID                             |
| `condition`          | TEXT    | Clinical condition (e.g. melanoma)     |
| `age`                | INTEGER | Age of subject                         |
| `sex`                | TEXT    | Sex (`M` or `F`)                        |
| `treatment`          | TEXT    | Treatment type (`tr1`, `tr2`, etc.)    |
| `response`           | TEXT    | Treatment response (`y` or `n`)        |
| `sample_type`        | TEXT    | PBMC, tumor, etc.                      |
| `time_from_treatment`| INTEGER | Days since treatment start             |

### `cell_counts` table:
Stores immune cell counts for each sample.

| Column        | Type    | Description                |
|---------------|---------|----------------------------|
| `sample_id`   | TEXT    | Foreign key to `samples`   |
| `b_cell`      | INTEGER | Count of B cells           |
| `cd8_t_cell`  | INTEGER | Count of CD8+ T cells      |
| `cd4_t_cell`  | INTEGER | Count of CD4+ T cells      |
| `nk_cell`     | INTEGER | Count of NK cells          |
| `monocyte`    | INTEGER | Count of monocytes         |

This schema is designed to support:
- Fast joins for cross-sample queries
- Independent updates to metadata or counts
- Scalable handling of thousands of samples and flexible analytics

---

## Code Structure

```
loblaw-analysis/
├── main.py                  # CLI entry point
├── data/                    # Contains cell-count.csv
├── db/                      # Holds loblaw.db (ignored in Git)
├── src/
│   ├── analysis.py          # Summary generation + statistical tests
│   ├── data_loader.py       # CSV and sample add/remove logic
│   ├── db_schema.py         # Table definitions and DB setup
│   ├── query_interface.py   # Subset filtering and high-level queries
│   └── visualization.py     # Boxplot rendering with seaborn
```

---

## Design Rationale

- **Modular code structure**: Clean separation of database logic, analysis, querying, and UI.
- **CLI interface**: Simple and extensible, easy for scientists to use and rerun without modifying code.
- **Database-first architecture**: Scales to support many projects, samples, and queries without needing to reload CSVs.
- **Safe data entry**: CLI validation when adding/removing samples prevents malformed data from corrupting the DB.

---