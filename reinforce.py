def CheckPercent(level):
    return 99-3*(level-1)


def CheckCost(level):
    cost_ingre=[]
    for i in range(5):
        if level>=i*6+1:
            cost_ingre.append(((level-6*i)//2+1)*level)
            print(cost_ingre)
        else:
            break

    cost_moa=1000*(level//5+1)*(level//10+1)*(level//15+1)*level

    return cost_moa,cost_ingre