import streamlit as st
import json
import os
from datetime import datetime
import qrcode
from PIL import Image
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'vehicles' not in st.session_state:
    st.session_state.vehicles = []
if 'qr_registry' not in st.session_state:
    st.session_state.qr_registry = []
if 'total_entries' not in st.session_state:
    st.session_state.total_entries = 0
if 'user' not in st.session_state:
    st.session_state.user = None

# Load data from file if exists
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
            st.session_state.vehicles = data.get('vehicles', [])
            st.session_state.qr_registry = data.get('qr_registry', [])
            st.session_state.total_entries = data.get('total_entries', 0)
            st.session_state.user = data.get('user', None)

def save_data():
    data = {
        'vehicles': st.session_state.vehicles,
        'qr_registry': st.session_state.qr_registry,
        'total_entries': st.session_state.total_entries,
        'user': st.session_state.user
    }
    with open('data.json', 'w') as f:
        json.dump(data, f)

load_data()

# Auth functions
def login(email, password):
    if st.session_state.user and st.session_state.user['email'] == email and st.session_state.user['password'] == password:
        st.session_state.logged_in = True
        return True
    return False

def signup(name, email, password):
    st.session_state.user = {'name': name, 'email': email, 'password': password}
    save_data()

# QR functions
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

# Main app
def main():
    st.set_page_config(page_title="V-Security Pro", layout="wide")
    
    if not st.session_state.logged_in:
        st.title("V-Security Pro | Enhanced Vehicle Management")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                if login(email, password):
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        with tab2:
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Sign Up"):
                signup(name, email, password)
                st.success("Registered! Please login.")
    
    else:
        st.sidebar.title("V-Security Pro")
        menu = st.sidebar.radio("Navigation", ["Dashboard", "QR Management", "Pass Registry", "Vehicle Logs", "Logout"])
        
        if menu == "Dashboard":
            st.header("Security Dashboard")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Logs", st.session_state.total_entries)
            counts = {'Cars': 0, 'Motorcycle': 0, 'Private': 0, 'Deliveries': 0}
            for v in st.session_state.vehicles:
                v_type = v.get('type', 'Private')
                if v_type in counts:
                    counts[v_type] += 1
            col2.metric("Cars", counts.get('Cars', 0))
            col3.metric("Motorcycle", counts.get('Motorcycle', 0))
            col4.metric("Private", counts.get('Private', 0))
            
            # Charts
            fig, ax = plt.subplots()
            labels = ['Cars', 'Motorcycle', 'Private', 'Deliveries']
            ax.pie([counts.get(l, 0) for l in labels], labels=labels, autopct='%1.1f%%')
            st.pyplot(fig)
        
        elif menu == "QR Management":
            st.header("QR Access Control")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Generate Digital Pass")
                photo = st.file_uploader("Add Owner Photo", type=['png', 'jpg', 'jpeg'])
                name = st.text_input("Owner Name")
                plate = st.text_input("Plate Number")
                phone = st.text_input("Contact #")
                messenger = st.text_input("Facebook (Optional)")
                qr_type = st.selectbox("Type", ["Cars", "Motorcycle", "Private", "Deliveries"])
                if st.button("Generate & Save"):
                    if name and plate:
                        photo_data = ""
                        if photo:
                            photo_data = base64.b64encode(photo.read()).decode()
                        data = {
                            'name': name,
                            'plate': plate,
                            'phone': phone,
                            'messenger': messenger,
                            'type': qr_type,
                            'photo': photo_data,
                            'id': datetime.now().timestamp()
                        }
                        st.session_state.qr_registry.append(data)
                        save_data()
                        qr_img = generate_qr({'id': data['id'], 'plate': plate, 'name': name, 'type': qr_type})
                        st.image(qr_img, caption=name)
                        st.success("Pass generated!")
                    else:
                        st.error("Name and Plate required")
            
            with col2:
                st.subheader("Scan Entry/Exit")
                # Placeholder for scanner; in real app, integrate camera
                st.info("Scanner not implemented in this demo. Use manual entry.")
                scan_input = st.text_area("Manual QR Data (JSON) - Continuous Mode (One per line)")
                manual_spot = st.text_input("Assign Parking Spot (Applies to entry batch)")
                if st.button("Process Scan"):
                    lines = [l.strip() for l in scan_input.split('\n') if l.strip()]
                    for line in lines:
                        data = None
                        try:
                            data = json.loads(line)
                            # If only ID provided, fetch details from registry
                            if isinstance(data, dict) and 'id' in data and 'plate' not in data and data.get('type') != 'helmet':
                                reg = next((q for q in st.session_state.qr_registry if q.get('id') == data['id']), None)
                                if reg:
                                    data.update({'plate': reg['plate'], 'name': reg['name'], 'type': reg['type']})
                        except json.JSONDecodeError:
                            # Fallback: Treat as plain plate number
                            plate = line.strip().upper()
                            reg = next((q for q in st.session_state.qr_registry if q.get('plate', '').upper() == plate), None)
                            if reg:
                                data = {'id': reg['id'], 'plate': reg['plate'], 'name': reg['name'], 'type': reg['type']}
                            else:
                                data = {'plate': plate, 'name': 'Manual Entry', 'type': 'Private'}

                        if data:
                            now = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
                            idx = next((i for i, v in enumerate(st.session_state.vehicles) if v.get('plate', '').upper() == data.get('plate', '').upper() and v.get('logOutTime') == "---"), -1)
                            if idx != -1:
                                st.session_state.vehicles[idx]['logOutTime'] = now
                                st.success(f"Goodbye {data.get('name')}!")
                            else:
                                st.session_state.vehicles.append({**data, 'logInTime': now, 'logOutTime': "---", 'type': data.get('type', 'Private'), 'spot': manual_spot if manual_spot else "N/A"})
                                st.session_state.total_entries += 1
                                st.success(f"Welcome {data.get('name')}!")
                        else:
                            st.error(f"Invalid Input: {line}")
                    save_data()
                    st.rerun()
        
        elif menu == "Pass Registry":
            st.header("Issued Pass Registry")
            for item in st.session_state.qr_registry:
                col1, col2, col3 = st.columns([1, 3, 1])
                if item['photo']:
                    col1.image(base64.b64decode(item['photo']), width=50)
                col2.write(f"{item['name']} - {item['plate']}")
                col3.write(item['type'])
                if st.button(f"View {item['id']}", key=f"view_{item['id']}"):
                    st.write(f"Name: {item['name']}")
                    st.write(f"Type: {item['type']}")
                    st.write(f"Plate: {item['plate']}")
                    st.write(f"Phone: {item['phone']}")
                    qr_img = generate_qr({'id': item['id'], 'plate': item['plate'], 'name': item['name'], 'type': item['type']})
                    st.image(qr_img)
        
        elif menu == "Vehicle Logs":
            st.header("Vehicle Logs")
            df = pd.DataFrame(st.session_state.vehicles)
            st.dataframe(df)
        
        elif menu == "Logout":
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()