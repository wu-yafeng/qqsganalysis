import math
from models import 元神属性点数与属性百分比对应表


def 计算每级增加点数(成长):
    if 成长 <= 5:
        return 成长 ** 2 / 2
    else:
        return 12.5 + 2.5 * (成长 - 5)


def 计算元神属性(form):
    融合材料元神最高等级 = [9, 19, 29, 39, 49, 59, 69, 74, 79, 84]

    result = {}
    当前等级 = int(form['当前等级'])
    等级 = int(form['等级'])
    for 属性名称 in ['物理攻击', '法术攻击', '物理防御', '法术防御']:
        当前黄字点数 = float(form[f'当前{属性名称}黄字点数'])
        当前成长 = float(form[f'当前{属性名称}成长'])

        初始点数 = 当前黄字点数 - 计算每级增加点数(当前成长) * (当前等级 - 1)

        手动分配点数 = float(form[f'{属性名称}手动分配点数'])
        融合点数 = float(form[f'{属性名称}融合点数'])
        成长 = float(form[f'{属性名称}成长'])

        黄字点数 = 初始点数 + 计算每级增加点数(成长) * (等级 - 1)
        绿字点数 = 手动分配点数 + 融合点数
        百分比 = 元神属性点数与属性百分比对应表.query.get(int(math.floor(黄字点数 + 绿字点数))).属性百分比

        融合后增加点数 = [(初始点数 + 计算每级增加点数(成长) * (融合材料元神等级 - 1) + 5 * (融合材料元神等级 - 1)) / 20 for 融合材料元神等级 in 融合材料元神最高等级]

        result[f'{属性名称}黄字点数'] = 黄字点数
        result[f'{属性名称}绿字点数'] = 绿字点数
        result[f'{属性名称}百分比'] = 百分比
        result[f'{属性名称}融合后增加点数'] = 融合后增加点数

    for 属性名称 in ['攻击配合', '防御配合']:
        当前黄字点数 = float(form[f'当前{属性名称}黄字点数'])
        当前成长 = float(form[f'当前{属性名称}成长'])

        初始点数 = 当前黄字点数 - 计算每级增加点数(当前成长) * (当前等级 - 1)

        手动分配点数 = float(form[f'{属性名称}手动分配点数'])
        成长 = 当前成长

        黄字点数 = 初始点数 + 计算每级增加点数(成长) * (等级 - 1)
        绿字点数 = 手动分配点数
        if 黄字点数 + 绿字点数 > 800:
            黄字点数 = 800 - 绿字点数
        百分比 = round(math.floor(黄字点数 + 绿字点数) / 8, 2)

        result[f'{属性名称}黄字点数'] = 黄字点数
        result[f'{属性名称}绿字点数'] = 绿字点数
        result[f'{属性名称}百分比'] = 百分比

    return result
