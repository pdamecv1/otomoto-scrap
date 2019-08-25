import os
import sys
import csv
from os.path import join, dirname
from settings import REQUIRED_VARS, CARS_TABLE
from dotenv import load_dotenv
from sqlalchemy import (create_engine, inspect,
                        Table, Column, Integer, String, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError


Base = declarative_base()


class Car(Base):

    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    car = Column(String)
    price = Column(Integer)
    contact = Column(String)
    url = Column(String, unique=True)
    image = Column(String)

    def __init__(self, car, price, contact, url, image):
        self.car = car
        self.price = price
        self.contact = contact
        self.url = url
        self.image = image


class DbSync:

    ENV_FILE = '.env_db'

    def __init__(self):
        self.verify_db_info()
        self.db = self.prepare_db()

    def verify_db_info(self):
        env_path = join(dirname(__file__), DbSync.ENV_FILE)
        is_env = os.path.isfile(env_path)

        if is_env:
            load_dotenv(env_path)
        else:
            print(f'{DbSync.ENV_FILE} file is not present. Trying to fetch vars directly from env...')
            try:
                for var in REQUIRED_VARS:
                    os.environ[var]
            except KeyError:
                print(f'No required variables detected. Please set following environment variables: {REQUIRED_VARS}')
                sys.exit()
                
    def prepare_db(self):
        engine = create_engine(f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['HOSTNAME']}/{os.environ['POSTGRES_DB']}")
        Base.metadata.create_all(bind=engine)
        return sessionmaker(bind=engine)()

    @staticmethod
    def load_data(csv_file):
        with open(csv_file, newline='') as f:
            next(f)
            car_data = csv.reader(f, delimiter=',')
        
            for row in car_data:
                yield row

    def insert_car_data(self):
        for row in self.load_data('artifacts/scrapper/otomoto_scrap.txt'):
            car = Car(row[0], row[1].replace(' ', ''), row[2], row[3], row[4])
            self.db.add(car)

            try:
                self.db.commit()
            except (IntegrityError, InvalidRequestError) as e:
                print('Cannot add data because:')
                print(e)

    def inspect_db(self):
        inspector = inspect(self.db)
        print(inspector.get_columns(CARS_TABLE))


if __name__ == '__main__':
    dbs = DbSync()
    dbs.insert_car_data()