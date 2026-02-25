from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import database
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cantina-digitale-secret-2024'

database.init_db()

def calcola_giudizio(punteggio):
    if punteggio >= 97: return "Memorabile"
    elif punteggio >= 91: return "Eccellente"
    elif punteggio >= 86: return "Ottimo"
    elif punteggio >= 78: return "Buono"
    elif punteggio >= 70: return "Accettabile"
    else: return "—"

@app.route('/')
def index():
    search = request.args.get('q', '')
    degustazioni = database.get_all_degustazioni(search if search else None)
    stats = database.get_stats()
    return render_template('index.html', degustazioni=degustazioni, search=search, stats=stats)

@app.route('/nuova')
def nuova():
    return render_template('scheda.html', today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/salva', methods=['POST'])
def salva():
    form = request.form

    ocp = int(form.get('olfatto_complessita_punti', 0) or 0)
    oqp = int(form.get('olfatto_qualita_punti', 0) or 0)
    gep = int(form.get('gusto_equilibrio_punti', 0) or 0)
    gpp = int(form.get('gusto_persistenza_punti', 0) or 0)
    gqp = int(form.get('gusto_qualita_punti', 0) or 0)
    dp  = int(form.get('dimensione_punti', 0) or 0)
    totale = ocp + oqp + gep + gpp + gqp + dp
    giudizio = calcola_giudizio(totale)

    # Olfatto descrittori: lista checkbox
    descrittori = ', '.join(form.getlist('olfatto_descrittori'))

    data = {
        'luogo': form.get('luogo', ''),
        'data': form.get('data', ''),
        'vino': form.get('vino', ''),
        'alcol': float(form.get('alcol', 0) or 0),
        'colore': form.get('colore', ''),
        'riflesso': form.get('riflesso', ''),
        'densita_cromatica': form.get('densita_cromatica', ''),
        'limpidezza': form.get('limpidezza', ''),
        'vivacita': form.get('vivacita', ''),
        'perlage_grana': form.get('perlage_grana', ''),
        'olfatto_descrittori': descrittori,
        'olfatto_note': form.get('olfatto_note', ''),
        'olfatto_complessita': form.get('olfatto_complessita', ''),
        'olfatto_complessita_punti': ocp,
        'olfatto_qualita': form.get('olfatto_qualita', ''),
        'olfatto_qualita_punti': oqp,
        'gusto_zucchero': form.get('gusto_zucchero', ''),
        'gusto_alcol': form.get('gusto_alcol', ''),
        'gusto_acidita': form.get('gusto_acidita', ''),
        'gusto_tannino': form.get('gusto_tannino', ''),
        'gusto_equilibrio': form.get('gusto_equilibrio', ''),
        'gusto_equilibrio_punti': gep,
        'gusto_persistenza': form.get('gusto_persistenza', ''),
        'gusto_persistenza_punti': gpp,
        'gusto_sapidita': form.get('gusto_sapidita', ''),
        'gusto_chiusura': form.get('gusto_chiusura', ''),
        'gusto_qualita': form.get('gusto_qualita', ''),
        'gusto_qualita_punti': gqp,
        'dimensione': form.get('dimensione', ''),
        'dimensione_punti': dp,
        'prospettive': form.get('prospettive', ''),
        'punteggio_totale': totale,
        'giudizio_finale': giudizio,
    }

    id = database.save_degustazione(data)
    flash('Degustazione salvata con successo!', 'success')
    return redirect(url_for('dettaglio', id=id))

@app.route('/dettaglio/<int:id>')
def dettaglio(id):
    deg = database.get_degustazione(id)
    if not deg:
        flash('Degustazione non trovata.', 'error')
        return redirect(url_for('index'))
    return render_template('dettaglio.html', d=deg)

@app.route('/elimina/<int:id>', methods=['POST'])
def elimina(id):
    database.delete_degustazione(id)
    flash('Degustazione eliminata.', 'success')
    return redirect(url_for('index'))

@app.route('/api/degustazioni')
def api_degustazioni():
    search = request.args.get('q', '')
    data = database.get_all_degustazioni(search if search else None)
    return jsonify(data)

if __name__ == '__main__':
    print("🍷 Cantina Digitale - Avvio in corso...")
    print("   Apri il browser su: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

# ---- ABBINAMENTO ROUTES ----

database.init_abbinamenti_db()

@app.route('/abbinamento')
def abbinamento():
    from datetime import datetime
    return render_template('abbinamento.html', today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/salva_abbinamento', methods=['POST'])
def salva_abbinamento():
    form = request.form
    p1 = int(form.get('pulizia_punti', 0) or 0)
    p2 = int(form.get('piacevolezza_punti', 0) or 0)
    p3 = int(form.get('sensazioni_punti', 0) or 0)
    totale = p1 + p2 + p3
    if totale >= 13: giudizio = 'Appagante'
    elif totale >= 9: giudizio = 'Buono'
    elif totale >= 6: giudizio = 'Accettabile'
    elif totale >= 3: giudizio = 'Sconsigliato'
    else: giudizio = '—'

    data = {
        'luogo': form.get('luogo',''), 'data': form.get('data',''),
        'cibo': form.get('cibo',''), 'vino': form.get('vino',''),
        'anno': form.get('anno',''), 'alcol': float(form.get('alcol',0) or 0),
        'cibo_dolce': int(form.get('cibo_dolce',0) or 0),
        'cibo_grassezza': int(form.get('cibo_grassezza',0) or 0),
        'cibo_tendenza_dolce': int(form.get('cibo_tendenza_dolce',0) or 0),
        'cibo_untuosita': int(form.get('cibo_untuosita',0) or 0),
        'cibo_succulenza': int(form.get('cibo_succulenza',0) or 0),
        'cibo_sapidita': int(form.get('cibo_sapidita',0) or 0),
        'cibo_acidita': int(form.get('cibo_acidita',0) or 0),
        'cibo_amaro': int(form.get('cibo_amaro',0) or 0),
        'cibo_aromatici': form.get('cibo_aromatici',''),
        'cibo_metalliche': form.get('cibo_metalliche',''),
        'cibo_condimenti': form.get('cibo_condimenti',''),
        'vino_dolce': int(form.get('vino_dolce',0) or 0),
        'vino_acidita': int(form.get('vino_acidita',0) or 0),
        'vino_sapidita': int(form.get('vino_sapidita',0) or 0),
        'vino_tannino': int(form.get('vino_tannino',0) or 0),
        'vino_effervescenza': int(form.get('vino_effervescenza',0) or 0),
        'vino_alcol': int(form.get('vino_alcol',0) or 0),
        'vino_glicerina': int(form.get('vino_glicerina',0) or 0),
        'vino_tendenza_dolce': int(form.get('vino_tendenza_dolce',0) or 0),
        'vino_aromatici': form.get('vino_aromatici',''),
        'vino_finale_amm': form.get('vino_finale_amm',''),
        'vino_tattilita': form.get('vino_tattilita',''),
        'pulizia_punti': p1, 'piacevolezza_punti': p2, 'sensazioni_punti': p3,
        'punteggio_totale': totale, 'giudizio_finale': giudizio,
        'note': form.get('note',''),
    }
    id = database.save_abbinamento(data)
    flash('Abbinamento salvato!', 'success')
    return redirect(url_for('dettaglio_abbinamento', id=id))

@app.route('/abbinamento/<int:id>')
def dettaglio_abbinamento(id):
    ab = database.get_abbinamento(id)
    if not ab:
        flash('Abbinamento non trovato.', 'error')
        return redirect(url_for('index'))
    return render_template('dettaglio_abbinamento.html', d=ab)

@app.route('/elimina_abbinamento/<int:id>', methods=['POST'])
def elimina_abbinamento(id):
    database.delete_abbinamento(id)
    flash('Abbinamento eliminato.', 'success')
    return redirect(url_for('index'))
