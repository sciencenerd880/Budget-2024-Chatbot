import streamlit as st

# Define a UserProfile class to store user inputs from the Streamlit Form
class UserProfile:
    def __init__(self, age, citizenship, avg_income, av_residence, num_properties):
        self.age = age
        self.citizenship = citizenship
        self.avg_income = avg_income
        self.av_residence = av_residence
        self.num_properties = num_properties
        # self.cpf_savings = cpf_savings
        # self.cpf_life = cpf_life
        # self.disability_status = disability_status
    
    def __str__(self):
        return (f"User Profile: \n"
                f"Age: {self.age}\n"
                f"Citizenship: {self.citizenship}\n"
                f"Average Monthly Income: {self.avg_income}\n"
                f"Annual Value of Residence: {self.av_residence}\n"
                f"Number of Properties: {self.num_properties}\n"
                #f"CPF Savings: {self.cpf_savings}\n"
                #f"CPF LIFE Status: {self.cpf_life}\n"
                #f"Disability Status: {self.disability_status}\n"
                )

def user_profile_form():
    # Streamlit form to capture user inputs
    #st.title("Eligibility Form for Majulah Package Bonuses")
    with st.form("user_profile_form"):
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False
        # Basic Demographics
        st.subheader("Basic Information")
        
        age = st.number_input("Enter your Age", 
                              min_value=1, max_value=120, step=1, 
                              value=68,
                              help="Please enter your current age as of birthdate. Age must be between 1 and 120.")
        citizenship = st.selectbox("Are you a Singapore Citizen?", ("Yes", "No"))

        # Income Information
        st.subheader("Income Information")
        avg_income = st.selectbox("Average Monthly Income", 
                                ("$500-$2,500", "$2,500-$3,500", "$3,500-$6,000"),
                                help="Please enter your average monthly income in SGD before taxes. Include bonuses or allowances if applicable.")
        # "Less than $500", 
        
        # Housing Information
        st.subheader("Housing Information")
        av_residence = st.selectbox("Annual Value (AV) of Residence", ("Less than $25,000", "More than $25,000"),
                                    help='Please enter the Annual Value of your residence as stated in the property tax notice. This is used for government-related schemes.')
        num_properties = st.selectbox("Number of Properties Owned", ("1", "2 or more"),
                                      help='Please input only local/Singapore Properties owned including commercial properties under yourself.')

        # # CPF Information
        # st.subheader("CPF Information")
        # cpf_savings = st.selectbox("CPF Retirement Savings", ("Below $60,000", "Between $60,000 and $99,400"))
        # cpf_life = st.selectbox("Are you a CPF LIFE Member?", ("Yes", "No"))

        # # Special Conditions
        # st.subheader("Special Conditions")
        # disability_status = st.selectbox("Do you have any disabilities or are a caregiver for someone with disabilities?", ("Yes", "No"))
        
        def save_user_profile():
            st.session_state.clicked = True
            user_profile = UserProfile(
                age=age, 
                citizenship=citizenship, 
                avg_income=avg_income, 
                av_residence=av_residence, 
                num_properties=num_properties, 
                #cpf_savings=cpf_savings, 
                #cpf_life=cpf_life, 
                #disability_status=disability_status, 
            )
            #st.session_state['page'] = "chat"
            st.session_state['page'] = "chat"
            st.session_state['user_profile'] = user_profile
            print('at external',user_profile)
            return user_profile

        # Submit button
        user_profile = st.form_submit_button("Submit", on_click=save_user_profile)
        
        # Display the user's profile
        if user_profile:
            st.write("Your Profile has been saved!")
            st.text(str(user_profile))
            #st.session_state['page'] = "chat"
            #return user_profile