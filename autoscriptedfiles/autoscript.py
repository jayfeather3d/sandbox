print('ONLY RUN WHEN INSIDE OF A /BIN FOLDER CONTAINING: BIGSTICK.X, SD.SPS, FP.SPS, GX1A.INT, USDB.INT')
import subprocess
import time
import pandas as pd
import numpy as np
import re
tallest = pd.DataFrame()
sps = str(input('where it is contained in your ./bin folder, enter .sps name (without the file extension) (fp or sd). \n \n SD.SPS = Oxygen 8 Core \n FP.SPS = Ca 20 Core \n .sps name ---: '))
inputfile = str(input('where it is contained in your ./bin folder, enter .int name (without the file extension) (gx1a, usdb). \n check if you are using autoscaling by interpretation of the sign of the first constant in a .int \n .int name ---: '))
if sps == 'fp':
    print('Z, N values <= 20 ONLY \n \n')
if sps == 'sd':
    print('Z, N values <= 12 ONLY \n \n')
z = int(input('Valence Proton # ---: '))
if sps =='fp':
    while z > 20 or z < 2:
        print('z value is out of bounds, re-enter ---:\n')
        z = int(input())
if sps == 'sd':
    while z > 12 or z < 2 :
        print('z value is out of bounds, re-enter ---: \n')
        z = int(input())
n = int(input('Valence Neutron # ---: '))
if sps =='fp':
    while n > 20 or n < 2:
        print('z value is out of bounds, re-enter ---: \n')
        n = int(input())
if sps == 'sd':
    while n > 12 or n < 2 :
        print('z value is out of bounds, re-enter ---: \n')
        n = int(input())
if z % n != 0:
    jz = 1
else:
    jz = 0
globvarstoragen = n
globvarstoragez = z
output = str(input('file name, which will be given the suffix _{alphabetic}_{numerals} \n'))
nkeep = int(input('starting nkeep value \n'))
while nkeep < 10:
        nkeep=int(input('You cannot start iterations with values approaching experimentally acquired limit.\ please re-enter ---:  \n'))
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
for a in 'abcdefjhijklmnopqrstuvwxyz':
    count=0
    b=0
    nkeep=10
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
    if n == 20 and z < 20:
        z=z+1
        n=globvarstoragen
    if n < 20:
        n=n+1
    if z % n != 0:
        jz = 1
    else:
        jz = 0 
        
