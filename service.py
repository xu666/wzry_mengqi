""" 在以前写的程序的基础上, 进一步进行封装 """
from typing import Any, NamedTuple, List

import numpy as np
import pandas as pd
from pydantic import BaseModel
from typing_extensions import Literal

from model import 铭文属性类, 计算梦奇普攻伤害


class Param(BaseModel):
    """ 计算伤害需要的参数 """
    # 护甲: float = 0  # 敌人护甲
    魔抗: float = 0  # 敌人魔抗
    英雄等级: int = 15  # 梦奇英雄等级
    质量: int = 100  # 梦奇质量，最高100
    装备攻击力: float = 0  # 装备提供的攻击力
    精准: float = 0  # 总的精准伤害，例如影刃是40
    装备攻速: float = 0  # 装备提供的攻速
    装备暴击率: float = 0  # 装备提供的暴击率，0~1
    黑切: bool = False  # 是否出了暗影战斧
    陨星: bool = False  # 是否出了陨星
    碎星锤: bool = False  # 是否出了碎星锤
    无尽: bool = False  # 是否出了无尽
    电刀: bool = False  # 是否出了电刀
    冰痕: bool = False  # 是否出了冰痕
    宗师: bool = False  # 是否出了宗师
    考虑强击: bool = False  # 是否考虑强击伤害
    敌人血量: float = 0  # 敌人当前血量（关系到末世的伤害）
    铭文: Any = None  # 英雄铭文，需要传入一个铭文属性对象，铭文属性类的定义在前面
    计算类型: Literal["单次普攻", "DPS"] = "单次普攻"  # “单次普攻”或者“DPS”

    def __add__(self, other: 'Param'):
        """ 装备属性叠加方法 """
        self.装备攻击力 += other.装备攻击力
        self.精准 += other.精准
        self.装备攻速 += other.装备攻速
        self.装备暴击率 += other.装备暴击率
        for field in ['黑切', '陨星', '碎星锤', '无尽', '电刀', '冰痕', '宗师']:
            setattr(self, field, getattr(self, field) or getattr(other, field))
        return self


equips = {  # 常见攻击装备及其属性
    '红刀': Param(装备攻击力=40),
    # '肉刀': Param(),  # 暂时没有考虑肉刀灼烧伤害
    # '末世': Param(装备攻击力=60, 装备攻速=30, 末世=True),
    '影刃': Param(装备攻速=55, 装备暴击率=.25, 精准=40),
    '苍穹': Param(装备攻击力=100),
    '宗师': Param(装备攻击力=80, 装备暴击率=.20, 宗师=True),
    '无尽': Param(装备攻击力=110, 装备暴击率=.20, 无尽=True),
    '逐风': Param(装备攻击力=100, 装备暴击率=.15, 装备攻速=50),
    # '逐风(不触发)': Param(装备攻击力=100, 装备暴击率=.15, ),
    '不祥debuff': Param(装备攻速=-40),
    '黑切': Param(装备攻击力=85, 黑切=True),
    '碎星锤': Param(装备攻击力=80, 碎星锤=True),
    '电刀': Param(装备攻速=35, 电刀=True),
    # '冰痕': Param(装备攻击力=40, 冰痕=True),
    '泣血': Param(装备攻击力=100),
    '攻速鞋': Param(装备攻速=25),
    '第二影刃': Param(装备攻速=35, 装备暴击率=.25),
}


class LineChartData(NamedTuple):
    """ 返给前台的折线图的数据 """
    data: pd.DataFrame  # 数据
    x: str = '护甲'  # x轴
    y: List[str] = []  # y轴的列


def get_line_chart(ss: dict, step=5) -> LineChartData:
    """ 根据streamlit的session字典, 生成折线图 """
    # 读取共同的条件
    param0 = Param(
        魔抗=ss['敌方魔抗'],
        英雄等级=ss['英雄等级'],
        质量=ss['质量'],
        # 考虑强击=ss['考虑强击'],
        考虑强击=ss['计算类型'] == '单次普攻',
        计算类型=ss['计算类型']
    )
    x_data = range(200, 1200, step)

    param1 = param0.copy()
    param1.铭文 = 铭文属性类.from_str(ss['铭文1'])
    for equip in set(ss['共同装备']).union(ss['装备1']):
        param1 += equips[equip]
    y1 = [计算梦奇普攻伤害(护甲=x, **param1.dict()) for x in x_data]

    param2 = param0.copy()
    param2.铭文 = 铭文属性类.from_str(ss['铭文2'])
    for equip in set(ss['共同装备']).union(ss['装备2']):
        param2 += equips[equip]
    y2 = [计算梦奇普攻伤害(护甲=x, **param2.dict()) for x in x_data]

    suit_names = [ss['装备1'][0] if ss['装备1'] else '套装1', ss['装备2'][0] if ss['装备2'] else '套装2']
    return LineChartData(
        data=pd.DataFrame(np.array([x_data, y1, y2]).T, columns=['护甲', *suit_names]),
        x='护甲',
        y=suit_names,
    )


if __name__ == '__main__':
    p = Param()
