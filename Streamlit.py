import streamlit as st
import pandas as pd
import hashlib
from transformers import pipeline
from streamlit_drawable_canvas import st_canvas
from translate import Translator



def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()
	
def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def Sentiment():
	st.title('Sentiment Analyser App')
	page_bg_img = '''
		<style>
			.stApp,.e8zbici2 {
			background-image: url("https://images-na.ssl-images-amazon.com/images/I/61+oIVFF7FL.png");
			background-size: cover;
			}
			</style>
			'''

	st.markdown(page_bg_img, unsafe_allow_html=True)
	form = st.form(key='sentiment-form')
	user_input = form.text_area('Enter your text')

	submit = form.form_submit_button('Submit')
		
	if submit:
		classifier = pipeline("sentiment-analysis")		
		result = classifier(user_input)[0]
		label = result['label']
		score = result['score']
	
		if label == 'POSITIVE':
			st.success(f'{label} sentiment (score: {score})')
		else:
			st.error(f'{label} sentiment (score: {score})')
def draw():
	st.header("End-to-end Cypress test")
	canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=10,
    stroke_color="green",
    background_color="#eee",
    height=150,
    width=500,
    drawing_mode="freedraw",
    key="canvas",)
	page_bg_img = '''
		<style>
			.stApp,.e8zbici2 {
			background-image: url("https://images-na.ssl-images-amazon.com/images/I/61+oIVFF7FL.png");
			background-size: cover;
			}
			</style>
			'''

	st.markdown(page_bg_img, unsafe_allow_html=True)
	
	if canvas_result.image_data is not None:
		st.image(canvas_result.image_data)
		st.dataframe(pd.json_normalize(canvas_result.json_data["objects"]))
def translate():
		st.title("Text Translator ❤")

		text=st.text_input("Write here")
		lan1=st.selectbox("Select Language from",["English","Spanish","French","German","Japanese","Latin"])
		lan2=st.selectbox("Translate to ",["Spanish","German","French","Latin","Japanese","English"])

		translator=  Translator(from_lang=lan1.lower(),to_lang=lan2.lower())
		translation = translator.translate(text)
		page_bg_img = '''
		<style>
			.stApp,.e8zbici2 {
			background-image: url("https://images-na.ssl-images-amazon.com/images/I/61+oIVFF7FL.png");
			background-size: cover;
			}
			</style>
			'''

		st.markdown(page_bg_img, unsafe_allow_html=True)
		if(st.button("TRANSLATE")): 
			st.header(' ')
		st.header(translation)

def main():
	st.title("WEB TEXT ANALYSIS")
	
	menu = ["Home","Login","SignUp"]
	page_bg_img = '''
		<style>
			.stApp,.e8zbici2 {
			background-image: url("https://images-na.ssl-images-amazon.com/images/I/61+oIVFF7FL.png");
			background-size: cover;
			}
			</style>
			'''

	st.markdown(page_bg_img, unsafe_allow_html=True)
	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Home":
		st.subheader("Home")
	elif choice == "Login":
		st.subheader("Login Section")
		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))
				task = st.selectbox("Task",["Draw Signature","Analytics","Translate","Profiles"])
				if task == "Draw Signature":
					st.subheader(draw())
				elif task == "Analytics":
					st.subheader(Sentiment())
				elif task == "Translate":
					st.subheader(translate())
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")
	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
if __name__ == '__main__':
	main()