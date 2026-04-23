import streamlit as st
import json
import os
from datetime import datetime
import qrcode
import base64
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="V-Security Pro", layout="wide", initial_sidebar_state="expanded")

# Enhanced Glassmorphism CSS
st.markdown(
    '''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');
    
    :root {
        --sidebar-bg: rgba(0, 0, 0, 0.15);
        --active-blue: #1a73e8;
        --card-bg: rgba(255, 255, 255, 0.33);
        --text-dark: #000000;
        --text-muted: #333333;
        --success: #ffd700;
        --warning: #ff7f50;
        --info: #1a73e8;
        --orange: #ff6b35;
        --yellow: #ffd700;
    }
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #e0eafc, #cfdef3);
        min-height: 100vh;
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
    }
    
    [data-testid="stSidebarNav"] {
        background: var(--sidebar-bg) !important;
        backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255,255,255,0.4);
        border-radius: 0 24px 24px 0;
    }
    
    [data-testid="stSidebar"] {
        background: transparent !important;
    }
    
    .stButton>button {
        border-radius: 50px !important;
        font-weight: 600 !important;
        background: #ff7f50 !important;
        border: none !important;
        color: white !important;
        padding: 10px 30px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255, 127, 80, 0.4) !important;
    }
    
    .glass-card {
        background: var(--card-bg) !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        border-radius: 28px !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        padding: 28px !important;
        box-shadow: inset 5px 5px 15px rgba(255,255,255,0.4), 10px 10px 30px rgba(0,0,0,0.08) !important;
    }
    
    .metric-card {
        background: rgba(255,255,255,0.35) !important;
        border: 1px solid rgba(255,255,255,0.68) !important;
        border-radius: 24px !important;
        padding: 22px !important;
        text-align: center !important;
        backdrop-filter: blur(15px) !important;
    }
    
    .metric-card h3 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 10px 0 0 0 !important;
        color: var(--text-dark) !important;
    }
    
    .metric-label {
        font-size: 0.85rem !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] select,
    [data-testid="stFileUploader"] input {
        border-radius: 40px !important;
        background: rgba(255,255,255,0.88) !important;
        border: 1px solid rgba(255,255,255,0.9) !important;
        padding: 14px 20px !important;
        color: var(--text-dark) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {
        color: #999 !important;
    }
    
    .stDataFrame {
        border-radius: 20px !important;
    }
    
    .registry-item {
        background: rgba(255,255,255,0.34) !important;
        border: 1px solid rgba(255,255,255,0.7) !important;
        border-radius: 24px !important;
        padding: 18px !important;
        margin-bottom: 14px !important;
        backdrop-filter: blur(15px) !important;
        transition: all 0.3s ease !important;
    }
    
    .registry-item:hover {
        transform: translateY(-2px) !important;
        background: rgba(255,255,255,0.45) !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    }
    
    .qr-preview {
        background: rgba(255,255,255,0.95) !important;
        padding: 20px !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255,255,255,0.9) !important;
        text-align: center !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .success-badge {
        background: var(--success) !important;
        color: white !important;
        padding: 6px 16px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    .warning-badge {
        background: var(--warning) !important;
        color: #333 !important;
        padding: 6px 16px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    .info-badge {
        background: var(--info) !important;
        color: white !important;
        padding: 6px 16px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark) !important;
        font-weight: 800 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--active-blue) !important;
        border-bottom: 3px solid var(--active-blue) !important;
    }
    </style>
    ''',
    unsafe_allow_html=True,
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'Login'
if 'vehicles' not in st.session_state:
    st.session_state.vehicles = []
if 'qr_registry' not in st.session_state:
    st.session_state.qr_registry = []
if 'total_entries' not in st.session_state:
    st.session_state.total_entries = 0
if 'user' not in st.session_state:
    st.session_state.user = None
if 'custom_bg' not in st.session_state:
    st.session_state.custom_bg = None

# Load data from file if exists
def load_data():
    """Load user and vehicle data from JSON file"""
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Load user
                user = data.get('user')
                if isinstance(user, dict) and user.get('email'):
                    st.session_state.user = user
                
                # Load vehicles
                vehicles = data.get('vehicles', [])
                if isinstance(vehicles, list):
                    st.session_state.vehicles = vehicles
                
                # Load QR registry
                qr_registry = data.get('qr_registry', [])
                if isinstance(qr_registry, list):
                    st.session_state.qr_registry = qr_registry
                
                # Load total entries
                total = data.get('total_entries', 0)
                st.session_state.total_entries = int(total) if total else 0
                
                # Load custom background
                bg = data.get('custom_bg')
                if bg:
                    st.session_state.custom_bg = bg
        except Exception as e:
            st.error(f'⚠️ Error loading data: {str(e)}')
            st.session_state.vehicles = []
            st.session_state.qr_registry = []
            st.session_state.total_entries = 0
            st.session_state.user = None

def save_data():
    """Save user and vehicle data to JSON file"""
    try:
        data = {
            'vehicles': st.session_state.vehicles,
            'qr_registry': st.session_state.qr_registry,
            'total_entries': st.session_state.total_entries,
            'user': st.session_state.user,
            'custom_bg': st.session_state.custom_bg
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f'⚠️ Failed to save data: {str(e)}')

# Auth functions
def login(email, password):
    """Authenticate user against stored credentials"""
    if not st.session_state.user:
        return False
    
    stored_email = st.session_state.user.get('email', '')
    stored_pass = st.session_state.user.get('password', '')
    
    return email.strip() == stored_email.strip() and password == stored_pass

def signup(name, email, password):
    """Create new user account"""
    if not name.strip() or not email.strip() or not password.strip():
        return False
    
    st.session_state.user = {
        'name': name.strip(),
        'email': email.strip(),
        'password': password
    }
    save_data()
    return True


def apply_custom_background():
    """Apply custom background image if available"""
    if st.session_state.custom_bg:
        st.markdown(
            f'''
            <style>
            html, body, [data-testid="stAppViewContainer"] {{
                background-image: url("{st.session_state.custom_bg}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
            }}
            </style>
            ''',
            unsafe_allow_html=True
        )


def upload_background():
    """Handle background image upload"""
    bg_file = st.file_uploader('🖼️ Change Background', type=['png', 'jpg', 'jpeg'], key='bg_uploader')
    if bg_file:
        try:
            bg_data = base64.b64encode(bg_file.read()).decode()
            bg_url = f"data:image/{'png' if bg_file.name.endswith('.png') else 'jpeg'};base64,{bg_data}"
            st.session_state.custom_bg = bg_url
            save_data()
            st.success('✅ Background updated! Refresh to see changes.')
        except Exception as e:
            st.error(f'❌ Failed to upload background: {str(e)}')

# QR functions
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img

# Main app
def main():
    load_data()
    apply_custom_background()
    
    if not st.session_state.logged_in:
        # Modern Auth UI
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.markdown(
                '''
                <div style="text-align: center; margin-bottom: 40px;">
                    <h1 style="font-size: 2.8rem; margin-bottom: 8px;">🔐 V-Security Pro</h1>
                    <p style="color: #333333; font-size: 1.05rem; margin: 0;">Enhanced Vehicle Management System</p>
                </div>
                ''',
                unsafe_allow_html=True,
            )
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Auth mode selector
            tab1, tab2 = st.tabs(['🔑 Login', '📝 Sign Up'])
            
            with tab1:
                st.markdown('### Sign Into Your Account')
                
                if st.session_state.user:
                    st.info(f'✅ Account registered: **{st.session_state.user.get("email")}**')
                
                email_input = st.text_input(
                    'Email Address', 
                    key='login_email', 
                    placeholder='admin@example.com',
                    label_visibility='collapsed'
                )
                password_input = st.text_input(
                    'Password', 
                    type='password', 
                    key='login_pass', 
                    placeholder='••••••••',
                    label_visibility='collapsed'
                )
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                with col_btn2:
                    if st.button('🔓 LOGIN', use_container_width=True, key='login_btn'):
                        if not email_input or not password_input:
                            st.error('❌ Please enter email and password')
                        elif login(email_input, password_input):
                            st.session_state.logged_in = True
                            st.balloons()
                            st.success('✅ Login successful! Redirecting...')
                            st.rerun()
                        else:
                            st.error('❌ Invalid email or password')
            
            with tab2:
                st.markdown('### Create New Account')
                
                name_input = st.text_input(
                    'Full Name', 
                    key='signup_name', 
                    placeholder='John Doe',
                    label_visibility='collapsed'
                )
                email_input = st.text_input(
                    'Email Address', 
                    key='signup_email', 
                    placeholder='admin@example.com',
                    label_visibility='collapsed'
                )
                password_input = st.text_input(
                    'Password', 
                    type='password', 
                    key='signup_pass', 
                    placeholder='••••••••',
                    label_visibility='collapsed'
                )
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                with col_btn2:
                    if st.button('✨ CREATE ACCOUNT', use_container_width=True, key='signup_btn'):
                        if not name_input.strip() or not email_input.strip() or not password_input.strip():
                            st.error('❌ All fields are required')
                        elif len(password_input) < 4:
                            st.error('❌ Password must be at least 4 characters')
                        elif signup(name_input, email_input, password_input):
                            st.success('✅ Account created successfully!')
                            st.info('👉 Go to the **Login** tab to sign in')
                        else:
                            st.error('❌ Failed to create account')
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Main Dashboard UI
        with st.sidebar:
            if st.session_state.user:
                st.markdown(
                    f'<div style="padding: 15px; background: rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 20px;"><p style="margin: 0; color: #333; font-size: 0.9rem;">👤 {st.session_state.user.get("name", "User")}</p><p style="margin: 5px 0 0 0; color: #666; font-size: 0.8rem;">{st.session_state.user.get("email")}</p></div>',
                    unsafe_allow_html=True
                )
            
            st.markdown('<h2 style="margin-top: 0;">V-Security Pro</h2>', unsafe_allow_html=True)
            st.markdown('---')
            
            page = st.radio(
                'Navigation',
                ['🎯 Dashboard', '📱 QR Management', '🏷️ Pass Registry', '🚗 Vehicle Logs'],
                label_visibility='collapsed'
            )
            
            st.markdown('---')
            if st.button('🚪 Logout', use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.auth_mode = 'Login'
                st.rerun()
            
            st.markdown('---')
            upload_background()
        
        # Page content
        if '🎯' in page:
            render_dashboard()
        elif '📱' in page:
            render_qr_management()
        elif '🏷️' in page:
            render_registry()
        elif '🚗' in page:
            render_vehicle_logs()


def render_dashboard():
    """Modern dashboard with metrics and charts"""
    st.markdown('<h2 class="glass-card" style="padding: 20px; margin-bottom: 20px;">🎯 Security Dashboard</h2>', unsafe_allow_html=True)
    
    # Calculate metrics
    counts = {'Cars': 0, 'Motorcycle': 0, 'Private': 0, 'Deliveries': 0}
    for v in st.session_state.vehicles:
        v_type = v.get('type', 'Private')
        if v_type in counts:
            counts[v_type] += 1
    
    # Metrics row
    metric_cols = st.columns(5)
    with metric_cols[0]:
        st.markdown(
            f'''<div class="metric-card">
                <div class="metric-label">📊 Total Logs</div>
                <h3>{st.session_state.total_entries}</h3>
            </div>''',
            unsafe_allow_html=True
        )
    with metric_cols[1]:
        st.markdown(
            f'''<div class="metric-card">
                <div class="metric-label">🚗 Cars</div>
                <h3 style="color: #ffd700;">{counts.get('Cars', 0)}</h3>
            </div>''',
            unsafe_allow_html=True
        )
    with metric_cols[2]:
        st.markdown(
            f'''<div class="metric-card">
                <div class="metric-label">🏍️ Motorcycle</div>
                <h3 style="color: #ff7f50;">{counts.get('Motorcycle', 0)}</h3>
            </div>''',
            unsafe_allow_html=True
        )
    with metric_cols[3]:
        st.markdown(
            f'''<div class="metric-card">
                <div class="metric-label">👤 Private</div>
                <h3 style="color: #1a73e8;">{counts.get('Private', 0)}</h3>
            </div>''',
            unsafe_allow_html=True
        )
    with metric_cols[4]:
        st.markdown(
            f'''<div class="metric-card">
                <div class="metric-label">📦 Deliveries</div>
                <h3 style="color: #ff6b35;">{counts.get('Deliveries', 0)}</h3>
            </div>''',
            unsafe_allow_html=True
        )
    
    st.markdown('')  # Spacing
    
    # Charts
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('#### 📈 Access Distribution Over Time')
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='none')
        ax.set_facecolor('rgba(255,255,255,0)')
        ax.plot([0, 1], [0, 1], color='#ff7f50', linewidth=3, label='Traffic')
        ax.fill_between([0, 1], 0, [0, 1], alpha=0.1, color='#ff7f50')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#ddd')
        ax.spines['bottom'].set_color('#ddd')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('#### 🎯 Access Types')
        figweb, axweb = plt.subplots(figsize=(5, 5), facecolor='none')
        axweb.set_facecolor('rgba(255,255,255,0)')
        colors = ['#ffd700', '#ff7f50', '#1a73e8', '#ff6b35']
        wedges, texts, autotexts = axweb.pie(
            [counts['Cars'], counts['Motorcycle'], counts['Private'], counts['Deliveries']],
            labels=['Cars', 'Motorcycle', 'Private', 'Deliveries'],
            autopct='%1.1f%%',
            colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        st.pyplot(figweb)
        st.markdown('</div>', unsafe_allow_html=True)


def render_qr_management():
    """QR generation and scanning interface"""
    st.markdown('<h2 class="glass-card" style="padding: 20px; margin-bottom: 20px;">📱 QR Access Control</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1.3])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('### 🎟️ Generate Digital Pass')
        
        photo_uploaded = st.file_uploader('📸 Owner Photo', type=['png', 'jpg', 'jpeg'], key='photo_uploader')
        owner_name = st.text_input('👤 Owner Name', placeholder='Full Name')
        plate_num = st.text_input('🚗 Plate Number', placeholder='ABC-1234')
        phone_num = st.text_input('📞 Contact #', placeholder='+1234567890')
        messenger_id = st.text_input('💬 Messenger (Optional)', placeholder='Facebook/WhatsApp')
        access_type = st.selectbox('🔑 Access Type', ['Cars', 'Motorcycle', 'Private', 'Deliveries'])
        
        if st.button('✈️ GENERATE & SAVE', use_container_width=True, key='gen_qr_btn'):
            if not owner_name.strip() or not plate_num.strip():
                st.error('❌ Owner name and plate number are required')
            else:
                photo_data = ''
                if photo_uploaded:
                    try:
                        photo_data = base64.b64encode(photo_uploaded.read()).decode()
                    except Exception as e:
                        st.warning(f'⚠️ Could not process photo: {str(e)}')
                
                qr_data = {
                    'name': owner_name.strip(),
                    'plate': plate_num.strip(),
                    'phone': phone_num.strip(),
                    'messenger': messenger_id.strip(),
                    'type': access_type,
                    'photo': photo_data,
                    'id': int(datetime.now().timestamp() * 1000)
                }
                st.session_state.qr_registry.append(qr_data)
                save_data()
                
                # Display generated QR
                st.markdown('<div class="qr-preview">', unsafe_allow_html=True)
                try:
                    qr_img = generate_qr({'id': qr_data['id'], 'plate': plate_num, 'name': owner_name, 'type': access_type})
                    st.image(qr_img, caption=f'✅ Pass Generated: {owner_name}', width=200)
                except Exception as e:
                    st.error(f'Failed to generate QR: {str(e)}')
                st.markdown('</div>', unsafe_allow_html=True)
                st.success('✅ Digital pass saved to registry!')
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('### 🔍 Scan Entry/Exit')
        
        st.info('📌 **Unlimited Mode**: Paste multiple QR JSONs or Plate numbers (one per line)')
        scan_json = st.text_area(
            'Continuous Scan Input',
            placeholder='Paste JSON objects or Plate numbers here...',
            height=200,
            label_visibility='collapsed'
        )
        manual_spot_val = st.text_input(
            '📍 Manual Spot Assignment (Applies to entry batch)',
            placeholder='e.g., A-10',
            key='manual_spot_input'
        )
        
        if st.button('⚡ PROCESS SCAN', use_container_width=True, key='process_scan_btn'):
            if not scan_json.strip():
                st.error('❌ Please paste QR data')
            else:
                lines = [l.strip() for l in scan_json.split('\n') if l.strip()]
                processed_count = 0
                entries = 0
                exits = 0
                
                for line in lines:
                    payload = None
                    try:
                        # 1. Try to parse as JSON (Full QR Data)
                        payload = json.loads(line)
                    except json.JSONDecodeError:
                        # 2. Fallback: Treat as plain plate number
                        plate = line.strip().upper()
                        # Check registry for metadata
                        reg_item = next((q for q in st.session_state.qr_registry if q.get('plate', '').upper() == plate), None)
                        if reg_item:
                            payload = {
                                'plate': reg_item.get('plate'),
                                'name': reg_item.get('name'),
                                'type': reg_item.get('type'),
                                'id': reg_item.get('id')
                            }
                        else:
                            payload = {'plate': plate, 'name': 'Manual Entry', 'type': 'Private'}

                    if payload and (payload.get('plate') or payload.get('type') == 'helmet'):
                        now = datetime.now().strftime('%m/%d/%Y, %I:%M %p')
                        
                        # Handle Helmet vs Vehicle
                        is_helmet = payload.get('type') == 'helmet'
                        search_key = 'id' if is_helmet else 'plate'
                        search_val = str(payload.get(search_key, '')).strip().upper() if not is_helmet else payload.get(search_key)
                        
                        # Find active session
                        idx = next((i for i, v in enumerate(st.session_state.vehicles) 
                                   if (str(v.get(search_key, '')).strip().upper() == search_val if not is_helmet else v.get(search_key) == search_val) 
                                   and v.get('logOutTime') == '---'), -1)
                        
                        if idx != -1:
                            st.session_state.vehicles[idx]['logOutTime'] = now
                            exits += 1
                        else:
                            entry = {
                                'id': payload.get('id', int(datetime.now().timestamp() * 1000)),
                                'name': payload.get('name', 'Unknown').strip(),
                                'plate': payload.get('plate', 'HELMET').strip(),
                                'type': payload.get('type', 'Private'),
                                'phone': payload.get('phone', '').strip(),
                                'messenger': payload.get('messenger', '').strip(),
                                'logInTime': now,
                                'logOutTime': '---',
                                'spot': manual_spot_val if manual_spot_val else 'N/A'
                            }
                            st.session_state.vehicles.append(entry)
                            if not is_helmet: st.session_state.total_entries += 1
                            entries += 1
                        processed_count += 1
                
                if processed_count > 0:
                    save_data()
                    st.success(f'✅ Processed {processed_count} scans ({entries} Entries, {exits} Exits)')
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_registry():
    """Pass registry with photo thumbnails"""
    st.markdown('<h2 class="glass-card" style="padding: 20px; margin-bottom: 20px;">🏷️ Issued Pass Registry</h2>', unsafe_allow_html=True)
    
    if not st.session_state.qr_registry:
        st.markdown('<div class="glass-card"><p style="text-align: center; color: #54667a;">📭 No passes issued yet</p></div>', unsafe_allow_html=True)
    else:
        for item in st.session_state.qr_registry:
            st.markdown('<div class="registry-item">', unsafe_allow_html=True)
            cols = st.columns([0.8, 3, 1.2])
            
            # Photo
            with cols[0]:
                if item.get('photo'):
                    try:
                        st.image(base64.b64decode(item['photo']), width=60)
                    except:
                        st.markdown('<div style="width:60px; height:60px; background: #eee; border-radius:50%; display:flex; align-items:center; justify-content:center;"><small>❌</small></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="width:60px; height:60px; background: #eee; border-radius:50%; display:flex; align-items:center; justify-content:center;"><small>📷</small></div>', unsafe_allow_html=True)
            
            # Info
            with cols[1]:
                st.markdown(f"**{item.get('name', 'Unknown')}**")
                st.markdown(f"*Plate:* `{item.get('plate', 'Unknown')}`")
                st.markdown(f"*Type:* {item.get('type', 'Private')}")
            
            # View button
            with cols[2]:
                if st.button(f"👁️ View", key=f"view_{item.get('id')}", use_container_width=True):
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f"#### {item.get('name')}")
                    
                    detail_cols = st.columns([1, 1])
                    with detail_cols[0]:
                        if item.get('photo'):
                            try:
                                st.image(base64.b64decode(item.get('photo')), width=120)
                            except:
                                st.markdown('<div style="background: #eee; padding: 20px; text-align: center;">Photo Error</div>', unsafe_allow_html=True)
                        st.markdown(f"**Type:** {item.get('type')}")
                    
                    with detail_cols[1]:
                        qr_img = generate_qr({'id': item.get('id'), 'plate': item.get('plate'), 'name': item.get('name'), 'type': item.get('type')})
                        st.image(qr_img, caption='Access QR')
                    
                    st.markdown(f"**Plate:** {item.get('plate')}")
                    st.markdown(f"**Phone:** {item.get('phone', 'N/A')}")
                    st.markdown(f"**Messenger:** {item.get('messenger', 'N/A')}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)


def render_vehicle_logs():
    """Vehicle entry/exit logs with editing capab ilities"""
    st.markdown('<h2 class="glass-card" style="padding: 20px; margin-bottom: 20px;">🚗 Vehicle Logs</h2>', unsafe_allow_html=True)
    
    if not st.session_state.vehicles:
        st.markdown('<div class="glass-card"><p style="text-align: center; color: #54667a;">📭 No vehicle logs yet</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        df_display = pd.DataFrame([
            {
                'Owner': v.get('name', 'Unknown'),
                'Plate': v.get('plate', 'Unknown'),
                'Type': v.get('type', 'Private'),
                'Entry Time': v.get('logInTime', '---'),
                'Exit Time': v.get('logOutTime', '---'),
            }
            for v in st.session_state.vehicles
        ])
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()