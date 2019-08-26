# Otomoto Scrap
Project's goal is to automate the search for car at [otomoto](https://www.otomoto.pl) website. 

Main features:
- automate search for car with specific criterias (make, model, price, etc.)
- Postgresql database setup (user, db, table)
- store data in DB and plain file
- generate report 


## Prerequisites
- Chromedriver 76. For more information refer to [official site](https://sites.google.com/a/chromium.org/chromedriver/downloads).
- Python 3.7 with modules in requirements.txt
- PostgreSQL DBMS, ver 11

Also keep in mind that everything above is already containerized, should the project be launched with docker. 


## Usage
### 1. Input

Fill up input.json with information concerning the car, i.e.

```json
{
    "car_spec": {
        "make": "BMW", 
        "model": "M3"
    },
    "results": 15,
    "download_image": true
}
```

### 2. Env

Fill up .env_db with variables used for DB, i.e.:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin123
HOSTNAME=db
POSTGRES_DB=otomoto
```

### 3. Execution

Docker:

```bash
docker-compose up
```

Standard:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

## Artifacts
Scrapper stores logs, results and optionally images if declared in input.json. It will create following directory structure:

```
artifacts
├───logs
│       debug.log
│
├───report
│       scrapper_report.html
│
└───scrapper
    │   otomoto_scrap.json
    │   otomoto_scrap.txt
    │
    └───images
            BMW_M3_698_421_953.jpg
            BMW_M3_733_525_582.jpg
```



Example data structure of Scrapper's output:

- txt
```csv
Car,Price,Contact,Url,Image
BMW M3,145 000,733 525 582,https://www.otomoto.pl/oferta/bmw-m3-ac-oc-nowe-hamulce-przod-tyl-panewki-bezwypadkowa-ID6CpXNh.html,some_url
BMW M3,120 000,698 523 814,https://www.otomoto.pl/oferta/bmw-m3-dkg-pdc-mpower-ID6C1y9j.html,some_url2

```
- json
```json
[
    {
        "car": "BMW M3",
        "additionalInfo": [],
        "results": [
            {
                "price": "145 000",
                "contact": "733 525 582",
                "image": "https://apollo-ireland.akamaized.net/v1/files/example1.jpg",
                "url": "https://www.otomoto.pl/oferta/bmw-m3-ac-oc-nowe-hamulce-przod-tyl-panewki-bezwypadkowa-ID6CpXNh.html"
            },
            {
                "price": "120 000",
                "contact": "698 523 814",
                "image": "https://apollo-ireland.akamaized.net/v1/files/example2.jpg",
                "url": "https://www.otomoto.pl/oferta/bmw-m3-dkg-pdc-mpower-ID6C1y9j.html"
            }
        ]
    }
]

```

## Database
Data structure of *cars* table:

```txt
| Column  |       Type        |
+---------+-------------------+
| id      | integer           |
| car     | character varying |
| price   | integer           |
| contact | character varying |
| url     | character varying |
| image   | character varying |

Indexes:
    "cars_pkey" PRIMARY KEY, btree (id)
    "cars_url_key" UNIQUE CONSTRAINT, btree (url)
```
