import re

import streamlit as st

# 初始化
st.set_page_config(layout='wide', page_icon='😏')
if 'pattern' not in st.session_state:
    st.session_state['pattern'] = '[a-s]{3}'
if 'text' not in st.session_state:
    st.session_state['text'] = 'this is the test string!'

# 标题
st.markdown("# S31 梦奇出装分析\n\n### *by 果果分水果* 😎")

# 推荐出装
st.markdown('## 个人推荐出装')
with st.expander('🤾 别说话，点我！'):
    tab1, tab2, tab3 = st.tabs(['第一套', '第二套', '第三套'])
    tab1.image(r'./data/出装1.png')
    tab2.image(r'./data/出装2.png')
    tab3.image(r'./data/出装3.png')

# 题外话
st.markdown('## 题外话\n\n最近在学习 ***Streamlit*** ，'
            '一个快速搭建页面的 Python web 框架，很适合快速验证想法、演示数据、制作小工具等。'
            '今天的这个简易网页就是用 Streamlit 写的。'
            '看完这期视频，你也能大致体会到 Streamlit 的能耐了👍')

# 小工具
with st.expander('🎸 这是一个简单的小工具'):
    with st.echo():
        st.success('💪 so easy!')  # 你会读吗?
        col1, col2 = st.columns(2)  # 双列布局
        with col1:  # 第一列
            text = st.text_input('文本', value='Madness? This is Sparta! 🦵 😨')  # 输入框，用于输入文本
            pattern = st.text_input('模式', value='[a-zA-Z]+')  # 输入框，用于输入模式
        with col2:  # 第二列
            st.write('结果:', re.findall(pattern, text))  # 显示结果
