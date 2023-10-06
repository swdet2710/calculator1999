import math
import time
from itertools import permutations

print('vision 2.2,made by 熙影镜')
print('感谢up主少言的信提供的数据支持')
value_list = {'颤颤之齿':4,'苦盐簇':3,'破碎骨片':3,'银原矿石':3,'清扫咒':3,
              '液化战栗':12,'精磨苦盐':12,'未知种根骨':12,'粗糙银锭':12,'幸运咒语':12,'罗马金币':12,
              '百灵百验鸟':48,'祝圣秘银':48,'双头形骨架':48,'盐封曼德拉':48,'齿咬盒':48,'金爪灵摆':48,
              '铂金通灵板':288,'狂人絮语':240,'银光子弹':240,'幼骨龙标本':240,'不腐猴爪':240,'床下怪物':288,
              '金羊毛':288*2+96,'长青剑':480+4*48,'分辨善恶之果':240+288+4*38,'微尘':12/4000,'利齿子儿':16/4000,'启寤I':1/400}

dirc_list = {'颤颤之齿':1,'苦盐簇':2,'破碎骨片':3,'银原矿石':4,'清扫咒':5,
              '液化战栗':6,'精磨苦盐':7,'未知种根骨':8,'粗糙银锭':9,'幸运咒语':10,'罗马金币':11,
              '百灵百验鸟':12,'祝圣秘银':13,'双头形骨架':14,'盐封曼德拉':15,'齿咬盒':16,'金爪灵摆':17,
              '铂金通灵板':18,'狂人絮语':19,'银光子弹':20,'幼骨龙标本':21,'不腐猴爪':22,'床下怪物':23,
              '金羊毛':24,'长青剑':25,'分辨善恶之果':26,'微尘':27,'利齿子儿':28,'启寤I':29}
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
   # p01 = dt(12,'1-1')
   # p01.addget('颤颤之齿',2.3)
   # p01.addget('苦盐簇', 0.3)
   # p01.addget('破碎骨片', 0.3)
   # p01.addget('银原矿石', 0.3)
   # p01.addget('清扫咒', 0.3)
   # dts.append(p01)

   # p02 = dt(12,'1-4')
   # p02.addget('颤颤之齿', 0.3)
   # p02.addget('苦盐簇', 0.3)
   # p02.addget('破碎骨片', 0.3)
   # p02.addget('银原矿石', 0.3)
   # p02.addget('清扫咒', 2.3)
   # dts.append(p02)

   # p03 = dt(12,'1-5')
   # p03.addget('颤颤之齿', 0.3)
   # p03.addget('苦盐簇', 0.3)
   # p03.addget('破碎骨片', 0.3)
   # p03.addget('银原矿石', 2.3)
   # p03.addget('清扫咒', 0.3)
   # dts.append(p03)

   # p04 = dt(12,'1-6')
   # p04.addget('颤颤之齿', 0.3)
   # p04.addget('苦盐簇', 0.3)
   # p04.addget('破碎骨片', 2.3)
   # p04.addget('银原矿石', 0.3)
   # p04.addget('清扫咒', 0.3)
   # dts.append(p04)
   #
   # p05 = dt(12, '1-7')
   # p05.addget('颤颤之齿', 0.3)
   # p05.addget('苦盐簇', 0.3)
   # p05.addget('破碎骨片', 0.3)
   # p05.addget('银原矿石', 0.3)
   # p05.addget('清扫咒', 0.3)
   # p05.addget('幸运咒语', 0.7)
   # dts.append(p05)
   #
   # p06 = dt(12, '1-8')
   # p06.addget('颤颤之齿', 0.3)
   # p06.addget('苦盐簇', 0.3)
   # p06.addget('破碎骨片', 0.3)
   # p06.addget('银原矿石', 0.3)
   # p06.addget('清扫咒', 0.3)
   # p06.addget('粗糙银锭', 0.7)
   # dts.append(p06)
   #
   # p07 = dt(12, '1-11')
   # p07.addget('颤颤之齿', 0.3)
   # p07.addget('苦盐簇', 0.3)
   # p07.addget('破碎骨片', 0.3)
   # p07.addget('银原矿石', 0.3)
   # p07.addget('清扫咒', 0.3)
   # p07.addget('未知种根骨', 0.7)
   # dts.append(p07)
   #
   # p08 = dt(12, '1-12')
   # p08.addget('颤颤之齿', 0.3)
   # p08.addget('苦盐簇', 0.3)
   # p08.addget('破碎骨片', 0.3)
   # p08.addget('银原矿石', 0.3)
   # p08.addget('清扫咒', 0.3)
   # p08.addget('精磨苦盐', 0.7)
   # dts.append(p08)
   #
   # p09 = dt(12, '1-14')
   # p09.addget('颤颤之齿', 0.3)
   # p09.addget('苦盐簇', 0.3)
   # p09.addget('破碎骨片', 0.3)
   # p09.addget('银原矿石', 0.3)
   # p09.addget('清扫咒', 0.3)
   # p09.addget('液化战栗', 0.7)
   # dts.append(p09)
   #
   # p10 = dt(12, '1-15')
   # p10.addget('颤颤之齿', 0.3)
   # p10.addget('苦盐簇', 0.3)
   # p10.addget('破碎骨片', 0.3)
   # p10.addget('银原矿石', 0.3)
   # p10.addget('清扫咒', 0.3)
   # p10.addget('罗马金币', 0.7)
   # dts.append(p10)
   #
   # p11 = dt(12, '1-16')
   # p11.addget('液化战栗', 0.3)
   # p11.addget('精磨苦盐', 0.3)
   # p11.addget('未知种根骨', 0.3)
   # p11.addget('粗糙银锭', 0.3)
   # p11.addget('清扫咒', 0.3)
   # p11.addget('罗马金币', 0.3)
   # dts.append(p11)

   # p12 = dt(14, '2-1')
   # p12.addget('液化战栗', 0.3)
   # p12.addget('精磨苦盐', 0.3)
   # p12.addget('未知种根骨', 0.3)
   # p12.addget('粗糙银锭', 0.3)
   # p12.addget('幸运咒语', 0.3)
   # dts.append(p12)

   p14 = Level(16, '2-3')
   p14.addget('液化战栗', 0.02)
   p14.addget('精磨苦盐', 0.034)
   p14.addget('未知种根骨', 0.028)
   p14.addget('粗糙银锭', 0.05)
   p14.addget('幸运咒语', 0.036)
   p14.addget('银原矿石', 1.728)
   p14.addget('祝圣秘银', 0.348)
   p14.addget('利齿子儿', 0.06 * 500)
   p14.addget('微尘', 0.046 * 1000)
   p14.addget('启寤I', 0.066)
   Levels.append(p14)
   #
   # p13 = dt(16, '2-4')
   # p13.addget('未知种根骨', 0.7)
   # p13.addget('粗糙银锭', 0.7)
   # p13.addget('颤颤之齿', 0.3)
   # p13.addget('苦盐簇', 0.3)
   # p13.addget('破碎骨片', 0.3)
   # p13.addget('银原矿石', 0.3)
   # p13.addget('清扫咒', 0.3)
   # dts.append(p13)
   #
   #
   #
   # p15 = dt(16, '2-5')
   # p15.addget('幸运咒语', 0.7)
   # p15.addget('粗糙银锭', 0.7)
   # p15.addget('颤颤之齿', 0.3)
   # p15.addget('苦盐簇', 0.3)
   # p15.addget('破碎骨片', 0.3)
   # p15.addget('银原矿石', 0.3)
   # p15.addget('清扫咒', 0.3)
   # dts.append(p15)
   #
   p160 = Level(16, '2-6')
   p160.addget('液化战栗', 0.028)
   p160.addget('精磨苦盐', 0.046)
   p160.addget('未知种根骨', 0.034)
   p160.addget('粗糙银锭', 0.058)
   p160.addget('清扫咒', 1)
   p160.addget('幸运咒语', 0.042)
   p160.addget('百灵百验鸟', 0.448)
   p160.addget('利齿子儿', 0.048 * 500)
   p160.addget('微尘', 0.046 * 1000)
   p160.addget('启寤I', 0.064)
   Levels.append(p160)

   p16 = Level(16, '2-8')
   p16.addget('液化战栗', 0.028)
   p16.addget('精磨苦盐', 0.032)
   p16.addget('未知种根骨', 0.038)
   p16.addget('粗糙银锭', 0.064)
   p16.addget('破碎骨片', 1.602)
   p16.addget('幸运咒语', 0.068)
   p16.addget('双头形骨架', 0.312)
   p16.addget('利齿子儿', 0.06 * 500)
   p16.addget('微尘', 0.046 * 1000)
   p16.addget('启寤I', 0.066)
   Levels.append(p16)

   p17 = Level(16, '2-9')
   p17.addget('清扫咒', 0.7306)
   p17.addget('苦盐簇', 1)
   p17.addget('幸运咒语', 0.01417)
   p17.addget('盐封曼德拉', 0.275)
   Levels.append(p17)

   # p18 = dt(16, '2-10')
   # p18.addget('精磨苦盐', 0.7)
   # p18.addget('未知种根骨', 0.3)
   # p18.addget('颤颤之齿', 0.3)
   # p18.addget('苦盐簇', 0.3)
   # p18.addget('破碎骨片', 0.3)
   # p18.addget('银原矿石', 0.3)
   # p18.addget('清扫咒', 0.3)
   # dts.append(p18)

   # p19 = dt(16, '2-11')
   # p19.addget('液化战栗', 0.3)
   # p19.addget('精磨苦盐', 0.3)
   # p19.addget('未知种根骨', 0.3)
   # p19.addget('粗糙银锭', 0.3)
   # p19.addget('清扫咒', 0.3)
   # p19.addget('幸运咒语', 2.3)
   # dts.append(p19)

   p20 = Level(18, '2-12')
   p20.addget('液化战栗', 0.02917)
   p20.addget('精磨苦盐', 0.03542)
   p20.addget('未知种根骨', 0.03333)
   p20.addget('粗糙银锭', 0.03958)
   p20.addget('颤颤之齿', 1)
   p20.addget('幸运咒语', 0.06458)
   p20.addget('齿咬盒', 0.28542)
   p20.addget('利齿子儿', 0.005417*500)
   p20.addget('微尘', 0.04792*1000)
   p20.addget('启寤I', 0.07083)
   Levels.append(p20)

   # p21 = dt(18, '2-13')
   # p21.addget('液化战栗', 0.7)
   # p21.addget('精磨苦盐', 0.3)
   # p21.addget('颤颤之齿', 0.3)
   # p21.addget('苦盐簇', 0.3)
   # p21.addget('破碎骨片', 0.3)
   # p21.addget('银原矿石', 0.3)
   # p21.addget('清扫咒', 0.3)
   # dts.append(p21)

   # p22 = dt(18, '2-14')
   # p22.addget('液化战栗', 0.3)
   # p22.addget('精磨苦盐', 0.3)
   # p22.addget('未知种根骨', 0.3)
   # p22.addget('粗糙银锭', 0.3)
   # p22.addget('幸运咒语', 0.3)
   # dts.append(p22)

   p23 = Level(18, '3-3')
   p23.addget('清扫咒', 0.908)
   p23.addget('银原矿石', 0.752)
   p23.addget('幸运咒语', 0.278)
   p23.addget('金爪灵摆', 0.248)
   p23.addget('利齿子儿', 0.042 * 500)
   p23.addget('微尘', 0.048 * 1000)
   p23.addget('启寤I', 0.09)
   Levels.append(p23)
   #
   # p24 = dt(18, '3-5')
   # p24.addget('罗马金币', 0.3)
   # p24.addget('银原矿石', 0.7)
   # p24.addget('粗糙银锭', 0.3)
   # dts.append(p24)
   #
   # p25 = dt(18, '3-6')
   # p25.addget('液化战栗', 0.3)
   # p25.addget('精磨苦盐', 0.3)
   # p25.addget('未知种根骨', 0.7)
   # p25.addget('粗糙银锭', 0.3)
   # p25.addget('破碎骨片', 0.3)
   # p25.addget('幸运咒语', 0.3)
   # p25.addget('颤颤之齿', 0.3)
   # dts.append(p25)

   p26 = Level(18, '3-7')
   p26.addget('破碎骨片', 0.675)
   p26.addget('颤颤之齿', 0.5958)
   p26.addget('液化战栗', 0.1958)
   p26.addget('双头形骨架', 0.325)
   p26.addget('利齿子儿', 0.0375*500)
   p26.addget('微尘', 0.04583*1000)
   p26.addget('启寤I', 0.05417)
   Levels.append(p26)

   p27 = Level(18, '3-8')
   p27.addget('破碎骨片', 1.175)
   p27.addget('银原矿石', 0.64583)
   p27.addget('未知种根骨', 0.29375)
   p27.addget('祝圣秘银', 0.35417)
   p27.addget('利齿子儿', 0.04583*500)
   p27.addget('微尘', 0.04792*1000)
   p27.addget('启寤I', 0.08125)
   Levels.append(p27)

   p28 = Level(18, '3-9')
   p28.addget('液化战栗', 0.025)
   p28.addget('精磨苦盐', 0.02292)
   p28.addget('未知种根骨', 0.0375)
   p28.addget('粗糙银锭', 0.5854)
   p28.addget('清扫咒', 0.54792)
   p28.addget('幸运咒语', 0.05833)
   p28.addget('百灵百验鸟', 0.45208)
   p28.addget('利齿子儿', 0.04583*500)
   p28.addget('微尘', 0.04792*1000)
   p28.addget('启寤I', 0.08958)
   Levels.append(p28)

   p290 = Level(18, '3-11')
   p290.addget('清扫咒', 0.708)
   p290.addget('苦盐簇', 0.412)
   p290.addget('精磨苦盐', 0.114)
   p290.addget('金爪灵摆', 0.292)
   p290.addget('利齿子儿', 0.06 * 500)
   p290.addget('微尘', 0.054 * 1000)
   p290.addget('启寤I', 0.072)
   Levels.append(p290)

   p29 = Level(18, '3-13')
   p29.addget('狂人絮语', 0.026)
   p29.addget('苦盐簇', 0.6875)
   p29.addget('精磨苦盐', 0.1125)
   p29.addget('盐封曼德拉', 0.352)
   p29.addget('利齿子儿', 0.064*500)
   p29.addget('微尘', 0.048*1000)
   p29.addget('启寤I', 0.07)
   Levels.append(p29)

   # p30 = dt(18, '3-15')
   # p30.addget('液化战栗', 0.3)
   # p30.addget('精磨苦盐', 0.3)
   # p30.addget('未知种根骨', 0.3)
   # p30.addget('粗糙银锭', 0.7)
   # p30.addget('银原矿石', 0.7)
   # p30.addget('幸运咒语', 0.3)
   # dts.append(p30)

   # p31 = dt(18, '4-3')
   # p31.addget('液化战栗', 0.3)
   # p31.addget('精磨苦盐', 0.3)
   # p31.addget('未知种根骨', 0.3)
   # p31.addget('粗糙银锭', 0.3)
   # p31.addget('幸运咒语', 0.3)
   # dts.append(p31)

   # p32 = dt(18, '4-4')
   # p32.addget('液化战栗', 0.7)
   # p32.addget('清扫咒', 0.3)
   # p32.addget('幸运咒语', 0.7)
   # dts.append(p32)
   #
   # ########
   #
   p35 = Level(18, '4-10')
   p35.addget('液化战栗', 0.052)
   p35.addget('精磨苦盐', 0.034)
   p35.addget('未知种根骨', 0.042)
   p35.addget('粗糙银锭', 0.518)
   p35.addget('银原矿石', 0.718)
   p35.addget('幸运咒语', 0.048)
   p35.addget('齿咬盒', 0.282)
   p35.addget('利齿子儿', 0.04375 * 500)
   p35.addget('微尘', 0.06042 * 1000)
   p35.addget('启寤I', 0.08333)
   Levels.append(p35)

   p36 = Level(18, '4-11')
   p36.addget('破碎骨片', 1.1583)
   p36.addget('清扫咒', 0.54167)
   p36.addget('未知种根骨', 0.3208)
   p36.addget('百灵百验鸟', 0.45833)
   p36.addget('利齿子儿', 0.04375*500)
   p36.addget('微尘', 0.06042*1000)
   p36.addget('启寤I', 0.08333)
   Levels.append(p36)

   p37 = Level(18, '4-13')
   p37.addget('精磨苦盐', 0.238)
   p37.addget('银原矿石', 0.646)
   p37.addget('苦盐簇', 0.578)
   p37.addget('祝圣秘银', 0.354)
   p37.addget('利齿子儿', 0.048 * 500)
   p37.addget('微尘', 0.06 * 1000)
   p37.addget('启寤I', 0.062)
   Levels.append(p37)
   ####

   p38 = Level(18, '4-16')
   p38.addget('液化战栗', 0.025)
   p38.addget('精磨苦盐', 0.025)
   p38.addget('未知种根骨', 0.0307)
   p38.addget('粗糙银锭', 0.0208)
   p38.addget('幸运咒语', 2.0333)
   Levels.append(p38)

   p39 = Level(18, '4-20')
   p39.addget('破碎骨片', 0.65833)
   p39.addget('清扫咒', 2.14167)
   p39.addget('幸运咒语', 0.4104)
   p39.addget('双头形骨架', 0.34162)
   p39.addget('利齿子儿', 0.05*500)
   p39.addget('微尘', 0.0333*1000)
   p39.addget('启寤I', 0.05833)
   Levels.append(p39)

   p40 = Level(18, '4-21')
   p40.addget('颤颤之齿', 0.56)
   p40.addget('苦盐簇', 0.686)
   p40.addget('液化战栗', 0.182)
   p40.addget('盐封曼德拉', 0.314)
   p40.addget('利齿子儿', 0.05 * 500)
   p40.addget('微尘', 0.088 * 1000)
   p40.addget('启寤I', 0.064)
   Levels.append(p40)

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
    p[dirc_list['利齿子儿']] = p.get(dirc_list['利齿子儿'], 0.0) + 10 * mincost
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
    p[dirc_list['利齿子儿']] = p.get(dirc_list['利齿子儿'], 0.0) + 10 * mincost
    for i in p:
        strs += de_dirc_list[i] + '{0:.2f}\n'.format(p[i])
    strs += 'APP、计算程序均由b站@熙影镜制作，数据源自b站up主少言的信，如在使用时碰到任何问题，或者希望了解一些计算方法，欢迎私信或者评论'
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
         f.write('分辨善恶之果\n')
         f.write(str(0)+'\n')

         f.write('长青剑\n')
         f.write(str(0) + '\n')

         f.write('金羊毛\n')
         f.write(str(0) + '\n')

         f.write('床下怪物\n')
         f.write(str(0) + '\n')

         f.write('不腐猴爪\n')
         f.write(str(0) + '\n')

         f.write('幼骨龙标本\n')
         f.write(str(0) + '\n')

         f.write('银光子弹\n')
         f.write(str(0) + '\n')

         f.write('狂人絮语\n')
         f.write(str(0) + '\n')

         f.write('铂金通灵板\n')
         f.write(str(0) + '\n')

         f.write('金爪灵摆\n')
         f.write(str(0) + '\n')

         f.write('齿咬盒\n')
         f.write(str(0) + '\n')

         f.write('盐封曼德拉\n')
         f.write(str(0) + '\n')

         f.write('双头形骨架\n')
         f.write(str(0) + '\n')

         f.write('祝圣秘银\n')
         f.write(str(0) + '\n')

         f.write('百灵百验鸟\n')
         f.write(str(0) + '\n')

         f.write('罗马金币\n')
         f.write(str(0) + '\n')

         f.write('幸运咒语\n')
         f.write(str(0) + '\n')

         f.write('粗糙银锭\n')
         f.write(str(0) + '\n')

         f.write('未知种根骨\n')
         f.write(str(0) + '\n')

         f.write('精磨苦盐\n')
         f.write(str(0) + '\n')

         f.write('液化战栗\n')
         f.write(str(0) + '\n')

         f.write('清扫咒\n')
         f.write(str(0) + '\n')

         f.write('银原矿石\n')
         f.write(str(0) + '\n')

         f.write('破碎骨片\n')
         f.write(str(0) + '\n')

         f.write('苦盐簇\n')
         f.write(str(0) + '\n')

         f.write('颤颤之齿\n')
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
