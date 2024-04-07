from typing import Any
import logging
from pathlib import Path
from dynaconf import Dynaconf
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


# ------------------------------ config dynaconf ---------------------------------------
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['../config.yaml'],
)

# ------------------------------ config logger ---------------------------------------
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# ------------------------------- database ------------------------------------------------
_engine = create_engine(url=settings.database.url)
session = sessionmaker(autocommit=False, bind=_engine)
BaseModel = declarative_base()


