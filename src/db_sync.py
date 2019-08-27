import os
import sys
import csv
import logging as log
from os.path import join, dirname
from dotenv import load_dotenv
from .settings import REQUIRED_VARS, CARS_TABLE

from sqlalchemy import (create_engine, inspect,
                        Table, Column, Integer, String, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError


logger = log.getLogger(__name__)
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

    def __repr__(self):
        return f"""<User(car='{self.car}', price='{self.price}', contact='{self.contact}',
                 url='{self.url}', image='{self.image}')>"""


class DbSync:

    ENV_FILE = '.env_db'

    def __init__(self):
        self.verify_db_info()
        self.db = self.prepare_db()

    @property
    def db_connection(self):
        user = os.environ['POSTGRES_USER']
        passwd = os.environ['POSTGRES_PASSWORD']
        hostname = os.environ['POSTGRES_HOSTNAME']
        port = os.environ['POSTGRES_PORT']
        db = os.environ['POSTGRES_DB']
        return f'postgresql+psycopg2://{user}:{passwd}@{hostname}:{port}/{db}'

    def verify_db_info(self):
        env_path = join(dirname(__file__), DbSync.ENV_FILE)
        is_env = os.path.isfile(env_path)

        if is_env:
            load_dotenv(env_path)
        else:
            logger.info(f'{DbSync.ENV_FILE} file is not present. Trying to fetch vars directly from env...')
            try:
                for var in REQUIRED_VARS:
                    os.environ[var]
            except KeyError:
                logger.info(f'No required variables detected. Please set following environment variables: {REQUIRED_VARS}')
                sys.exit()
                
    def prepare_db(self):
        engine = create_engine(self.db_connection)
        log.info(f'Connected to: {self.db_connection}')
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
                logger.info('Cannot add data:')
                logger.error(e)

    def inspect_db(self):
        inspector = inspect(self.db)
        logger.info(inspector.get_columns(CARS_TABLE))
