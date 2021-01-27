from stock_data import db
import datetime


class StockTechnicalTerms(db.Model):
    __tablename__ = "stock_tech_terms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO create slug field
    term_name = db.Column(db.String(255), nullable=False, unique=True)
    definition = db.Column(db.String(500))
    description = db.Column(db.String(500))
    calculation_process = db.Column(db.String(500))
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self,
                 term_name_,
                 definition_=None,
                 description_=None,
                 calculation_process_=None,
                 # updated_=datetime.datetime.utcnow,
                 ):
        self.term_name = term_name_
        self.definition = definition_
        self.description = description_
        self.calculation_process = calculation_process_
        # self.updated = updated_

    def get_id(self):
        return self.id

    def get_term_name(self):
        return self.term_name
