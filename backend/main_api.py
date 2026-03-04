import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "LienReservationPrestation", "description": "Operations for LienReservationPrestation entities"},
        {"name": "LienReservationPrestation Relationships", "description": "Manage LienReservationPrestation relationships"},
        {"name": "LienReservationPrestation Methods", "description": "Execute LienReservationPrestation methods"},
        {"name": "LienReservationMateriel", "description": "Operations for LienReservationMateriel entities"},
        {"name": "LienReservationMateriel Relationships", "description": "Manage LienReservationMateriel relationships"},
        {"name": "LienReservationMateriel Methods", "description": "Execute LienReservationMateriel methods"},
        {"name": "LienReservationElement", "description": "Operations for LienReservationElement entities"},
        {"name": "LienReservationElement Relationships", "description": "Manage LienReservationElement relationships"},
        {"name": "LienReservationElement Methods", "description": "Execute LienReservationElement methods"},
        {"name": "Prestation", "description": "Operations for Prestation entities"},
        {"name": "Prestation Relationships", "description": "Manage Prestation relationships"},
        {"name": "Prestation Methods", "description": "Execute Prestation methods"},
        {"name": "Materiel", "description": "Operations for Materiel entities"},
        {"name": "Materiel Relationships", "description": "Manage Materiel relationships"},
        {"name": "Materiel Methods", "description": "Execute Materiel methods"},
        {"name": "Reservation", "description": "Operations for Reservation entities"},
        {"name": "Reservation Relationships", "description": "Manage Reservation relationships"},
        {"name": "Reservation Methods", "description": "Execute Reservation methods"},
        {"name": "CentreCongres", "description": "Operations for CentreCongres entities"},
        {"name": "CentreCongres Relationships", "description": "Manage CentreCongres relationships"},
        {"name": "CentreCongres Methods", "description": "Execute CentreCongres methods"},
        {"name": "TarifSaisonnier", "description": "Operations for TarifSaisonnier entities"},
        {"name": "TarifSaisonnier Relationships", "description": "Manage TarifSaisonnier relationships"},
        {"name": "TarifSaisonnier Methods", "description": "Execute TarifSaisonnier methods"},
        {"name": "Indisponibilite", "description": "Operations for Indisponibilite entities"},
        {"name": "Indisponibilite Relationships", "description": "Manage Indisponibilite relationships"},
        {"name": "Indisponibilite Methods", "description": "Execute Indisponibilite methods"},
        {"name": "ElementCentre", "description": "Operations for ElementCentre entities"},
        {"name": "ElementCentre Relationships", "description": "Manage ElementCentre relationships"},
        {"name": "ElementCentre Methods", "description": "Execute ElementCentre methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["lienreservationprestation_count"] = database.query(LienReservationPrestation).count()
    stats["lienreservationmateriel_count"] = database.query(LienReservationMateriel).count()
    stats["lienreservationelement_count"] = database.query(LienReservationElement).count()
    stats["prestation_count"] = database.query(Prestation).count()
    stats["materiel_count"] = database.query(Materiel).count()
    stats["reservation_count"] = database.query(Reservation).count()
    stats["centrecongres_count"] = database.query(CentreCongres).count()
    stats["tarifsaisonnier_count"] = database.query(TarifSaisonnier).count()
    stats["indisponibilite_count"] = database.query(Indisponibilite).count()
    stats["elementcentre_count"] = database.query(ElementCentre).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   LienReservationPrestation functions
#
############################################

@app.get("/lienreservationprestation/", response_model=None, tags=["LienReservationPrestation"])
def get_all_lienreservationprestation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(LienReservationPrestation)
        query = query.options(joinedload(LienReservationPrestation.inclut))
        query = query.options(joinedload(LienReservationPrestation.prestation))
        lienreservationprestation_list = query.all()

        # Serialize with relationships included
        result = []
        for lienreservationprestation_item in lienreservationprestation_list:
            item_dict = lienreservationprestation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if lienreservationprestation_item.inclut:
                related_obj = lienreservationprestation_item.inclut
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['inclut'] = related_dict
            else:
                item_dict['inclut'] = None
            if lienreservationprestation_item.prestation:
                related_obj = lienreservationprestation_item.prestation
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['prestation'] = related_dict
            else:
                item_dict['prestation'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(LienReservationPrestation).all()


@app.get("/lienreservationprestation/count/", response_model=None, tags=["LienReservationPrestation"])
def get_count_lienreservationprestation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of LienReservationPrestation entities"""
    count = database.query(LienReservationPrestation).count()
    return {"count": count}


@app.get("/lienreservationprestation/paginated/", response_model=None, tags=["LienReservationPrestation"])
def get_paginated_lienreservationprestation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of LienReservationPrestation entities"""
    total = database.query(LienReservationPrestation).count()
    lienreservationprestation_list = database.query(LienReservationPrestation).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": lienreservationprestation_list
    }


@app.get("/lienreservationprestation/search/", response_model=None, tags=["LienReservationPrestation"])
def search_lienreservationprestation(
    database: Session = Depends(get_db)
) -> list:
    """Search LienReservationPrestation entities by attributes"""
    query = database.query(LienReservationPrestation)


    results = query.all()
    return results


@app.get("/lienreservationprestation/{lienreservationprestation_id}/", response_model=None, tags=["LienReservationPrestation"])
async def get_lienreservationprestation(lienreservationprestation_id: int, database: Session = Depends(get_db)) -> LienReservationPrestation:
    db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
    if db_lienreservationprestation is None:
        raise HTTPException(status_code=404, detail="LienReservationPrestation not found")

    response_data = {
        "lienreservationprestation": db_lienreservationprestation,
}
    return response_data



@app.post("/lienreservationprestation/", response_model=None, tags=["LienReservationPrestation"])
async def create_lienreservationprestation(lienreservationprestation_data: LienReservationPrestationCreate, database: Session = Depends(get_db)) -> LienReservationPrestation:

    if lienreservationprestation_data.inclut is not None:
        db_inclut = database.query(Reservation).filter(Reservation.id == lienreservationprestation_data.inclut).first()
        if not db_inclut:
            raise HTTPException(status_code=400, detail="Reservation not found")
    else:
        raise HTTPException(status_code=400, detail="Reservation ID is required")
    if lienreservationprestation_data.prestation is not None:
        db_prestation = database.query(Prestation).filter(Prestation.id == lienreservationprestation_data.prestation).first()
        if not db_prestation:
            raise HTTPException(status_code=400, detail="Prestation not found")
    else:
        raise HTTPException(status_code=400, detail="Prestation ID is required")

    db_lienreservationprestation = LienReservationPrestation(
        id=lienreservationprestation_data.id,        quantite=lienreservationprestation_data.quantite,        coutCalcule=lienreservationprestation_data.coutCalcule,        inclut_id=lienreservationprestation_data.inclut,        prestation_id=lienreservationprestation_data.prestation        )

    database.add(db_lienreservationprestation)
    database.commit()
    database.refresh(db_lienreservationprestation)




    return db_lienreservationprestation


@app.post("/lienreservationprestation/bulk/", response_model=None, tags=["LienReservationPrestation"])
async def bulk_create_lienreservationprestation(items: list[LienReservationPrestationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple LienReservationPrestation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.inclut:
                raise ValueError("Reservation ID is required")
            if not item_data.prestation:
                raise ValueError("Prestation ID is required")

            db_lienreservationprestation = LienReservationPrestation(
                id=item_data.id,                quantite=item_data.quantite,                coutCalcule=item_data.coutCalcule,                inclut_id=item_data.inclut,                prestation_id=item_data.prestation            )
            database.add(db_lienreservationprestation)
            database.flush()  # Get ID without committing
            created_items.append(db_lienreservationprestation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} LienReservationPrestation entities"
    }


@app.delete("/lienreservationprestation/bulk/", response_model=None, tags=["LienReservationPrestation"])
async def bulk_delete_lienreservationprestation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple LienReservationPrestation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == item_id).first()
        if db_lienreservationprestation:
            database.delete(db_lienreservationprestation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} LienReservationPrestation entities"
    }

@app.put("/lienreservationprestation/{lienreservationprestation_id}/", response_model=None, tags=["LienReservationPrestation"])
async def update_lienreservationprestation(lienreservationprestation_id: int, lienreservationprestation_data: LienReservationPrestationCreate, database: Session = Depends(get_db)) -> LienReservationPrestation:
    db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
    if db_lienreservationprestation is None:
        raise HTTPException(status_code=404, detail="LienReservationPrestation not found")

    setattr(db_lienreservationprestation, 'id', lienreservationprestation_data.id)
    setattr(db_lienreservationprestation, 'quantite', lienreservationprestation_data.quantite)
    setattr(db_lienreservationprestation, 'coutCalcule', lienreservationprestation_data.coutCalcule)
    if lienreservationprestation_data.inclut is not None:
        db_inclut = database.query(Reservation).filter(Reservation.id == lienreservationprestation_data.inclut).first()
        if not db_inclut:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_lienreservationprestation, 'inclut_id', lienreservationprestation_data.inclut)
    if lienreservationprestation_data.prestation is not None:
        db_prestation = database.query(Prestation).filter(Prestation.id == lienreservationprestation_data.prestation).first()
        if not db_prestation:
            raise HTTPException(status_code=400, detail="Prestation not found")
        setattr(db_lienreservationprestation, 'prestation_id', lienreservationprestation_data.prestation)
    database.commit()
    database.refresh(db_lienreservationprestation)

    return db_lienreservationprestation


@app.delete("/lienreservationprestation/{lienreservationprestation_id}/", response_model=None, tags=["LienReservationPrestation"])
async def delete_lienreservationprestation(lienreservationprestation_id: int, database: Session = Depends(get_db)):
    db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
    if db_lienreservationprestation is None:
        raise HTTPException(status_code=404, detail="LienReservationPrestation not found")
    database.delete(db_lienreservationprestation)
    database.commit()
    return db_lienreservationprestation



############################################
#   LienReservationPrestation Method Endpoints
############################################




@app.post("/lienreservationprestation/{lienreservationprestation_id}/methods/calculerCoutLien/", response_model=None, tags=["LienReservationPrestation Methods"])
async def execute_lienreservationprestation_calculerCoutLien(
    lienreservationprestation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCoutLien method on a LienReservationPrestation instance.
    """
    # Retrieve the entity from the database
    _lienreservationprestation_object = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
    if _lienreservationprestation_object is None:
        raise HTTPException(status_code=404, detail="LienReservationPrestation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_lienreservationprestation_object):
            """Calcule le coût d'une prestation."""
            presta = await get_prestation(_lienreservationprestation_object.cible)
            cout = 0.0
            
            if presta.type == "GLOBALE":
                cout = presta.prixUnitaireBase
            else: # DIMENSIONNEE
                cout = presta.prixUnitaireBase * _lienreservationprestation_object.quantite
                
            await update_lienreservationprestation(_lienreservationprestation_object.id, LienReservationPrestationCreate(coutCalcule=cout))
            return cout

        result = await wrapper(_lienreservationprestation_object)
        # Commit DB
        database.commit()
        database.refresh(_lienreservationprestation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "lienreservationprestation_id": lienreservationprestation_id,
            "method": "calculerCoutLien",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   LienReservationMateriel functions
#
############################################

@app.get("/lienreservationmateriel/", response_model=None, tags=["LienReservationMateriel"])
def get_all_lienreservationmateriel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(LienReservationMateriel)
        query = query.options(joinedload(LienReservationMateriel.materiel))
        lienreservationmateriel_list = query.all()

        # Serialize with relationships included
        result = []
        for lienreservationmateriel_item in lienreservationmateriel_list:
            item_dict = lienreservationmateriel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if lienreservationmateriel_item.materiel:
                related_obj = lienreservationmateriel_item.materiel
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['materiel'] = related_dict
            else:
                item_dict['materiel'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).filter(Reservation.lienreservationmateriel_id == lienreservationmateriel_item.id).all()
            item_dict['inclut'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['inclut'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(LienReservationMateriel).all()


@app.get("/lienreservationmateriel/count/", response_model=None, tags=["LienReservationMateriel"])
def get_count_lienreservationmateriel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of LienReservationMateriel entities"""
    count = database.query(LienReservationMateriel).count()
    return {"count": count}


@app.get("/lienreservationmateriel/paginated/", response_model=None, tags=["LienReservationMateriel"])
def get_paginated_lienreservationmateriel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of LienReservationMateriel entities"""
    total = database.query(LienReservationMateriel).count()
    lienreservationmateriel_list = database.query(LienReservationMateriel).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": lienreservationmateriel_list
        }

    result = []
    for lienreservationmateriel_item in lienreservationmateriel_list:
        inclut_ids = database.query(Reservation.id).filter(Reservation.lienreservationmateriel_id == lienreservationmateriel_item.id).all()
        item_data = {
            "lienreservationmateriel": lienreservationmateriel_item,
            "inclut_ids": [x[0] for x in inclut_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/lienreservationmateriel/search/", response_model=None, tags=["LienReservationMateriel"])
def search_lienreservationmateriel(
    database: Session = Depends(get_db)
) -> list:
    """Search LienReservationMateriel entities by attributes"""
    query = database.query(LienReservationMateriel)


    results = query.all()
    return results


@app.get("/lienreservationmateriel/{lienreservationmateriel_id}/", response_model=None, tags=["LienReservationMateriel"])
async def get_lienreservationmateriel(lienreservationmateriel_id: int, database: Session = Depends(get_db)) -> LienReservationMateriel:
    db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == lienreservationmateriel_id).first()
    if db_lienreservationmateriel is None:
        raise HTTPException(status_code=404, detail="LienReservationMateriel not found")

    inclut_ids = database.query(Reservation.id).filter(Reservation.lienreservationmateriel_id == db_lienreservationmateriel.id).all()
    response_data = {
        "lienreservationmateriel": db_lienreservationmateriel,
        "inclut_ids": [x[0] for x in inclut_ids]}
    return response_data



@app.post("/lienreservationmateriel/", response_model=None, tags=["LienReservationMateriel"])
async def create_lienreservationmateriel(lienreservationmateriel_data: LienReservationMaterielCreate, database: Session = Depends(get_db)) -> LienReservationMateriel:

    if lienreservationmateriel_data.materiel is not None:
        db_materiel = database.query(Materiel).filter(Materiel.id == lienreservationmateriel_data.materiel).first()
        if not db_materiel:
            raise HTTPException(status_code=400, detail="Materiel not found")
    else:
        raise HTTPException(status_code=400, detail="Materiel ID is required")

    db_lienreservationmateriel = LienReservationMateriel(
        id=lienreservationmateriel_data.id,        coutCalcule=lienreservationmateriel_data.coutCalcule,        quantite=lienreservationmateriel_data.quantite,        materiel_id=lienreservationmateriel_data.materiel        )

    database.add(db_lienreservationmateriel)
    database.commit()
    database.refresh(db_lienreservationmateriel)

    if lienreservationmateriel_data.inclut:
        # Validate that all Reservation IDs exist
        for reservation_id in lienreservationmateriel_data.inclut:
            db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
            if not db_reservation:
                raise HTTPException(status_code=400, detail=f"Reservation with id {reservation_id} not found")

        # Update the related entities with the new foreign key
        database.query(Reservation).filter(Reservation.id.in_(lienreservationmateriel_data.inclut)).update(
            {Reservation.lienreservationmateriel_id: db_lienreservationmateriel.id}, synchronize_session=False
        )
        database.commit()



    inclut_ids = database.query(Reservation.id).filter(Reservation.lienreservationmateriel_id == db_lienreservationmateriel.id).all()
    response_data = {
        "lienreservationmateriel": db_lienreservationmateriel,
        "inclut_ids": [x[0] for x in inclut_ids]    }
    return response_data


@app.post("/lienreservationmateriel/bulk/", response_model=None, tags=["LienReservationMateriel"])
async def bulk_create_lienreservationmateriel(items: list[LienReservationMaterielCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple LienReservationMateriel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.materiel:
                raise ValueError("Materiel ID is required")

            db_lienreservationmateriel = LienReservationMateriel(
                id=item_data.id,                coutCalcule=item_data.coutCalcule,                quantite=item_data.quantite,                materiel_id=item_data.materiel            )
            database.add(db_lienreservationmateriel)
            database.flush()  # Get ID without committing
            created_items.append(db_lienreservationmateriel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} LienReservationMateriel entities"
    }


@app.delete("/lienreservationmateriel/bulk/", response_model=None, tags=["LienReservationMateriel"])
async def bulk_delete_lienreservationmateriel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple LienReservationMateriel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == item_id).first()
        if db_lienreservationmateriel:
            database.delete(db_lienreservationmateriel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} LienReservationMateriel entities"
    }

@app.put("/lienreservationmateriel/{lienreservationmateriel_id}/", response_model=None, tags=["LienReservationMateriel"])
async def update_lienreservationmateriel(lienreservationmateriel_id: int, lienreservationmateriel_data: LienReservationMaterielCreate, database: Session = Depends(get_db)) -> LienReservationMateriel:
    db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == lienreservationmateriel_id).first()
    if db_lienreservationmateriel is None:
        raise HTTPException(status_code=404, detail="LienReservationMateriel not found")

    setattr(db_lienreservationmateriel, 'id', lienreservationmateriel_data.id)
    setattr(db_lienreservationmateriel, 'coutCalcule', lienreservationmateriel_data.coutCalcule)
    setattr(db_lienreservationmateriel, 'quantite', lienreservationmateriel_data.quantite)
    if lienreservationmateriel_data.materiel is not None:
        db_materiel = database.query(Materiel).filter(Materiel.id == lienreservationmateriel_data.materiel).first()
        if not db_materiel:
            raise HTTPException(status_code=400, detail="Materiel not found")
        setattr(db_lienreservationmateriel, 'materiel_id', lienreservationmateriel_data.materiel)
    if lienreservationmateriel_data.inclut is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Reservation).filter(Reservation.lienreservationmateriel_id == db_lienreservationmateriel.id).update(
            {Reservation.lienreservationmateriel_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if lienreservationmateriel_data.inclut:
            # Validate that all IDs exist
            for reservation_id in lienreservationmateriel_data.inclut:
                db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
                if not db_reservation:
                    raise HTTPException(status_code=400, detail=f"Reservation with id {reservation_id} not found")

            # Update the related entities with the new foreign key
            database.query(Reservation).filter(Reservation.id.in_(lienreservationmateriel_data.inclut)).update(
                {Reservation.lienreservationmateriel_id: db_lienreservationmateriel.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_lienreservationmateriel)

    inclut_ids = database.query(Reservation.id).filter(Reservation.lienreservationmateriel_id == db_lienreservationmateriel.id).all()
    response_data = {
        "lienreservationmateriel": db_lienreservationmateriel,
        "inclut_ids": [x[0] for x in inclut_ids]    }
    return response_data


@app.delete("/lienreservationmateriel/{lienreservationmateriel_id}/", response_model=None, tags=["LienReservationMateriel"])
async def delete_lienreservationmateriel(lienreservationmateriel_id: int, database: Session = Depends(get_db)):
    db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == lienreservationmateriel_id).first()
    if db_lienreservationmateriel is None:
        raise HTTPException(status_code=404, detail="LienReservationMateriel not found")
    database.delete(db_lienreservationmateriel)
    database.commit()
    return db_lienreservationmateriel



############################################
#   LienReservationMateriel Method Endpoints
############################################




@app.post("/lienreservationmateriel/{lienreservationmateriel_id}/methods/calculerCoutLien/", response_model=None, tags=["LienReservationMateriel Methods"])
async def execute_lienreservationmateriel_calculerCoutLien(
    lienreservationmateriel_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCoutLien method on a LienReservationMateriel instance.

    Parameters:
    - duree: Any    """
    # Retrieve the entity from the database
    _lienreservationmateriel_object = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == lienreservationmateriel_id).first()
    if _lienreservationmateriel_object is None:
        raise HTTPException(status_code=404, detail="LienReservationMateriel not found")

    # Prepare method parameters
    duree = params.get('duree')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_lienreservationmateriel_object):
            """Calcule le coût : Prix journalier * Quantité * Durée."""
            materiel = await get_materiel(_lienreservationmateriel_object.cible)
            cout = materiel.prixJournalierBase * _lienreservationmateriel_object.quantite * duree
            await update_lienreservationmateriel(_lienreservationmateriel_object.id, LienReservationMaterielCreate(coutCalcule=cout))
            return cout


        result = await wrapper(_lienreservationmateriel_object)
        # Commit DB
        database.commit()
        database.refresh(_lienreservationmateriel_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "lienreservationmateriel_id": lienreservationmateriel_id,
            "method": "calculerCoutLien",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   LienReservationElement functions
#
############################################

@app.get("/lienreservationelement/", response_model=None, tags=["LienReservationElement"])
def get_all_lienreservationelement(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(LienReservationElement)
        query = query.options(joinedload(LienReservationElement.concerne))
        query = query.options(joinedload(LienReservationElement.Cible))
        lienreservationelement_list = query.all()

        # Serialize with relationships included
        result = []
        for lienreservationelement_item in lienreservationelement_list:
            item_dict = lienreservationelement_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if lienreservationelement_item.concerne:
                related_obj = lienreservationelement_item.concerne
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['concerne'] = related_dict
            else:
                item_dict['concerne'] = None
            if lienreservationelement_item.Cible:
                related_obj = lienreservationelement_item.Cible
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['Cible'] = related_dict
            else:
                item_dict['Cible'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(LienReservationElement).all()


@app.get("/lienreservationelement/count/", response_model=None, tags=["LienReservationElement"])
def get_count_lienreservationelement(database: Session = Depends(get_db)) -> dict:
    """Get the total count of LienReservationElement entities"""
    count = database.query(LienReservationElement).count()
    return {"count": count}


@app.get("/lienreservationelement/paginated/", response_model=None, tags=["LienReservationElement"])
def get_paginated_lienreservationelement(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of LienReservationElement entities"""
    total = database.query(LienReservationElement).count()
    lienreservationelement_list = database.query(LienReservationElement).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": lienreservationelement_list
    }


@app.get("/lienreservationelement/search/", response_model=None, tags=["LienReservationElement"])
def search_lienreservationelement(
    database: Session = Depends(get_db)
) -> list:
    """Search LienReservationElement entities by attributes"""
    query = database.query(LienReservationElement)


    results = query.all()
    return results


@app.get("/lienreservationelement/{lienreservationelement_id}/", response_model=None, tags=["LienReservationElement"])
async def get_lienreservationelement(lienreservationelement_id: int, database: Session = Depends(get_db)) -> LienReservationElement:
    db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
    if db_lienreservationelement is None:
        raise HTTPException(status_code=404, detail="LienReservationElement not found")

    response_data = {
        "lienreservationelement": db_lienreservationelement,
}
    return response_data



@app.post("/lienreservationelement/", response_model=None, tags=["LienReservationElement"])
async def create_lienreservationelement(lienreservationelement_data: LienReservationElementCreate, database: Session = Depends(get_db)) -> LienReservationElement:

    if lienreservationelement_data.concerne is not None:
        db_concerne = database.query(Reservation).filter(Reservation.id == lienreservationelement_data.concerne).first()
        if not db_concerne:
            raise HTTPException(status_code=400, detail="Reservation not found")
    else:
        raise HTTPException(status_code=400, detail="Reservation ID is required")
    if lienreservationelement_data.Cible is not None:
        db_Cible = database.query(ElementCentre).filter(ElementCentre.id == lienreservationelement_data.Cible).first()
        if not db_Cible:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_lienreservationelement = LienReservationElement(
        coutCalcule=lienreservationelement_data.coutCalcule,        id=lienreservationelement_data.id,        concerne_id=lienreservationelement_data.concerne,        Cible_id=lienreservationelement_data.Cible        )

    database.add(db_lienreservationelement)
    database.commit()
    database.refresh(db_lienreservationelement)




    return db_lienreservationelement


@app.post("/lienreservationelement/bulk/", response_model=None, tags=["LienReservationElement"])
async def bulk_create_lienreservationelement(items: list[LienReservationElementCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple LienReservationElement entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.concerne:
                raise ValueError("Reservation ID is required")
            if not item_data.Cible:
                raise ValueError("ElementCentre ID is required")

            db_lienreservationelement = LienReservationElement(
                coutCalcule=item_data.coutCalcule,                id=item_data.id,                concerne_id=item_data.concerne,                Cible_id=item_data.Cible            )
            database.add(db_lienreservationelement)
            database.flush()  # Get ID without committing
            created_items.append(db_lienreservationelement.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} LienReservationElement entities"
    }


@app.delete("/lienreservationelement/bulk/", response_model=None, tags=["LienReservationElement"])
async def bulk_delete_lienreservationelement(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple LienReservationElement entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == item_id).first()
        if db_lienreservationelement:
            database.delete(db_lienreservationelement)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} LienReservationElement entities"
    }

@app.put("/lienreservationelement/{lienreservationelement_id}/", response_model=None, tags=["LienReservationElement"])
async def update_lienreservationelement(lienreservationelement_id: int, lienreservationelement_data: LienReservationElementCreate, database: Session = Depends(get_db)) -> LienReservationElement:
    db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
    if db_lienreservationelement is None:
        raise HTTPException(status_code=404, detail="LienReservationElement not found")

    setattr(db_lienreservationelement, 'coutCalcule', lienreservationelement_data.coutCalcule)
    setattr(db_lienreservationelement, 'id', lienreservationelement_data.id)
    if lienreservationelement_data.concerne is not None:
        db_concerne = database.query(Reservation).filter(Reservation.id == lienreservationelement_data.concerne).first()
        if not db_concerne:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_lienreservationelement, 'concerne_id', lienreservationelement_data.concerne)
    if lienreservationelement_data.Cible is not None:
        db_Cible = database.query(ElementCentre).filter(ElementCentre.id == lienreservationelement_data.Cible).first()
        if not db_Cible:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_lienreservationelement, 'Cible_id', lienreservationelement_data.Cible)
    database.commit()
    database.refresh(db_lienreservationelement)

    return db_lienreservationelement


@app.delete("/lienreservationelement/{lienreservationelement_id}/", response_model=None, tags=["LienReservationElement"])
async def delete_lienreservationelement(lienreservationelement_id: int, database: Session = Depends(get_db)):
    db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
    if db_lienreservationelement is None:
        raise HTTPException(status_code=404, detail="LienReservationElement not found")
    database.delete(db_lienreservationelement)
    database.commit()
    return db_lienreservationelement



############################################
#   LienReservationElement Method Endpoints
############################################




@app.post("/lienreservationelement/{lienreservationelement_id}/methods/calculerCoutLien/", response_model=None, tags=["LienReservationElement Methods"])
async def execute_lienreservationelement_calculerCoutLien(
    lienreservationelement_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCoutLien method on a LienReservationElement instance.

    Parameters:
    - duree: Any    """
    # Retrieve the entity from the database
    _lienreservationelement_object = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
    if _lienreservationelement_object is None:
        raise HTTPException(status_code=404, detail="LienReservationElement not found")

    # Prepare method parameters
    duree = params.get('duree')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_lienreservationelement_object):
            """Calcule le coût de location de la salle (Simplifié)."""
            element = await get_elementcentre(_lienreservationelement_object.cible)
            # En vrai, on appellerait la méthode getPrixPourDate des Tarifs de l'élément
            cout = 100.0 * duree # Base forfaitaire pour l'exemple
            await update_lienreservationelement(_lienreservationelement_object.id, LienReservationElementCreate(coutCalcule=cout))
            return cout

        result = await wrapper(_lienreservationelement_object)
        # Commit DB
        database.commit()
        database.refresh(_lienreservationelement_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "lienreservationelement_id": lienreservationelement_id,
            "method": "calculerCoutLien",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Prestation functions
#
############################################

@app.get("/prestation/", response_model=None, tags=["Prestation"])
def get_all_prestation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Prestation)
        prestation_list = query.all()

        # Serialize with relationships included
        result = []
        for prestation_item in prestation_list:
            item_dict = prestation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            lienreservationprestation_list = database.query(LienReservationPrestation).filter(LienReservationPrestation.prestation_id == prestation_item.id).all()
            item_dict['lienreservationprestation'] = []
            for lienreservationprestation_obj in lienreservationprestation_list:
                lienreservationprestation_dict = lienreservationprestation_obj.__dict__.copy()
                lienreservationprestation_dict.pop('_sa_instance_state', None)
                item_dict['lienreservationprestation'].append(lienreservationprestation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Prestation).all()


@app.get("/prestation/count/", response_model=None, tags=["Prestation"])
def get_count_prestation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Prestation entities"""
    count = database.query(Prestation).count()
    return {"count": count}


@app.get("/prestation/paginated/", response_model=None, tags=["Prestation"])
def get_paginated_prestation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Prestation entities"""
    total = database.query(Prestation).count()
    prestation_list = database.query(Prestation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": prestation_list
        }

    result = []
    for prestation_item in prestation_list:
        lienreservationprestation_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.prestation_id == prestation_item.id).all()
        item_data = {
            "prestation": prestation_item,
            "lienreservationprestation_ids": [x[0] for x in lienreservationprestation_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/prestation/search/", response_model=None, tags=["Prestation"])
def search_prestation(
    database: Session = Depends(get_db)
) -> list:
    """Search Prestation entities by attributes"""
    query = database.query(Prestation)


    results = query.all()
    return results


@app.get("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def get_prestation(prestation_id: int, database: Session = Depends(get_db)) -> Prestation:
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    lienreservationprestation_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.prestation_id == db_prestation.id).all()
    response_data = {
        "prestation": db_prestation,
        "lienreservationprestation_ids": [x[0] for x in lienreservationprestation_ids]}
    return response_data



@app.post("/prestation/", response_model=None, tags=["Prestation"])
async def create_prestation(prestation_data: PrestationCreate, database: Session = Depends(get_db)) -> Prestation:


    db_prestation = Prestation(
        type=prestation_data.type.value,        prixUnitaireBase=prestation_data.prixUnitaireBase,        nom=prestation_data.nom,        description=prestation_data.description,        id=prestation_data.id,        maxParticipants=prestation_data.maxParticipants        )

    database.add(db_prestation)
    database.commit()
    database.refresh(db_prestation)

    if prestation_data.lienreservationprestation:
        # Validate that all LienReservationPrestation IDs exist
        for lienreservationprestation_id in prestation_data.lienreservationprestation:
            db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
            if not db_lienreservationprestation:
                raise HTTPException(status_code=400, detail=f"LienReservationPrestation with id {lienreservationprestation_id} not found")

        # Update the related entities with the new foreign key
        database.query(LienReservationPrestation).filter(LienReservationPrestation.id.in_(prestation_data.lienreservationprestation)).update(
            {LienReservationPrestation.prestation_id: db_prestation.id}, synchronize_session=False
        )
        database.commit()



    lienreservationprestation_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.prestation_id == db_prestation.id).all()
    response_data = {
        "prestation": db_prestation,
        "lienreservationprestation_ids": [x[0] for x in lienreservationprestation_ids]    }
    return response_data


@app.post("/prestation/bulk/", response_model=None, tags=["Prestation"])
async def bulk_create_prestation(items: list[PrestationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Prestation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_prestation = Prestation(
                type=item_data.type.value,                prixUnitaireBase=item_data.prixUnitaireBase,                nom=item_data.nom,                description=item_data.description,                id=item_data.id,                maxParticipants=item_data.maxParticipants            )
            database.add(db_prestation)
            database.flush()  # Get ID without committing
            created_items.append(db_prestation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Prestation entities"
    }


@app.delete("/prestation/bulk/", response_model=None, tags=["Prestation"])
async def bulk_delete_prestation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Prestation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prestation = database.query(Prestation).filter(Prestation.id == item_id).first()
        if db_prestation:
            database.delete(db_prestation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Prestation entities"
    }

@app.put("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def update_prestation(prestation_id: int, prestation_data: PrestationCreate, database: Session = Depends(get_db)) -> Prestation:
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    setattr(db_prestation, 'type', prestation_data.type.value)
    setattr(db_prestation, 'prixUnitaireBase', prestation_data.prixUnitaireBase)
    setattr(db_prestation, 'nom', prestation_data.nom)
    setattr(db_prestation, 'description', prestation_data.description)
    setattr(db_prestation, 'id', prestation_data.id)
    setattr(db_prestation, 'maxParticipants', prestation_data.maxParticipants)
    if prestation_data.lienreservationprestation is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LienReservationPrestation).filter(LienReservationPrestation.prestation_id == db_prestation.id).update(
            {LienReservationPrestation.prestation_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if prestation_data.lienreservationprestation:
            # Validate that all IDs exist
            for lienreservationprestation_id in prestation_data.lienreservationprestation:
                db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
                if not db_lienreservationprestation:
                    raise HTTPException(status_code=400, detail=f"LienReservationPrestation with id {lienreservationprestation_id} not found")

            # Update the related entities with the new foreign key
            database.query(LienReservationPrestation).filter(LienReservationPrestation.id.in_(prestation_data.lienreservationprestation)).update(
                {LienReservationPrestation.prestation_id: db_prestation.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_prestation)

    lienreservationprestation_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.prestation_id == db_prestation.id).all()
    response_data = {
        "prestation": db_prestation,
        "lienreservationprestation_ids": [x[0] for x in lienreservationprestation_ids]    }
    return response_data


@app.delete("/prestation/{prestation_id}/", response_model=None, tags=["Prestation"])
async def delete_prestation(prestation_id: int, database: Session = Depends(get_db)):
    db_prestation = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="Prestation not found")
    database.delete(db_prestation)
    database.commit()
    return db_prestation



############################################
#   Prestation Method Endpoints
############################################




@app.post("/prestation/{prestation_id}/methods/validerCapacite/", response_model=None, tags=["Prestation Methods"])
async def execute_prestation_validerCapacite(
    prestation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the validerCapacite method on a Prestation instance.

    Parameters:
    - participants: Any    """
    # Retrieve the entity from the database
    _prestation_object = database.query(Prestation).filter(Prestation.id == prestation_id).first()
    if _prestation_object is None:
        raise HTTPException(status_code=404, detail="Prestation not found")

    # Prepare method parameters
    participants = params.get('participants')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_prestation_object):
            """Valide si la prestation peut gérer autant de personnes."""
            if _prestation_object.type == "GLOBALE":
                return True # Pas de limite stricte si globale
            return participants <= _prestation_object.maxParticipants


        result = await wrapper(_prestation_object)
        # Commit DB
        database.commit()
        database.refresh(_prestation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "prestation_id": prestation_id,
            "method": "validerCapacite",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Materiel functions
#
############################################

@app.get("/materiel/", response_model=None, tags=["Materiel"])
def get_all_materiel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Materiel)
        materiel_list = query.all()

        # Serialize with relationships included
        result = []
        for materiel_item in materiel_list:
            item_dict = materiel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            lienreservationmateriel_list = database.query(LienReservationMateriel).filter(LienReservationMateriel.materiel_id == materiel_item.id).all()
            item_dict['lienreservationmateriel_1'] = []
            for lienreservationmateriel_obj in lienreservationmateriel_list:
                lienreservationmateriel_dict = lienreservationmateriel_obj.__dict__.copy()
                lienreservationmateriel_dict.pop('_sa_instance_state', None)
                item_dict['lienreservationmateriel_1'].append(lienreservationmateriel_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Materiel).all()


@app.get("/materiel/count/", response_model=None, tags=["Materiel"])
def get_count_materiel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Materiel entities"""
    count = database.query(Materiel).count()
    return {"count": count}


@app.get("/materiel/paginated/", response_model=None, tags=["Materiel"])
def get_paginated_materiel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Materiel entities"""
    total = database.query(Materiel).count()
    materiel_list = database.query(Materiel).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": materiel_list
        }

    result = []
    for materiel_item in materiel_list:
        lienreservationmateriel_1_ids = database.query(LienReservationMateriel.id).filter(LienReservationMateriel.materiel_id == materiel_item.id).all()
        item_data = {
            "materiel": materiel_item,
            "lienreservationmateriel_1_ids": [x[0] for x in lienreservationmateriel_1_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/materiel/search/", response_model=None, tags=["Materiel"])
def search_materiel(
    database: Session = Depends(get_db)
) -> list:
    """Search Materiel entities by attributes"""
    query = database.query(Materiel)


    results = query.all()
    return results


@app.get("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def get_materiel(materiel_id: int, database: Session = Depends(get_db)) -> Materiel:
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    lienreservationmateriel_1_ids = database.query(LienReservationMateriel.id).filter(LienReservationMateriel.materiel_id == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "lienreservationmateriel_1_ids": [x[0] for x in lienreservationmateriel_1_ids]}
    return response_data



@app.post("/materiel/", response_model=None, tags=["Materiel"])
async def create_materiel(materiel_data: MaterielCreate, database: Session = Depends(get_db)) -> Materiel:


    db_materiel = Materiel(
        nom=materiel_data.nom,        id=materiel_data.id,        prixJournalierBase=materiel_data.prixJournalierBase,        description=materiel_data.description,        stockTotal=materiel_data.stockTotal        )

    database.add(db_materiel)
    database.commit()
    database.refresh(db_materiel)

    if materiel_data.lienreservationmateriel_1:
        # Validate that all LienReservationMateriel IDs exist
        for lienreservationmateriel_id in materiel_data.lienreservationmateriel_1:
            db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == lienreservationmateriel_id).first()
            if not db_lienreservationmateriel:
                raise HTTPException(status_code=400, detail=f"LienReservationMateriel with id {lienreservationmateriel_id} not found")

        # Update the related entities with the new foreign key
        database.query(LienReservationMateriel).filter(LienReservationMateriel.id.in_(materiel_data.lienreservationmateriel_1)).update(
            {LienReservationMateriel.materiel_id: db_materiel.id}, synchronize_session=False
        )
        database.commit()



    lienreservationmateriel_1_ids = database.query(LienReservationMateriel.id).filter(LienReservationMateriel.materiel_id == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "lienreservationmateriel_1_ids": [x[0] for x in lienreservationmateriel_1_ids]    }
    return response_data


@app.post("/materiel/bulk/", response_model=None, tags=["Materiel"])
async def bulk_create_materiel(items: list[MaterielCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Materiel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_materiel = Materiel(
                nom=item_data.nom,                id=item_data.id,                prixJournalierBase=item_data.prixJournalierBase,                description=item_data.description,                stockTotal=item_data.stockTotal            )
            database.add(db_materiel)
            database.flush()  # Get ID without committing
            created_items.append(db_materiel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Materiel entities"
    }


@app.delete("/materiel/bulk/", response_model=None, tags=["Materiel"])
async def bulk_delete_materiel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Materiel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_materiel = database.query(Materiel).filter(Materiel.id == item_id).first()
        if db_materiel:
            database.delete(db_materiel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Materiel entities"
    }

@app.put("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def update_materiel(materiel_id: int, materiel_data: MaterielCreate, database: Session = Depends(get_db)) -> Materiel:
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    setattr(db_materiel, 'nom', materiel_data.nom)
    setattr(db_materiel, 'id', materiel_data.id)
    setattr(db_materiel, 'prixJournalierBase', materiel_data.prixJournalierBase)
    setattr(db_materiel, 'description', materiel_data.description)
    setattr(db_materiel, 'stockTotal', materiel_data.stockTotal)
    if materiel_data.lienreservationmateriel_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LienReservationMateriel).filter(LienReservationMateriel.materiel_id == db_materiel.id).update(
            {LienReservationMateriel.materiel_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if materiel_data.lienreservationmateriel_1:
            # Validate that all IDs exist
            for lienreservationmateriel_id in materiel_data.lienreservationmateriel_1:
                db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == lienreservationmateriel_id).first()
                if not db_lienreservationmateriel:
                    raise HTTPException(status_code=400, detail=f"LienReservationMateriel with id {lienreservationmateriel_id} not found")

            # Update the related entities with the new foreign key
            database.query(LienReservationMateriel).filter(LienReservationMateriel.id.in_(materiel_data.lienreservationmateriel_1)).update(
                {LienReservationMateriel.materiel_id: db_materiel.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_materiel)

    lienreservationmateriel_1_ids = database.query(LienReservationMateriel.id).filter(LienReservationMateriel.materiel_id == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "lienreservationmateriel_1_ids": [x[0] for x in lienreservationmateriel_1_ids]    }
    return response_data


@app.delete("/materiel/{materiel_id}/", response_model=None, tags=["Materiel"])
async def delete_materiel(materiel_id: int, database: Session = Depends(get_db)):
    db_materiel = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="Materiel not found")
    database.delete(db_materiel)
    database.commit()
    return db_materiel



############################################
#   Materiel Method Endpoints
############################################




@app.post("/materiel/{materiel_id}/methods/verifierDispoStock/", response_model=None, tags=["Materiel Methods"])
async def execute_materiel_verifierDispoStock(
    materiel_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the verifierDispoStock method on a Materiel instance.

    Parameters:
    - quantiteDemandee: Any    - debut: Any    - fin: Any    """
    # Retrieve the entity from the database
    _materiel_object = database.query(Materiel).filter(Materiel.id == materiel_id).first()
    if _materiel_object is None:
        raise HTTPException(status_code=404, detail="Materiel not found")

    # Prepare method parameters
    quantiteDemandee = params.get('quantiteDemandee')
    debut = params.get('debut')
    fin = params.get('fin')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_materiel_object):
            """Vérifie qu'il y a assez de stock disponible."""
            # Logique simplifiée : vérifie juste contre le stock total
            if quantiteDemandee <= _materiel_object.stockTotal:
                return True
            return False

        result = await wrapper(_materiel_object)
        # Commit DB
        database.commit()
        database.refresh(_materiel_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "materiel_id": materiel_id,
            "method": "verifierDispoStock",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Reservation functions
#
############################################

@app.get("/reservation/", response_model=None, tags=["Reservation"])
def get_all_reservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Reservation)
        query = query.options(joinedload(Reservation.lienreservationmateriel))
        reservation_list = query.all()

        # Serialize with relationships included
        result = []
        for reservation_item in reservation_list:
            item_dict = reservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reservation_item.lienreservationmateriel:
                related_obj = reservation_item.lienreservationmateriel
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['lienreservationmateriel'] = related_dict
            else:
                item_dict['lienreservationmateriel'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            lienreservationelement_list = database.query(LienReservationElement).filter(LienReservationElement.concerne_id == reservation_item.id).all()
            item_dict['lienreservationelement'] = []
            for lienreservationelement_obj in lienreservationelement_list:
                lienreservationelement_dict = lienreservationelement_obj.__dict__.copy()
                lienreservationelement_dict.pop('_sa_instance_state', None)
                item_dict['lienreservationelement'].append(lienreservationelement_dict)
            lienreservationprestation_list = database.query(LienReservationPrestation).filter(LienReservationPrestation.inclut_id == reservation_item.id).all()
            item_dict['lienreservationprestation_1'] = []
            for lienreservationprestation_obj in lienreservationprestation_list:
                lienreservationprestation_dict = lienreservationprestation_obj.__dict__.copy()
                lienreservationprestation_dict.pop('_sa_instance_state', None)
                item_dict['lienreservationprestation_1'].append(lienreservationprestation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Reservation).all()


@app.get("/reservation/count/", response_model=None, tags=["Reservation"])
def get_count_reservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Reservation entities"""
    count = database.query(Reservation).count()
    return {"count": count}


@app.get("/reservation/paginated/", response_model=None, tags=["Reservation"])
def get_paginated_reservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Reservation entities"""
    total = database.query(Reservation).count()
    reservation_list = database.query(Reservation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": reservation_list
        }

    result = []
    for reservation_item in reservation_list:
        lienreservationelement_ids = database.query(LienReservationElement.id).filter(LienReservationElement.concerne_id == reservation_item.id).all()
        lienreservationprestation_1_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.inclut_id == reservation_item.id).all()
        item_data = {
            "reservation": reservation_item,
            "lienreservationelement_ids": [x[0] for x in lienreservationelement_ids],            "lienreservationprestation_1_ids": [x[0] for x in lienreservationprestation_1_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/reservation/search/", response_model=None, tags=["Reservation"])
def search_reservation(
    database: Session = Depends(get_db)
) -> list:
    """Search Reservation entities by attributes"""
    query = database.query(Reservation)


    results = query.all()
    return results


@app.get("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def get_reservation(reservation_id: int, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    lienreservationelement_ids = database.query(LienReservationElement.id).filter(LienReservationElement.concerne_id == db_reservation.id).all()
    lienreservationprestation_1_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.inclut_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "lienreservationelement_ids": [x[0] for x in lienreservationelement_ids],        "lienreservationprestation_1_ids": [x[0] for x in lienreservationprestation_1_ids]}
    return response_data



@app.post("/reservation/", response_model=None, tags=["Reservation"])
async def create_reservation(reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:

    if reservation_data.lienreservationmateriel is not None:
        db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == reservation_data.lienreservationmateriel).first()
        if not db_lienreservationmateriel:
            raise HTTPException(status_code=400, detail="LienReservationMateriel not found")
    else:
        raise HTTPException(status_code=400, detail="LienReservationMateriel ID is required")

    db_reservation = Reservation(
        telephoneContact=reservation_data.telephoneContact,        coutTotalFinal=reservation_data.coutTotalFinal,        delaiConfirmationJours=reservation_data.delaiConfirmationJours,        id=reservation_data.id,        statut=reservation_data.statut.value,        emailReferent=reservation_data.emailReferent,        dateDebut=reservation_data.dateDebut,        description=reservation_data.description,        nomContact=reservation_data.nomContact,        dateFin=reservation_data.dateFin,        nomEvenement=reservation_data.nomEvenement,        participantsPrevus=reservation_data.participantsPrevus,        lienreservationmateriel_id=reservation_data.lienreservationmateriel        )

    database.add(db_reservation)
    database.commit()
    database.refresh(db_reservation)

    if reservation_data.lienreservationelement:
        # Validate that all LienReservationElement IDs exist
        for lienreservationelement_id in reservation_data.lienreservationelement:
            db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
            if not db_lienreservationelement:
                raise HTTPException(status_code=400, detail=f"LienReservationElement with id {lienreservationelement_id} not found")

        # Update the related entities with the new foreign key
        database.query(LienReservationElement).filter(LienReservationElement.id.in_(reservation_data.lienreservationelement)).update(
            {LienReservationElement.concerne_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()
    if reservation_data.lienreservationprestation_1:
        # Validate that all LienReservationPrestation IDs exist
        for lienreservationprestation_id in reservation_data.lienreservationprestation_1:
            db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
            if not db_lienreservationprestation:
                raise HTTPException(status_code=400, detail=f"LienReservationPrestation with id {lienreservationprestation_id} not found")

        # Update the related entities with the new foreign key
        database.query(LienReservationPrestation).filter(LienReservationPrestation.id.in_(reservation_data.lienreservationprestation_1)).update(
            {LienReservationPrestation.inclut_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()



    lienreservationelement_ids = database.query(LienReservationElement.id).filter(LienReservationElement.concerne_id == db_reservation.id).all()
    lienreservationprestation_1_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.inclut_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "lienreservationelement_ids": [x[0] for x in lienreservationelement_ids],        "lienreservationprestation_1_ids": [x[0] for x in lienreservationprestation_1_ids]    }
    return response_data


@app.post("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_create_reservation(items: list[ReservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Reservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.lienreservationmateriel:
                raise ValueError("LienReservationMateriel ID is required")

            db_reservation = Reservation(
                telephoneContact=item_data.telephoneContact,                coutTotalFinal=item_data.coutTotalFinal,                delaiConfirmationJours=item_data.delaiConfirmationJours,                id=item_data.id,                statut=item_data.statut.value,                emailReferent=item_data.emailReferent,                dateDebut=item_data.dateDebut,                description=item_data.description,                nomContact=item_data.nomContact,                dateFin=item_data.dateFin,                nomEvenement=item_data.nomEvenement,                participantsPrevus=item_data.participantsPrevus,                lienreservationmateriel_id=item_data.lienreservationmateriel            )
            database.add(db_reservation)
            database.flush()  # Get ID without committing
            created_items.append(db_reservation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Reservation entities"
    }


@app.delete("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_delete_reservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Reservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == item_id).first()
        if db_reservation:
            database.delete(db_reservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Reservation entities"
    }

@app.put("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def update_reservation(reservation_id: int, reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    setattr(db_reservation, 'telephoneContact', reservation_data.telephoneContact)
    setattr(db_reservation, 'coutTotalFinal', reservation_data.coutTotalFinal)
    setattr(db_reservation, 'delaiConfirmationJours', reservation_data.delaiConfirmationJours)
    setattr(db_reservation, 'id', reservation_data.id)
    setattr(db_reservation, 'statut', reservation_data.statut.value)
    setattr(db_reservation, 'emailReferent', reservation_data.emailReferent)
    setattr(db_reservation, 'dateDebut', reservation_data.dateDebut)
    setattr(db_reservation, 'description', reservation_data.description)
    setattr(db_reservation, 'nomContact', reservation_data.nomContact)
    setattr(db_reservation, 'dateFin', reservation_data.dateFin)
    setattr(db_reservation, 'nomEvenement', reservation_data.nomEvenement)
    setattr(db_reservation, 'participantsPrevus', reservation_data.participantsPrevus)
    if reservation_data.lienreservationmateriel is not None:
        db_lienreservationmateriel = database.query(LienReservationMateriel).filter(LienReservationMateriel.id == reservation_data.lienreservationmateriel).first()
        if not db_lienreservationmateriel:
            raise HTTPException(status_code=400, detail="LienReservationMateriel not found")
        setattr(db_reservation, 'lienreservationmateriel_id', reservation_data.lienreservationmateriel)
    if reservation_data.lienreservationelement is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LienReservationElement).filter(LienReservationElement.concerne_id == db_reservation.id).update(
            {LienReservationElement.concerne_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.lienreservationelement:
            # Validate that all IDs exist
            for lienreservationelement_id in reservation_data.lienreservationelement:
                db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
                if not db_lienreservationelement:
                    raise HTTPException(status_code=400, detail=f"LienReservationElement with id {lienreservationelement_id} not found")

            # Update the related entities with the new foreign key
            database.query(LienReservationElement).filter(LienReservationElement.id.in_(reservation_data.lienreservationelement)).update(
                {LienReservationElement.concerne_id: db_reservation.id}, synchronize_session=False
            )
    if reservation_data.lienreservationprestation_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LienReservationPrestation).filter(LienReservationPrestation.inclut_id == db_reservation.id).update(
            {LienReservationPrestation.inclut_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.lienreservationprestation_1:
            # Validate that all IDs exist
            for lienreservationprestation_id in reservation_data.lienreservationprestation_1:
                db_lienreservationprestation = database.query(LienReservationPrestation).filter(LienReservationPrestation.id == lienreservationprestation_id).first()
                if not db_lienreservationprestation:
                    raise HTTPException(status_code=400, detail=f"LienReservationPrestation with id {lienreservationprestation_id} not found")

            # Update the related entities with the new foreign key
            database.query(LienReservationPrestation).filter(LienReservationPrestation.id.in_(reservation_data.lienreservationprestation_1)).update(
                {LienReservationPrestation.inclut_id: db_reservation.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_reservation)

    lienreservationelement_ids = database.query(LienReservationElement.id).filter(LienReservationElement.concerne_id == db_reservation.id).all()
    lienreservationprestation_1_ids = database.query(LienReservationPrestation.id).filter(LienReservationPrestation.inclut_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "lienreservationelement_ids": [x[0] for x in lienreservationelement_ids],        "lienreservationprestation_1_ids": [x[0] for x in lienreservationprestation_1_ids]    }
    return response_data


@app.delete("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def delete_reservation(reservation_id: int, database: Session = Depends(get_db)):
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    database.delete(db_reservation)
    database.commit()
    return db_reservation



############################################
#   Reservation Method Endpoints
############################################




@app.post("/reservation/{reservation_id}/methods/annuler/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_annuler(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the annuler method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Fait passer l'état à ANNULEE (Pattern State)."""
            if _reservation_object.statut == "PASSEE":
                raise Exception("Impossible d'annuler une réservation déjà passée.")
                
            resultat = await update_reservation(_reservation_object.id, ReservationCreate(statut="ANNULEE"))
            return resultat


        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "annuler",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/verifierDelaiConfirmation/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_verifierDelaiConfirmation(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the verifierDelaiConfirmation method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Vérifie si le délai autorisé pour confirmer est dépassé."""
            # La logique réelle comparerait la date d'aujourd'hui avec (dateCreation + delai)
            return True

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "verifierDelaiConfirmation",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/calculerCoutTotal/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_calculerCoutTotal(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCoutTotal method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Consolide le coût total à partir des tables de pont."""
            total = 0.0
            
            # 1. Elements
            liens_elem = await get_lienreservationelement(_reservation_object.contient)
            for lien in liens_elem:
                total += lien.coutCalcule
                
            # 2. Materiel
            liens_mat = await get_lienreservationmateriel(_reservation_object.inclut)
            for lien in liens_mat:
                total += lien.coutCalcule
                
            # 3. Prestation
            liens_pres = await get_lienreservationprestation(_reservation_object.inclut)
            for lien in liens_pres:
                total += lien.coutCalcule
                
            # Sauvegarde du nouveau total
            await update_reservation(_reservation_object.id, ReservationCreate(coutTotalFinal=total))
            return total

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "calculerCoutTotal",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/modifier/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_modifier(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the modifier method on a Reservation instance.

    Parameters:
    - nouvellesDates: Any    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters
    nouvellesDates = params.get('nouvellesDates')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Autorise la modification uniquement si l'événement n'a pas commencé."""
            if _reservation_object.statut in ["PASSEE", "ANNULEE"]:
                raise Exception("Réservation non modifiable dans son état actuel.")
                
            # Ici, mise à jour des dates
            resultat = await update_reservation(_reservation_object.id, ReservationCreate(dateDebut=nouvellesDates))
            return resultat

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "modifier",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/confirmer/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_confirmer(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the confirmer method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """Fait passer l'état à CONFIRMEE (Pattern State)."""
            if _reservation_object.statut != "EN_ATTENTE":
                raise Exception("Seule une réservation EN_ATTENTE peut être confirmée.")
            
            resultat = await update_reservation(_reservation_object.id, ReservationCreate(statut="CONFIRMEE"))
            return resultat

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "confirmer",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   CentreCongres functions
#
############################################

@app.get("/centrecongres/", response_model=None, tags=["CentreCongres"])
def get_all_centrecongres(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(CentreCongres)
        centrecongres_list = query.all()

        # Serialize with relationships included
        result = []
        for centrecongres_item in centrecongres_list:
            item_dict = centrecongres_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            elementcentre_list = database.query(ElementCentre).filter(ElementCentre.compose_id == centrecongres_item.id).all()
            item_dict['elementcentre'] = []
            for elementcentre_obj in elementcentre_list:
                elementcentre_dict = elementcentre_obj.__dict__.copy()
                elementcentre_dict.pop('_sa_instance_state', None)
                item_dict['elementcentre'].append(elementcentre_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(CentreCongres).all()


@app.get("/centrecongres/count/", response_model=None, tags=["CentreCongres"])
def get_count_centrecongres(database: Session = Depends(get_db)) -> dict:
    """Get the total count of CentreCongres entities"""
    count = database.query(CentreCongres).count()
    return {"count": count}


@app.get("/centrecongres/paginated/", response_model=None, tags=["CentreCongres"])
def get_paginated_centrecongres(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of CentreCongres entities"""
    total = database.query(CentreCongres).count()
    centrecongres_list = database.query(CentreCongres).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": centrecongres_list
        }

    result = []
    for centrecongres_item in centrecongres_list:
        elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.compose_id == centrecongres_item.id).all()
        item_data = {
            "centrecongres": centrecongres_item,
            "elementcentre_ids": [x[0] for x in elementcentre_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/centrecongres/search/", response_model=None, tags=["CentreCongres"])
def search_centrecongres(
    database: Session = Depends(get_db)
) -> list:
    """Search CentreCongres entities by attributes"""
    query = database.query(CentreCongres)


    results = query.all()
    return results


@app.get("/centrecongres/{centrecongres_id}/", response_model=None, tags=["CentreCongres"])
async def get_centrecongres(centrecongres_id: int, database: Session = Depends(get_db)) -> CentreCongres:
    db_centrecongres = database.query(CentreCongres).filter(CentreCongres.id == centrecongres_id).first()
    if db_centrecongres is None:
        raise HTTPException(status_code=404, detail="CentreCongres not found")

    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.compose_id == db_centrecongres.id).all()
    response_data = {
        "centrecongres": db_centrecongres,
        "elementcentre_ids": [x[0] for x in elementcentre_ids]}
    return response_data



@app.post("/centrecongres/", response_model=None, tags=["CentreCongres"])
async def create_centrecongres(centrecongres_data: CentreCongresCreate, database: Session = Depends(get_db)) -> CentreCongres:


    db_centrecongres = CentreCongres(
        ville=centrecongres_data.ville,        nom=centrecongres_data.nom,        telephoneContact=centrecongres_data.telephoneContact,        id=centrecongres_data.id,        adresse=centrecongres_data.adresse,        emailContact=centrecongres_data.emailContact        )

    database.add(db_centrecongres)
    database.commit()
    database.refresh(db_centrecongres)

    if centrecongres_data.elementcentre:
        # Validate that all ElementCentre IDs exist
        for elementcentre_id in centrecongres_data.elementcentre:
            db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
            if not db_elementcentre:
                raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

        # Update the related entities with the new foreign key
        database.query(ElementCentre).filter(ElementCentre.id.in_(centrecongres_data.elementcentre)).update(
            {ElementCentre.compose_id: db_centrecongres.id}, synchronize_session=False
        )
        database.commit()



    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.compose_id == db_centrecongres.id).all()
    response_data = {
        "centrecongres": db_centrecongres,
        "elementcentre_ids": [x[0] for x in elementcentre_ids]    }
    return response_data


@app.post("/centrecongres/bulk/", response_model=None, tags=["CentreCongres"])
async def bulk_create_centrecongres(items: list[CentreCongresCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple CentreCongres entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_centrecongres = CentreCongres(
                ville=item_data.ville,                nom=item_data.nom,                telephoneContact=item_data.telephoneContact,                id=item_data.id,                adresse=item_data.adresse,                emailContact=item_data.emailContact            )
            database.add(db_centrecongres)
            database.flush()  # Get ID without committing
            created_items.append(db_centrecongres.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} CentreCongres entities"
    }


@app.delete("/centrecongres/bulk/", response_model=None, tags=["CentreCongres"])
async def bulk_delete_centrecongres(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple CentreCongres entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_centrecongres = database.query(CentreCongres).filter(CentreCongres.id == item_id).first()
        if db_centrecongres:
            database.delete(db_centrecongres)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} CentreCongres entities"
    }

@app.put("/centrecongres/{centrecongres_id}/", response_model=None, tags=["CentreCongres"])
async def update_centrecongres(centrecongres_id: int, centrecongres_data: CentreCongresCreate, database: Session = Depends(get_db)) -> CentreCongres:
    db_centrecongres = database.query(CentreCongres).filter(CentreCongres.id == centrecongres_id).first()
    if db_centrecongres is None:
        raise HTTPException(status_code=404, detail="CentreCongres not found")

    setattr(db_centrecongres, 'ville', centrecongres_data.ville)
    setattr(db_centrecongres, 'nom', centrecongres_data.nom)
    setattr(db_centrecongres, 'telephoneContact', centrecongres_data.telephoneContact)
    setattr(db_centrecongres, 'id', centrecongres_data.id)
    setattr(db_centrecongres, 'adresse', centrecongres_data.adresse)
    setattr(db_centrecongres, 'emailContact', centrecongres_data.emailContact)
    if centrecongres_data.elementcentre is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ElementCentre).filter(ElementCentre.compose_id == db_centrecongres.id).update(
            {ElementCentre.compose_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if centrecongres_data.elementcentre:
            # Validate that all IDs exist
            for elementcentre_id in centrecongres_data.elementcentre:
                db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
                if not db_elementcentre:
                    raise HTTPException(status_code=400, detail=f"ElementCentre with id {elementcentre_id} not found")

            # Update the related entities with the new foreign key
            database.query(ElementCentre).filter(ElementCentre.id.in_(centrecongres_data.elementcentre)).update(
                {ElementCentre.compose_id: db_centrecongres.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_centrecongres)

    elementcentre_ids = database.query(ElementCentre.id).filter(ElementCentre.compose_id == db_centrecongres.id).all()
    response_data = {
        "centrecongres": db_centrecongres,
        "elementcentre_ids": [x[0] for x in elementcentre_ids]    }
    return response_data


@app.delete("/centrecongres/{centrecongres_id}/", response_model=None, tags=["CentreCongres"])
async def delete_centrecongres(centrecongres_id: int, database: Session = Depends(get_db)):
    db_centrecongres = database.query(CentreCongres).filter(CentreCongres.id == centrecongres_id).first()
    if db_centrecongres is None:
        raise HTTPException(status_code=404, detail="CentreCongres not found")
    database.delete(db_centrecongres)
    database.commit()
    return db_centrecongres



############################################
#   CentreCongres Method Endpoints
############################################




@app.post("/centrecongres/{centrecongres_id}/methods/getElementsDisponibles/", response_model=None, tags=["CentreCongres Methods"])
async def execute_centrecongres_getElementsDisponibles(
    centrecongres_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the getElementsDisponibles method on a CentreCongres instance.

    Parameters:
    - debut: Any    - fin: Any    """
    # Retrieve the entity from the database
    _centrecongres_object = database.query(CentreCongres).filter(CentreCongres.id == centrecongres_id).first()
    if _centrecongres_object is None:
        raise HTTPException(status_code=404, detail="CentreCongres not found")

    # Prepare method parameters
    debut = params.get('debut')
    fin = params.get('fin')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_centrecongres_object):
            """Retourne la liste des éléments disponibles pour une période donnée."""
            elements_du_centre = await get_elementcentre(_centrecongres_object.compose)
            elements_dispos = []
            
            for element in elements_du_centre:
                # Appel de la méthode estDisponible sur chaque ElementCentre
                params = {"debut": debut, "fin": fin}
                disponible = await execute_elementcentre_estdisponible(element.id, params)
                if disponible:
                    elements_dispos.append(element)
                    
            return elements_dispos

        result = await wrapper(_centrecongres_object)
        # Commit DB
        database.commit()
        database.refresh(_centrecongres_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "centrecongres_id": centrecongres_id,
            "method": "getElementsDisponibles",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/centrecongres/{centrecongres_id}/methods/genererStatistiques/", response_model=None, tags=["CentreCongres Methods"])
async def execute_centrecongres_genererStatistiques(
    centrecongres_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the genererStatistiques method on a CentreCongres instance.

    Parameters:
    - annee: Any    """
    # Retrieve the entity from the database
    _centrecongres_object = database.query(CentreCongres).filter(CentreCongres.id == centrecongres_id).first()
    if _centrecongres_object is None:
        raise HTTPException(status_code=404, detail="CentreCongres not found")

    # Prepare method parameters
    annee = params.get('annee')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_centrecongres_object):
            """Génère un résumé statistique du centre."""
            # Implémentation simplifiée : on pourrait itérer sur toutes les réservations
            # "PASSEE" pour calculer le CA réel.
            return f"Statistiques de l'année {annee} générées pour {_centrecongres_object.nom}."

        result = await wrapper(_centrecongres_object)
        # Commit DB
        database.commit()
        database.refresh(_centrecongres_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "centrecongres_id": centrecongres_id,
            "method": "genererStatistiques",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   TarifSaisonnier functions
#
############################################

@app.get("/tarifsaisonnier/", response_model=None, tags=["TarifSaisonnier"])
def get_all_tarifsaisonnier(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(TarifSaisonnier)
        query = query.options(joinedload(TarifSaisonnier.possede))
        tarifsaisonnier_list = query.all()

        # Serialize with relationships included
        result = []
        for tarifsaisonnier_item in tarifsaisonnier_list:
            item_dict = tarifsaisonnier_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if tarifsaisonnier_item.possede:
                related_obj = tarifsaisonnier_item.possede
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['possede'] = related_dict
            else:
                item_dict['possede'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(TarifSaisonnier).all()


@app.get("/tarifsaisonnier/count/", response_model=None, tags=["TarifSaisonnier"])
def get_count_tarifsaisonnier(database: Session = Depends(get_db)) -> dict:
    """Get the total count of TarifSaisonnier entities"""
    count = database.query(TarifSaisonnier).count()
    return {"count": count}


@app.get("/tarifsaisonnier/paginated/", response_model=None, tags=["TarifSaisonnier"])
def get_paginated_tarifsaisonnier(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of TarifSaisonnier entities"""
    total = database.query(TarifSaisonnier).count()
    tarifsaisonnier_list = database.query(TarifSaisonnier).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": tarifsaisonnier_list
    }


@app.get("/tarifsaisonnier/search/", response_model=None, tags=["TarifSaisonnier"])
def search_tarifsaisonnier(
    database: Session = Depends(get_db)
) -> list:
    """Search TarifSaisonnier entities by attributes"""
    query = database.query(TarifSaisonnier)


    results = query.all()
    return results


@app.get("/tarifsaisonnier/{tarifsaisonnier_id}/", response_model=None, tags=["TarifSaisonnier"])
async def get_tarifsaisonnier(tarifsaisonnier_id: int, database: Session = Depends(get_db)) -> TarifSaisonnier:
    db_tarifsaisonnier = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == tarifsaisonnier_id).first()
    if db_tarifsaisonnier is None:
        raise HTTPException(status_code=404, detail="TarifSaisonnier not found")

    response_data = {
        "tarifsaisonnier": db_tarifsaisonnier,
}
    return response_data



@app.post("/tarifsaisonnier/", response_model=None, tags=["TarifSaisonnier"])
async def create_tarifsaisonnier(tarifsaisonnier_data: TarifSaisonnierCreate, database: Session = Depends(get_db)) -> TarifSaisonnier:

    if tarifsaisonnier_data.possede is not None:
        db_possede = database.query(ElementCentre).filter(ElementCentre.id == tarifsaisonnier_data.possede).first()
        if not db_possede:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_tarifsaisonnier = TarifSaisonnier(
        saison=tarifsaisonnier_data.saison.value,        id=tarifsaisonnier_data.id,        prixJournalier=tarifsaisonnier_data.prixJournalier,        possede_id=tarifsaisonnier_data.possede        )

    database.add(db_tarifsaisonnier)
    database.commit()
    database.refresh(db_tarifsaisonnier)




    return db_tarifsaisonnier


@app.post("/tarifsaisonnier/bulk/", response_model=None, tags=["TarifSaisonnier"])
async def bulk_create_tarifsaisonnier(items: list[TarifSaisonnierCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple TarifSaisonnier entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.possede:
                raise ValueError("ElementCentre ID is required")

            db_tarifsaisonnier = TarifSaisonnier(
                saison=item_data.saison.value,                id=item_data.id,                prixJournalier=item_data.prixJournalier,                possede_id=item_data.possede            )
            database.add(db_tarifsaisonnier)
            database.flush()  # Get ID without committing
            created_items.append(db_tarifsaisonnier.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} TarifSaisonnier entities"
    }


@app.delete("/tarifsaisonnier/bulk/", response_model=None, tags=["TarifSaisonnier"])
async def bulk_delete_tarifsaisonnier(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple TarifSaisonnier entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tarifsaisonnier = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == item_id).first()
        if db_tarifsaisonnier:
            database.delete(db_tarifsaisonnier)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} TarifSaisonnier entities"
    }

@app.put("/tarifsaisonnier/{tarifsaisonnier_id}/", response_model=None, tags=["TarifSaisonnier"])
async def update_tarifsaisonnier(tarifsaisonnier_id: int, tarifsaisonnier_data: TarifSaisonnierCreate, database: Session = Depends(get_db)) -> TarifSaisonnier:
    db_tarifsaisonnier = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == tarifsaisonnier_id).first()
    if db_tarifsaisonnier is None:
        raise HTTPException(status_code=404, detail="TarifSaisonnier not found")

    setattr(db_tarifsaisonnier, 'saison', tarifsaisonnier_data.saison.value)
    setattr(db_tarifsaisonnier, 'id', tarifsaisonnier_data.id)
    setattr(db_tarifsaisonnier, 'prixJournalier', tarifsaisonnier_data.prixJournalier)
    if tarifsaisonnier_data.possede is not None:
        db_possede = database.query(ElementCentre).filter(ElementCentre.id == tarifsaisonnier_data.possede).first()
        if not db_possede:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_tarifsaisonnier, 'possede_id', tarifsaisonnier_data.possede)
    database.commit()
    database.refresh(db_tarifsaisonnier)

    return db_tarifsaisonnier


@app.delete("/tarifsaisonnier/{tarifsaisonnier_id}/", response_model=None, tags=["TarifSaisonnier"])
async def delete_tarifsaisonnier(tarifsaisonnier_id: int, database: Session = Depends(get_db)):
    db_tarifsaisonnier = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == tarifsaisonnier_id).first()
    if db_tarifsaisonnier is None:
        raise HTTPException(status_code=404, detail="TarifSaisonnier not found")
    database.delete(db_tarifsaisonnier)
    database.commit()
    return db_tarifsaisonnier



############################################
#   TarifSaisonnier Method Endpoints
############################################




@app.post("/tarifsaisonnier/{tarifsaisonnier_id}/methods/getPrixPourDate/", response_model=None, tags=["TarifSaisonnier Methods"])
async def execute_tarifsaisonnier_getPrixPourDate(
    tarifsaisonnier_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the getPrixPourDate method on a TarifSaisonnier instance.

    Parameters:
    - dateCible: Any    """
    # Retrieve the entity from the database
    _tarifsaisonnier_object = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == tarifsaisonnier_id).first()
    if _tarifsaisonnier_object is None:
        raise HTTPException(status_code=404, detail="TarifSaisonnier not found")

    # Prepare method parameters
    dateCible = params.get('dateCible')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_tarifsaisonnier_object):
            """Retourne le tarif applicable (simplifié ici au prix journalier de base)."""
            # La logique complexe déterminerait si la dateCible tombe dans cette saison
            return _tarifsaisonnier_object.prixJournalier

        result = await wrapper(_tarifsaisonnier_object)
        # Commit DB
        database.commit()
        database.refresh(_tarifsaisonnier_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "tarifsaisonnier_id": tarifsaisonnier_id,
            "method": "getPrixPourDate",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Indisponibilite functions
#
############################################

@app.get("/indisponibilite/", response_model=None, tags=["Indisponibilite"])
def get_all_indisponibilite(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Indisponibilite)
        query = query.options(joinedload(Indisponibilite.Subit))
        indisponibilite_list = query.all()

        # Serialize with relationships included
        result = []
        for indisponibilite_item in indisponibilite_list:
            item_dict = indisponibilite_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if indisponibilite_item.Subit:
                related_obj = indisponibilite_item.Subit
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['Subit'] = related_dict
            else:
                item_dict['Subit'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Indisponibilite).all()


@app.get("/indisponibilite/count/", response_model=None, tags=["Indisponibilite"])
def get_count_indisponibilite(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Indisponibilite entities"""
    count = database.query(Indisponibilite).count()
    return {"count": count}


@app.get("/indisponibilite/paginated/", response_model=None, tags=["Indisponibilite"])
def get_paginated_indisponibilite(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Indisponibilite entities"""
    total = database.query(Indisponibilite).count()
    indisponibilite_list = database.query(Indisponibilite).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": indisponibilite_list
    }


@app.get("/indisponibilite/search/", response_model=None, tags=["Indisponibilite"])
def search_indisponibilite(
    database: Session = Depends(get_db)
) -> list:
    """Search Indisponibilite entities by attributes"""
    query = database.query(Indisponibilite)


    results = query.all()
    return results


@app.get("/indisponibilite/{indisponibilite_id}/", response_model=None, tags=["Indisponibilite"])
async def get_indisponibilite(indisponibilite_id: int, database: Session = Depends(get_db)) -> Indisponibilite:
    db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if db_indisponibilite is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")

    response_data = {
        "indisponibilite": db_indisponibilite,
}
    return response_data



@app.post("/indisponibilite/", response_model=None, tags=["Indisponibilite"])
async def create_indisponibilite(indisponibilite_data: IndisponibiliteCreate, database: Session = Depends(get_db)) -> Indisponibilite:

    if indisponibilite_data.Subit is not None:
        db_Subit = database.query(ElementCentre).filter(ElementCentre.id == indisponibilite_data.Subit).first()
        if not db_Subit:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
    else:
        raise HTTPException(status_code=400, detail="ElementCentre ID is required")

    db_indisponibilite = Indisponibilite(
        dateDebut=indisponibilite_data.dateDebut,        remarques=indisponibilite_data.remarques,        id=indisponibilite_data.id,        dateFin=indisponibilite_data.dateFin,        motif=indisponibilite_data.motif.value,        Subit_id=indisponibilite_data.Subit        )

    database.add(db_indisponibilite)
    database.commit()
    database.refresh(db_indisponibilite)




    return db_indisponibilite


@app.post("/indisponibilite/bulk/", response_model=None, tags=["Indisponibilite"])
async def bulk_create_indisponibilite(items: list[IndisponibiliteCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Indisponibilite entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.Subit:
                raise ValueError("ElementCentre ID is required")

            db_indisponibilite = Indisponibilite(
                dateDebut=item_data.dateDebut,                remarques=item_data.remarques,                id=item_data.id,                dateFin=item_data.dateFin,                motif=item_data.motif.value,                Subit_id=item_data.Subit            )
            database.add(db_indisponibilite)
            database.flush()  # Get ID without committing
            created_items.append(db_indisponibilite.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Indisponibilite entities"
    }


@app.delete("/indisponibilite/bulk/", response_model=None, tags=["Indisponibilite"])
async def bulk_delete_indisponibilite(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Indisponibilite entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == item_id).first()
        if db_indisponibilite:
            database.delete(db_indisponibilite)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Indisponibilite entities"
    }

@app.put("/indisponibilite/{indisponibilite_id}/", response_model=None, tags=["Indisponibilite"])
async def update_indisponibilite(indisponibilite_id: int, indisponibilite_data: IndisponibiliteCreate, database: Session = Depends(get_db)) -> Indisponibilite:
    db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if db_indisponibilite is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")

    setattr(db_indisponibilite, 'dateDebut', indisponibilite_data.dateDebut)
    setattr(db_indisponibilite, 'remarques', indisponibilite_data.remarques)
    setattr(db_indisponibilite, 'id', indisponibilite_data.id)
    setattr(db_indisponibilite, 'dateFin', indisponibilite_data.dateFin)
    setattr(db_indisponibilite, 'motif', indisponibilite_data.motif.value)
    if indisponibilite_data.Subit is not None:
        db_Subit = database.query(ElementCentre).filter(ElementCentre.id == indisponibilite_data.Subit).first()
        if not db_Subit:
            raise HTTPException(status_code=400, detail="ElementCentre not found")
        setattr(db_indisponibilite, 'Subit_id', indisponibilite_data.Subit)
    database.commit()
    database.refresh(db_indisponibilite)

    return db_indisponibilite


@app.delete("/indisponibilite/{indisponibilite_id}/", response_model=None, tags=["Indisponibilite"])
async def delete_indisponibilite(indisponibilite_id: int, database: Session = Depends(get_db)):
    db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if db_indisponibilite is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")
    database.delete(db_indisponibilite)
    database.commit()
    return db_indisponibilite



############################################
#   Indisponibilite Method Endpoints
############################################




@app.post("/indisponibilite/{indisponibilite_id}/methods/estEnConflit/", response_model=None, tags=["Indisponibilite Methods"])
async def execute_indisponibilite_estEnConflit(
    indisponibilite_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the estEnConflit method on a Indisponibilite instance.

    Parameters:
    - debut: Any    - fin: Any    """
    # Retrieve the entity from the database
    _indisponibilite_object = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
    if _indisponibilite_object is None:
        raise HTTPException(status_code=404, detail="Indisponibilite not found")

    # Prepare method parameters
    debut = params.get('debut')
    fin = params.get('fin')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_indisponibilite_object):
            """Détecte un chevauchement de dates."""
            # Si la date de début demandée est avant la fin de l'indispo 
            # ET la date de fin demandée est après le début de l'indispo
            return (debut <= _indisponibilite_object.dateFin) and (fin >= _indisponibilite_object.dateDebut)

        result = await wrapper(_indisponibilite_object)
        # Commit DB
        database.commit()
        database.refresh(_indisponibilite_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "indisponibilite_id": indisponibilite_id,
            "method": "estEnConflit",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   ElementCentre functions
#
############################################

@app.get("/elementcentre/", response_model=None, tags=["ElementCentre"])
def get_all_elementcentre(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ElementCentre)
        query = query.options(joinedload(ElementCentre.compose))
        elementcentre_list = query.all()

        # Serialize with relationships included
        result = []
        for elementcentre_item in elementcentre_list:
            item_dict = elementcentre_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if elementcentre_item.compose:
                related_obj = elementcentre_item.compose
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['compose'] = related_dict
            else:
                item_dict['compose'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            indisponibilite_list = database.query(Indisponibilite).filter(Indisponibilite.Subit_id == elementcentre_item.id).all()
            item_dict['indisponibilite'] = []
            for indisponibilite_obj in indisponibilite_list:
                indisponibilite_dict = indisponibilite_obj.__dict__.copy()
                indisponibilite_dict.pop('_sa_instance_state', None)
                item_dict['indisponibilite'].append(indisponibilite_dict)
            lienreservationelement_list = database.query(LienReservationElement).filter(LienReservationElement.Cible_id == elementcentre_item.id).all()
            item_dict['lienreservationelement_1'] = []
            for lienreservationelement_obj in lienreservationelement_list:
                lienreservationelement_dict = lienreservationelement_obj.__dict__.copy()
                lienreservationelement_dict.pop('_sa_instance_state', None)
                item_dict['lienreservationelement_1'].append(lienreservationelement_dict)
            tarifsaisonnier_list = database.query(TarifSaisonnier).filter(TarifSaisonnier.possede_id == elementcentre_item.id).all()
            item_dict['tarifsaisonnier'] = []
            for tarifsaisonnier_obj in tarifsaisonnier_list:
                tarifsaisonnier_dict = tarifsaisonnier_obj.__dict__.copy()
                tarifsaisonnier_dict.pop('_sa_instance_state', None)
                item_dict['tarifsaisonnier'].append(tarifsaisonnier_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ElementCentre).all()


@app.get("/elementcentre/count/", response_model=None, tags=["ElementCentre"])
def get_count_elementcentre(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ElementCentre entities"""
    count = database.query(ElementCentre).count()
    return {"count": count}


@app.get("/elementcentre/paginated/", response_model=None, tags=["ElementCentre"])
def get_paginated_elementcentre(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ElementCentre entities"""
    total = database.query(ElementCentre).count()
    elementcentre_list = database.query(ElementCentre).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": elementcentre_list
        }

    result = []
    for elementcentre_item in elementcentre_list:
        indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.Subit_id == elementcentre_item.id).all()
        lienreservationelement_1_ids = database.query(LienReservationElement.id).filter(LienReservationElement.Cible_id == elementcentre_item.id).all()
        tarifsaisonnier_ids = database.query(TarifSaisonnier.id).filter(TarifSaisonnier.possede_id == elementcentre_item.id).all()
        item_data = {
            "elementcentre": elementcentre_item,
            "indisponibilite_ids": [x[0] for x in indisponibilite_ids],            "lienreservationelement_1_ids": [x[0] for x in lienreservationelement_1_ids],            "tarifsaisonnier_ids": [x[0] for x in tarifsaisonnier_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/elementcentre/search/", response_model=None, tags=["ElementCentre"])
def search_elementcentre(
    database: Session = Depends(get_db)
) -> list:
    """Search ElementCentre entities by attributes"""
    query = database.query(ElementCentre)


    results = query.all()
    return results


@app.get("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def get_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)) -> ElementCentre:
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.Subit_id == db_elementcentre.id).all()
    lienreservationelement_1_ids = database.query(LienReservationElement.id).filter(LienReservationElement.Cible_id == db_elementcentre.id).all()
    tarifsaisonnier_ids = database.query(TarifSaisonnier.id).filter(TarifSaisonnier.possede_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "indisponibilite_ids": [x[0] for x in indisponibilite_ids],        "lienreservationelement_1_ids": [x[0] for x in lienreservationelement_1_ids],        "tarifsaisonnier_ids": [x[0] for x in tarifsaisonnier_ids]}
    return response_data



@app.post("/elementcentre/", response_model=None, tags=["ElementCentre"])
async def create_elementcentre(elementcentre_data: ElementCentreCreate, database: Session = Depends(get_db)) -> ElementCentre:

    if elementcentre_data.compose is not None:
        db_compose = database.query(CentreCongres).filter(CentreCongres.id == elementcentre_data.compose).first()
        if not db_compose:
            raise HTTPException(status_code=400, detail="CentreCongres not found")
    else:
        raise HTTPException(status_code=400, detail="CentreCongres ID is required")

    db_elementcentre = ElementCentre(
        capaciteMax=elementcentre_data.capaciteMax,        description=elementcentre_data.description,        surfaceM2=elementcentre_data.surfaceM2,        id=elementcentre_data.id,        dureeMinJours=elementcentre_data.dureeMinJours,        nom=elementcentre_data.nom,        type=elementcentre_data.type.value,        compose_id=elementcentre_data.compose        )

    database.add(db_elementcentre)
    database.commit()
    database.refresh(db_elementcentre)

    if elementcentre_data.indisponibilite:
        # Validate that all Indisponibilite IDs exist
        for indisponibilite_id in elementcentre_data.indisponibilite:
            db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
            if not db_indisponibilite:
                raise HTTPException(status_code=400, detail=f"Indisponibilite with id {indisponibilite_id} not found")

        # Update the related entities with the new foreign key
        database.query(Indisponibilite).filter(Indisponibilite.id.in_(elementcentre_data.indisponibilite)).update(
            {Indisponibilite.Subit_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()
    if elementcentre_data.lienreservationelement_1:
        # Validate that all LienReservationElement IDs exist
        for lienreservationelement_id in elementcentre_data.lienreservationelement_1:
            db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
            if not db_lienreservationelement:
                raise HTTPException(status_code=400, detail=f"LienReservationElement with id {lienreservationelement_id} not found")

        # Update the related entities with the new foreign key
        database.query(LienReservationElement).filter(LienReservationElement.id.in_(elementcentre_data.lienreservationelement_1)).update(
            {LienReservationElement.Cible_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()
    if elementcentre_data.tarifsaisonnier:
        # Validate that all TarifSaisonnier IDs exist
        for tarifsaisonnier_id in elementcentre_data.tarifsaisonnier:
            db_tarifsaisonnier = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == tarifsaisonnier_id).first()
            if not db_tarifsaisonnier:
                raise HTTPException(status_code=400, detail=f"TarifSaisonnier with id {tarifsaisonnier_id} not found")

        # Update the related entities with the new foreign key
        database.query(TarifSaisonnier).filter(TarifSaisonnier.id.in_(elementcentre_data.tarifsaisonnier)).update(
            {TarifSaisonnier.possede_id: db_elementcentre.id}, synchronize_session=False
        )
        database.commit()



    indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.Subit_id == db_elementcentre.id).all()
    lienreservationelement_1_ids = database.query(LienReservationElement.id).filter(LienReservationElement.Cible_id == db_elementcentre.id).all()
    tarifsaisonnier_ids = database.query(TarifSaisonnier.id).filter(TarifSaisonnier.possede_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "indisponibilite_ids": [x[0] for x in indisponibilite_ids],        "lienreservationelement_1_ids": [x[0] for x in lienreservationelement_1_ids],        "tarifsaisonnier_ids": [x[0] for x in tarifsaisonnier_ids]    }
    return response_data


@app.post("/elementcentre/bulk/", response_model=None, tags=["ElementCentre"])
async def bulk_create_elementcentre(items: list[ElementCentreCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ElementCentre entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.compose:
                raise ValueError("CentreCongres ID is required")

            db_elementcentre = ElementCentre(
                capaciteMax=item_data.capaciteMax,                description=item_data.description,                surfaceM2=item_data.surfaceM2,                id=item_data.id,                dureeMinJours=item_data.dureeMinJours,                nom=item_data.nom,                type=item_data.type.value,                compose_id=item_data.compose            )
            database.add(db_elementcentre)
            database.flush()  # Get ID without committing
            created_items.append(db_elementcentre.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ElementCentre entities"
    }


@app.delete("/elementcentre/bulk/", response_model=None, tags=["ElementCentre"])
async def bulk_delete_elementcentre(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ElementCentre entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == item_id).first()
        if db_elementcentre:
            database.delete(db_elementcentre)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ElementCentre entities"
    }

@app.put("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def update_elementcentre(elementcentre_id: int, elementcentre_data: ElementCentreCreate, database: Session = Depends(get_db)) -> ElementCentre:
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    setattr(db_elementcentre, 'capaciteMax', elementcentre_data.capaciteMax)
    setattr(db_elementcentre, 'description', elementcentre_data.description)
    setattr(db_elementcentre, 'surfaceM2', elementcentre_data.surfaceM2)
    setattr(db_elementcentre, 'id', elementcentre_data.id)
    setattr(db_elementcentre, 'dureeMinJours', elementcentre_data.dureeMinJours)
    setattr(db_elementcentre, 'nom', elementcentre_data.nom)
    setattr(db_elementcentre, 'type', elementcentre_data.type.value)
    if elementcentre_data.compose is not None:
        db_compose = database.query(CentreCongres).filter(CentreCongres.id == elementcentre_data.compose).first()
        if not db_compose:
            raise HTTPException(status_code=400, detail="CentreCongres not found")
        setattr(db_elementcentre, 'compose_id', elementcentre_data.compose)
    if elementcentre_data.indisponibilite is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Indisponibilite).filter(Indisponibilite.Subit_id == db_elementcentre.id).update(
            {Indisponibilite.Subit_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.indisponibilite:
            # Validate that all IDs exist
            for indisponibilite_id in elementcentre_data.indisponibilite:
                db_indisponibilite = database.query(Indisponibilite).filter(Indisponibilite.id == indisponibilite_id).first()
                if not db_indisponibilite:
                    raise HTTPException(status_code=400, detail=f"Indisponibilite with id {indisponibilite_id} not found")

            # Update the related entities with the new foreign key
            database.query(Indisponibilite).filter(Indisponibilite.id.in_(elementcentre_data.indisponibilite)).update(
                {Indisponibilite.Subit_id: db_elementcentre.id}, synchronize_session=False
            )
    if elementcentre_data.lienreservationelement_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(LienReservationElement).filter(LienReservationElement.Cible_id == db_elementcentre.id).update(
            {LienReservationElement.Cible_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.lienreservationelement_1:
            # Validate that all IDs exist
            for lienreservationelement_id in elementcentre_data.lienreservationelement_1:
                db_lienreservationelement = database.query(LienReservationElement).filter(LienReservationElement.id == lienreservationelement_id).first()
                if not db_lienreservationelement:
                    raise HTTPException(status_code=400, detail=f"LienReservationElement with id {lienreservationelement_id} not found")

            # Update the related entities with the new foreign key
            database.query(LienReservationElement).filter(LienReservationElement.id.in_(elementcentre_data.lienreservationelement_1)).update(
                {LienReservationElement.Cible_id: db_elementcentre.id}, synchronize_session=False
            )
    if elementcentre_data.tarifsaisonnier is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(TarifSaisonnier).filter(TarifSaisonnier.possede_id == db_elementcentre.id).update(
            {TarifSaisonnier.possede_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if elementcentre_data.tarifsaisonnier:
            # Validate that all IDs exist
            for tarifsaisonnier_id in elementcentre_data.tarifsaisonnier:
                db_tarifsaisonnier = database.query(TarifSaisonnier).filter(TarifSaisonnier.id == tarifsaisonnier_id).first()
                if not db_tarifsaisonnier:
                    raise HTTPException(status_code=400, detail=f"TarifSaisonnier with id {tarifsaisonnier_id} not found")

            # Update the related entities with the new foreign key
            database.query(TarifSaisonnier).filter(TarifSaisonnier.id.in_(elementcentre_data.tarifsaisonnier)).update(
                {TarifSaisonnier.possede_id: db_elementcentre.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_elementcentre)

    indisponibilite_ids = database.query(Indisponibilite.id).filter(Indisponibilite.Subit_id == db_elementcentre.id).all()
    lienreservationelement_1_ids = database.query(LienReservationElement.id).filter(LienReservationElement.Cible_id == db_elementcentre.id).all()
    tarifsaisonnier_ids = database.query(TarifSaisonnier.id).filter(TarifSaisonnier.possede_id == db_elementcentre.id).all()
    response_data = {
        "elementcentre": db_elementcentre,
        "indisponibilite_ids": [x[0] for x in indisponibilite_ids],        "lienreservationelement_1_ids": [x[0] for x in lienreservationelement_1_ids],        "tarifsaisonnier_ids": [x[0] for x in tarifsaisonnier_ids]    }
    return response_data


@app.delete("/elementcentre/{elementcentre_id}/", response_model=None, tags=["ElementCentre"])
async def delete_elementcentre(elementcentre_id: int, database: Session = Depends(get_db)):
    db_elementcentre = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if db_elementcentre is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")
    database.delete(db_elementcentre)
    database.commit()
    return db_elementcentre



############################################
#   ElementCentre Method Endpoints
############################################




@app.post("/elementcentre/{elementcentre_id}/methods/verifierContraintes/", response_model=None, tags=["ElementCentre Methods"])
async def execute_elementcentre_verifierContraintes(
    elementcentre_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the verifierContraintes method on a ElementCentre instance.

    Parameters:
    - duree: Any    - participants: Any    """
    # Retrieve the entity from the database
    _elementcentre_object = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if _elementcentre_object is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    # Prepare method parameters
    duree = params.get('duree')
    participants = params.get('participants')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_elementcentre_object):
            """Vérifie que la demande respecte les capacités et durées minimales."""
            if participants > _elementcentre_object.capaciteMax:
                return False
            if duree < _elementcentre_object.dureeMinJours:
                return False
            return True

        result = await wrapper(_elementcentre_object)
        # Commit DB
        database.commit()
        database.refresh(_elementcentre_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "elementcentre_id": elementcentre_id,
            "method": "verifierContraintes",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/elementcentre/{elementcentre_id}/methods/estDisponible/", response_model=None, tags=["ElementCentre Methods"])
async def execute_elementcentre_estDisponible(
    elementcentre_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the estDisponible method on a ElementCentre instance.

    Parameters:
    - debut: Any    - fin: Any    """
    # Retrieve the entity from the database
    _elementcentre_object = database.query(ElementCentre).filter(ElementCentre.id == elementcentre_id).first()
    if _elementcentre_object is None:
        raise HTTPException(status_code=404, detail="ElementCentre not found")

    # Prepare method parameters
    debut = params.get('debut')
    fin = params.get('fin')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_elementcentre_object):
            """Vérifie si l'élément n'a pas d'indisponibilité sur la période."""
            indisponibilites = await get_indisponibilite(_elementcentre_object.subit)
            
            for indispo in indisponibilites:
                params = {"debut": debut, "fin": fin}
                conflit = await execute_indisponibilite_estenconflit(indispo.id, params)
                if conflit:
                    return False
            return True

        result = await wrapper(_elementcentre_object)
        # Commit DB
        database.commit()
        database.refresh(_elementcentre_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "elementcentre_id": elementcentre_id,
            "method": "estDisponible",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



