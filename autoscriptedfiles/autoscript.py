print("loading imports")
import subprocess
import time
import pandas as pd
import numpy as np
import re
tallest = pd.DataFrame()
print('ONLY RUN WHEN INSIDE OF A /BIN FOLDER CONTAINING: BIGSTICK.X, SD.SPS, FP.SPS, GX1A.INT, USDB.INT')
debugq = str(input("RUN DEBUG FILE? y/n:"))
if debugq == "y":
    place = "y"
    namequestion = "debugquilt"
    sps = "fp"
    inputfile = "gx1a"
    jz = 0
    z = 2
    n = 2
    maxN = 3
    maxZ = 3
    nkeepstar = 10
    maxnkeep = 20
    diffcharge = 5
    output = "debug"
    maxnumiter = 5000
    csvname = "debugcsv"
if debugq == "n":
    place = str(input("Would you like to quilt at the end of this process? \n y/n: "))
    namequestion = str(input("quilt output filename: "))
    sps = str(input('where it is contained in your ./bin folder, enter .sps name (without the file extension) (fp or sd). \n \n SD.SPS = Oxygen 8 Core \n FP.SPS = Ca 20 Core \n .sps name ---: '))
    inputfile = str(input('where it is contained in your ./bin folder, enter .int name (without the file extension) (gx1a, usdb). \n check if you are using autoscaling by interpretation of the sign of the first constant in a .int \n .int name ---: '))
    if sps == 'fp':
        print('Z, N values <= 20 ONLY \n \n')
    if sps == 'sd':
        print('Z, N values <= 12 ONLY \n \n')
    z = int(input('Valence Proton # ---: '))
    n = int(input('Valence Neutron # ---: '))
    if sps =='fp':
        while z > 20 or z < 2:
            print('z value is out of bounds, re-enter ---:\n')
            z = int(input())
        while n > 20 or n < 2:
            print('z value is out of bounds, re-enter ---: \n')
            n = int(input())
    if sps == 'sd':
        while z > 12 or z < 2 :
            print('z value is out of bounds, re-enter ---: \n')
            z = int(input())
        while n > 12 or n < 2 :
            print('z value is out of bounds, re-enter ---: \n')
            n = int(input())
    if z % n != 0:
        jz = 1
    else:
        jz = 0
    if sps == "fp":
        maxZ = int(input("maximum Z value: "))
        maxN = int(input("maximum N value: "))
        if maxZ > 20 or z < 2:
            print('your max value is out of bounds, re-enter ---:\n')
            maxZ = int(input("maximum Z value: "))
        if maxN > 20 or z < 2:
            print('your max value is out of bounds, re-enter ---:\n')
            maxN = int(input("maximum N value: "))
    output = str(input('file name, which will be given the suffix _{alphabetic}_{numerals} \n'))
    nkeepstar = int(input('starting nkeep value \n'))
    while nkeepstar < 10:
            nkeepstar=int(input('You cannot start iterations with values approaching experimentally acquired limit.\n please re-enter ---:  \n'))
    maxnkeep = int(input('maximum nkeep value \n'))
    while maxnkeep == nkeep:
            maxnkeep = int(input('values cannot be equal, reenter \n'))
    if maxnkeep <= 50:
            print('low maxnkeep value, be advised to enter an appropriate resolution, proceeding \n')
    diffcharge = int(input('increment of nkeep from one iteration to the next \n'))
    if diffcharge <= 5:
            print('please consider that this is very high resolution...! \n')
    maxnumiter = int(input('enter max # iterations (kept constant) \n  be aware values sub ~100 give degenerate or low value cases. \n'))
    csvname = str(input('Please enter your output .csv name ---:'))
globvarstoragen = n
globvarstoragez = z
for a in 'abcdefjhijklmnopqrstuvwxyz':
    count=0
    b=0
    nkeep=nkeepstar
    while z < maxZ:
        while nkeep <= maxnkeep:  
            arg1='n      ! menu choice'
            arg2=f"{output}_{a}_{b}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "
            arg3=f"{sps}    !  name of .sps file "
            arg4=f"           {z}           {n}  ! # of valence protons, neutrons "
            arg5=f"           {jz}        ! 2 x Jz of systems"
            arg6='0     !  LANCZOS FRAGMENT SIZE in millions (0 = use default)'
            arg7=f'{inputfile}'
            arg8='end'
            arg9='ld'
            arg10=f"          {nkeep}         {maxnumiter}      ! # states to keep, max # iterations "
            with open('autoinput.bigstick','w+') as f:
                f.writelines(arg1+'\n')
                f.writelines(arg2+'\n')
                f.writelines(arg3+'\n')
                f.writelines(arg4+'\n')
                f.writelines(arg5+'\n')
                f.writelines(arg6+'\n')
                f.writelines(arg7+'\n')
                f.writelines(arg8+'\n')
                f.writelines(arg9+'\n')
                f.writelines(arg10+'\n')

            subprocess.run(args=['./bigstick-openmp.x'], shell=True, text=True, input='i')
            print(f"ran with values OF \n Z = {z} \n N = {n} \n jz = {jz} \n nkeep = {nkeep} \n")
            print(f"--------------------------------- {output}_{a}_{b} finished ---------------------------------")
            time.sleep(1)
            print('---------------------- continuing to tile step in 3 ----------------------\n')
            time.sleep(1)
            print('---------------------- continuing to tile step in 2 ----------------------\n')
            time.sleep(1)
            print('---------------------- continuing to tile step in 1 ----------------------\n')
            time.sleep(1)
            print('-------------------------- beginning tiling... ---------------------------\n' )
            #np1 and np2 seem to have inconsistencies
            np1 = 0
            np2 = 0
            jumpst=0
            reorth=0
            diagonal=0
            lanczos=0
            df = pd.read_table(f"{output}_{a}_{b}.log", header=None)
            print('---------------------- reading in output file... ------------------------\n')
            for x in range(0,df.size):
                current = df.iloc[x].item()
                if "Valence Z =" in current:
                    enter = int(df.iloc[x+1].item().strip())
                    np1 = enter
                if "Valence N =" in current:
                    enter = int(df.iloc[x+1].item().strip())
                    np2 = enter        
                if "Time to compute jumps :" in current:
                    enter = float(df.iloc[x+1].item().strip())
                    jumpst = enter 
                if "  Time in reorthogonalization : " in current:
                    enter = float(df.iloc[x+1].item().strip())
                    reorth = enter        
                if "  Time spent diagonalizing. : " in current:
                    enter = float(df.iloc[x+1].item().strip())
                    diagonal = enter
                if "  Time to compute lanczos :" in current:
                    enter = float(df.iloc[x+1].item().strip())
                    lanczos = enter
                if "iterations" in current and current != "  max iterations ":
                    dummy = df.iloc[x].item().strip()
                    enter = re.sub(r"[iterations]", "", dummy)
                    iterations = float(enter)
            #if theres a better way to do this let me know
            headers = ["Z", "N", "nkeep", "Jumptime", "reorthog", "diagonal", "iteration#", "lanczos"]
            if lanczos > 0:
                tiles = [z,n,nkeep,jumpst,reorth,diagonal,iterations,lanczos]
                hold = dict(zip(headers, tiles))
                tall = pd.DataFrame(hold, index=[1])
                tall.to_csv(f"tiled_{output}_{a}_{b}.csv")
                print("\n \n ---------------------- output csv written ---------------------- \n \n")
                print(f"read from {output}_{a}_{b}.log: \n Z = {np1} \n N = {np2} \n nkeep (from program) = {nkeep} \n jumptime = {jumpst} \n reorthog = {reorth} \n diagonal = {diagonal} \n iterations of {iterations} \n and lanczos time = {lanczos}.")
                if (np1 != z) or (np2 != n):
                    print(f"read in values are {np1}, {np2}. actual input values are {z}, {n}. \n") #Just to showcase it easier
                # for values where np(1) np(2) != z,n im unsure what the cause is
                # as far as i know np(1) and np(2) are held by system parameter subroutine
                # or other subroutines inside of bigstick
                # my only guess is that its a factor of some other point where np input is reset which passes before np(1) and np(2) are written to console
                print(f"---------------------- tile of {output}_{a}_{b} complete ----------------------\n")
                print("--------------------------------  quilting... -----------------------------------\n")
                
                tallest = pd.concat([pd.read_csv(f"tiled_{output}_{a}_{b}.csv"), tallest])
                tallest.to_csv(f"{csvname}.csv")
                print("\n \n ---------------------- total csv written ---------------------------------- \n \n")
            else:
                print(f"!+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n failed case!!! \n continuing to next set \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+!\n") 
            nkeep=nkeep + 10 
            count=count+1
        b=b+1
        if n == maxN and z < maxZ:
            z=z+1
            n=globvarstoragen
        if n < maxN:
            n=n+1
        if z % n != 0:
            jz = 1
        else:
            jz = 0 
if place == "y":
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression
    import sys
    intake = pd.read_csv(f"{csvname}.csv")
    independentvar = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Jumptime','reorthog','diagonal','iteration#','lanczos'])
    dependentvar = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Z','N','nkeep'])
    model=LinearRegression()
    model.fit(independentvar,dependentvar)
    exportercoef = pd.DataFrame.from_records(data=model.coef_, index=['Jumptime','reorthog','diagonal','iteration#','lanczos'], columns=["Z_coef", "N_coef", "nkeep_coef"])
    exporterinter = pd.DataFrame(data=model.intercept_.tolist(), index=['Jumptime','reorthog','diagonal','iteration#','lanczos'], columns=["intercept"])
    exporter = pd.concat([exportercoef, exporterinter], axis=1)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!QUILT OUTPUT BELOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n\n", exporter)
    print("""\\
           __..--''``---....___   _..._    __
 /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
///_.-' _..--.'_   [                    `( ) ) // //   You made it!
/ (_..-' // (< _     ;_..__               ; `' / ///      :)    
 / // // //  `-._,_)' // / ``--...____..-' /// / //
""")
    exporter.to_csv(f"{namequestion}.csv")


                        


                        

