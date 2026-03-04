from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class TypeElement(Enum):
    SALLE_REUNION = "SALLE_REUNION"
    SALLE_RESTAURATION = "SALLE_RESTAURATION"
    AUTRE = "AUTRE"
    AMPHITHEATRE = "AMPHITHEATRE"

class JourSemaine(Enum):
    Mercredi = "Mercredi"
    Dimanche = "Dimanche"
    Samedi = "Samedi"
    Vendredi = "Vendredi"
    Lundi = "Lundi"
    Jeudi = "Jeudi"
    Mardi = "Mardi"

class TypeSaison(Enum):
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    BASSE = "BASSE"

class TypePrestation(Enum):
    GLOBALE = "GLOBALE"
    DIMENSIONNEE = "DIMENSIONNEE"

class StatutReservation(Enum):
    EN_ATTENTE = "EN_ATTENTE"
    CONFIRMEE = "CONFIRMEE"
    ANNULEE = "ANNULEE"
    PASSEE = "PASSEE"

class MotifIndisponibilite(Enum):
    FERMETURE = "FERMETURE"
    TRAVAUX = "TRAVAUX"
    MAINTENANCE = "MAINTENANCE"

############################################
# Classes are defined here
############################################
class LienReservationPrestationCreate(BaseModel):
    id: str
    quantite: int
    coutCalcule: float
    inclut: int  # N:1 Relationship (mandatory)
    prestation: int  # N:1 Relationship (mandatory)


class LienReservationMaterielCreate(BaseModel):
    id: str
    coutCalcule: float
    quantite: int
    materiel: int  # N:1 Relationship (mandatory)
    inclut: Optional[List[int]] = None  # 1:N Relationship


class LienReservationElementCreate(BaseModel):
    coutCalcule: float
    id: str
    concerne: int  # N:1 Relationship (mandatory)
    Cible: int  # N:1 Relationship (mandatory)


class PrestationCreate(BaseModel):
    type: TypePrestation
    prixUnitaireBase: float
    nom: str
    description: str
    id: str
    maxParticipants: int
    lienreservationprestation: Optional[List[int]] = None  # 1:N Relationship


class MaterielCreate(BaseModel):
    nom: str
    id: str
    prixJournalierBase: float
    description: str
    stockTotal: int
    lienreservationmateriel_1: Optional[List[int]] = None  # 1:N Relationship


class ReservationCreate(BaseModel):
    telephoneContact: str
    coutTotalFinal: float
    delaiConfirmationJours: int
    id: str
    statut: StatutReservation
    emailReferent: str
    dateDebut: date
    description: str
    nomContact: str
    dateFin: date
    nomEvenement: str
    participantsPrevus: int
    lienreservationelement: Optional[List[int]] = None  # 1:N Relationship
    lienreservationprestation_1: Optional[List[int]] = None  # 1:N Relationship
    lienreservationmateriel: int  # N:1 Relationship (mandatory)


class CentreCongresCreate(BaseModel):
    ville: str
    nom: str
    telephoneContact: str
    id: str
    adresse: str
    emailContact: str
    elementcentre: Optional[List[int]] = None  # 1:N Relationship


class TarifSaisonnierCreate(BaseModel):
    saison: TypeSaison
    id: str
    prixJournalier: float
    possede: int  # N:1 Relationship (mandatory)


class IndisponibiliteCreate(BaseModel):
    dateDebut: date
    remarques: str
    id: str
    dateFin: date
    motif: MotifIndisponibilite
    Subit: int  # N:1 Relationship (mandatory)


class ElementCentreCreate(BaseModel):
    capaciteMax: int
    description: str
    surfaceM2: int
    id: str
    dureeMinJours: int
    nom: str
    type: TypeElement
    indisponibilite: Optional[List[int]] = None  # 1:N Relationship
    compose: int  # N:1 Relationship (mandatory)
    lienreservationelement_1: Optional[List[int]] = None  # 1:N Relationship
    tarifsaisonnier: Optional[List[int]] = None  # 1:N Relationship


