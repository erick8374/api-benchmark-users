from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import time

load_dotenv()  # carrega o .env

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Tenta esperar o banco estar pronto
for i in range(10):
    try:
        with engine.connect() as conn:
            print("✅ Conectado ao banco de dados!")
            break
    except Exception as e:
        print(f"⏳ Tentando conectar ao banco... ({i+1}/10)")
        time.sleep(2)
else:
    raise ConnectionError("❌ Não foi possível conectar ao banco de dados após várias tentativas.")


with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS api_python"))
    conn.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
