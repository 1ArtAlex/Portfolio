from app import db


class CitySearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(64), index=True, unique=False)
    search_count = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<CitySearch {self.city_name}>'