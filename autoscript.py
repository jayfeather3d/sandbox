print("loading imports")
import subprocess
import time
import pandas as pd
import numpy as np
import re
tallest = pd.DataFrame()
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
print("""--------------------------------------------------------------------------------------------
                            AUTOSCRIPT . PY launch menu:
                    TO RUN DEBUG FILE: enter "d"
                    TO CONTINUE MENU: enter "n"
                    TO RUN ORACLE: enter "o"
                    TO RESUME: enter "r"
                    TO REPAIR: enter "q"
        """                                                                                                   
      
      )
debug = 0
debugq = str(input("\n-----:"))
#FUNCTION CALLS
enter=0
def extract(dataf, index, flin, str):
    if flin == "float":
        enter == float(re.sub(f"[{str}]","", dataf.iloc[x].item().strip()))
    if flin == "int":
        enter == int(re.sub(f"[{str}]","", dataf.iloc[x].item().strip()))
    return enter
def EXPORT(modelN, colname):
    exportercoef = pd.DataFrame.from_records(data=modelN.coef_, index=['totaltime','reorthog','diagonal','iteration#','lanczos'], columns=colname)
    exporterinter = pd.DataFrame(data=modelN.intercept_.tolist(), index=['totaltime','reorthog','diagonal','iteration#','lanczos'], columns=["intercept"])
    exporter = pd.concat([exportercoef, exporterinter], axis=1)
    return exporter 
def errorcalc(exp, real, type):
    if type == "percent":
        out = abs((exp - real)/real * 100)
    if type == "relative":
        out = abs((exp-real)/real)
    if type == "absolute":
        out = abs(exp-real)
    return out
def AUTOINPUT_Creator(output,a,b,sps,z,n,jz,inputfile,nkeep,menu,maxnumiter):
        arg1=f'{menu}      ! menu choice'
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
def configREADIN(configname):
    DQ = pd.read_table(f"{configname}")
    global place, namequestion, sps, inputfile, z, n, jz, maxN, maxZ, nkeepstar, maxnkeep, diffcharge, output, maxnumiter, csvname, globvarstoragez, globvarstoragen
    place = str(DQ.loc[1].item());
    namequestion = str(DQ.loc[2].item())
    sps = str(DQ.loc[3].item())
    inputfile = str(DQ.loc[4].item())
    z = int(DQ.loc[5].item())
    n = int(DQ.loc[6].item())
    if z % n != 0:
        jz= 1
    else:
        jz = 0 
    maxN = int(DQ.loc[7].item())
    maxZ = int(DQ.loc[8].item())
    nkeepstar = int(DQ.loc[9].item())
    maxnkeep = int(DQ.loc[10].item())
    diffcharge = int(DQ.loc[11].item())
    output = str(DQ.loc[13].item())
    maxnumiter = int(DQ.loc[14].item())
    csvname = str(DQ.loc[15].item())
    globvarstoragez = z
    globvarstoragen = n
def CALCULATOR(current, model, V_OR_B):
    calcreturn=0
    if V_OR_B == "b":
        calcreturn = current.b * model._A + current.k * model._Nk + model._INTERCEPT
    if V_OR_B == "v":
        calcreturn = current.v * model._A + current.k * model._Nk + model._INTERCEPT
    return calcreturn
skiptoend="n"
configq = str(input("config file read-in? y/n ----:"))
if debugq == "d":
    skiptoend = str(input("skip to end? y/n:"))
    configREADIN("debugconfig.txt")
if debugq == "n":
    skiptoend="n"
    if configq != "y":
        place = str(input("Would you like to quilt at the end of this process? \n y/n: "))
        namequestion = str(input("quilt output filename: "))
        sps = str(input('enter .sps name (without the file extension) (fp or sd). \n \n SD.SPS = Oxygen 8 Core \n FP.SPS = Ca 20 Core \n .sps name ---: '))
        inputfile = str(input('enter .int name (without the file extension) (gx1a, usdb). \n check if you are using autoscaling by interpretation of the sign of the first constant in a .int \n .int name ---: '))
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
        maxZ = int(input("maximum Z value: "))
        maxN = int(input("maximum N value: "))
        if sps == "fp":
            if maxZ > 20 or z < 2:
                print('your max value is out of bounds, re-enter ---:\n')
                maxZ = int(input("maximum Z value: "))
            if maxN > 20 or z < 2:
                print('your max value is out of bounds, re-enter ---:\n')
                maxN = int(input("maximum N value: "))
        if sps == "sd":
            if maxZ > 12 or z < 2:
                print('your max value is out of bounds, re-enter ---:\n')
                maxZ = int(input("maximum Z value: "))
            if maxN > 12 or z < 2:
                print('your max value is out of bounds, re-enter ---:\n')
                maxN = int(input("maximum N value: "))
        output = str(input('file name, which will be given the suffix _{alphabetic}_{numerals} \n'))
        nkeepstar = int(input('starting nkeep value \n'))
        while nkeepstar < 10:
            nkeepstar=int(input('You cannot start iterations with values approaching experimentally acquired limit.\n please re-enter ---:  \n'))
        maxnkeep = int(input('maximum nkeep value \n'))
        while maxnkeep == nkeepstar:
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
    else: 
        configREADIN("config.txt")
if debugq == "r":
    place = str(input("Would you like to quilt at the end of this process? \n y/n: "))
    namequestion = str(input("quilt output filename: "))
    configq = "n"
    subprocess.run(["ls", "-tr"])
    print("\n Please review your files.")
    autoreadin = str(input("What is the name of your last .log? \n if you would like to continue from a flat restart enter simply 0.\n -----: "))
    quiltnm = str(input("Your last quilt's name? ----:"))
    lastquilt = pd.read_csv(f"{quiltnm}_QUILT.csv")
    tallest = lastquilt.drop(columns=["Unnamed: 0"])
    if autoreadin != 0:
        df = pd.read_table(f"{autoreadin}.log", header=None)
        print(f'---------------------- reading in the  last output file, {autoreadin}.log... ------------------------\n')
        for x in range(0,df.size):
            current = df.iloc[x].item()
            if "Valence Z =" in current:
                z = extract(df, x, "int", "Valence = Z")
            if "Valence N =" in current:
                n = extract(df, x, "int", "Valence = N")  
            if "gx1a.int" in current:
                inputfile = "gx1a.int"
            if "usdb.int" in current:
                inputfile = "usdb.int"
            if "  Menu choice:" in current:
                menu = str(re.sub("[Menu choice:", "", current.strip()))
            if "  Single particle space found in" in current:
                sps = str(re.sub("[Single particle space found in]", "", current.strip()))
    else: 
        place = str(input("Would you like to quilt at the end of this process? \n y/n: "))
        namequestion = str(input("quilt output filename: "))
        sps = str(input('enter .sps name (without the file extension) (fp or sd). \n \n SD.SPS = Oxygen 8 Core \n FP.SPS = Ca 20 Core \n .sps name ---: '))
        inputfile = str(input('enter .int name (without the file extension) (gx1a, usdb). \n check if you are using autoscaling by interpretation of the sign of the first constant in a .int \n .int name ---: '))
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
    maxZ = int(input("maximum Z value: "))
    maxN = int(input("maximum N value: "))
    if sps == "fp":
        if maxZ > 20 or z < 2:
            print('your max value is out of bounds, re-enter ---:\n')
            maxZ = int(input("maximum Z value: "))
        if maxN > 20 or z < 2:
            print('your max value is out of bounds, re-enter ---:\n')
            maxN = int(input("maximum N value: "))
    if sps == "sd":
        if maxZ > 12 or z < 2:
            print('your max value is out of bounds, re-enter ---:\n')
            maxZ = int(input("maximum Z value: "))
        if maxN > 12 or z < 2:
            print('your max value is out of bounds, re-enter ---:\n')
            maxN = int(input("maximum N value: "))
            output = str(input('file name, which will be given the suffix _{alphabetic}_{numerals} \n'))
   
    nkeepstar = int(input('starting nkeep value \n'))
    while nkeepstar < 10:
        nkeepstar=int(input('You cannot start iterations with values approaching experimentally acquired limit.\n please re-enter ---:  \n'))
    maxnkeep = int(input('maximum nkeep value \n'))
    while maxnkeep == nkeepstar:
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
    nkeepstar = nkeepstar
    if debugq == "r" or "n":
        for a in 'abcdefjhijklmnopqrstuvwxyzabcdefjhijklmnopqrstuvwxyzabcdefjhijklmnopqrstuvwxyzabcdefjhijklmnopqrstuvwxyzabcdefjhijklmnopqrstuvwxyz':
            b=0
            nkeep =nkeepstar
            while nkeep <= maxnkeep: 
                AUTOINPUT_Creator(output,a,b,sps,z,n,jz,inputfile,nkeep,"n",maxnumiter)
                subprocess.run(args=['./bigstick-openmp.x'], shell=True, text=True, input='i')
                print(f"ran with values OF \n Z = {z} \n N = {n} \n jz = {jz} \n nkeep = {nkeep} \n")
                print(f"--------------------------------- {output}_{a}_{b} finished ---------------------------------")
                print('-------------------------- beginning tiling... ---------------------------\n' )
                #np1 and np2 seem to have inconsistencies
                np1 = 0
                np2 = 0
                tt=0
                reorth=0
                diagonal=0
                lanczos=0
                BASIS=0
                df = pd.read_table(f"{output}_{a}_{b}.log", header=None)
                print('---------------------- reading in output file... ------------------------\n')
                for x in range(0,df.size):
                    current = df.iloc[x].item()
                    if "Valence Z =" in current:
                        np1 = extract(df, x, "int", "Valence = Z")
                    if "Valence N =" in current:
                        np2 = extract(df, x, "int", "Valence = N")
                    if "Total time to run :" in current:
                        tt = extract(df, x, "float", "Total time to run :")
                    if "  Time in reorthogonalization : " in current:
                        reorth = extract(df, x, "float", "Time in reorthogonalization :")
                    if "  Time spent diagonalizing. : " in current:
                        diagonal = extract(df, x, "float", "Time spent diagonalizing. : ")
                    if "  Time to compute lanczos :" in current:
                        lanczos = extract(df, x, "float", "Time to compute lanczos :")
                    if "iterations" in current and current != "  max iterations ":
                        iterations = extract(df,x,"float", "iterations")
                    if "Total basis dimension:" in current:
                        BASIS=extract(df,x,"int", "Total basis dimension:")
                V=z+n
                headers = ["Z", "N","V","BASIS", "nkeep", "totaltime", "reorthog", "diagonal", "iteration#", "lanczos"]
                if lanczos > 0:
                    tiles = [z,n,V,BASIS,nkeep,tt,reorth,diagonal,iterations,lanczos]
                    hold = dict(zip(headers, tiles))
                    tall = pd.DataFrame(hold, index=[1])
                    print("\n \n ---------------------- output csv written ---------------------- \n \n")
                    print(f"read from {output}_{a}_{b}.log: \n Z = {np1} \n N = {np2} and a sum V = {V} \n nkeep (from program) = {nkeep} \n totaltime = {tt} \n reorthog = {reorth} \n diagonal = {diagonal} \n iterations of {iterations} \n and lanczos time = {lanczos}.")
                    if (np1 != z) or (np2 != n):
                        print(f"read in values are {np1}, {np2}. actual input values are {z}, {n}. \n") #Just to showcase it easier
                    # for values where np(1) np(2) != z,n im unsure what the cause is
                    # as far as i know np(1) and np(2) are held by system parameter subroutine
                    # or other subroutines inside of bigstick
                    # my only guess is that its a factor of some other point where np input is reset which passes before np(1) and np(2) are written to console
                    print(f"---------------------- tile of {output}_{a}_{b} complete ----------------------\n")
        
                    print("--------------------------------  quilting... -----------------------------------\n")
        
                    tallest = pd.concat([tallest,tall],axis=0)
                    tallest.to_csv(f"{csvname}_QUILT.csv")
                    print("\n \n ---------------------- total csv written ---------------------------------- \n \n")
                else:
                    print(f"!+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n failed case!!! \n continuing to next set \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+!\n") 
                nkeep=nkeep + 10 
                b=b+1
            #conditions
            if z == maxZ:
                break
            if n == maxN and z < maxZ:
                z=z+1
                n=globvarstoragen
            if n < maxN:
                n=n+1
            if z % n != 0:
                jz = 1
            else:
                jz = 0 
if debugq == "o":
    place="y" 
    weavein = str(input("would you like to take in multiple quilts into one file (replicates the main quilt)? y/n \n -----:"))
    if weavein == "y":
        firstfile = str(input("your first quilt files name  :"))
        secondfile = str(input("your second quilt files name :"))
        together = pd.concat([pd.read_csv(f"{firstfile}_QUILT.csv"),pd.read_csv(f"{secondfile}_QUILT.csv")], axis=0)
        anymore = str(input("would you like to include another file (weaved together main quilt + 3rd new quilt)? y/n \n ------:"))
        while anymore == "y":
            secondfile = str(input("your next quilt files name :"))
            together = pd.concat([together, pd.read_csv(f"{secondfile}_QUILT.csv")])
            anymore = str(input("would you like to include another file (weaved together main quilt + 3rd new quilt)? y/n \n ------:"))
        csvname = str(input("your csvname for output:"))
        together.to_csv(f"{csvname}_QUILT.csv")
    if weavein == "n":
        csvname = str(input("your TOTAL quilt files name: "))
if place == "y":
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    import sys
    intake = pd.read_csv(f"{csvname}_QUILT.csv").drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])
    SIndependentVariables = intake.drop(columns=["V", 'BASIS','totaltime','reorthog','diagonal','iteration#','lanczos'])
    VIndependentVariables = intake.drop(columns=['Z', 'N', 'BASIS','totaltime','reorthog','diagonal','iteration#','lanczos'])
    HBasisIn = intake.drop(columns=['Z','N','V','totaltime','reorthog','diagonal','iteration#','lanczos'])
    DependentVariables = intake.drop(columns=['Z','N','V','BASIS','nkeep'])
    seer=LinearRegression()
    mage=LinearRegression()
    heir=LinearRegression()
    seer.fit(SIndependentVariables, DependentVariables)
    seercol = ["Z", "N","Nk"]
    mage.fit(VIndependentVariables, DependentVariables)
    magecol = ["V","Nk"]
    heir.fit(HBasisIn, DependentVariables)
    heircol = ["B", "Nk"]
    S_m = EXPORT(seer, seercol)
    M_m = EXPORT(mage, magecol)
    H_m = EXPORT(heir, heircol)

    pd.concat([S_m, M_m, H_m], axis = 1).to_csv(f"{csvname}_ORACLE.csv")

    S_m.to_csv(f"{csvname}_SEER.csv")
    M_m.to_csv(f"{csvname}_MAGE.csv")
    H_m.to_csv(f"{csvname}_HEIR.csv")

    print("""\\
            __..--''``---....___   _..._    __
    /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
    ///_.-' _..--.'_   [                    `( ) ) // //   You made it!
    / (_..-' // (< _     ;_..__               ; `' / ///      :)    
    / // // //  `-._,_)' // / ``--...____..-' /// / //
    """)
quilt = pd.read_csv(f"{csvname}_QUILT.csv")
quilt_M = pd.read_csv(f"{csvname}_MAGE.csv")
quilt_S = pd.read_csv(f"{csvname}_SEER.csv")
quilt_H = pd.read_csv(f"{csvname}_HEIR.csv")
class working:
    def __init__(self,Zval,Nval,BASIS,NKval):
        self.z = Zval
        self.n = Nval
        self.v = Zval+Nval
        self.b = BASIS
        self.k = NKval
type = 0
totalout=pd.DataFrame()
caseerror=[]
HEAD = []
carryon = pd.DataFrame()
for ind in range(0,len(quilt.index)):
    current = working(quilt.at[ind,"Z"], quilt.at[ind,"N"], quilt.at[ind,"BASIS"], quilt.at[ind,"nkeep"])
    for type in ['totaltime','reorthog','diagonal','iteration#','lanczos']:
        if type == "totaltime":
            curl=0
        if type == "reorthog":
            curl=1
        if type == "diagonal":
            curl=2
        if type == "iteration#":
            curl=3
        if type == "lanczos":
            curl=4
        calch = float(quilt_H.at[curl,"intercept"]) + quilt_H.at[curl,"B"]*current.b**2 + quilt_H.at[curl,"Nk"] * current.k 
        calcm = float(quilt_M.at[curl, "intercept"]) + quilt_M.at[curl, "V"] * current.v + quilt_M.at[curl, 'Nk'] * current.k
        calcs = float(quilt_S.at[curl,"intercept"]) + quilt_S.at[curl,"Z"] * current.z + quilt_S.at[curl,"N"] * current.n +  current.k * quilt_S.at[curl,"Nk"]
        tryinglist = [calcs,calcm,calch,(errorcalc(calcs, quilt.at[ind,type], "percent")),(errorcalc(calcm, quilt.at[ind,type], "percent")),(errorcalc(calch, quilt.at[ind,type], "percent"))]
        experimental = pd.DataFrame(data=[tryinglist])
        carryon = pd.concat([carryon, experimental], axis = 1, ignore_index=True)
        print("CURRENT CASERROR LIST VALS: \n", carryon)
        if ind == 0:
            HEAD.extend([f"SEER_{type}",f"MAGE_{type}",f"HEIR_{type}",f"SEER_{type}_ERR", f"MAGE_{type}_ERR", f"HEIR_{type}_ERR"])
    print(f"current index is {ind}. \n")
    totalout = pd.DataFrame(pd.concat([totalout, carryon], axis=0))
    carryon = pd.DataFrame()
totalout.to_csv(f'{csvname}_WEAVE.csv', sep=",", header=HEAD)
treble = pd.read_csv(f'{csvname}_WEAVE.csv') #oh but why read the csv instead of just the dataframe wah ?!? trust me you dont want to know 
hdc = pd.concat([quilt.drop(columns = ['Unnamed: 0']),treble], axis=1)
print(hdc)
hdc.to_csv(f'{csvname}_TOTAL_OUT_real.csv', sep=",")