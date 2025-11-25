from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import time

load_dotenv()  # carrega o .env

DATABASE_URL = os.getenv("DATABASE_URL")

# Tenta esperar o banco estar pronto
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            print("✅ Conectado ao banco de dados!")
            break
    except Exception as e:
        print(f"⏳ Tentando conectar ao banco... ({i+1}/10)")
        time.sleep(2)
else:
    raise ConnectionError("❌ Não foi possível conectar ao banco de dados após várias tentativas.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
