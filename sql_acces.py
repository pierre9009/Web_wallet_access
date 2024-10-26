#app.py
from flask import Flask, render_template
from flask import jsonify
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='/app/.env')

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/wallet'

def get_db_connection():
    """Crée et retourne une connexion à la base de données PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=os.getenv('IP_WALLET_DB'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('USER_WALLET_DB'),
            password=os.getenv('POSTGRES_PASSWORD'),
            dbname=os.getenv('DB_WALLET')
        )
        print(f"Connexion réussie à la base de données {os.getenv('DB_WALLET')}")
        return conn
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        raise


@app.route('/wallet/')
def index():
    """Récupère les données de la table wallet_stats et les passe au template."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Requête pour récupérer toutes les données de la table wallet_stats
    cursor.execute("SELECT * FROM wallet_stats;")
    wallet_stats = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # Passer les résultats au template HTML
    return render_template('index.html', wallet_stats=wallet_stats)
@app.route('/wallet/api/wallet_stats')
def api_wallet_stats():
    """Retourne les données de la table wallet_stats en JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Requête pour récupérer toutes les données
    cursor.execute("SELECT * FROM wallet_stats;")
    wallet_stats = cursor.fetchall()
    
    cursor.close()
    conn.close()

    # Convertir les résultats en format JSON
    data = []
    for stat in wallet_stats:
        data.append({
            'id': stat[0],
            'address': stat[1],
            'gross_profit': str(stat[2]),  # On convertit les valeurs numériques en string pour JSON
            'win_rate': str(stat[3]),
            'total_roi': str(stat[4]),
            'volume': str(stat[5]),
            'total_traded': str(stat[6]),
            'total_token_traded': str(stat[7])
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False)
