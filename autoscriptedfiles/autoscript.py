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
                    
        """                                                                                                   
      
      )
debugq = str(input("\n-----:"))
skiptoend="n"
if debugq == "d":
    skiptoend = str(input("skip to end? only works if you ran previously. y/n:"))
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
    globvarstoragen = n
    globvarstoragez = z
if debugq == "n":
    skiptoend="n"
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
if skiptoend == "n":
    for a in 'abcdefjhijklmnopqrstuvwxyz':
        b=0
        nkeep=nkeepstar
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
                    enter = int(df.iloc[x+1].item().strip())
                    np1 = enter#Because the values of np1 and np2 seem to not actually be reflecting what was input in the bigstick when exported to the logs i have written so that these values taken in from the log are not used.
                if "Valence N =" in current:
                    enter = int(df.iloc[x+1].item().strip())
                    np2 = enter        
                if "Total time to run :" in current:
                    enter = float(df.iloc[x+1].item().strip())
                    tt = enter 
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
                if "Total basis dimension:" in current:
                    dummy = df.iloc[x].item().strip()
                    enter = re.sub(r"[Total basis dimension:]", "", dummy)
                    BASIS=enter
            V=z+n
            headers = ["Z", "N","V","BASIS", "nkeep", "totaltime", "reorthog", "diagonal", "iteration#", "lanczos"]
            if lanczos > 0:
                tiles = [z,n,V,BASIS,nkeep,tt,reorth,diagonal,iterations,lanczos]
                hold = dict(zip(headers, tiles))
                tall = pd.DataFrame(hold, index=[1])
                #tall.to_csv(f"tiled_{output}_{a}_{b}.csv")
                #unfortunately this makes a lot of files...
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
                
                tallest = pd.concat([pd.read_csv(f"tiled_{output}_{a}_{b}.csv"), tallest])
                tallest.to_csv(f"{csvname}_QUILT.csv")
                print("\n \n ---------------------- total csv written ---------------------------------- \n \n")
            else:
                print(f"!+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n failed case!!! \n continuing to next set \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+! \n !+!+!+!+!+!+!+!+!+!\n") 
            nkeep=nkeep + 10 
            b=b+1
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
if place == "y":
    from sklearn.linear_model import LinearRegression
    import sys
    intake = pd.read_csv(f"{csvname}_QUILT.csv")
    VIndependentVariables = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Z','N','BASIS','totaltime','reorthog','diagonal','iteration#','lanczos'])
    SIndependentVariables = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','BASIS','V','totaltime','reorthog','diagonal','iteration#','lanczos'])
    #SIn = Z,N,NK
    #Vin = V,Nk
    BasisNkIn = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Z','N','V','totaltime','reorthog','diagonal','iteration#','lanczos'])
    #BasisNkIn = Only basis, nk
    DependentVariables = intake.drop(columns=['Unnamed: 0.1', 'Unnamed: 0','Z','N','V','BASIS','nkeep'])
    #seer = Sin -> Z & N + nk linear
    #mage = Vin -> V + nk linear
    #heir = Bin -> basis + nk linear
    seer=LinearRegression()
    mage=LinearRegression()
    heir=LinearRegression()
    seer.fit(SIndependentVariables, DependentVariables)
    seercol = ["Z","N","nkeep"]
    mage.fit(VIndependentVariables, DependentVariables)
    magecol = ["V","nkeep"]
    heir.fit(BasisNkIn, DependentVariables)
    heircol = ["BASIS","nkeep"]
    def EXPORT(modelN, colname):
        exportercoef = pd.DataFrame.from_records(data=modelN.coef_, index=['totaltime','reorthog','diagonal','iteration#','lanczos'], columns=colname)
        exporterinter = pd.DataFrame(data=modelN.intercept_.tolist(), index=['totaltime','reorthog','diagonal','iteration#','lanczos'], columns=["intercept"])
        exporter = pd.concat([exportercoef, exporterinter], axis=1)
        return exporter 
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
print("BEGINNING DELPHI----------------------\n\n\n\n")
quilt = pd.read_csv(f"{csvname}_QUILT.csv")
quilt_M = pd.read_csv(f"{csvname}_MAGE.csv")
quilt_S = pd.read_csv(f"{csvname}_SEER.csv")
quilt_H = pd.read_csv(f"{csvname}_HEIR.csv")
diskE = quilt
ENT1=pd.DataFrame()
ENT2=pd.DataFrame()
# WHY is it all classes?, I DONT KNOW
class working: #the useable inputs
    def __init__(self,Zval,Nval,BASIS,NKval):
        self.z = Zval
        self.n = Nval
        self.v = Zval+Nval
        self.b = BASIS
        self.k = NKval
class MODEL:
    def __init__(self, hopto):
        self._Z = hopto[0]
        self._N = hopto[1]
        self._V = hopto[2]
        self._B = hopto[3]
        self._K = hopto[4]
        self._INTERCEPT = hopto[5]
def CALCULATOR(current,coef):
    calced = (current.z * coef._Z) + (current.n * coef._N) + (current.v * coef._V) + (current.b * coef._B) + (current.k * coef._K) + coef._INTERCEPT
    return calced
def errorcalc(exp, real, type):
    match type:
        case "percent":
            out = abs((exp - real)/real * 100)
        case "relative":
            out = abs((exp-real)/real)
        case "absolute":
            out = abs(exp-real)
    return out
# according to:
    #seer = Sin -> Z & N + nk linear
    #mage = Vin -> V + nk linear
    #heir = Bin -> basis + nk linear
#inputs in order: Z,N,V (calculated), BASIS,NK
#IF MISSING AN INPUT, JUST INPUT AS 0
type = 0
totalout=pd.DataFrame()
caseerror=[]
carryon = pd.DataFrame()
HEAD = []

for ind in range(0,len(quilt.index)):
    current = working(quilt.at[ind,"Z"], quilt.at[ind,"N"], quilt.at[ind,"BASIS"], quilt.at[ind,"nkeep"])
    for type in ['totaltime','reorthog','diagonal','iteration#','lanczos']:
        #'Z','N','V','BASIS','nkeep'
        match type:
            case "totaltime":
                curl=0
            case "reorthog":
                curl=1
            case "diagonal":
                curl=2
            case "iteration#":
                curl=3
            case "lanczos":
                curl=4
        SEER_M = MODEL([quilt_S.at[curl,"Z"], quilt_S.at[curl,"N"], 0, 0, quilt_S.at[curl,"nkeep"], quilt_S.at[curl,"intercept"]])   
        MAGE_M = MODEL([0,0, quilt_M.at[curl,"V"], 0, quilt_M.at[curl,"nkeep"], quilt_M.at[curl,"intercept"]])
        HEIR_M = MODEL([0,0,0,quilt_H.at[curl,"BASIS"], quilt_H.at[curl,"nkeep"], quilt_H.at[curl,"intercept"]])
        #basically our weights
        tryinglist = [CALCULATOR(current, SEER_M),CALCULATOR(current, MAGE_M),CALCULATOR(current, HEIR_M),(errorcalc(CALCULATOR(current, SEER_M), quilt.at[ind,type], "percent")),(errorcalc(CALCULATOR(current, MAGE_M), quilt.at[ind,type], "percent")),(errorcalc(CALCULATOR(current, HEIR_M), quilt.at[ind,type], "percent"))]
        experimental = pd.DataFrame(data=[tryinglist])
        carryon = pd.concat([carryon, experimental], axis = 1, ignore_index=True)
        print("CURRENT CASERROR LIST VALS: \n", carryon)
        if ind == 0:
            HEAD.extend([f"SEER_{type}",f"MAGE_{type}",f"HEIR_{type}",f"SEER_{type}_ERR", f"MAGE_{type}_ERR", f"HEIR_{type}_ERR"])
    print(f"current index is {ind}. \n")
    totalout = pd.DataFrame(pd.concat([totalout, carryon], axis=0))
    carryon = pd.DataFrame()
totalout.to_csv(f'{csvname}_WEAVE.csv', sep=",", header=HEAD)

#Now we take it back in :) this is just easier than pandas reindex nonsense
cryostat = pd.read_csv(f'{csvname}_WEAVE.csv')
mudkip = pd.concat([quilt,cryostat], axis=1)
print(mudkip)
mudkip.to_csv(f'{csvname}_TOTAL_OUT_real.csv', sep=",")