import requests
import streamlit as st
# Streamlit frontend
# Configure Page
st.set_page_config(page_title="Task & Mood Tracker", layout="centered")
st.title("🎓 Task & Mood Tracker :heart:")

# Backend API Base URL Configuration
API_URL = st.sidebar.text_input("Backend API Base URL", value="https://YOUR-NEW-BACKEND-URL.onrender.com")
# API_URL = "https://task-and-mood.onrender.com"

# Navigation Menu
option = st.sidebar.selectbox(
    "Select Action",
    [
        "View All Entries",
        "View entry by ID",
        "Add New Entry",
        "Update Entry",
        "Delete Entry",
        "Search by Mood"
    ],
    
)


# ==============================================================================
# 1. READ ALL Entries
# ==============================================================================
if option == "View All Entries":
    st.subheader("All entrie records")
    task_filter=st.text_input("Filter by Task(Optional)", placeholder="e.g., clean room")
    if st.button("Fetch entries"):
        try:
            params ={"task":task_filter} if task_filter else{}
            response = requests.get(f"{API_URL}/details",params=params)
            st.write("Status code:", response.status_code)
            st.write("Response:", response.text)
            data=response.json()
            if data:
                st.json(data)
            else:
                st.info("No Entries found")
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")
elif option == "Search by Mood":
    st.subheader("😊 Search Entries by Mood")
    mood = st.text_input("Enter mood (e.g., happy, sad, neutral)")

    if st.button("Search"):
        try:
            response = requests.get(f"{API_URL}/details/by-mood", params={"mood": mood})
            data = response.json()
            if data:
                st.json(data)
            else:
                st.info("No entries found with that mood.")
        except Exception as e:
            st.error(f"Connection error: {e}")

# ==============================================================================
# 2. READ SINGLE STUDENT
# ==============================================================================
elif option == "View entry by ID":
    st.subheader("search entrie by ID")
    id = st.number_input("Enter entry ID", min_value=0,step=1)


    if st.button("Get Details"):
        try:
            response = requests.get(f"{API_URL}/details")
            data = response.json()
            found = False
            for entry in data:
                if entry["id"] == id:
                    st.success("Entry Found!")
                    st.json(entry)
                    found = True
            if not found:
                st.warning("Entry not found")
        except Exception as e:
            st.error(f"Failed to connect to backend API: {e}")
# ==============================================================================
# 3. CREATE STUDENT (POST)
# ==============================================================================
elif option == "Add New Entry":
    st.subheader("➕ Add New Entry")

    with st.form("add Entry form"):
        task = st.text_input("Entry name")
        status = st.text_input("Status")
        mood = st.text_input("Mood")

        submit_button = st.form_submit_button("Create Entry")

        if submit_button:
            if not task or not mood:
                st.warning("Please fill in all fields.")
            else:
                payload = {"task": task, "status": status, "mood": mood}
                try:
                    response = requests.post(
                        f"{API_URL}/send_data", json=payload
                    )
                    st.success("entry created successfully!")
                    st.json(response.json())
                except Exception as e:
                    st.error(f"Connection error: {e}")

# =============================================================================
# 4. UPDATE STUDENT (PUT)
# ==============================================================================
elif option == "Update Entry":
    st.subheader("✏️ Update Existing entry")

    id = st.number_input("Enter Entry ID to Update", min_value=0, step=1)

    if st.button("Load Entry"):
        response = requests.put(f"{API_URL}/details")
        st.write("Status code:", response.status_code)
        st.write("Response:", response.text)
        data = response.json()
        for entry in data:
            if entry["id"] == id:
                st.json(entry)

    with st.form("update_entry_form"):
        task = st.text_input("Updated task")
        status= st.text_input("Updated status")
        mood = st.text_input("Updated mood")

        submit_button = st.form_submit_button("Update entry")

        if submit_button:
            payload = {"task": task, "status": status, "mood": mood}
            try:
                response = requests.put(
                    f"{API_URL}/details/{id}", json=payload
                )
                data = response.json()

                if "error" in data:
                    st.warning(data["error"])
                else:
                    st.success(f"entry #{id} updated successfully!")
                    st.json(data)
            except Exception as e:
                st.error(f"Connection error: {e}")

# ==============================================================================
# 5. DELETE STUDENT (DELETE)
# ==============================================================================
elif option == "Delete Entry":
    st.subheader("🗑️ Delete Entry Record")

    id = st.number_input("Enter Student ID to Delete", min_value=0, step=1)

    if st.button("Delete entry", type="primary"):
        try:
            response = requests.delete(f"{API_URL}/delete/{id}")
            data = response.json()

            if "error" in data:
                st.warning(data["error"])
            else:
                st.success(f"Entry #{id} deleted successfully!")
                st.json(data)
        except Exception as e:
            st.error(f"Connection error: {e}")
