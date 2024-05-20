
#function to search images containing the dossard
def search_images_from_bib(dossard_searched, db):
    cursor = db.cursor()
    # Sous-requête pour récupérer les IDs d'images uniques correspondant au dossard
    sql = """
        SELECT i.filename
        FROM images i
        WHERE i.id IN (
            SELECT di.image_id
            FROM dossard_image di
            WHERE di.dossard_id = %s
        )
    """
    
    cursor.execute(sql, (dossard_searched,))
    # cursor.execute(sql, (search_query,))
    image_files = [row[0] for row in cursor.fetchall()]
    return image_files