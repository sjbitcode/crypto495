from cryptoapi import app, db


class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    symbol = db.Column(db.String(20), unique=True, index=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, index=True, nullable=False)
    website = db.Column(db.String(100))
    repo = db.Column(db.String(100))
    description = db.Column(db.Text)
    platform = db.Column(db.String(50))
    category = db.Column(db.String(10))
    logo = db.Column(db.String(100))

    def __str__(self):
        return f'({self.symbol}) - {self.name}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'slug': self.slug,
            'website': self.website,
            'repo': self.repo,
            'description': self.description,
            'platform': self.platform,
            'category': self.category,
            'logo': self.logo
        }

    def root_to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'slug': self.slug
        }
