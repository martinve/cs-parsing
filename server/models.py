from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    passage = Column(String)
    rawdata = Column(String)
    context = Column(String)

    sentences = relationship("Sentence")

    def __repr__(self):
        return f"<Sentence id={self.id} text={self.passage}>"


class Sentence(Base):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    text = Column(String)
    parse_amr = Column(String)
    parse_ud = Column(String)
    parse_ud_raw = Column(String)
    context = Column(String)
    logic = Column(String)
    simpl_logic = Column(String)

    experiment = relationship("Experiment", back_populates="sentences")

    def __repr__(self):
        return f"<Sentence id={self.id} experiment_id={self.experiment_id} text={self.text} logic={self.logic}>"
