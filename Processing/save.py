import os



# Fonction pour sauvegarder l'image localement
def save_images_locally(image_file, dest_folder):
    filename = os.path.join(dest_folder, image_file.filename)
    image_file.save(filename)
    print("Image", image_file.filename, "saved locally successfully.")



# Fonction pour sauvegarder l'image dans la base de données MySQL
def save_image_to_database(image_file, source_folder, db):
    cursor = db.cursor()

    # Insérer l'image dans la table images
    sql_insert_image = "INSERT INTO images (filename, data, id_competition) VALUES (%s, %s, %s)"

    with open(os.path.join(source_folder, image_file.filename), "rb") as file:
        image_data = file.read()
    
    val_image = (image_file.filename, image_data,1)

    cursor.execute(sql_insert_image, val_image)

    id_image = cursor.lastrowid

    db.commit()
    
    print("Image", image_file.filename, "saved in the database successfully.")
    
    # Fermer le curseur après l'insertion et le traitement
    cursor.close()

    return id_image



def save_dossard(dossard, id_image, db):
    cursor = db.cursor()
    # Insérer l'association dans la table dossard_images
    sql_insert_dossard_images = "INSERT INTO dossard_image (image_id, dossard_id) VALUES (%s, %s)"

    val_dossard_images = (id_image, dossard)
    cursor.execute(sql_insert_dossard_images, val_dossard_images)

    db.commit()
    print("OCR results saved in the database successfully.")
    
    # Fermer le curseur après l'insertion et le traitement
    cursor.close()
