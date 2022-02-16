
from fileinput import filename
import orjson

from nextcord.ext import commands
import random
import os

bot=commands.Bot(command_prefix="$")

version={"bot order":3,"major":1,"minor":0,"fix":0}
verstr=f'''{version["bot order"]}.{version["major"]}.{version["minor"]}.{version["fix"]}'''

@bot.command()
async def version(ctx):
    await ctx.reply(verstr)

@bot.command()
async def dayget(ctx):
    
    fname=f"data/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    
    reward=[]
    prob=[48,32,16,3,1]
    for j in range(3):
        result=random.random()*100
        sum=0
        for i in range(5):
            sum+=prob[i]
            if result<sum:
                if j==0:
                    reward.append(i+1)
                elif j==1:
                    reward.append(plusend(i+1))
                else:
                    reward.append(plusend(i+1)*100000)
                break
    data=None
    if os.path.isfile(fname):
        with open(fname) as f:
            data=f.readlines()
            data[3]=int(data[3])
            data[reward[0]-1+5]=int(data[reward[0]-1+5])
            data[3]+=reward[2]
            data[reward[0]-1+5]+=reward[1]
        with open(fname) as f:
            for i in data:
                f.write()
    else:
        CreateUser(reward,fname)

    await ctx.reply(f"{reward}")


def CreateUesr(reward,fname):
    with open(fname) as f:
        f.write("level\n1\nmoa\n")
        f.write(f"{reward[2]}\nreinmat\n")
        for i in range(5):
            if i==reward[0]-1:
                f.write(f"{}\n")
        f.write("level\n1\n")
        f.write("level\n1\n")
        f.write("level\n1\n")
    return

def plusend(num):
    sum=0
    for i in range(num):
        sum+=i+1
    return sum

bot.run(open("token.txt").read())