import streamlit as st 

def main():

	st.title("Question Duplicacy")


	activities = ["Dashboard","Question Match","Question Search"]

	choices = st.sidebar.selectbox('Select Activities',activities)

	if choices == 'Dashboard':
		st.subheader("Dashboard")

	elif choices == 'Question Match':
		with st.form("my_form"):
			question1 = st.text_area('Question 1', '''
		''')
			question2 = st.text_area('Question 2', '''
			''')
			
			st.form_submit_button(label="Submit", on_click=None, kwargs={"question1": question1, "question2": question2}, type="secondary")

	elif choices == 'Question Search':
		st.subheader("Question Search")


if __name__ == '__main__':
	main()