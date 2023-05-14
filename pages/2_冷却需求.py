import pandas as pd
import streamlit as st


@st.cache_data
def get_df() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_excel(r'./data/冷却.xlsx', engine='openpyxl').set_index('冷却').T
    return df.rename_axis(index='冷却')


st.set_page_config(layout='wide', page_icon='😏')
st.title('梦奇的冷却需求')
st.markdown('### 主要变化\n\n🤔 **攻速阈值取消**')
st.write(r"$$梦奇攻击间隔 ≈ \frac{1}{1+攻速/100} + 0.066$$")

st.markdown('### 冷却需求表')
st.dataframe(get_df())
st.markdown('这个表格的含义是：比方说，当冷却是25时，如果攻速不超过100，就能做到每A3下刷新一次一技能。\n\n'
            '表格中的数据是我自己在 **训练营** 测试得到的。\n\n'
            '因为是手工测出来的，因此结果比较粗略，存在一定的误差。')

st.markdown('### 简单来说')
st.warning('⚠️ 影刃： 25 CD\n\n⚠️ 影刃+逐风： 30 CD')
