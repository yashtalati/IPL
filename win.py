import streamlit as st
import pickle
import pandas as pd
import base64



def add_bg(image_file):
    if image_file.endswith('png'):
        mime_type = 'png'
    elif image_file.endswith('webp'):
        mime_type = 'webp'
    else:
        st.warning("Unsupported file format.")
        return
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    style = f"""
    <style>
    .stApp {{
        background-image: url('data:image/{mime_type};base64,{encoded_string}');
        background-size: cover;
        background-position: center;
        opacity: 1.0;

    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

add_bg('b3.png')



teams = [
    'Chennai Super Kings',
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Punjab Kings',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Gujarat Titans',
    'Lucknow Super Giants'
]

wickets_fell = [ '1','2', '3', '4', '5', '6', '7', '8','9']


cities =['Ahmedabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai', 'Hyderabad',
       'Mohali', 'Jaipur', 'Bangalore']

pipe = pickle.load(open('p2.pkl','rb'))

st.markdown("<h1 class='title'>Win Predictor</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Select Batting Team</p>""", unsafe_allow_html=True)
    BattingTeam = st.selectbox ("", sorted(teams),key='batting_team_selectbox')

with col2:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Select Bowling Team</p>""", unsafe_allow_html=True)
    BowlingTeam = st.selectbox('',sorted(teams), key='bowling_team_selectbox')

col3, col4 = st.columns(2)

with col3:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Select Host City</p>""", unsafe_allow_html=True)
    selected_city = st.selectbox ("", sorted(cities),key='city_selectbox')

with col4:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Target</p>""",
                unsafe_allow_html=True)
    target = st.number_input('', step=1)

col5,col6,col7 = st.columns(3)

with col5:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Current Score</p>""", unsafe_allow_html=True)
    score = st.number_input('', step=1, key='a')
with col6:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Over Done</p>""", unsafe_allow_html=True)
    overs = st.number_input('', step= 0.5, key='b')

with col7:
    st.markdown("""<p style='font-weight: bold; color:#F5F923; font-size:30px'>Wickets Fell</p>""", unsafe_allow_html=True)
    wicket = st.number_input('', step=1 , key='c')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wicket = 10 - wicket
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'BattingTeam':[BattingTeam],'BowlingTeam':[BowlingTeam],'City':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wicket':[wicket],'total_run_x':[target],'crr':[crr],'rrr':[rrr]})


    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(BattingTeam + "- " + str(round(win*100)) + "%")
    st.header(BowlingTeam + "- " + str(round(loss*100)) + "%")