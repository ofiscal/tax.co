# Read into memory the data generated in main.py
# These use python.vat.main.readStage

purchases = readStage('/2.purchases,prices,taxes') # memory hog

demog = readStage('/4.demog')
people = readStage('/5.person-demog-expenditures')
households = readStage('/6.households')
