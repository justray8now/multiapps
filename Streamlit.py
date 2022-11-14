import hashlib
import pandas as pd
import streamlit as st
import tweepy as tw
from transformers import pipeline
from translate import Translator

st.title("WEB TEXT ANALYSIS ")

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


api_key = 'Jx83pyq5CcytIpFlsUSlVBZHi'
api_key_secret = 'FJhW9tD6QerZ1zved8CyBsTh1Y8cx1n4IVkIUuHu8nDIm7OQk9'
access_token = '1582171594067443712-VfKh6tfMenQgjHnbXT1wzIqPBug8Kt'
access_token_secret = 'YBkuskp8B1IMbdTxPAMoIWNe7FYVlx6qEudj18ULAtA2e'
auth = tw.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

classifier = pipeline('sentiment-analysis')

def run():  
	st.title('Twitter Analyser App')
	st.markdown('Analisis sentiment twitter secara online!')
	with st.form(key="key1"):
		search_words = st.text_input('Masukkan topik yang ingin di analisis')
		no_of_tweets = st.number_input('Masukkan jumlah cuitan (maximum 50 cuitan)', 0,50,10)
		submit_button = st.form_submit_button("Analisis")
	if submit_button:
		tweets = tw.Cursor(api.search_tweets,q=search_words,lang="id").items(no_of_tweets)
		tweet_list = [i.text for i in tweets]
		output = [i for i in classifier(tweet_list)]
		labels =[output[i]['label'] for i in range(len(output))]
		df = pd.DataFrame(list(zip(tweet_list, labels)),columns =['Latest '+str(no_of_tweets)+' tweets'+' on '+search_words, 'Sentiment'])
		st.write(df)
		

		if __name__=='__main__':
			run()
	


def Sentiment():
	st.title('Sentiment Analyser App')
	
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

def translate():
		st.title("Text Translator App")

		text=st.text_input("Write here")
		lan1=st.selectbox("Select Language from",["English","Spanish","French","German","Japanese","Latin"])
		lan2=st.selectbox("Translate to ",["Spanish","German","French","Latin","Japanese","English"])

		translator=  Translator(from_lang=lan1.lower(),to_lang=lan2.lower())
		translation = translator.translate(text)
		page_bg_img = '''
		<style>
			.stApp,.e8zbici2 {
			background-image: url("https://raw.githubusercontent.com/justray8now/multiapps/main/background1.png");
			background-size: cover;
			}
			</style>
			'''

		st.markdown(page_bg_img, unsafe_allow_html=True)
		if(st.button("Translate")): 
			st.header(' ')
		st.header(translation)	

def main():
	
	menu = ["Home","Login","SignUp"]
	page_bg_img = '''
		<style>
			.stApp,.e8zbici2 {
			background-image: url("https://raw.githubusercontent.com/justray8now/multiapps/main/background1.png");
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
				task = st.selectbox("Task",["Scrapper","Analytics","Translate","Profiles"])
				if task == "Scrapper":
						st.subheader(run())
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