# used to run wc.py multiple times.  place this file in the same folder as wc.py
import subprocess

# how many times do you want to run wc.py
run_count = 3

# copy flagstring into "flagstring" variable
flagstring = "-cg -cgdepth 2 -sl -oa 2.2.2.2.6.6.4.9.9 -ob 3.1.1.2.9.9.4.12.12 -oc 30.8.8.1.1.11.8 -od 59.1.1.11.31 -sc1 random -sc2 random -sc3 random -sal -eu -csrp 80 125 -fst -brl -slr 3 5 -lmprp 75 125 -lel -srr 25 35 -rnl -rnc -sdr 1 2 -das -dda -dns -sch -scis -com 98989898989898989898989898 -rec1 28 -rec2 27 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2 -hmced 2 -xgced 2 -ase 2 -msl 40 -sed -bbs -drloc shuffle -stloc mix -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 2 5 -ebr 82 -emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 5000 -smc 3 -sto 1 -ieor 33 -ieror 33 -csb 3 14 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 4 -npi -sebr -sesb -ccsr 20 -cms -frw -wmhc -cor -crr -crvr 50 60 -crm -ari -anca -adeh -nmc -noshoes -nu -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -rr -etn -drdc"
flagargs = flagstring.split(" ")

# replace f.smc with what your FF6 is rom named
flagargs.insert(0, "f.smc")
flagargs.insert(0, "-i")
flagargs.insert(0, "wc.py")
flagargs.insert(0, "python")
#print(flagargs)

for x in range(run_count):
    subprocess.run(flagargs)
