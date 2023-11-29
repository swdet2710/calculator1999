#vision 2.3.0
import math
import time
from itertools import permutations

#####             声明
#    本计算器材料的掉率以及价值参考均取自NGA的伴春风而归的材料掉率共建表，本计算器不用于任何商业用途，仅供交流使用
#    使用的是截止11月29日所记录的掉率
#####
value_list = {'颤颤之齿':3.49,'苦盐簇':2.31,'破碎骨片':2.04,'银原矿石':1.86,'清扫咒':1.57 ,'利齿子儿':0.00286,'启寤I':1/400,
              '液化战栗':10.47,'精磨苦盐':9.24,'未知种根骨':8.17,'粗糙银锭':7.44 ,'幸运咒语':6.27,'罗马金币':17.49,
              '百灵百验鸟':25.09,'祝圣秘银':32.80,'双头形骨架':31.95,'盐封曼德拉':35.88,'齿咬盒':37.68,'金爪灵摆':47.39,
              '铂金通灵板':225.99,'狂人絮语':147.02,'银光子弹':166.23,'幼骨龙标本':171.20,'不腐猴爪':171.53,'床下怪物':196.01,
              '金羊毛':515.88,'长青剑':473.61,'分辨善恶之果':467.90,'不休轮':10.46,'干蝉翼':10.62,'弯曲鹅颈':37.66,
              '砂金甲虫':51.32,'翼造门钥':41.09,'赤金罗盘':230.43,'轮与轴之芯':183.47,'微光蛾翼灯':195.02,'双蛇权杖':497.20,'微尘':0.00194}

dirc_list = {'颤颤之齿':1,'苦盐簇':2,'破碎骨片':3,'银原矿石':4,'清扫咒':5,'利齿子儿':37,'启寤I':38,
              '液化战栗':6,'精磨苦盐':7,'未知种根骨':9,'粗糙银锭':10,'幸运咒语':11,'罗马金币':12,
              '百灵百验鸟':14,'祝圣秘银':15,'双头形骨架':16,'盐封曼德拉':17,'齿咬盒':18,'金爪灵摆':19,
              '铂金通灵板':26,'狂人絮语':27,'银光子弹':28,'幼骨龙标本':29,'不腐猴爪':30,'床下怪物':31,
              '金羊毛':32,'长青剑':33,'分辨善恶之果':34,'不休轮':8,'干蝉翼':13,'弯曲鹅颈':20,'砂金甲虫':21,
              '翼造门钥':22,'赤金罗盘':23,'轮与轴之芯':24,'微光蛾翼灯':25,'双蛇权杖':35,'微尘':36}
de_dirc_list = {}
for s in dirc_list:
    de_dirc_list[dirc_list[s]] = s

class Sets:
    def __init__(self):
        self.value_type = 1.2
        self.difficult = 1
# print(
#    '已知问题: 分辨善恶果进行任意数量计算均至少需要10分钟'
# )
sets = Sets()
class SysFuntion:
    def __init__(self):
        self.get = False
        self.function=None
        self.args = None
class Level:
    def __init__(self, cost, name):
        self.cost = cost
        self.value = 0
        self.gets = {}
        self.getones = {}
        self.name = name

    def addget(self, name, pb):
        self.gets[dirc_list[name]] = pb
        self.value += value_list[name] * pb
        self.getones[dirc_list[name]] = 1.0 / pb
        # print(1.0/pb)

    def getone(self, name):
        # print(self.getones[name])
        return self.getones[name]

    def playsum(self, ps, sums=1.0):
        for i in self.gets:
            ps[i] = ps.get(i, 0.0) + self.gets[i] * sums

    def deplaysum(self, ps: dict, sums=1.0):
        for i in self.gets:
            if ps.get(i, 0.0):
                ps[i] = ps[i] - self.gets[i] * sums
                if ps[i] <= 0:
                    ps.pop(i)


class Material:
    def __init__(self, name):
        self.level_list = []
        self.name = dirc_list[name]
        self.next = {}
        # self.value = 0

    def addk(self, name, sums):
        self.next[dirc_list[name]] = sums
        # self.value +=

    def getnext(self, sums, p, pops=True):
        if sums < 0:
            return
        p[self.name] = p[self.name] - sums
        if pops and p[self.name] <= 0:
            p.pop(self.name)
        for i in self.next:
            p[i] = p.get(i, 0.0) + self.next[i] * sums


Materials = {}
Materials2 = {}
Levels = []

getsolve = False
bestsolves = []
mincost = 0
mincostvalue = 0

valuesolves = []
valuelevel = 0
minvaluecost = 0


def init():
    global getsolve, bestsolves, mincost, mincostvalue, valuesolves, valuelevel, minvaluecost
    getsolve = False
    bestsolves = []
    mincost = 0
    mincostvalue = 0

    valuesolves = []
    valuelevel = 0
    minvaluecost = 0


def solve_leveldeep(perm, level_list: dict, cost=0.0, value=0.0):
    global mincost, bestsolves, minvaluecost, valuelevel, valuesolves, getsolve, mincostvalue
    # f = perm.copy()
    if not perm:
        return
    i = None
    for i in perm:
        if Materials2[i].level_list:
            break
    # print(i,len(perm))

    # mincos = 0
    # maxval = 0
    # play = [0,0]
    for j in Materials2[i].level_list:
        # play_sum = math.ceil(j.getone(i) * perm[i])
        # addcost = cost +j.cost * play_sum
        # if  addcost < mincos or not mincos:
        #    mincos = addcost
        #    play[0] = j
        # valueadd = value + j.value * play_sum
        # if valueadd/addcost > maxval:
        #    maxval = valueadd/addcost
        #    play[1] = j

        # level_list2[j.name] = level_list2.get(j.name, 0.0) + play_sum
        # j.deplaysum(ff, play_sum)
        # for j in play:

        play_sum = math.ceil(j.getone(i) * perm[i])

        cost += j.cost * play_sum
        value += j.value * play_sum
        if mincost and ((cost > mincost and (valuelevel and valuelevel > value / cost)) or cost > mincost * sets.value_type):
            cost -= j.cost * play_sum
            value -= j.value * play_sum
            continue
        ff = perm.copy()
        level_list2 = level_list.copy()
        level_list2[j.name] = level_list2.get(j.name, 0.0) + play_sum
        j.deplaysum(ff, play_sum)
        # print(ff)
        if len(ff):
            solve_leveldeep(ff, level_list2.copy(), cost, value)
        else:
            if not mincost or cost < mincost:
                bestsolves = level_list2.copy()
                mincost = cost
                getsolve = True
                mincostvalue = value / cost
            elif cost == mincost:
                if mincostvalue < value / cost:
                    bestsolves = level_list2.copy()
                    mincostvalue = value / cost
                getsolve = True

            if (not valuelevel or valuelevel < value / cost) and cost < mincost * sets.value_type:
                valuesolves = level_list2.copy()
                valuelevel = value / cost
                minvaluecost = cost
                getsolve = True
            elif valuelevel == value / cost:
                if cost < minvaluecost:
                    valuesolves = level_list2.copy()
                    minvaluecost = cost
                getsolve = True
            if minvaluecost > cost * sets.value_type:
                valuesolves = level_list2.copy()
                valuelevel = value / cost
                minvaluecost = cost
                getsolve = True
        # print(valuesolves,minvaluecost,cost,mincost)
        cost -= j.cost * play_sum
        value -= j.value * play_sum


def solve_level(needs_sum):
    # for perm2 in permutations(needs):
    #    perm = {}
    #    # print(perm2,needs)
    #    for i in perm2:
    #       perm[i] = needs[i]
    # print(needs)
    needs = {}
    for i in needs_sum:
        if needs_sum[i] > 0:
            needs[i] = needs_sum[i]
    if not needs:
        return True
    solve_leveldeep(needs, {})
    return False


def get_lists2(needs_sum, dircs):
    # print(len(dircs))
    fs = True
    for i in needs_sum:
        if Materials2[i].next:
            f = needs_sum.copy()
            if fs:
                for j in f:
                    if Materials2[j].next:
                        high_level = {}
                        low_level = {}

                        for k in needs_sum:
                            if sets.difficult == 3:
                                high_level[k] = needs_sum[k]
                            elif Materials2[k].next and needs_sum[k] > 0:
                                if sets.difficult == 2:
                                    high_level[k] = needs_sum[k]
                                else:
                                    o = True
                                    for e in Materials2[k].next:
                                        if Materials2[e].next:
                                            high_level[k] = needs_sum[k]
                                            o = False
                                            break
                                    if o:
                                        low_level[k] = needs_sum[k]
                            else:
                                low_level[k] = needs_sum[k]
                        for perm in permutations(high_level):
                            perm2 = {}
                            for k in perm:
                                perm2[k] = needs_sum[k]
                            for k in low_level:
                                perm2[k] = low_level[k]
                            dircs.append(perm2)
                        Materials2[i].getnext(f[i], f)
                        t = True
                        for y in dircs:
                            if y == f:
                                t = False
                        if t:
                            get_lists2(f, dircs)
                        break
                fs = False


# def get_lists(needs_sum,dircs):
#    for i in needs_sum:
#       for perm in permutations(i):
#          perm2 = {}
#          for j in perm:
#             # if Materials2[i].next:
#             #    for j in Materials2[i].next:
#             #       if Materials2[j].next:
#             #          f = needs_sum.copy()
#             #          Materials2[i].getnext(f[i],f)
#             #          dircs.append(f)
#             #          get_lists2(f,dircs)
#             perm2[j] = i[j]
#          dircs.append(perm2)
def clock(times):
    timem = 0
    timeh = 0
    strs = ''
    if times > 60:
        timem = times // 60
        times = times - timem * 60
    if timem > 60:
        timeh = timem // 60
        timem = timem - timeh * 60
    if timeh > 0:
        strs = '{0:.2f}'.format(timeh) + '小时'
    if timem > 0:
        strs = strs + '{0:.2f}'.format(timem) + '分钟'
    strs = strs + '{0:.2f}'.format(times) + '秒                                           '
    return strs


def solve(needs):
    global getsolve
    needs_sum = {}
    for i in needs:
        needs_sum[dirc_list[i]] = needs[i]
    getsolve = False
    keep = True
    while keep:
        keep = False
        f = needs_sum.copy()
        for i in needs_sum:
            if f[i] > 0 and not Materials2[i].level_list:
                # print(needs_sum,i)
                Materials2[i].getnext(f[i], f)
                keep = True
        needs_sum = f.copy()
    # print(needs_sum)
    if solve_level(needs_sum):
        return '材料已经可以一键合成！'

    # perm = []
    perm = []
    get_lists2(needs_sum, perm)
    # get_lists(perm3, perm)
    sums = 1
    t = 0
    # print(len(perm))
    time1 = time.time()
    # print(len(perm3))
    for perm2 in perm:
        if time.time() - time1:
            t = (time.time() - time1) * (len(perm) - sums) / sums
        # print(t,sums,len(perm),(time.time() - time1))
        print('完成{0:.2f}%,预计还需'.format(sums / len(perm) * 100)+clock(t),end='\r')
        sums += 1
        for i in perm2.copy():
            if Materials2[i].next:
                getsolve = True
                while perm2.get(i, 0) > 0 and getsolve:
                    getsolve = False
                    # print(perm,Materials2[i].name)
                    Materials2[i].getnext(1, perm2)
                    if solve_level(perm2):
                        return '材料已经可以一键合成！'



def initcl(f):
    for i in Levels:
        if i.gets.get(f.name, 0.0) > 0:
            # print(f.name,i.name)
            f.level_list.append(i)
            # print(i.gets.get(f.name, 0.0))


def initclanddts():
    p = Level(18, '5-4普通')
    p.addget('砂金甲虫', 0.2832)
    p.addget('液化战栗', 0.0075)
    p.addget('精磨苦盐', 0.0045000000000000005)
    p.addget('未知种根骨', 0.1386)
    p.addget('粗糙银锭', 0.0015)
    Levels.append(p)
    p = Level(18, '5-3厄险')
    p.addget('翼造门钥', 0.2836)
    p.addget('未知种根骨', 0.28800000000000003)
    p.addget('银原矿石', 0.7048000000000001)
    p.addget('破碎骨片', 1.2185)
    Levels.append(p)
    p = Level(18, '5-4厄险')
    p.addget('弯曲鹅颈', 0.3028)
    p.addget('粗糙银锭', 0.5361)
    p.addget('清扫咒', 0.6790999999999999)
    p.addget('液化战栗', 0.020099999999999996)
    p.addget('精磨苦盐', 0.026699999999999998)
    p.addget('未知种根骨', 0.0294)
    p.addget('幸运咒语', 0.0495)
    p.addget('干蝉翼', 0.0274)
    p.addget('不休轮', 0.0227)
    Levels.append(p)
    p = Level(18, '5-5厄险')
    p.addget('祝圣秘银', 0.34759999999999996)
    p.addget('液化战栗', 0.1966)
    p.addget('银原矿石', 0.6524)
    p.addget('颤颤之齿', 0.5726)
    Levels.append(p)
    p = Level(18, '5-7厄险')
    p.addget('双头形骨架', 0.3544)
    p.addget('未知种根骨', 0.25739999999999996)
    p.addget('破碎骨片', 1.2953999999999999)
    Levels.append(p)
    p = Level(18, '5-8厄险')
    p.addget('百灵百验鸟', 0.4771)
    p.addget('精磨苦盐', 0.2418)
    p.addget('清扫咒', 0.5163)
    p.addget('苦盐簇', 0.7712)
    Levels.append(p)
    p = Level(18, '5-9厄险')
    p.addget('盐封曼德拉', 0.2774)
    p.addget('粗糙银锭', 0.5032)
    p.addget('苦盐簇', 0.7290000000000001)
    p.addget('液化战栗', 0.0194)
    p.addget('精磨苦盐', 0.0581)
    p.addget('未知种根骨', 0.0452)
    p.addget('幸运咒语', 0.0452)
    p.addget('干蝉翼', 0.0258)
    p.addget('不休轮', 0.006500000000000001)
    Levels.append(p)
    p = Level(18, '5-14厄险')
    p.addget('金爪灵摆', 0.2963)
    p.addget('幸运咒语', 0.1481)
    p.addget('银原矿石', 0.6840999999999999)
    p.addget('清扫咒', 0.7342)
    Levels.append(p)
    p = Level(18, '5-19厄险')
    p.addget('银光子弹', 0.0213)
    p.addget('齿咬盒', 0.3207)
    p.addget('银原矿石', 0.7025)
    p.addget('液化战栗', 0.10189999999999999)
    Levels.append(p)
    p = Level(16, '4-6普通')
    p.addget('弯曲鹅颈', 0.2656)
    p.addget('幸运咒语', 0.1563)
    p.addget('清扫咒', 1.3906)
    Levels.append(p)
    p = Level(16, '4-18普通')
    p.addget('翼造门钥', 0.305)
    p.addget('银原矿石', 0.6823999999999999)
    p.addget('精磨苦盐', 0.1447)
    p.addget('苦盐簇', 0.3726)
    Levels.append(p)
    p = Level(18, '4-4厄险')
    p.addget('液化战栗', 0.6568999999999999)
    p.addget('幸运咒语', 0.902)
    p.addget('清扫咒', 0.7059000000000001)
    Levels.append(p)
    p = Level(18, '4-5厄险')
    p.addget('精磨苦盐', 0.7115)
    p.addget('粗糙银锭', 0.6923)
    p.addget('银原矿石', 0.7212000000000001)
    p.addget('苦盐簇', 0.33649999999999997)
    Levels.append(p)
    p = Level(18, '4-10厄险')
    p.addget('齿咬盒', 0.3)
    p.addget('粗糙银锭', 0.525)
    p.addget('银原矿石', 0.6625)
    p.addget('液化战栗', 0.0167)
    p.addget('幸运咒语', 0.0583)
    p.addget('精磨苦盐', 0.0417)
    p.addget('未知种根骨', 0.0292)
    p.addget('干蝉翼', 0.0333)
    p.addget('不休轮', 0.0333)
    Levels.append(p)
    p = Level(18, '4-11厄险')
    p.addget('百灵百验鸟', 0.4456)
    p.addget('未知种根骨', 0.33159999999999995)
    p.addget('破碎骨片', 1.1519)
    p.addget('清扫咒', 0.5215)
    Levels.append(p)
    p = Level(18, '4-13厄险')
    p.addget('祝圣秘银', 0.3475)
    p.addget('精磨苦盐', 0.2202)
    p.addget('银原矿石', 0.6393)
    p.addget('苦盐簇', 0.7984)
    Levels.append(p)
    p = Level(18, '4-16厄险')
    p.addget('幸运咒语', 2.0395)
    p.addget('液化战栗', 0.0526)
    p.addget('精磨苦盐', 0.0395)
    p.addget('未知种根骨', 0.0329)
    p.addget('粗糙银锭', 0.0329)
    Levels.append(p)
    p = Level(18, '4-20厄险')
    p.addget('双头形骨架', 0.3358)
    p.addget('幸运咒语', 0.4393)
    p.addget('破碎骨片', 0.6659999999999999)
    p.addget('清扫咒', 2.0136000000000003)
    Levels.append(p)
    p = Level(18, '4-21厄险')
    p.addget('盐封曼德拉', 0.2992)
    p.addget('液化战栗', 0.2102)
    p.addget('颤颤之齿', 0.5821999999999999)
    p.addget('苦盐簇', 0.7034999999999999)
    Levels.append(p)
    p = Level(14, '3-3普通')
    p.addget('翼造门钥', 0.2614)
    p.addget('银原矿石', 0.7404000000000001)
    p.addget('液化战栗', 0.019299999999999998)
    p.addget('精磨苦盐', 0.0246)
    p.addget('未知种根骨', 0.019299999999999998)
    p.addget('粗糙银锭', 0.0333)
    p.addget('幸运咒语', 0.038599999999999995)
    p.addget('干蝉翼', 0.0368)
    p.addget('不休轮', 0.021099999999999997)
    Levels.append(p)
    p = Level(14, '3-9普通')
    p.addget('弯曲鹅颈', 0.2545)
    p.addget('清扫咒', 0.7454999999999999)
    p.addget('液化战栗', 0.0143)
    p.addget('精磨苦盐', 0.0358)
    p.addget('未知种根骨', 0.0287)
    p.addget('粗糙银锭', 0.043)
    p.addget('幸运咒语', 0.050199999999999995)
    p.addget('干蝉翼', 0.025099999999999997)
    p.addget('不休轮', 0.0072)
    Levels.append(p)
    p = Level(14, '3-15普通')
    p.addget('砂金甲虫', 0.1997)
    p.addget('破碎骨片', 0.8049)
    p.addget('液化战栗', 0.0183)
    p.addget('精磨苦盐', 0.0229)
    p.addget('未知种根骨', 0.0351)
    p.addget('粗糙银锭', 0.0412)
    p.addget('幸运咒语', 0.06709999999999999)
    p.addget('干蝉翼', 0.042699999999999995)
    p.addget('不休轮', 0.0229)
    Levels.append(p)
    p = Level(18, '3-3厄险')
    p.addget('金爪灵摆', 0.2414)
    p.addget('银原矿石', 0.7056999999999999)
    p.addget('幸运咒语', 0.2437)
    p.addget('清扫咒', 1.3724)
    Levels.append(p)
    p = Level(18, '3-5厄险')
    p.addget('罗马金币', 0.465)
    p.addget('粗糙银锭', 0.3822)
    p.addget('银原矿石', 1.5159)
    p.addget('清扫咒', 0.1465)
    p.addget('苦盐簇', 0.0318)
    p.addget('颤颤之齿', 0.0764)
    p.addget('破碎骨片', 0.0637)
    Levels.append(p)
    p = Level(18, '3-6厄险')
    p.addget('未知种根骨', 0.5962)
    p.addget('幸运咒语', 0.11539999999999999)
    p.addget('精磨苦盐', 0.0288)
    p.addget('粗糙银锭', 0.08650000000000001)
    p.addget('液化战栗', 0.4808)
    p.addget('清扫咒', 0.2788)
    p.addget('破碎骨片', 0.1635)
    p.addget('银原矿石', 0.17309999999999998)
    p.addget('苦盐簇', 0.125)
    p.addget('颤颤之齿', 0.0673)
    Levels.append(p)
    p = Level(18, '3-7厄险')
    p.addget('双头形骨架', 0.3347)
    p.addget('液化战栗', 0.2298)
    p.addget('破碎骨片', 0.6645)
    p.addget('颤颤之齿', 0.5677)
    Levels.append(p)
    p = Level(18, '3-8厄险')
    p.addget('祝圣秘银', 0.3504)
    p.addget('未知种根骨', 0.2992)
    p.addget('银原矿石', 0.6329)
    p.addget('破碎骨片', 1.2274)
    Levels.append(p)
    p = Level(18, '3-9厄险')
    p.addget('百灵百验鸟', 0.4752)
    p.addget('粗糙银锭', 0.5362)
    p.addget('液化战栗', 0.0248)
    p.addget('精磨苦盐', 0.0362)
    p.addget('未知种根骨', 0.0393)
    p.addget('幸运咒语', 0.059000000000000004)
    p.addget('清扫咒', 0.5052)
    p.addget('破碎骨片', 0.0040999999999999995)
    Levels.append(p)
    p = Level(18, '3-11厄险')
    p.addget('金爪灵摆', 0.3146)
    p.addget('精磨苦盐', 0.1283)
    p.addget('清扫咒', 0.6743000000000001)
    p.addget('苦盐簇', 0.3671)
    Levels.append(p)
    p = Level(18, '3-13厄险')
    p.addget('盐封曼德拉', 0.3423)
    p.addget('精磨苦盐', 0.1285)
    p.addget('苦盐簇', 0.6843)
    p.addget('狂人絮语', 0.020099999999999996)
    Levels.append(p)
    p = Level(18, '3-15厄险')
    p.addget('粗糙银锭', 1.0893000000000002)
    p.addget('液化战栗', 0.0536)
    p.addget('未知种根骨', 0.13390000000000002)
    p.addget('精磨苦盐', 0.08039999999999999)
    p.addget('颤颤之齿', 0.0536)
    p.addget('苦盐簇', 0.1429)
    p.addget('银原矿石', 0.9554)
    p.addget('清扫咒', 0.2054)
    p.addget('破碎骨片', 0.10710000000000001)
    p.addget('幸运咒语', 0.09820000000000001)
    Levels.append(p)
    p = Level(12, '2-9普通')
    p.addget('干蝉翼', 0.71)
    p.addget('液化战栗', 0.03)
    p.addget('精磨苦盐', 0.01)
    p.addget('未知种根骨', 0.04)
    p.addget('粗糙银锭', 0.04)
    p.addget('幸运咒语', 0.06)
    Levels.append(p)
    p = Level(12, '2-10普通')
    p.addget('不休轮', 0.6087)
    p.addget('液化战栗', 0.0072)
    p.addget('精磨苦盐', 0.028999999999999998)
    p.addget('未知种根骨', 0.0362)
    p.addget('粗糙银锭', 0.0507)
    p.addget('幸运咒语', 0.0362)
    p.addget('干蝉翼', 0.0072)
    Levels.append(p)
    p = Level(16, '2-3厄险')
    p.addget('祝圣秘银', 0.3519)
    p.addget('液化战栗', 0.026000000000000002)
    p.addget('精磨苦盐', 0.0334)
    p.addget('未知种根骨', 0.0455)
    p.addget('粗糙银锭', 0.0516)
    p.addget('幸运咒语', 0.0565)
    p.addget('银原矿石', 1.6711)
    Levels.append(p)
    p = Level(16, '2-3厄险')
    p.addget('祝圣秘银', 0.34630000000000005)
    p.addget('银原矿石', 1.6327)
    p.addget('液化战栗', 0.0241)
    p.addget('精磨苦盐', 0.024700000000000003)
    p.addget('未知种根骨', 0.027200000000000002)
    p.addget('粗糙银锭', 0.034)
    p.addget('幸运咒语', 0.044500000000000005)
    p.addget('干蝉翼', 0.018600000000000002)
    p.addget('不休轮', 0.0161)
    Levels.append(p)
    p = Level(16, '2-6厄险')
    p.addget('百灵百验鸟', 0.4512)
    p.addget('液化战栗', 0.025699999999999997)
    p.addget('精磨苦盐', 0.0288)
    p.addget('未知种根骨', 0.0348)
    p.addget('粗糙银锭', 0.04769999999999999)
    p.addget('幸运咒语', 0.0659)
    p.addget('清扫咒', 1.9425)
    Levels.append(p)
    p = Level(16, '2-6厄险')
    p.addget('百灵百验鸟', 0.47859999999999997)
    p.addget('清扫咒', 1.9066)
    p.addget('液化战栗', 0.0195)
    p.addget('精磨苦盐', 0.015600000000000001)
    p.addget('未知种根骨', 0.035)
    p.addget('粗糙银锭', 0.042800000000000005)
    p.addget('幸运咒语', 0.0233)
    p.addget('干蝉翼', 0.0078000000000000005)
    p.addget('不休轮', 0.027200000000000002)
    Levels.append(p)
    p = Level(16, '2-8厄险')
    p.addget('双头形骨架', 0.302)
    p.addget('液化战栗', 0.0332)
    p.addget('精磨苦盐', 0.0318)
    p.addget('未知种根骨', 0.0535)
    p.addget('粗糙银锭', 0.0405)
    p.addget('幸运咒语', 0.037599999999999995)
    p.addget('破碎骨片', 1.5751)
    Levels.append(p)
    p = Level(16, '2-9厄险')
    p.addget('盐封曼德拉', 0.25)
    p.addget('幸运咒语', 0.1512)
    p.addget('苦盐簇', 1.0)
    p.addget('清扫咒', 0.6453)
    Levels.append(p)
    p = Level(18, '2-12厄险')
    p.addget('齿咬盒', 0.2868)
    p.addget('颤颤之齿', 0.9861)
    p.addget('未知种根骨', 0.037599999999999995)
    p.addget('粗糙银锭', 0.0536)
    p.addget('幸运咒语', 0.0525)
    p.addget('精磨苦盐', 0.033)
    p.addget('液化战栗', 0.0273)
    Levels.append(p)

    f1 = Material('颤颤之齿')
    initcl(f1)
    Materials['颤颤之齿'] = f1

    f2 = Material('苦盐簇')
    initcl(f2)
    Materials['苦盐簇'] = f2

    f3 = Material('破碎骨片')
    initcl(f3)
    Materials['破碎骨片'] = f3

    f4 = Material('银原矿石')
    initcl(f4)
    Materials['银原矿石'] = f4

    f5 = Material('清扫咒')
    initcl(f5)
    Materials['清扫咒'] = f5

    f5_1 = Material('不休轮')
    initcl(f5_1)
    Materials['不休轮'] = f5_1

    f5_2 = Material('干蝉翼')
    initcl(f5_2)
    Materials['干蝉翼'] = f5_2

    f6 = Material('液化战栗')
    f6.addk('颤颤之齿',3)
    initcl(f6)
    Materials['液化战栗'] = f6

    f7 = Material('精磨苦盐')
    f7.addk('苦盐簇',4)
    initcl(f7)
    Materials['精磨苦盐'] = f7

    f8 = Material('未知种根骨')
    f8.addk('破碎骨片',4)
    initcl(f8)
    Materials['未知种根骨'] = f8

    f9 = Material('粗糙银锭')
    f9.addk('银原矿石', 4)
    initcl(f9)
    Materials['粗糙银锭'] = f9

    f11 = Material('幸运咒语')
    f11.addk('清扫咒',4)
    initcl(f11)
    Materials['幸运咒语'] = f11

    f10 = Material('罗马金币')
    f10.addk('银原矿石',5)
    f10.addk('清扫咒', 5)
    initcl(f10)
    Materials['罗马金币'] = f10

    f10_1 = Material('弯曲鹅颈')
    f10_1.addk('不休轮', 3)
    f10_1.addk('幸运咒语', 1)
    initcl(f10_1)
    Materials['弯曲鹅颈'] = f10_1

    f10_2 = Material('砂金甲虫')
    f10_2.addk('罗马金币', 2)
    f10_2.addk('未知种根骨', 2)
    initcl(f10_2)
    Materials['砂金甲虫'] = f10_2

    f10_3 = Material('翼造门钥')
    f10_3.addk('干蝉翼', 3)
    f10_3.addk('精磨苦盐', 1)
    initcl(f10_3)
    Materials['翼造门钥'] = f10_3

    f12 = Material('百灵百验鸟')
    f12.addk('幸运咒语', 4)
    initcl(f12)
    Materials['百灵百验鸟'] = f12

    f13 = Material('祝圣秘银')
    f13.addk('液化战栗', 1)
    f13.addk('粗糙银锭', 3)
    initcl(f13)
    Materials['祝圣秘银'] = f13

    f14 = Material('双头形骨架')
    f14.addk('未知种根骨', 3)
    f14.addk('粗糙银锭', 1)
    initcl(f14)
    Materials['双头形骨架'] = f14

    f15 = Material('盐封曼德拉')
    f15.addk('精磨苦盐', 3)
    f15.addk('未知种根骨', 1)
    initcl(f15)
    Materials['盐封曼德拉'] = f15

    f16 = Material('齿咬盒')
    f16.addk('液化战栗', 3)
    f16.addk('幸运咒语', 1)
    initcl(f16)
    Materials['齿咬盒'] = f16

    f17 = Material('金爪灵摆')
    f17.addk('罗马金币', 2)
    f17.addk('粗糙银锭', 2)
    initcl(f17)
    Materials['金爪灵摆'] = f17

    f17_1 = Material('赤金罗盘')
    f17_1.addk('砂金甲虫', 2)
    f17_1.addk('双头形骨架', 4)
    initcl(f17_1)
    Materials['赤金罗盘'] = f17_1

    f17_2 = Material('轮与轴之芯')
    f17_2.addk('弯曲鹅颈', 3)
    f17_2.addk('祝圣秘银', 1)
    f17_2.addk('齿咬盒', 1)
    initcl(f17_2)
    Materials['轮与轴之芯'] = f17_2

    f17_3 = Material('微光蛾翼灯')
    f17_3.addk('翼造门钥', 3)
    f17_3.addk('盐封曼德拉', 2)
    initcl(f17_3)
    Materials['微光蛾翼灯'] = f17_3

    f18 = Material('铂金通灵板')
    f18.addk('金爪灵摆', 2)
    f18.addk('祝圣秘银', 4)
    initcl(f18)
    Materials['铂金通灵板'] = f18

    f19 = Material('狂人絮语')
    f19.addk('盐封曼德拉', 2)
    f19.addk('百灵百验鸟', 3)
    initcl(f19)
    Materials['狂人絮语'] = f19

    f20 = Material('银光子弹')
    f20.addk('盐封曼德拉', 1)
    f20.addk('祝圣秘银', 3)
    f20.addk('百灵百验鸟', 1)
    initcl(f20)
    Materials['银光子弹'] = f20

    f21 = Material('幼骨龙标本')
    f21.addk('齿咬盒', 2)
    f21.addk('双头形骨架', 3)
    initcl(f21)
    Materials['幼骨龙标本'] = f21

    f22 = Material('不腐猴爪')
    f22.addk('盐封曼德拉', 3)
    f22.addk('双头形骨架', 2)
    initcl(f22)
    Materials['不腐猴爪'] = f22

    f23 = Material('床下怪物')
    f23.addk('齿咬盒', 3)
    f23.addk('百灵百验鸟', 2)
    f23.addk('祝圣秘银', 1)
    initcl(f23)
    Materials['床下怪物'] = f23

    f23_1 = Material('双蛇权杖')
    f23_1.addk('赤金罗盘', 1)
    f23_1.addk('微光蛾翼灯', 1)
    f23_1.addk('盐封曼德拉', 2)
    initcl(f23_1)
    Materials['双蛇权杖'] = f23_1

    f24 = Material('金羊毛')
    f24.addk('铂金通灵板', 2)
    f24.addk('双头形骨架', 2)
    initcl(f24)
    Materials['金羊毛'] = f24

    f25 = Material('长青剑')
    f25.addk('幼骨龙标本', 2)
    f25.addk('祝圣秘银', 4)
    initcl(f25)
    Materials['长青剑'] = f25

    f26 = Material('分辨善恶之果')
    f26.addk('不腐猴爪', 1)
    f26.addk('床下怪物', 1)
    f26.addk('百灵百验鸟', 4)
    initcl(f26)
    Materials['分辨善恶之果'] = f26


    for i in Materials:
      Materials2[dirc_list[i]] = Materials[i]

initclanddts()


def strp(a: str, b: str):
    for i, j in zip(a, b):
        if i == j:
            continue
        elif i > j:
            return False
        elif i < j:
            return True


def sorts(f: dict):
    ff = {}
    while len(f):
        mins = None
        for i in f:
            if not mins or strp(i, mins[0]):
                mins = i
        ff[mins] = f[mins]
        f.pop(mins)

    return ff


# for i in Levels:
#    print(i.name,i.value,i.value/i.cost)

def main(needs: dict):
    global bestsolves, valuesolves
    if not needs:
        return '请填写需要的材料'
    init()
    strs = '\n'
    times = time.time()
    # needs = {'分辨善恶之果':1}#'盐封曼德拉':5}#,,'分辨善恶之果':2
    strs += '价体比限制' + str(sets.value_type) + '计算复杂度' + str(sets.difficult) + '\n'
    for i in needs:
        if needs[i] > 0:
            strs += i + str(needs[i]) + ' - '
    strs += '\n'
    if solve(needs):
        return '材料已经可以一键合成！'
    # needs.clear()
    # print()
    bestsolves = sorts(bestsolves)
    valuesolves = sorts(valuesolves)

    for i in bestsolves:
        strs += i + ' ' + str(bestsolves[i]) + '次\n'
    # print(tss,sums,sumf)
    p = {}
    value = 0

    for i in bestsolves:
        for j in Levels:
            if i == j.name:
                # print(p)
                j.playsum(p, bestsolves[i])
                value += j.value * bestsolves[i]
                # print(p,j.gets)
    if mincost:
        strs += '消耗{0:.2f}点体力，价值{1:.2f}，价体力比{2:.2f}，耗时{3:.2f}s\n'.format(mincost,value,value / mincost,time.time() - times)
    #p[dirc_list['利齿子儿']] = p.get(dirc_list['利齿子儿'], 0.0) + 10 * mincost
    for i in p:
        strs += de_dirc_list[i] + '{0:.2f}\n'.format(p[i])
    cost = 0
    strs += '------------------价值版-------------------\n'
    for i in valuesolves:
        strs += i + ' ' + str(valuesolves[i]) + '次\n'
    p = {}
    for i in valuesolves:
        for j in Levels:
            if i == j.name:
                # print(p)
                j.playsum(p, valuesolves[i])
                cost += j.cost * valuesolves[i]
                # print(p,j.gets)
    if valuelevel is not None:
        strs += '消耗{0:.2f}点体力，价值{1:.2f}，价体力比{2:.2f}\n'.format(cost,valuelevel * cost,valuelevel)
    #p[dirc_list['利齿子儿']] = p.get(dirc_list['利齿子儿'], 0.0) + 10 * mincost
    for i in p:
        strs += de_dirc_list[i] + '{0:.2f}\n'.format(p[i])
    strs += 'APP、计算程序均由b站@熙影镜制作，本计算器材料的掉率以及价值参考均取自NGA伴春风而归的材料掉率共建表，本计算器不用于任何商业用途，仅供交流使用，如在使用时碰到任何问题，或者希望了解一些计算方法，欢迎私信或者评论'
    return strs
def getneed():
   try:
      with open('need.txt','r') as f:
         needs = {}
         f.readline()
         while True:
            a = f.readline()
            b = f.readline()
            if not a or not b:
               return needs
            if float(b[:-1])!= 0:
               needs[a[:-1]] = float(b[:-1])

   except OSError:
      print('cannot find need.txt,auto write')
      with open('need.txt','w') as f:
         f.write('需求\n')
         p = []
         a = 1
         while len(p) != len(dirc_list) - 3:
             for i in dirc_list:
                 if dirc_list[i] == a:
                     p.append(i)
                     a += 1
                     break

         while len(p):
             f.write(p.pop()+'\n')
             f.write(str(0) + '\n')
         f.write('价体比\n')
         f.write(str(1.2) + '\n')

         f.write('计算复杂度\n')
         f.write(str(1) + '\n')
         f.close()
   input('请在文件中修改你所需的数量')
   getneed()

if __name__ == '__main__':
    need = getneed()
    if need.get('价体比',0):
        sets.value_type = need.pop('价体比')
    if need.get('计算复杂度',0):
        sets.difficult = need.pop('计算复杂度')
    print(main(need))
    input('按任意键退出')
