from flask import render_template, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from app import create_app, db
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
    location = db.session.get(Location, location_id)

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

@app.route('/crear-item', methods=['POST'])
def guardar_item():
    itemName = request.form['itemName']
    itemImage = request.files['itemImage']
    itemDescription = request.form['itemDescription']
    idLocation = request.form['itemLocation']

    if not itemName or not itemImage:
        return jsonify({'error': 'Missing required fields'}), 400
    
    filename = secure_filename(itemImage.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'items', filename)

    itemImage.save(save_path)
    
    new_item = Item(
        itemName=itemName,
        itemImage=filename,
        itemDescription=itemDescription,
        location_id=idLocation
    )

    db.session.add(new_item)
    db.session.commit()

    selectLocation = select(Location).where(Location.id == idLocation)
    resultLocation = db.session.execute(selectLocation).scalar_one_or_none()
    
    return render_template('view-item.html', item=new_item, location=resultLocation)

@app.route('/crear-ubicacion', methods=['POST'])
def crear_ubicacion():
    nameLocation = request.form['nameLocation']
    imageLocation = request.files['imageLocation']
    descLocation = request.form['descLocation']

    if not nameLocation or not imageLocation:
        return jsonify({'error': 'Missing required fields'}), 400
    
    filename = secure_filename(imageLocation.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'locations', filename)

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