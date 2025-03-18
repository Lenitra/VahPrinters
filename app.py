# Point d'entrée Flask
import json
import os
import datetime
from flask import Flask, redirect, render_template, request
app = Flask(__name__)


# Configuration du dossier d'enregistrement et extensions autorisées
UPLOAD_FOLDER = 'demandes'
ALLOWED_EXTENSIONS = {'stl', 'obj'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Création du dossier principal si inexistant
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/form/send_devis_form', methods=['POST'])
def enregistrer_demande():

    nom = request.form.get('nom')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    materiau = request.form.get('materiau')
    quantite = request.form.get('quantite')
    description = request.form.get('description')
    fichier = request.files.get('fichier')
    
    # Print pour vérifier les données
    print(nom, email, telephone, materiau, quantite, description, fichier)

    # Traitement du fichier 3D
    fichier = request.files.get('fichier')
    if not fichier or not allowed_file(fichier.filename):
        return "Fichier non valide. Veuillez télécharger un fichier STL ou OBJ.", 400
    
    # Sécuriser le nom du fichier
    filename = fichier.filename
    
    # Création d'un dossier unique pour cette demande (utilisation du nom et d'un timestamp)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # définir le filename sur le nom en laissant que les caractères alphanumériques
    filename = "".join([c for c in nom if c.isalnum() or c in ('.', '_', '-')]) + f"_{timestamp}"
    # Créer le dossier pour la demande
    dossier_demande = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(dossier_demande, exist_ok=True)
    
    # Enregistrer le fichier 3D dans le dossier
    chemin_fichier = os.path.join(dossier_demande, filename)
    fichier.save(chemin_fichier)
    
    # Créer un fichier JSON avec les informations de la demande
    demande_data = {
        "nom": nom,
        "email": email,
        "telephone": telephone,
        "materiau": materiau,
        "quantite": quantite,
        "description": description,
        "fichier": filename
    }
    
    chemin_json = os.path.join(dossier_demande, "demande.json")
    with open(chemin_json, 'w', encoding='utf-8') as f:
        json.dump(demande_data, f, ensure_ascii=False, indent=4)
    
    return redirect("/")


@app.route('/')
def home():
    return render_template('all/index.html')

@app.route('/devis_formulaire', methods=['POST', 'GET'])
def formulaire():
    return render_template('all/form.html')

@app.route('/shop', methods=['GET'])
def shop():
    return render_template('all/shop.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)