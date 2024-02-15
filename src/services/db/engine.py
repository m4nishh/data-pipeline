from sqlalchemy import create_engine
from config import APP_CONFIG
# TODO: get this form env
engine = create_engine(
    f"mysql+pymysql://{APP_CONFIG.db_user}:{APP_CONFIG.db_password}@{APP_CONFIG.db_host}/{APP_CONFIG.db_name}"
    , pool_size=20, max_overflow=5, echo=False
    )

