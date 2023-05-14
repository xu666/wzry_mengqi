import streamlit as st
from streamlit import session_state as ss

from service import equips, get_line_chart

# 初始化session变量
default_values = {
    '共同装备': ['红刀', '影刃'],
    '质量': 100,
    '英雄等级': 15,
    '考虑强击': False,
    '敌方魔抗': 279,
    '计算类型': 'DPS',
    '装备1': [],
    '装备2': [],
    '铭文1': "8狩猎2夺萃10鹰眼10红月",
    '铭文2': "8狩猎2夺萃10鹰眼10红月",
}
for key, value in default_values.items():
    if key not in ss:
        ss[key] = value

st.set_page_config(layout='wide', page_icon='😏')
st.title('梦奇出装伤害对比')  # 设置标题

# 侧边栏控制共同选项
with st.sidebar.form('共同选项'):
    st.subheader('共同选项')
    st.multiselect('共同装备', options=equips.keys(), key='共同装备')
    st.number_input('英雄等级', min_value=1, max_value=15, step=1, key='英雄等级')
    st.number_input('质量', min_value=0, max_value=100, step=10, key='质量')
    # st.checkbox('考虑强击', key='考虑强击')
    st.number_input('敌方魔抗', step=1, key='敌方魔抗')
    st.radio('计算类型', options=['DPS', '单次普攻'], key='计算类型')
    submit_0 = st.form_submit_button('确定')

# 出装选择以及上图
with st.expander('📈 现场分析', expanded=True):
    col1, col2 = st.columns(2)  # 表单是双栏
    with col1.form('套装1'):
        st.subheader(ss['装备1'][0] if ss['装备1'] else '套装1')
        st.text_input('铭文', key='铭文1')
        st.multiselect('出装', options=set(equips.keys()) - set(ss['共同装备']), key='装备1')
        submit_1 = st.form_submit_button('确定')
    with col2.form('套装2'):
        st.subheader(ss['装备2'][0] if ss['装备2'] else '套装2')
        st.text_input('铭文', key='铭文2')
        st.multiselect('出装', options=set(equips.keys()) - set(ss['共同装备']), key='装备2')
        submit_2 = st.form_submit_button('确定')

    # 任意表单有提交那就上图
    if submit_0 or submit_1 or submit_2:
        line_chart = get_line_chart(ss)
        st.line_chart(data=line_chart.data, x=line_chart.x, y=line_chart.y)

# 分析以及结论
with st.expander('🍻 分析以及结论'):
    tab1, tab2, tab3 = st.tabs(['逐风 vs 无尽', '碎星锤 vs 无尽', '暗影战斧 vs 纯净苍穹'])
    with tab1:
        st.warning('在经典套装中, 逐风比无尽伤害低一丢丢, 防范不祥的能力高一丢丢, 但实际上差别极小.\n\n'
                   '所以二者的选择更多是看个人喜好.')
        st.markdown('#### 伤害对比')
        st.image(r'.\data\1_无尽vs逐风.png')
        st.markdown('#### 伤害对比(不祥debuff)')
        st.image(r'.\data\1_无尽vs逐风(不祥).png')
    with tab2:
        st.error('🚨 在经典套装中, 相比无尽, 碎星锤不仅打脆皮拉胯, 甚至连打肉的伤害也稍微逊色')
        st.image(r'.\data\2_无尽vs碎星锤.png')
    with tab3:
        st.success('🍹 当敌方护甲较低时, 暗影战斧的伤害优势显著')
        st.image(r'.\data\3_黑切vs苍穹.png')
