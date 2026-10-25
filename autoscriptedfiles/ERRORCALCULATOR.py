import pandas as pd
import numpy as np
#one may ask, why so many classes?
#my answer is, I have no idea

yourdata = str(input("your data file (csv): "))
actual = pd.read_csv(f"{yourdata}.csv", sep= ',')
yourmodel = str(input("name of your quilt (both csv): "))
quiltM = pd.read_csv(f"{yourmodel}_MAGE.csv")
quiltS = pd.read_csv(f"{yourmodel}_SEER.csv")
diskE = actual
totality=pd.DataFrame()
insist = pd.DataFrame()
class working: #the useable inputs
    def __init__(self,Zval,Nval,NKval):
        self.z = Zval
        self.n = Nval
        self.nk = NKval
class timing: #the timing outputs (for both files)
    def __init__(self, list):
        self.jump = list[0]
        self.reor = list[1]
        self.diag = list[2]
        self.lanc = list[3]
class SEER: #the simple linear regression one
    def __init__(self, zcoefficient, ncoefficient, nkeepcoefficient, interceptval):
        self.zc = zcoefficient
        self.nc = ncoefficient
        self.nkc = nkeepcoefficient
        self.inr = interceptval
plight = SEER(quiltS.iat[0,1], quiltS.iat[0,2], quiltS.iat[0,3], quiltS.iat[0,4])
class MAGE: #multivariable polynomic regression model
    def __init__(self, Zcoef, Ncoef, nkeepcoef, zsquare, zbyn, zbynk, nsquare, nbynk, nksquare, intercept):
        self.ZCOEF_ = Zcoef
        self.NCOEF_ = Ncoef
        self.NKCOEF_ = nkeepcoef
        self.ZSQUARE = zsquare
        self.ZxN = zbyn
        self.ZxNK = zbynk
        self.NSQUARE = nsquare
        self.NxNK = nbynk
        self.NKSQUARE = nksquare
        self.INR = intercept
class error:
    def __init__(self, EXPERIMENTAL, REAL, SEERINPUTS, SEEROUTPUTS):
        self.errorJ = abs((EXPERIMENTAL.jump - REAL.jump)/REAL.jump)
        self.errorR = abs((EXPERIMENTAL.reor - REAL.reor)/REAL.reor)
        self.errorD = abs((EXPERIMENTAL.diag - REAL.diag)/REAL.diag)
        self.errorI = abs((SEERINPUTS - SEEROUTPUTS)/SEEROUTPUTS)
        self.errorL = abs((EXPERIMENTAL.lanc - REAL.lanc)/REAL.lanc)
def calculator(z,n,nk,spellbook):
    ZVAL = z * spellbook.ZCOEF_ 
    NVAL = n * spellbook.NCOEF_
    NKVAL = nk * spellbook.NKCOEF_
    ZSQUARED = (z**2) * spellbook.ZSQUARE
    ZBYN = (z * n) * spellbook.ZxN
    ZBYNK = (z * nk) * spellbook.ZxNK
    NSQUARE = (n**2 ) * spellbook.NSQUARE
    NBYNK = n * nk * spellbook.NxNK
    NKSQUARE = nk **2 * spellbook.NKSQUARE
    experimental = ZVAL + NVAL + NKVAL + ZSQUARED + ZBYN + NSQUARE + NBYNK + NKSQUARE + spellbook.INR
    return experimental
Jspell = MAGE(
            quiltM.at[0,"Z"],
            quiltM.at[0,"N"],
            quiltM.at[0,"nkeep"],
            quiltM.at[0,"Z^2"],
            quiltM.at[0,"Z x N"],
            quiltM.at[0,"Z x nkeep"],
            quiltM.at[0,"N^2"],
            quiltM.at[0,"N x nkeep"],
            quiltM.at[0,"nkeep^2"],
            quiltM.at[0,"intercept"]
                    )
Rspell = MAGE(
            quiltM.at[1,"Z"],
            quiltM.at[1,"N"],
            quiltM.at[1,"nkeep"],
            quiltM.at[1,"Z^2"],
            quiltM.at[1,"Z x N"],
            quiltM.at[1,"Z x nkeep"],
            quiltM.at[1,"N^2"],
            quiltM.at[1,"N x nkeep"],
            quiltM.at[1,"nkeep^2"],
            quiltM.at[1,"intercept"]
                    )
Dspell = MAGE(
            quiltM.at[2,"Z"],
            quiltM.at[2,"N"],
            quiltM.at[2,"nkeep"],
            quiltM.at[2,"Z^2"],
            quiltM.at[2,"Z x N"],
            quiltM.at[2,"Z x nkeep"],
            quiltM.at[2,"N^2"],
            quiltM.at[2,"N x nkeep"],
            quiltM.at[2,"nkeep^2"],
            quiltM.at[2,"intercept"]
                    )
Lspell = MAGE(
            quiltM.at[3,"Z"],
            quiltM.at[3,"N"],
            quiltM.at[3,"nkeep"],
            quiltM.at[3,"Z^2"],
            quiltM.at[3,"Z x N"],
            quiltM.at[3,"Z x nkeep"],
            quiltM.at[3,"N^2"],
            quiltM.at[3,"N x nkeep"],
            quiltM.at[3,"nkeep^2"],
            quiltM.at[3,"intercept"]
                    )

for ind in range(0,len(actual.index)):
    current = working(actual.at[ind,"Z"], actual.at[ind,"N"], actual.at[ind,"nkeep"])
    timers = timing([actual.at[ind, "Jumptime"], 
                        actual.at[ind, "reorthog"], 
                        actual.at[ind, "diagonal"], 
                        actual.at[ind, "lanczos"]
    ])
    JUMPTIME = calculator(current.z,current.n,current.nk,Jspell)
    REORTHOG = calculator(current.z,current.n,current.nk,Rspell)
    DIAGONAL = calculator(current.z,current.n,current.nk,Dspell)
    LANCZOS = calculator(current.z,current.n,current.nk,Lspell)
    experimental = timing([JUMPTIME,REORTHOG,DIAGONAL,LANCZOS])
    SEERinp = actual.at[ind,"iteration#"]
    SEERout = plight.zc * current.z + plight.nc * current.n + plight.nkc * current.nk + plight.inr
    ERRORCALC = error(experimental, timers, SEERinp, SEERout)
    #this little maneuver is going to cost us 51 years
    insert_error = {"Err_Jump": ERRORCALC.errorJ, 
                    "Err_Reorth":ERRORCALC.errorR, 
                    "Err_Diagonal":ERRORCALC.errorD, 
                    "Err_Iteration":ERRORCALC.errorI, 
                    "Err_Lanczos":ERRORCALC.errorL}
    insert_experimental= {"Exp_Jump": experimental.jump,
                          "Exp_Reorth": experimental.reor,
                          "Exp_Diagonal": experimental.diag,
                          "Exp_Iteration": SEERout,
                          "Err_Lanczos": experimental.lanc}
    dfE = pd.DataFrame([insert_error])
    dfC = pd.DataFrame([insert_experimental])
    totality = pd.concat([dfC, dfE], axis = 1)
    insist = pd.concat([insist, totality], axis = 0)
diskE = pd.concat([actual.reset_index(), insist.reset_index()], axis = 1)
diskE = diskE.drop(columns=["index","Unnamed: 0.1","Unnamed: 0","index"])
diskE.to_csv("MAGIC.csv", sep = ",")
    
    


