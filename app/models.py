from app import db
from datetime import datetime, timezone

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(100), nullable=False)
    itemImage = db.Column(db.String(120), nullable=False)
    itemDescription = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameLocation = db.Column(db.String(120), nullable=False)
    imageLocation = db.Column(db.String(120), nullable=False)
    descLocation = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    items = db.relationship('Item', backref='location', lazy=True)

    #Esto sirve para serializar el objeto Location a un diccionario, en caso de que quiera hacerlo
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'image': self.image
    #     }