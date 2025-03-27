# Point d'entrée Flask
import json
import os
import datetime
from flask import Flask, redirect, render_template, request, session


app = Flask(__name__)


# Configuration du dossier d'enregistrement et extensions autorisées
UPLOAD_FOLDER = 'demandes'
ALLOWED_EXTENSIONS = {'stl', 'obj'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Création du dossier principal si inexistant
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)




@app.route('/')
def home():
    return render_template('all/index.html')



@app.route('/shop', methods=['GET'])
def shop():
    return render_template('all/shop.html')



@app.route('/devis_formulaire', methods=['POST', 'GET'])
def formulaire():
    return render_template('all/form.html')


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
    filename = fichier.filename
    if not fichier or (not '.' in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS):
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
        "fichier": filename,
        "status": "En attente"
    }
    
    chemin_json = os.path.join(dossier_demande, "demande.json")
    with open(chemin_json, 'w', encoding='utf-8') as f:
        json.dump(demande_data, f, ensure_ascii=False, indent=4)
    
    return redirect("/")








@app.route('/login', methods=['GET'])
def login():
    return render_template('printer/login.html')



@app.route('/check-login', methods=["POST"])
def checkLogin():
    # get the data
    data = request.form
    print(data)
    username = data.get('username')
    password = data.get('password')
    # check if the email and password are correct
    with open('config/printers.json', 'r') as f:
        users = json.load(f)
    for k, v in users.items():
        if k == username and v == password:
            session['username'] = username
            return redirect("/printers")
    return redirect("/login")



def getDemandes(status = "En attente"):
    # Lire les demandes
    demandes = []
    for dossier in os.listdir("demandes"):
        chemin_json = os.path.join("demandes", dossier, "demande.json")
        with open(chemin_json, 'r', encoding='utf-8') as f:
            demande = json.load(f)
            date = dossier.split('_')[-1]
            demande['date'] = date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' ' + date[8:10] + ':' + date[10:12] + ':' + date[12:14]
            if demande['status'] == status or status == 'all':
                demande['dossier'] = dossier
                demandes.append(demande)
    return demandes



@app.route('/printers', methods=['GET'])
def printers():
    return render_template('printer/dashboard.html', demandes = getDemandes(), travaux = getDemandes(session.get('username')), alldemandes = getDemandes('all'))


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)