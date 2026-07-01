from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# The engine manages a pool of actual connections to PostgreSQL.
# It is created ONCE when the application starts, not per-request —
# creating a new engine per request would exhaust connections under load.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,   # checks a connection is alive before using it,
                           # preventing errors from stale/dropped connections
                           # (e.g. after Postgres restarts or idle timeouts)
    echo=settings.debug,  # logs all SQL statements when DEBUG=True —
                           # invaluable while learning/debugging, should be
                           # False in production to avoid log noise and
                           # leaking query details
)

# SessionLocal is a factory that produces new Session objects.
# Each Session represents a single "unit of work" — typically scoped
# to one HTTP request — that gets opened, used, and closed.
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # we explicitly control when changes are committed
    autoflush=False,   # we explicitly control when pending changes are
                        # sent to the DB, rather than SQLAlchemy guessing
)


def get_db() -> Session:
    """
    FastAPI dependency that provides a database session per request.

    This is a generator-based dependency: FastAPI runs the code before
    `yield` at the start of the request, hands the session to the route,
    and runs the code after `yield` (closing the session) once the request
    finishes — even if an exception was raised. This guarantees connections
    are always returned to the pool and never leaked.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()