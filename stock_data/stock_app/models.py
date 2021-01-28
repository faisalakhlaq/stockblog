from stock_data import db
import datetime


class StockTechnicalTerms(db.Model):
    __tablename__ = "stock_tech_terms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO create slug field
    term_name = db.Column(db.String(255), nullable=False, unique=True)
    definition = db.Column(db.Text)
    description = db.Column(db.Text)
    calculation_process = db.Column(db.Text)
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('person.user_id'), nullable=False)

    def __init__(self,
                 term_name_,
                 definition_=None,
                 description_=None,
                 calculation_process_=None,
                 # updated_=datetime.datetime.utcnow,
                 user_id_=None,
                 ):
        self.term_name = term_name_
        self.definition = definition_
        self.description = description_
        self.calculation_process = calculation_process_
        self.user_id = user_id_
        # self.updated = updated_

    def get_id(self):
        return self.id

    def get_term_name(self):
        return self.term_name
