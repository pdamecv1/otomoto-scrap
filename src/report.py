import os
from datetime import datetime
import logging as log
from .settings import REPORT_PATH
import jinja2

logger = log.getLogger(__name__)

class GenerateReport:

    TEMPLATE = 'report_template.html'

    def __init__(self, db_session, table):
        """Fetches data from database and generates html report.

        Arguments:
        db_session -- session/connection to db
        table      -- (sqlalchemy) object representing table.
        """
        self.db = db_session
        self.table = table

    def get_car_data(self):
        logger.info(f'Getting data from {self.table}...')
        for row in self.db.query(self.table).all():
            data = {'car': row.car, 'price': row.price, 'contact': row.contact, 
                   'url': row.url, 'image': row.image}

            log.info(data)
            yield data

    @staticmethod
    def get_date():
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    def render_template(self, data):
        loader = jinja2.FileSystemLoader('src/resources')
        env = jinja2.Environment(autoescape=True, loader=loader, lstrip_blocks=True, trim_blocks=True)
        template = env.get_template(self.TEMPLATE)

        rendered_template = template.render(data=data, date=self.get_date())
        log.info(f'Template {self.TEMPLATE} rendered.')
        return rendered_template.encode('utf8')

    def save_report(self, data):
        if not os.path.exists(REPORT_PATH):
            os.makedirs(REPORT_PATH)
        
        
        with open(os.path.join(REPORT_PATH, self.TEMPLATE), 'wb') as f:
            f.write(data)
            log.info(f'{self.TEMPLATE} created.')
    
    def generate_report(self):
        data = list(self.get_car_data())
        rendered_template = self.render_template(data)
        self.save_report(rendered_template)

    

