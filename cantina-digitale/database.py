import sqlite3
from datetime import datetime

DB_NAME = 'cantina.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS degustazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            luogo TEXT,
            data TEXT,
            vino TEXT NOT NULL,
            alcol REAL,
            colore TEXT,
            riflesso TEXT,
            densita_cromatica TEXT,
            limpidezza TEXT,
            vivacita TEXT,
            perlage_grana TEXT,
            olfatto_descrittori TEXT,
            olfatto_note TEXT,
            olfatto_complessita TEXT,
            olfatto_complessita_punti INTEGER DEFAULT 0,
            olfatto_qualita TEXT,
            olfatto_qualita_punti INTEGER DEFAULT 0,
            gusto_zucchero TEXT,
            gusto_alcol TEXT,
            gusto_acidita TEXT,
            gusto_tannino TEXT,
            gusto_equilibrio TEXT,
            gusto_equilibrio_punti INTEGER DEFAULT 0,
            gusto_persistenza TEXT,
            gusto_persistenza_punti INTEGER DEFAULT 0,
            gusto_sapidita TEXT,
            gusto_chiusura TEXT,
            gusto_qualita TEXT,
            gusto_qualita_punti INTEGER DEFAULT 0,
            dimensione TEXT,
            dimensione_punti INTEGER DEFAULT 0,
            prospettive TEXT,
            punteggio_totale INTEGER DEFAULT 0,
            giudizio_finale TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_degustazione(data):
    conn = get_connection()
    c = conn.cursor()
    fields = list(data.keys())
    placeholders = ', '.join(['?' for _ in fields])
    field_names = ', '.join(fields)
    values = [data[f] for f in fields]
    c.execute(f'INSERT INTO degustazioni ({field_names}) VALUES ({placeholders})', values)
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id

def get_all_degustazioni(search=None):
    conn = get_connection()
    c = conn.cursor()
    if search:
        q = f'%{search}%'
        c.execute('''SELECT * FROM degustazioni 
                     WHERE vino LIKE ? OR luogo LIKE ? OR olfatto_note LIKE ?
                     ORDER BY created_at DESC''', (q, q, q))
    else:
        c.execute('SELECT * FROM degustazioni ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_degustazione(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM degustazioni WHERE id = ?', (id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_degustazione(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM degustazioni WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as tot, AVG(punteggio_totale) as media, MAX(punteggio_totale) as massimo FROM degustazioni')
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}

def init_abbinamenti_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS abbinamenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            luogo TEXT, data TEXT, cibo TEXT NOT NULL, vino TEXT NOT NULL,
            anno TEXT, alcol REAL,
            cibo_dolce INTEGER DEFAULT 0, cibo_grassezza INTEGER DEFAULT 0,
            cibo_tendenza_dolce INTEGER DEFAULT 0, cibo_untuosita INTEGER DEFAULT 0,
            cibo_succulenza INTEGER DEFAULT 0, cibo_sapidita INTEGER DEFAULT 0,
            cibo_acidita INTEGER DEFAULT 0, cibo_amaro INTEGER DEFAULT 0,
            cibo_aromatici TEXT, cibo_metalliche TEXT, cibo_condimenti TEXT,
            vino_dolce INTEGER DEFAULT 0, vino_acidita INTEGER DEFAULT 0,
            vino_sapidita INTEGER DEFAULT 0, vino_tannino INTEGER DEFAULT 0,
            vino_effervescenza INTEGER DEFAULT 0, vino_alcol INTEGER DEFAULT 0,
            vino_glicerina INTEGER DEFAULT 0, vino_tendenza_dolce INTEGER DEFAULT 0,
            vino_aromatici TEXT, vino_finale_amm TEXT, vino_tattilita TEXT,
            pulizia_punti INTEGER DEFAULT 0,
            piacevolezza_punti INTEGER DEFAULT 0,
            sensazioni_punti INTEGER DEFAULT 0,
            punteggio_totale INTEGER DEFAULT 0,
            giudizio_finale TEXT, note TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_abbinamento(data):
    conn = get_connection()
    c = conn.cursor()
    fields = list(data.keys())
    placeholders = ', '.join(['?' for _ in fields])
    values = [data[f] for f in fields]
    c.execute(f'INSERT INTO abbinamenti ({",".join(fields)}) VALUES ({placeholders})', values)
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id

def get_all_abbinamenti(search=None):
    conn = get_connection()
    c = conn.cursor()
    if search:
        q = f'%{search}%'
        c.execute('SELECT * FROM abbinamenti WHERE cibo LIKE ? OR vino LIKE ? OR luogo LIKE ? ORDER BY created_at DESC', (q,q,q))
    else:
        c.execute('SELECT * FROM abbinamenti ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_abbinamento(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM abbinamenti WHERE id = ?', (id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_abbinamento(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM abbinamenti WHERE id = ?', (id,))
    conn.commit()
    conn.close()
