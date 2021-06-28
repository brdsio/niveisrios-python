from google.appengine.ext import db

class Rio(db.Model):
    id = db.StringProperty()
    cidade = db.StringProperty()
    datahora = db.DateTimeProperty()
    nivel = db.FloatProperty()
    precipitacao = db.FloatProperty()
    status = db.StringProperty()
    precipitacao12 = db.FloatProperty()
    precipitacao24 = db.FloatProperty()
    precipitacao48 = db.FloatProperty()
