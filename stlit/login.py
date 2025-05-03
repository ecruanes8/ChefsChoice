import streamlit as st

# ✅ Dummy user store (you can later hash or pull from database)
users = {
    "ecruanes": {"password": "test123", "name": "Eve Cruanes"},
    "rbriggs": {"password": "pass456", "name": "Rebecca Briggs"}
}

def login():
    st.title("Login")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = users.get(username)
            if user and user["password"] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.name = user["name"]
                st.success(f"Welcome, {user['name']}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    else:
        st.success(f"You're already logged in as {st.session_state['name']}")
        if st.button("Logout"):
            for key in ["authenticated", "username", "name"]:
                st.session_state.pop(key, None)
            st.rerun()
