import os

def CreateUser(reward,fname,userid):
    modeString=open("secret/modeString.txt").read()
    os.makedirs(f"data/{modeString}/user{userid}")
    with open(fname,"w") as f:
        f.write("level\n1\nmoa\n")
        f.write(f"{reward[2]}\nreinmat\n")
        for i in range(5):
            if i==reward[0]-1:
                f.write(f"{reward[1]}\n")
            else:
                f.write("0\n")