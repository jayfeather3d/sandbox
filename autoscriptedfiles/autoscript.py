print('ONLY RUN WHEN INSIDE OF A /BIN/ FOLDER CONTAINING: BIGSTICK.X, SD.SPS, FP.SPS, GX1A.INT, USDB.INT')
import subprocess
import time
sps = str(input('where it is contained in your ./bin folder, enter .sps name (without the file extension) (fp or sd). \n SD.SPS = Oxygen 8 Core, FP.SPS = Ca 20 Core \n'))
inputfile = str(input('where it is contained in your ./bin folder, enter .int name (without the file extension) (gx1a, usdb). \n check if you are using autoscaling by interpretation of the sign of the first constant in a .int \n'))
if sps == 'fp':
    print('Z, N values <= 20 ONLY')
if sps == 'sd':
    print('Z, N values <= 12 ONLY')
z = int(input('Valence Proton # \n'))
if sps =='fp':
    while z > 20 or z < 2:
        print('z value is out of bounds, re-enter \n')
        z = int(input())
if sps == 'sd':
    while z > 12 or z < 2 :
        print('z value is out of bounds, re-enter \n')
        z = int(input())
n = int(input('Valence Neutron # \n'))
if sps =='fp':
    while n > 20 or m < 2:
        print('z value is out of bounds, re-enter \n')
        n = int(input())
if sps == 'sd':
    while n > 12 or n < 2 :
        print('z value is out of bounds, re-enter \n')
        n = int(input())
if z % n != 0:
    jz = 1
else:
    jz = 0
OUTPUT = str(input('file name, which will be given the suffix _{alphabetic}_{numerals} \n'))
nkeep = int(input('starting nkeep value \n'))
while nkeep < 10:
        nkeep=int(input('You cannot start iterations with values approaching limit. reenter \n'))
maxnkeep = int(input('maximum nkeep value \n'))
while maxnkeep == nkeep:
        maxnkeep = int(input('values cannot be equal, reenter \n'))
if maxnkeep <= 50:
        print('low maxnkeep value, be advised to enter an appropriate resolution. proceeding \n')
diffcharge = int(input('increment of nkeep from one iteration to the next \n'))
if diffcharge <= 5:
        print('very high resolution... \n')
maxnumiter = int(input('enter max # iterations (kept constant) \n be aware values sub ~100 give degenerate or low value cases \n'))
for a in 'abcdefjhijklmnopqrstuvwxyz':
    b=0
    nkeep=10
    if n == 20 and z < 20:
        z=z+1
    if n <= 20:
        n=n+1 
    while nkeep <= maxnkeep:
        if z % n != 0:
            jz = 1
        else:
            jz = 0   
        arg1='n      ! menu choice'
        arg2=f"{OUTPUT}_{a}_{b}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "
        arg3=f"{sps}    !  name of .sps file "
        arg4=f"           {z}           {n}  ! # of valence protons, neutrons "
        arg5=f"           {jz}        ! 2 x Jz of systems"
        arg6='0     !  LANCZOS FRAGMENT SIZE in millions (0 = use default)'
        arg7=inputfile
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
        nkeep = nkeep + 10 
        subprocess.run(args=['./bigstick.x'], shell=True, text=True, input='i')
        print(f"{output}_{a}_{b} finished, power napping")
        time.sleep(3.14159) # :)
        b=b+1
