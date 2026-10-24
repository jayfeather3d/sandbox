import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sys
sklearn.set_config(transform_output="pandas")


readin = str(input('Whats your filename? (no file extension): '))
intake = pd.read_csv(f"{readin}.csv")
independentvar = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Jumptime','reorthog','diagonal','iteration#','lanczos'])
dependentvar = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Z','N','nkeep'])
print(independentvar)
print(dependentvar)
independentvar_train, independentvar_test, dependentvar_train, dependentvar_test = train_test_split(independentvar, dependentvar, test_size=0.80, random_state=54)
model=LinearRegression()
trainer=LinearRegression()
trainer.fit(independentvar_train,dependentvar_train)
trainererror = trainer.predict(independentvar_test)
model.fit(independentvar,dependentvar)

menusel = 0
while menusel != 'exit':
    menusel = str(input('-------------MENU--------------\n Below is a selection menu to acquire outputs. \nOne input, one output, with error: one \nRange of inputs, range of output (looper): loop \n Export the entire model: export\nExit this program: exit \n \n \n selection---->:'))
    match menusel:
        case "one":
            questionZ = int(input("Your Z value ------: "))
            questionN = int(input("Your N value ------: "))
            questionNk = int(input("Your nkeep value : "))
            onesel = {"Z": questionZ, "N": questionN, "nkeep": questionNk}
            onedf = pd.DataFrame(data=onesel, index=[1])
            oracle = model.predict(onedf)
            print(oracle)
        case "loop":
            rangeselection = str(input("\n\n ----- Please select your range type below. ----- \n Nkeep iteration: nkeep\nZ and/or N iteration: zn\nBoth: znkeep\n"))
            match rangeselection:
                case nkeep:
                    Znksel = int(input("Constant Z value to maintain----:"))
                    Nnksel = int(input("Constant N value to maintain----:"))
                    nkmin = int(input("Starting nkeep value------------:"))
                    nkmax = int(input("Ending nkeep value--------------:"))
                    iterator = int(input("Amount to iterate by each time:"))
                    nkiter = nkmin
                    nkdf = pd.DataFrame()
                    while nkiter < nkmax:
                        passtime = {"Z":Znksel, "N":Nnksel, "nkeep":nkiter}
                        passdf = pd.DataFrame(data=passtime, index=[1])
                        nkdf = pd.concat([passdf,nkdf])
                        nkiter=nkiter+iterator
                    oracle = model.predict(nkdf)
                    print(oracle) 
                    exportquestion = str(input("Export?\n y/N: "))
                    if exportquestion == "y":
                        namequestion = str(input("filename: "))
                        exporter = pd.DataFrame(data=oracle, columns = ['Jumptime','reorthog','diagonal','iteration#','lanczos'])
                        exporter.to_csv(f"{namequestion}.csv")
                        
        case "export":
            namequestion = str(input("filename: "))
            exporter = pd.DataFrame.from_records(data=model.coef_, index=['Jumptime','reorthog','diagonal','iteration#','lanczos'], columns=["Z", "N", "nkeep"])
            print(exporter)
            exporter.to_csv(f"{namequestion}.csv")


                    


                    

