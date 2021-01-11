from stock_data import db


class StockTechnicalTerms(db.Model):
    __tablename__ = "stock_tech_terms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO drop constraint unique from term_name. One term can have
    # different definitions
    term_name = db.Column(db.String(255), nullable=False, unique=True)
    definition = db.Column(db.String(255))
    description = db.Column(db.String(500))
    calculation_process = db.Column(db.String(500))

    def __init__(self, term_name_, definition_=None, description_=None, calculation_process_=None):
        self.term_name = term_name_
        self.definition = definition_
        self.description = description_
        self.calculation_process = calculation_process_

    def get_id(self):
        return self.id

    def get_term_name(self):
        return self.term_name
