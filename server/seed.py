#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from datetime import datetime, timedelta

from app import app
from models import db, Message

fake = Faker()

# Generate a list of unique usernames
usernames = list(set([fake.first_name() for _ in range(4)]))  # Ensure uniqueness
if "Duane" not in usernames:
    usernames.append("Duane")
print(f"Generated usernames: {usernames}")

def make_messages():
    print("Clearing existing messages...")
    Message.query.delete()

    messages = []
    for _ in range(20):
        created_at = fake.date_time_between(start_date='-30d', end_date='now')
        message = Message(
            body=fake.sentence(),
            username=rc(usernames),
            created_at=created_at,
            updated_at=created_at + timedelta(days=fake.random_int(min=0, max=5))
        )
        messages.append(message)

    db.session.add_all(messages)
    db.session.commit()

    print(f"Seeded {len(messages)} messages!")

if __name__ == '__main__':
    with app.app_context():
        make_messages()