import streamlit as st

st.set_page_config(page_title="Career Salary Predictor")

# Background
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
background: repeating-linear-gradient(
  45deg,
  #2c2c2c,
  #2c2c2c 10px,
  #1a1a1a 10px,
  #1a1a1a 20px
);
color: white;
}
</style>

"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("💼 Career Salary Predictor")

# Initialize session state
if "career" not in st.session_state:
    st.session_state.career = None

if "experience" not in st.session_state:
    st.session_state.experience = 0

# Function to handle button click
def select_career(career_name):
    st.session_state.career = career_name
    st.session_state.experience = 0   

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("💻 Software Engineer"):
        select_career("SE")

with col2:
    if st.button("📈 Sales Officer"):
        select_career("SO")
# If selected
if st.session_state.career:

    experience = st.slider(
        "Years of Experience",
        0, 25,
        key="experience" 
    )

    if st.session_state.career == "SE":
        base = 4
        growth = 0.8
        role = "Software Engineer"
    else:
        base = 3
        growth = 0.5
        role = "Sales Officer"

    salary = base + (experience * growth)

    st.write(f"### 🎯 Role: {role}")
    st.write(f"### 💰 Expected Salary: ₹{salary:.2f} LPA") 
st.write("NOTE: salery vary based on location, company and skills level")