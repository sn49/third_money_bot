import os
import datetime



def CheckToday(now):
    y = now.year
    m = str(now.month).zfill(2)
    d = str(now.day).zfill(2)

    return f"{y}-{m}-{d}"


def CheckTime(now):
    ho = str(now.hour).zfill(2)
    mi = str(now.minute).zfill(2)
    se = str(now.second).zfill(2)

    return f"{ho}-{mi}-{se}"


def CheckMode():
    return open("secret/modeString.txt").read()


def CreateLog(userid, command, result):
    print(result)
    modeString = CheckMode()

    now = datetime.datetime.now()

    today = CheckToday(now)
    time = CheckTime(now)

    dname = f"data/{CheckMode()}/user{userid}/log/{today}"

    if not os.path.isdir(dname):
        os.makedirs(dname)

    fname = f"data/{modeString}/user{userid}/log/{today}/{time}-{command}.mylog"

    with open(fname, "w", encoding="UTF-8") as f:
        if command == "dayget":
            f.write(f"{result[0]}성 재료 {result[1]}개와 {result[2]}모아 획득")
        elif command == "rein":
            f.write(f"확률 {result[0]}%의 {result[1]} >> {result[1]+1} 결과 : {result[2]}")
        elif command == "split":
            f.write(
                f"{result[0]}성 재료 {result[1]}개를 분해하여 {result[0]-1}성 재료 {(1 + 2 * (result[0] - 2))*result[1]}개 획득"
            )

    return


def CheckLog(userid, date, command):
    checkdate = f"{date[0:4]}-{date[4:6]}-{date[6:]}"
    dirname = f"data/{CheckMode()}/user{userid}/log/{checkdate}"

    sendlist = []
    for i in os.listdir(dirname):
        if command in i:
            with open(
                f"data/{CheckMode()}/user{userid}/log/{checkdate}/{i}", encoding="UTF-8"
            ) as f:
                sendlist.append(f.read())

    return sendlist
