
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
async def inven(ctx):
    fname=f"data/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    data=None
    if os.path.isfile(fname):
        data=ReadInven(fname)
    sendData=""
    for i in data:
        sendData+=i
    await ctx.reply(sendData)

@bot.command()
async def rein(ctx,agree=None):
    fname=f"data/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    data=None
    if os.path.isfile(fname):
        data=ReadInven(fname)
    level=int(data[1])
    moa=int(data[3])
    cost_ingre=[]
    divmod(level,7)
    for i in range(5):
        if level>=i*6+1:
            cost_ingre.append(((level-6*i)//2+1)*level)
            print(cost_ingre)
        else:
            break
    

    cost_moa=1000*(level//5+1)*(level//10+1)*(level//15+1)
    ingre=data[5:5+len(cost_ingre)]

    if agree==None:
        await ctx.reply(f"{cost_ingre} {cost_moa}moa필요\n{ingre} {moa}moa보유")
        return
    elif agree=="agree":
        for i in range(len(ingre)):
            if ingre[i]<cost_ingre[i]:
                ctx.reply("재료 부족")
                return
            else:
                data[5+i]-=cost_ingre[i]
        if moa<cost_moa:
            ctx.reply(f"{cost_moa-moa}모아 부족")
            return
        else:
            data[3]-=cost_moa
        success=99-3*(level-1)
        dice=random.random()*100
        if dice<success:
            ctx.reply("success level+1")
            data[1]+=1
        else:
            ctx.reply("fail")
    data=inttostr(data)
    with open(fname,"w") as f:
        f.writelines(data)

    

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
        data=ReadInven(fname)
        print(data)
        data[3]=str(data[3]+reward[2])+"\n"
        data[reward[0]-1+5]=str(data[reward[0]-1+5]+reward[1])+"\n"
        data=inttostr(data)
        with open(fname,"w") as f:
            f.writelines(data)
    else:
        CreateUser(reward,fname,ctx.author.id)

    await ctx.reply(f"{reward}")

def inttostr(data):
    for i in range(len(data)):
        if type(data[i])==int:
            data[i]=str(data[i])+"\n"
    return data

def ReadInven(fname):
    data=None
    with open(fname,"r") as f:
        data=f.readlines()

    for i in range(len(data)):
        try:
            data[i]=int(data[i])
        except:
            pass
    return data

def CreateUser(reward,fname,userid):
    os.makedirs(f"data/user{userid}")
    with open(fname,"w") as f:
        f.write("level\n1\nmoa\n")
        f.write(f"{reward[2]}\nreinmat\n")
        for i in range(5):
            if i==reward[0]-1:
                f.write(f"{reward[1]}\n")
            else:
                f.write("0\n")
    return

def plusend(num):
    sum=0
    for i in range(num):
        sum+=i+1
    return sum

bot.run(open("token.txt").read())