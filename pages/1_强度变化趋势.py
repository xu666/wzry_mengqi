import pandas as pd
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def get_zscore_df() -> pd.DataFrame:
    """ 获取国服分zscore原始数据 """
    df_zscore: pd.DataFrame = pd.read_excel(r'./data/zscore.xlsx', sheet_name='图', engine='openpyxl')
    df_zscore = df_zscore.set_index('英雄').drop(columns=['变化'])
    return df_zscore


# 初始化
st.set_page_config(layout='wide', page_icon='😏')
st.title('梦奇的强度变化趋势')
if 'hero_list' not in st.session_state:
    st.session_state.hero_list = ['公孙离', '典韦', '梦奇']
st.success('梦奇的强度高于平均水平，且保持平稳。🉑🉑🉑')

tab1, tab2 = st.tabs(['静态图', '交互图'])
with tab1:
    st.image(r'./data/梦奇趋势.png')

with tab2 as t2:
    # 选取数据
    df_ = get_zscore_df()
    st.sidebar.multiselect('英雄选择', options=df_.index, key='hero_list')
    chart_data = df_.loc[st.session_state.hero_list, :]

    # 绘图
    fig = go.Figure()
    fig.update_layout(title="最近半年国服上榜分z-score趋势", xaxis=dict(title="时间"), yaxis=dict(title="国服上榜分z-score"))
    for hero in st.session_state.hero_list:
        fig.add_trace(go.Scatter(x=chart_data.columns, y=chart_data.loc[hero, :], name=hero))
    st.plotly_chart(fig, use_container_width=True)
