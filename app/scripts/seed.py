from datetime import date
from app.db.database import SessionLocal
from app.db.models.fighters import Fighters

def seed():
    db = SessionLocal()
    try:
        fighters_data = [
            Fighters(
                name="Conor",
                nickname="The Notorious",
                surname="McGregor",
                country="Ireland",
                weight_class="Lightweight",
                wins=22,
                loss=6,
                draw=0,
                current_streak=0,
                last_fight_date=date(2023, 7, 10)
            ),
            Fighters(
                name="Khabib",
                nickname="The Eagle",
                surname="Nurmagomedov",
                country="Russia",
                weight_class="Lightweight",
                wins=29,
                loss=0,
                draw=0,
                current_streak=0,
                last_fight_date=date(2020, 10, 24)
            ),
            Fighters(
                name="Israel",
                nickname="The Last Stylebender",
                surname="Adesanya",
                country="Nigeria/New Zealand",
                weight_class="Middleweight",
                wins=24,
                loss=1,
                draw=0,
                current_streak=0,
                last_fight_date=date(2023, 4, 8)
            ),
            Fighters(
                name="Amanda",
                nickname="The Lioness",
                surname="Nunes",
                country="Brazil",
                weight_class="Bantamweight",
                wins=21,
                loss=5,
                draw=0,
                current_streak=0,
                last_fight_date=date(2022, 7, 30)
            ),
        ]
        db.add_all(fighters_data)
        db.commit()
        print("Seed done!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()