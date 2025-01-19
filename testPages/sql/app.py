from flask import Flask, request
import sqlite3

app = Flask(__name__)


# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect("test.db")
    conn.row_factory = sqlite3.Row
    return conn


# Créer une base de données avec des données initiales
def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'mypassword')")
    conn.commit()
    conn.close()


# Route vulnérable à l'injection SQL
@app.route('/search', methods=['GET', 'POST'])
def search_user():
    # Obtenir le paramètre "username" à partir de GET ou POST
    if request.method == 'GET':
        username = request.args.get("username", "")
    elif request.method == 'POST':
        username = request.form.get("username", "")

    # Vulnérabilité : concaténation directe dans la requête SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        if rows:
            # Retourne les données si des utilisateurs correspondent
            return {"status": "success", "data": [dict(row) for row in rows]}
        else:
            # Message d'erreur si aucun utilisateur n'est trouvé
            return {"status": "error", "message": f"No user found for username: {username}"}
    except sqlite3.Error as e:
        # Message d'erreur explicite en cas de problème SQL
        return {"status": "error", "message": f"SQL Error: {str(e)}"}


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
