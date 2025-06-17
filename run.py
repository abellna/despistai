from flask import Flask, render_template, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from app import create_app, db, allowed_file
from app.models import Item, Location
from werkzeug.utils import secure_filename
import os

app = create_app()

@app.route('/')
def inicio():
    locations = Location.query.all()
    return render_template('form-item.html', locations=locations)

@app.route('/api/locations/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    location = Location.query.get(location_id)

    return jsonify({
        'success': True,
        'location': {
            'id': location.id,
            'nameLocation': location.nameLocation,
            'imageLocation': location.imageLocation,
            'descLocation': location.descLocation
        }
    }), 200

# @app.route('/form-item')
# def form_item():
#     return render_template('form-item.html')

@app.route('/guardar-item', methods=['POST'])
def guardar_item():
    itemName = request.form.get('itemName')
    itemImage = request.form.get('itemImage')
    itemDescription = request.form.get('itemDescription')
    itemLocation = request.form.get('itemLocation')
    imageLocation = request.form.get('imageLocation')
    descLocation = request.form.get('descLocation')
    idLocation = request.form.get('idLocation')

    itemAndLocation = Item(
        itemName=itemName,
        itemImage=itemImage,
        itemDescription=itemDescription,
        itemLocation=itemLocation,
        imageLocation=imageLocation,
        descLocation=descLocation,
        idLocation=idLocation
    )

    db.session.add(itemAndLocation)
    db.session.commit()

@app.route('/crear-ubicacion', methods=['POST'])
def crear_ubicacion():
    nameLocation = request.form['nameLocation']
    imageLocation = request.files['imageLocation']
    descLocation = request.form['descLocation']

    if not nameLocation or not imageLocation:
        return jsonify({'error': 'Missing required fields'}), 400
    
    filename = secure_filename(imageLocation.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    imageLocation.save(save_path)
    
    new_location = Location(
        nameLocation=nameLocation,
        imageLocation=filename,
        descLocation=descLocation
    )

    db.session.add(new_location)
    db.session.commit()

    return jsonify({'success': True,
                    'location_id': new_location.id,
                    'nameLocation': new_location.nameLocation,
                    'imageLocation': new_location.imageLocation,
                    'descLocation': new_location.descLocation}), 201

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)