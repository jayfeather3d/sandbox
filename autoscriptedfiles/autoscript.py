import subprocess


import time
sps = 'fp'
inputfile = 'gx1a'
z = 2
n = 2
jz = 0
nkeep = 10
for a in 'abcdefjhijklmnopqrstuvwxyz':
    b=0
    nkeep=10
    if z <12:
        z=z+1
    if n <12:
        n=n+1
    while nkeep <= 100:
        if z % n != 0:
            jz = 1
        else:
            jz = 0   
        arg1='n      ! menu choice'
        arg2=f"timer{a}_{b}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "
        arg3=f"{sps}    !  name of .sps file "
        arg4=f"           {z}           {n}  ! # of valence protons, neutrons "
        arg5=f"           {jz}        ! 2 x Jz of systems"
        arg6='0     !  LANCZOS FRAGMENT SIZE in millions (0 = use default)'
        arg7=inputfile
        arg8='end'
        arg9='ld'
        arg10=f"          {nkeep}         5000      ! # states to keep, max # iterations "
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
        subprocess.run('./bigstick.x i', shell=True)
        b=b+1
    
