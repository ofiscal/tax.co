# Read into memory the data generated in build.py
# These use python.vat.build.readStage

purchasesEarly = readStage('/1.purchases') # memory hog
purchases = readStage('/2.purchases,prices,taxes') # memory hog

demog = readStage('/4.demog')
people = readStage('/5.person-demog-expenditures')
households = readStage('/6.households')
