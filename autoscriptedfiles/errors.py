import pandas as pd
import numpy as np
yourdata = str(input("your data file (csv)"))
actual = pd.read_csv(f"{yourdata}.csv", sep= ',')
yourmodel = str(input("name of your quilt (csv)"))
quilt = pd.read_csv(f"{yourmodel}.csv")
print(quilt, "\n REVIEW ABOVE VALUES \n")
diskE = actual
insist = pd.DataFrame()
class working:
    def __init__(self,Zval,Nval,NKval):
        self.z = Zval
        self.n = Nval
        self.nk = NKval
class timing:
    def __init__(self, JUMPTIME_T, REORTHOG_T, DIAGONAL_T, ITERATIONNUM, LANCZOS_T):
        self.jump = JUMPTIME_T
        self.reor = REORTHOG_T
        self.diag = DIAGONAL_T
        self.iter = ITERATIONNUM
        self.lanc = LANCZOS_T
class oracle:
    def __init__(self, ZCOEF, NCOEF, NKEEPCOEF, INTERCEPT):
        self.zc = ZCOEF
        self.nc = NCOEF
        self.nkc = NKEEPCOEF
        self.inr = INTERCEPT
class error:
    def __init__(self, expj, realj, expreorth, realreorth, expdiag, realdiag, expiteration, realiteration, explanczos, reallanczos):
        self.errorJ = abs((expj - realj)/realj)
        self.errorR = abs((expreorth - realreorth)/realreorth)
        self.errorD = abs((expdiag - realdiag)/realdiag)
        self.errorI = abs((expiteration - realiteration)/realiteration)
        self.errorL = abs((explanczos - reallanczos)/reallanczos)
jumptester = oracle(quilt.at[0,"Z_coef"], quilt.at[0,"N_coef"], quilt.at[0,"nkeep_coef"], quilt.at[0, "intercept"])
reorthtester = oracle(quilt.at[1,"Z_coef"], quilt.at[1,"N_coef"], quilt.at[1,"nkeep_coef"], quilt.at[2, "intercept"])
diagonaltester = oracle(quilt.at[2,"Z_coef"], quilt.at[2,"N_coef"], quilt.at[2,"nkeep_coef"], quilt.at[2, "intercept"])
iterationtester = oracle(quilt.at[3,"Z_coef"], quilt.at[3,"N_coef"], quilt.at[3,"nkeep_coef"], quilt.at[3, "intercept"])
lanczostimetester = oracle(quilt.at[4,"Z_coef"], quilt.at[4,"N_coef"], quilt.at[4,"nkeep_coef"], quilt.at[4, "intercept"])
for ind in range(0,len(actual.index)):
    current = working(actual.at[ind,"Z"], actual.at[ind,"N"], actual.at[ind,"nkeep"])
    timers = timing(actual.at[ind, "Jumptime"], 
                    actual.at[ind, "reorthog"], 
                    actual.at[ind, "diagonal"], 
                    actual.at[ind, "iteration#"], 
                    actual.at[ind, "lanczos"]
                    )
    #this little maneuvers going to cost us 51 years
    experimental = timing(
        (current.z * jumptester.zc + current.n * jumptester.nc + current.nk * jumptester.nkc + jumptester.inr),
        (current.z * reorthtester.zc + current.n * reorthtester.nc + current.nk * reorthtester.nkc + reorthtester.inr),
        (current.z * diagonaltester.zc + current.n * diagonaltester.nc + current.nk * diagonaltester.nkc + diagonaltester.inr),
        (current.z * iterationtester.zc + current.n * iterationtester.nc + current.nk * iterationtester.nkc + iterationtester.inr),
        (current.z * lanczostimetester.zc + current.n * lanczostimetester.nc + current.nk * lanczostimetester.nkc + lanczostimetester.inr)                  
                        )
    TOTALERROR = error(experimental.jump, timers.jump, 
                       experimental.reor, timers.reor, 
                       experimental.diag, timers.diag, 
                       experimental.iter, timers.iter, 
                       experimental.lanc, timers.lanc )
    #fasten your seatbelt
    INSERTEXPERIMENTAL = {"exp JUMP": experimental.jump,
                        "exp REORTH": experimental.reor, 
                        "exp DIAG": experimental.diag, 
                        "exp ITER": experimental.iter, 
                        "exp LANC": experimental.lanc
                        } 
    INSERTERROR = {"JUMP ERROR": TOTALERROR.errorJ, 
                   "REORTH ERROR": TOTALERROR.errorR,
                   "DIAGO ERROR": TOTALERROR.errorD,
                   "ITER ERROR": TOTALERROR.errorI,
                   "LANC ERROR": TOTALERROR.errorL
                   }
    dfE = pd.DataFrame([INSERTERROR])
    dfC = pd.DataFrame([INSERTEXPERIMENTAL])
    totality = pd.concat([dfC, dfE], axis = 1)
    insist = pd.concat([insist, totality], axis = 0)
diskE = pd.concat([actual.reset_index(), insist.reset_index()], axis = 1)
diskE.to_csv("ding.csv", sep = ",")


    

