from random import randint, choice
import pandas as pd


def random_age() -> int:
    age: int = randint(18, 65)
    return age


def random_reisafstand() -> int:
    reisafstand: int = randint(0, 500)
    return reisafstand


def random_afdeling() -> str:
    afdelingen = ['BI', 'Accountant', 'Business analist', 'Financial controller', 'Credit controller', 'Boekhouder',
                  'Project controller', 'Business controller', 'Administratief medewerker', 'HR', 'Legal', 'Marketing',
                  'Office manager', 'Business development', 'IT']
    index: int = randint(0, len(afdelingen)) - 1
    return afdelingen[index]


def random_dienstperiode() -> int:
    dienstperiode: int = randint(0, 50)
    return dienstperiode


def random_businessunit() -> str:
    businessunit: list[str] = ['Detachering', 'Intern']
    index: int = randint(0, len(businessunit)) - 1
    return businessunit[index]


def random_geboortes() -> int:
    geboortes: int = randint(0, 10)
    return geboortes


def random_name() -> str:
    first_names = ["John", "Jane", "Sarah", "Michael", "Emily", "David", "Anna", "Robert", "Laura", "James"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                  "Martinez"]

    first_name = choice(first_names)
    last_name = choice(last_names)

    return f"{first_name} {last_name}"


def generate_data(max_index: int) -> list:
    generated_data: list = []
    for _ in range(max_index):
        generated_data.append(
            [random_name(), random_age(), random_dienstperiode(), random_reisafstand(), random_afdeling(), random_businessunit(),
             random_geboortes()])
    return generated_data


if __name__ == '__main__':
    generated_data: list = generate_data(50)
    column_names = ['name', 'leeftijd_begin_dienst', 'dienstperiode', 'reisafstand', 'afdeling', 'business_unit',
                    'aantal_geboortes_pf']
    df: pd.DataFrame = pd.DataFrame(generated_data, columns=column_names)
    df = pd.get_dummies(df, columns=['afdeling', 'business_unit'])
    df = df[
        ['name','leeftijd_begin_dienst', 'dienstperiode', 'reisafstand', 'dienstperiode', 'afdeling_Accountant', 'afdeling_BI',
         'afdeling_Boekhouder', 'afdeling_Business analist', 'afdeling_Business controller',
         'afdeling_Financial controller', 'afdeling_IT', 'afdeling_Legal', 'afdeling_Marketing',
         'afdeling_Office manager', 'afdeling_Project controller',
         'afdeling_Administratief medewerker', 'afdeling_Business development', 'afdeling_Credit controller',
         'afdeling_HR', 'business_unit_Intern', 'business_unit_Detachering', 'aantal_geboortes_pf']]
    df.to_csv('random_data.csv', sep=',', index=False)
