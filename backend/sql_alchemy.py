import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class TypeElement(enum.Enum):
    SALLE_REUNION = "SALLE_REUNION"
    SALLE_RESTAURATION = "SALLE_RESTAURATION"
    AUTRE = "AUTRE"
    AMPHITHEATRE = "AMPHITHEATRE"

class JourSemaine(enum.Enum):
    Mercredi = "Mercredi"
    Dimanche = "Dimanche"
    Samedi = "Samedi"
    Vendredi = "Vendredi"
    Lundi = "Lundi"
    Jeudi = "Jeudi"
    Mardi = "Mardi"

class TypeSaison(enum.Enum):
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    BASSE = "BASSE"

class TypePrestation(enum.Enum):
    GLOBALE = "GLOBALE"
    DIMENSIONNEE = "DIMENSIONNEE"

class StatutReservation(enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"
    PASSEE = "PASSEE"

class MotifIndisponibilite(enum.Enum):
    FERMETURE = "FERMETURE"
    TRAVAUX = "TRAVAUX"
    MAINTENANCE = "MAINTENANCE"


# Tables definition for many-to-many relationships

# Tables definition
class LienReservationPrestation(Base):
    __tablename__ = "lienreservationprestation"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    quantite: Mapped[int] = mapped_column(Integer)
    coutCalcule: Mapped[float] = mapped_column(Float)
    prestation_id: Mapped[int] = mapped_column(ForeignKey("prestation.id"))
    inclut_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))

class LienReservationMateriel(Base):
    __tablename__ = "lienreservationmateriel"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    quantite: Mapped[int] = mapped_column(Integer)
    coutCalcule: Mapped[float] = mapped_column(Float)
    materiel_id: Mapped[int] = mapped_column(ForeignKey("materiel.id"))

class LienReservationElement(Base):
    __tablename__ = "lienreservationelement"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    coutCalcule: Mapped[float] = mapped_column(Float)
    concerne_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))
    Cible_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class Prestation(Base):
    __tablename__ = "prestation"
    description: Mapped[str] = mapped_column(String(100))
    type: Mapped[TypePrestation] = mapped_column(Enum(TypePrestation))
    prixUnitaireBase: Mapped[float] = mapped_column(Float)
    maxParticipants: Mapped[int] = mapped_column(Integer)
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))

class Materiel(Base):
    __tablename__ = "materiel"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    prixJournalierBase: Mapped[float] = mapped_column(Float)
    stockTotal: Mapped[int] = mapped_column(Integer)

class Reservation(Base):
    __tablename__ = "reservation"
    nomContact: Mapped[str] = mapped_column(String(100))
    emailReferent: Mapped[str] = mapped_column(String(100))
    telephoneContact: Mapped[str] = mapped_column(String(100))
    dateDebut: Mapped[dt_date] = mapped_column(Date)
    dateFin: Mapped[dt_date] = mapped_column(Date)
    statut: Mapped[StatutReservation] = mapped_column(Enum(StatutReservation))
    delaiConfirmationJours: Mapped[int] = mapped_column(Integer)
    coutTotalFinal: Mapped[float] = mapped_column(Float)
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nomEvenement: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    participantsPrevus: Mapped[int] = mapped_column(Integer)
    lienreservationmateriel_id: Mapped[int] = mapped_column(ForeignKey("lienreservationmateriel.id"))

class CentreCongres(Base):
    __tablename__ = "centrecongres"
    emailContact: Mapped[str] = mapped_column(String(100))
    telephoneContact: Mapped[str] = mapped_column(String(100))
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    adresse: Mapped[str] = mapped_column(String(100))
    ville: Mapped[str] = mapped_column(String(100))

class TarifSaisonnier(Base):
    __tablename__ = "tarifsaisonnier"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    saison: Mapped[TypeSaison] = mapped_column(Enum(TypeSaison))
    prixJournalier: Mapped[float] = mapped_column(Float)
    possede_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class Indisponibilite(Base):
    __tablename__ = "indisponibilite"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    motif: Mapped[MotifIndisponibilite] = mapped_column(Enum(MotifIndisponibilite))
    dateDebut: Mapped[dt_date] = mapped_column(Date)
    dateFin: Mapped[dt_date] = mapped_column(Date)
    remarques: Mapped[str] = mapped_column(String(100))
    Subit_id: Mapped[int] = mapped_column(ForeignKey("elementcentre.id"))

class ElementCentre(Base):
    __tablename__ = "elementcentre"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    type: Mapped[TypeElement] = mapped_column(Enum(TypeElement))
    capaciteMax: Mapped[int] = mapped_column(Integer)
    surfaceM2: Mapped[int] = mapped_column(Integer)
    dureeMinJours: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(100))
    compose_id: Mapped[int] = mapped_column(ForeignKey("centrecongres.id"))


#--- Relationships of the lienreservationprestation table
LienReservationPrestation.prestation: Mapped["Prestation"] = relationship("Prestation", back_populates="lienreservationprestation", foreign_keys=[LienReservationPrestation.prestation_id])
LienReservationPrestation.inclut: Mapped["Reservation"] = relationship("Reservation", back_populates="lienreservationprestation_1", foreign_keys=[LienReservationPrestation.inclut_id])

#--- Relationships of the lienreservationmateriel table
LienReservationMateriel.inclut: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="lienreservationmateriel", foreign_keys=[Reservation.lienreservationmateriel_id])
LienReservationMateriel.materiel: Mapped["Materiel"] = relationship("Materiel", back_populates="lienreservationmateriel_1", foreign_keys=[LienReservationMateriel.materiel_id])

#--- Relationships of the lienreservationelement table
LienReservationElement.concerne: Mapped["Reservation"] = relationship("Reservation", back_populates="lienreservationelement", foreign_keys=[LienReservationElement.concerne_id])
LienReservationElement.Cible: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="lienreservationelement_1", foreign_keys=[LienReservationElement.Cible_id])

#--- Relationships of the prestation table
Prestation.lienreservationprestation: Mapped[List["LienReservationPrestation"]] = relationship("LienReservationPrestation", back_populates="prestation", foreign_keys=[LienReservationPrestation.prestation_id])

#--- Relationships of the materiel table
Materiel.lienreservationmateriel_1: Mapped[List["LienReservationMateriel"]] = relationship("LienReservationMateriel", back_populates="materiel", foreign_keys=[LienReservationMateriel.materiel_id])

#--- Relationships of the reservation table
Reservation.lienreservationmateriel: Mapped["LienReservationMateriel"] = relationship("LienReservationMateriel", back_populates="inclut", foreign_keys=[Reservation.lienreservationmateriel_id])
Reservation.lienreservationelement: Mapped[List["LienReservationElement"]] = relationship("LienReservationElement", back_populates="concerne", foreign_keys=[LienReservationElement.concerne_id])
Reservation.lienreservationprestation_1: Mapped[List["LienReservationPrestation"]] = relationship("LienReservationPrestation", back_populates="inclut", foreign_keys=[LienReservationPrestation.inclut_id])

#--- Relationships of the centrecongres table
CentreCongres.elementcentre: Mapped[List["ElementCentre"]] = relationship("ElementCentre", back_populates="compose", foreign_keys=[ElementCentre.compose_id])

#--- Relationships of the tarifsaisonnier table
TarifSaisonnier.possede: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="tarifsaisonnier", foreign_keys=[TarifSaisonnier.possede_id])

#--- Relationships of the indisponibilite table
Indisponibilite.Subit: Mapped["ElementCentre"] = relationship("ElementCentre", back_populates="indisponibilite", foreign_keys=[Indisponibilite.Subit_id])

#--- Relationships of the elementcentre table
ElementCentre.lienreservationelement_1: Mapped[List["LienReservationElement"]] = relationship("LienReservationElement", back_populates="Cible", foreign_keys=[LienReservationElement.Cible_id])
ElementCentre.indisponibilite: Mapped[List["Indisponibilite"]] = relationship("Indisponibilite", back_populates="Subit", foreign_keys=[Indisponibilite.Subit_id])
ElementCentre.compose: Mapped["CentreCongres"] = relationship("CentreCongres", back_populates="elementcentre", foreign_keys=[ElementCentre.compose_id])
ElementCentre.tarifsaisonnier: Mapped[List["TarifSaisonnier"]] = relationship("TarifSaisonnier", back_populates="possede", foreign_keys=[TarifSaisonnier.possede_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)