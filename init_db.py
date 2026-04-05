# init_db.py

from database import engine, Base
import models  # 👈 VERY IMPORTANT (loads models)

Base.metadata.create_all(bind=engine)