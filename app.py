import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from flask import Flask, render_template, request, redirect, url_for,jsonify
import mysql.connector
from Processing.save import *
from Processing.detector import detect_dossard
from Processing.search import search_images_from_bib



app = Flask(__name__)
app.secret_key = 'Dossard@Nadia2002'
app.config['UPLOAD_FOLDER'] = 'static/uploads' # Chemin d'accès au répertoire temporaire pour stocker les images téléchargées

# Assurez-vous que le répertoire d'upload existe
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dossarddb"
)


# Définir la route pour la page d'accueil
@app.route('/')
def home():
    return render_template('services.html', css_file='style.css')

#Route pour telechargement d'images
@app.route('/upload', methods=['GET', 'POST'])
def upload_images():

    if request.method == 'GET':

        show_alert = request.args.get('show_popup')
        # Afficher le formulaire d'upload
        return render_template('upload.html', show_popup=show_alert)
    else:
        # Gérer l'upload des images
        image_files = request.files.getlist("image")

        # Envoyer les images localement et dans la base de données
        for image_file in image_files:
            # Sauvegarder l'image localement
            save_images_locally(image_file, app.config['UPLOAD_FOLDER'])

            # Détecter les dossards
            extracted_bibs = detect_dossard(os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename))
            
            id_image = save_image_to_database(image_file, app.config['UPLOAD_FOLDER'], mydb)

            for bib in extracted_bibs:
                if bib is not None:
                    save_dossard(bib, id_image, mydb)

        
        # Rediriger l'utilisateur vers la même page
        return redirect(url_for('upload_images', show_popup=True))

# @app.route('/se')
# def search_form():
#     return render_template('search.html')

# @app.route('/search', methods=['POST'])
# def search_images():
#     search_query = request.form['dossard_number']

#     image_files = search_images_from_bib(search_query, mydb)

#     return render_template('results.html', image_files=image_files)

# Existing route to display the search form
@app.route('/se')
def search_form():
    return render_template('search.html')

# New route to handle AJAX search requests
@app.route('/search', methods=['POST'])
def search_images():
    search_query = request.form['dossard_number']
    image_files = search_images_from_bib(search_query, mydb)
    return jsonify({'image_files': image_files})

@app.route('/images')
def show_all_images():
    # Récupérer les données de toutes les images à partir de la base de données
    cursor = mydb.cursor()
    sql = "SELECT id, filename, data FROM images"
    cursor.execute(sql)
    images = cursor.fetchall()
    print("Images retrieved from the database successfully.", images)
    # Rendre le modèle HTML et passer les données d'image à afficher
    return render_template('shows.html', images=images)


if __name__ == '__main__':
    app.run(debug=True)