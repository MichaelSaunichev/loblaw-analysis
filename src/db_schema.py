import sqlite3

def init_db(db_path="db/loblaw.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create samples table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS samples (
            sample_id TEXT PRIMARY KEY,
            project TEXT,
            subject TEXT,
            condition TEXT,
            age INTEGER,
            sex TEXT,
            treatment TEXT,
            response TEXT,
            sample_type TEXT,
            time_from_treatment INTEGER
        )
    ''')

    # Create cell_counts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cell_counts (
            sample_id TEXT PRIMARY KEY,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER,
            FOREIGN KEY(sample_id) REFERENCES samples(sample_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized at:", db_path)
