
import logging
from pathlib import Path
from dynaconf import Dynaconf

# ------------------------------ config dynaconf ---------------------------------------
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['../config.yaml'],
)

# ------------------------------ config logger ---------------------------------------
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

