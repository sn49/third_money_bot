from dis import dis
from fileinput import filename
import nextcord
import orjson

from nextcord.ext import commands
import random
import os
import datetime
from secret import opentime
import usermanage
import logmanage
import reinforce

optime = opentime

bot = commands.Bot(command_prefix="$$")

testmode = False
modeString = ""

version = {"bot order": 3, "major": 1, "minor": 2, "fix": 1}
verstr = f"""V{version["bot order"]}.{version["major"]}.{version["minor"]}.{version["fix"]}"""


@bot.event
async def on_message(msg):
    if str(msg.content).startswith(bot.command_prefix):
        now = datetime.datetime.now()
        wd = now.weekday()
        min = now.minute
        if (wd == 0 or wd == 3) and now.hour == 14 and 20 <= min and min < 40:
            await msg.reply(f"점검시간")
            return
        else:
            await bot.process_commands(msg)


@bot.event
async def on_ready():
    global modeString
    global testmode
    if testmode:
        await bot.change_presence(activity=nextcord.Game(name="TESTMODE"))
        bot.command_prefix = "m!"
        print(bot.command_prefix)
    else:
        await bot.change_presence(activity=nextcord.Game(name=verstr))

    try:
        os.makedirs(f"data/{modeString}")
    except:
        pass

    try:
        os.makedirs(f"data/{modeString}/log")
    except:
        pass

    with open("secret/modeString.txt", "w") as f:
        f.write(modeString)


@bot.command()
async def mode(ctx):
    await ctx.send(modeString)


@bot.command()
async def version(ctx):
    await ctx.reply(verstr)


@bot.command()
async def inven(ctx):
    global modeString
    fname = f"data/{modeString}/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    data = None
    if os.path.isfile(fname):
        data = ReadInven(fname)
    sendData = ""
    data = inttostr(data)
    for i in data:
        sendData += i
    await ctx.reply(sendData)


@bot.command()
async def rein(ctx, agree=None):
    global modeString
    fname = f"data/{modeString}/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    data = None
    if os.path.isfile(fname):
        data = ReadInven(fname)
    level = data[1]


    if modeString == "test":
        maxlevel = 13
    elif modeString == "main":
        maxlevel = 7

    if level == maxlevel:
        await ctx.reply("최고 레벨")
        return

    moa = data[3]

    cost_moa, cost_ingre = reinforce.CheckCost(level)
    ingre = data[5 : 5 + len(cost_ingre)]
    success = reinforce.CheckPercent(level)

    res = [success, level]
    if agree == None:
        await ctx.reply(
            f"{cost_ingre} {cost_moa}moa필요\n{ingre} {moa}moa보유\n확률 : {success}%"
        )
        return
    elif agree == "agree":

        for i in range(len(ingre)):
            if ingre[i] < cost_ingre[i]:
                await ctx.reply("재료 부족")
                return
            else:
                data[5 + i] -= cost_ingre[i]
        if moa < cost_moa:
            await ctx.reply(f"{cost_moa-moa}모아 부족")
            return
        else:
            data[3] -= cost_moa

        dice = random.random() * 100
        if dice < success:
            await ctx.reply("success level+1")
            data[1] += 1
            res.append("성공")
        else:
            ctx.reply("fail")
            res.append("실패")

    data = inttostr(data)
    with open(fname, "w") as f:
        f.writelines(data)

    logmanage.CreateLog(ctx.author.id, "rein", res)


@bot.command()
async def log(ctx, date, command):
    if len(date) == 8:
        await ctx.reply(logmanage.CheckLog(ctx.author.id, date, command))


@bot.command()
async def split(ctx, number, amount, agree=None):
    global modeString

    fname = f"data/{modeString}/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    data = None
    if os.path.isfile(fname):
        data = ReadInven(fname)

    try:
        number = int(number)
        amount = int(amount)
    except:
        await ctx.reply("숫자 2개를 입력")
        return

    if number >= 2 and number <= 5:
        if agree == "agree":
            if amount > 0:
                if data[5 + int(number) - 1] >= amount:
                    data[5 + int(number) - 1] -= amount
                    data[5 + int(number) - 2] += (1 + 2 * (number - 2)) * amount
                    data = inttostr(data)

                    with open(fname, "w") as f:
                        f.writelines(data)

                    logmanage.CreateLog(ctx.author.id, "split", [number, amount])

                    await ctx.reply(
                        f"{number}성 재료 {amount}개를 분해하여 {number-1}성 재료 {(1 + 2 * (number - 2))*amount}개 획득"
                    )

        else:
            await ctx.reply(
                f"{number}성 재료 {amount}개를 분해하여 {number-1}성 재료 {(1 + 2 * (number - 2))*amount}개 획득 가능"
            )
            return


@bot.command()
async def dayget(ctx):
    global modeString
    now = datetime.datetime.now()
    today = f"{now.year}-{now.month}-{now.day}"
    fname = f"data/{modeString}/user{ctx.author.id}/userinfo{ctx.author.id}.data"
    fname2 = f"data/{modeString}/user{ctx.author.id}/dailygift{ctx.author.id}.data"
    if os.path.isfile(fname2):
        with open(fname2, "r") as f:
            if f.readlines()[1] == today:
                await ctx.reply("이미 받음")
                return

    reward = []
    prob = [48, 32, 16, 3, 1]
    for j in range(3):
        result = random.random() * 100
        sum = 0
        for i in range(5):
            sum += prob[i]
            if result < sum:
                if j == 0:
                    reward.append(i + 1)
                elif j == 1:
                    reward.append(plusend(i + 1))
                else:
                    reward.append(plusend(i + 1) * 100000)
                break
    data = None
    if os.path.isfile(fname):
        data = ReadInven(fname)
        print(data)
        data[3] = str(data[3] + reward[2]) + "\n"
        data[reward[0] - 1 + 5] = str(data[reward[0] - 1 + 5] + reward[1]) + "\n"
        data = inttostr(data)
        with open(fname, "w") as f:
            f.writelines(data)
    else:
        usermanage.CreateUser(reward, fname, ctx.author.id)
    with open(fname2, "w") as f:
        f.writelines("dayget\n" + today)

    logmanage.CreateLog(ctx.author.id, "dayget", reward)

    await ctx.reply(f"{reward}")


def inttostr(data):
    for i in range(len(data)):
        if type(data[i]) == int:
            data[i] = str(data[i]) + "\n"
    return data


def ReadInven(fname):
    data = None
    with open(fname, "r") as f:
        data = f.readlines()

    for i in range(len(data)):
        try:
            data[i] = int(data[i])
        except:
            pass
    return data


def CreateUser(reward, fname, userid):
    os.makedirs(f"data/{modeString}/user{userid}")
    os.makedirs(f"data/{modeString}/user{userid}/log")
    with open(fname, "w") as f:
        f.write("level\n1\nmoa\n")
        f.write(f"{reward[2]}\nreinmat\n")
        for i in range(5):
            if i == reward[0] - 1:
                f.write(f"{reward[1]}\n")
            else:
                f.write("0\n")


def plusend(num):
    sum = 0
    for i in range(num):
        sum += i + 1
    return sum


if input("test입력시 test모드") == "test":
    testmode = True
    modeString = "test"
    bot.run(open("secret/test_token.txt").read())

else:
    testmode = False
    modeString = "main"
    bot.run(open("secret/token.txt").read())
