from src.db.session import SessionLocal
from src.db.seed import seed_initial_data


def main() -> None:
    db = SessionLocal()
    try:
        seed_initial_data(db)
        print("Seed inicial ejecutado correctamente")
    finally:
        db.close()


if __name__ == "__main__":
    main()
