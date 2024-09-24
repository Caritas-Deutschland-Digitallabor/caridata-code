import pandas as pd
from typing import Any
import json
import random
import datetime
import faker


sheetnames = ["SBVERAN", "SBKONT", "SBKERN2_Inhalte", "SBKERN1_Inhalte", "STELLE"]
rep_numbers = ["tsnr", "lzrnr", "betrnr"]
fake = faker.Faker(locale="de_DE")


def get_schema(sheetname: str) -> Any:
    """finds schema for table

    Parameters
    ----------
    sheetname : str

    Returns
    -------
    json
        schema for table
    """
    return json.load(open(f"backend/utils/{sheetname}_schema.json"))


def random_date():
    earliest = datetime.date(year=2023, month=1, day=1)
    latest = datetime.date(year=2024, month=12, day=31)
    delta = latest - earliest
    random_days = random.randrange(delta.days)
    return earliest + datetime.timedelta(days=random_days)


def create_case(sheetname: str, tsnr: int, lzrnr: int, betrnr: str) -> dict:
    """creates one data instance (with unique fallnr) for specified table

    Parameters
    ----------
    sheetname : str
        table for which data is to be created
    tsnr : int
    lzrnr : int
    betrnr : str
    Returns
    -------
    dict
        one data instance for specified table
    """
    new_case = {}
    schema = get_schema(sheetname)
    for field in schema:
        if field["variable_name"] == "tsnr":
            new_case[field["variable_name"].upper()] = tsnr
        elif field["variable_name"] == "lzrnr":
            new_case[field["variable_name"].upper()] = lzrnr
        elif field["variable_name"] == "betrnr":
            new_case[field["variable_name"].upper()] = betrnr
        # treat fallnr seperately because it is value_type: string
        elif field["variable_name"] == "fallnr":
            new_case[field["variable_name"].upper()] = str(random.randint(1, 99999))
        elif field["value_type"] == "string":
            if (
                "einrichtung" in field["variable_text"].lower()
                and len(field["variable_text"].split("-")) > 1
            ):
                subquestion = field["variable_text"].split("-")[1].strip().lower()
                if subquestion == "name":
                    new_case[field["variable_name"].upper()] = fake.name()
                elif "straße" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.street_address()
                elif "postleitzahl" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.postcode()
                elif "stadt" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.city()
                elif "telefon" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.phone_number()
                elif "mail" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.email()
                elif "fax" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.phone_number()
                elif "web" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.url()
                elif "ansprechpartner" in subquestion:
                    new_case[field["variable_name"].upper()] = fake.name()
            else:
                new_case[field["variable_name"].upper()] = "".join(
                    random.choices("abcdefghijklmnopqrstuvwxyz", k=10)
                )
        elif field["value_type"] == "integer":
            if field["value_to"]:
                # int() because value_from and value_to are floats
                new_case[field["variable_name"].upper()] = [
                    random.randint(int(field["value_from"]), int(field["value_to"]))
                ]
            else:  # manche int columns sind Jahreszahlen und haben keine value_from und value_to
                new_case[field["variable_name"].upper()] = random.randint(1950, 2024)
        elif field["value_type"] == "float":
            new_case[field["variable_name"].upper()] = [
                round(random.uniform(field["value_from"], field["value_to"]), 2)
            ]
        elif field["value_type"] == "date":
            date = random_date()
            new_case[field["variable_name"].upper()] = "{:%d.%m.%Y}".format(date)
        elif field["value_type"] == "boolean":
            new_case[field["variable_name"].upper()] = random.choice([True, False])
        elif field["value_type"] == "categorical":
            new_case[field["variable_name"].upper()] = random.choice(
                [el["value"] for el in field["categories"]]
            )
    return new_case


def create_missing(sheetname: str, columns=[]) -> dict:
    """_summary_

    Parameters
    ----------
    sheetname : str
        _description_
    columns : list, optional
        for which columns missing value should be generated, by default []

    Returns
    -------
    dict
        case isntance with missing values
    """
    new_case = {}
    return new_case


def create_data(sheetname: str, n_total=100, n_cases=50) -> pd.DataFrame:
    """creates mock data for table

    Parameters
    ----------
    sheetname : str
         table for which data is to be created
    n_total : int, optional
        total number of instances, default = 100
    n_cases : int, optional
        number of cases per betrnr/tsnr/lzrnr, default = 50

    Returns
    -------
    pd.DataFrame
        mock data with n_total instances for specified table
    """
    schema = get_schema(sheetname=sheetname)
    data = pd.DataFrame(columns=[field["variable_name"].upper() for field in schema])
    while len(data) < n_total:
        betrnr = str(random.randint(1, 99))
        tsnr = random.randint(1, 999)
        lzrnr = random.randint(1, 5)
        for _ in range(n_cases):
            new_case = create_case(
                sheetname=sheetname, tsnr=tsnr, lzrnr=lzrnr, betrnr=betrnr
            )
            data = pd.concat([data, pd.DataFrame(new_case)], ignore_index=True)
    return data


for sheetname in sheetnames:
    mydata = create_data(sheetname)
    mydata.to_csv(f"backend/mock_data/data/{sheetname}_mock.csv", index=False)
