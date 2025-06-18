import sqlite3
import csv
import os

DB_PATH = "db/loblaw.db"
CSV_PATH = "data/cell-count.csv"

def load_data(db_path=DB_PATH, csv_path=CSV_PATH):
    if not os.path.exists(csv_path):
        print("CSV file not found:", csv_path)
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            sample_id = row['sample']

            # Insert metadata into samples
            cursor.execute('''
                INSERT OR REPLACE INTO samples (
                    sample_id, project, subject, condition, age, sex,
                    treatment, response, sample_type, time_from_treatment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sample_id,
                row.get('project'),
                row.get('subject'),
                row.get('condition'),
                int(row['age']) if row['age'].strip() != '' else None,
                row.get('sex'),
                row.get('treatment'),
                row.get('response') if row.get('response', '').strip() != '' else None,
                row.get('sample_type'),
                int(row['time_from_treatment_start']) if row['time_from_treatment_start'].strip() != '' else None
            ))


            # Insert counts into cell_counts
            cursor.execute('''
                INSERT OR REPLACE INTO cell_counts (
                    sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sample_id,
                int(row['b_cell']) if row['b_cell'].strip() != '' else None,
                int(row['cd8_t_cell']) if row['cd8_t_cell'].strip() != '' else None,
                int(row['cd4_t_cell']) if row['cd4_t_cell'].strip() != '' else None,
                int(row['nk_cell']) if row['nk_cell'].strip() != '' else None,
                int(row['monocyte']) if row['monocyte'].strip() != '' else None
            ))


    conn.commit()
    conn.close()
    print("Data loaded successfully.")

def add_sample(sample_metadata: dict, cell_counts: dict, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert into samples
    cursor.execute('''
        INSERT OR REPLACE INTO samples (
            sample_id, project, subject, condition, age, sex,
            treatment, response, sample_type, time_from_treatment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        sample_metadata['sample_id'], sample_metadata['project'],
        sample_metadata['subject'], sample_metadata['condition'],
        sample_metadata['age'], sample_metadata['sex'],
        sample_metadata['treatment'], sample_metadata['response'],
        sample_metadata['sample_type'], sample_metadata['time_from_treatment']
    ))

    # Insert into cell_counts
    cursor.execute('''
        INSERT OR REPLACE INTO cell_counts (
            sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        sample_metadata['sample_id'],
        cell_counts['b_cell'], cell_counts['cd8_t_cell'],
        cell_counts['cd4_t_cell'], cell_counts['nk_cell'],
        cell_counts['monocyte']
    ))

    conn.commit()
    conn.close()
    print(f"Sample {sample_metadata['sample_id']} added.")

def remove_sample(sample_id, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM cell_counts WHERE sample_id = ?', (sample_id,))
    cursor.execute('DELETE FROM samples WHERE sample_id = ?', (sample_id,))

    conn.commit()
    conn.close()
    print(f"Sample {sample_id} removed.")
