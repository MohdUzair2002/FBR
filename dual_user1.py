import streamlit as st
import zipfile
import sqlite3
import json
import requests
import bcrypt
from datetime import datetime, date
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import io
import base64


# Enhanced CSS Styling
def load_css():
    st.markdown(
        """
    <style>
    /* Main App Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom Header Styling */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    .custom-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .custom-header p {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Card Styling */
    .custom-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e5e9;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    /* Action Cards */
    .action-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
    }
    
    .action-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.3);
    }
    
    .action-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.3rem;
    }
    
    .action-card p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Success/Error Cards */
    .success-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-left: 5px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left: 5px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Form Enhancements */
    .stSelectbox > div > div {
        background: #f8fafc;
        border-radius: 8px;
    }
    
    .stTextInput > div > div {
        background: #f8fafc;
        border-radius: 8px;
    }
    
    .stTextArea > div > div {
        background: #f8fafc;
        border-radius: 8px;
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .css-1d391kg {
        color: white;
    }
    
    /* Navigation Breadcrumb */
    .nav-breadcrumb {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        font-size: 0.9rem;
        color: #64748b;
    }
    
    /* Table Enhancements */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    /* Upload Zone */
    .uploadedFile {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 10px;
        margin-top: 3rem;
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# Enhanced Components
def create_header(title, subtitle=""):
    st.markdown(
        f"""
    <div class="custom-header fade-in">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_action_card(title, description, icon="🚀"):
    return st.markdown(
        f"""
    <div class="action-card slide-up">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_stats_card(number, label):
    return st.markdown(
        f"""
    <div class="stats-card">
        <p class="stats-number">{number}</p>
        <p class="stats-label">{label}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_success_message(message):
    st.markdown(
        f"""
    <div class="success-card">
        <strong>✅ Success:</strong> {message}
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_error_message(message):
    st.markdown(
        f"""
    <div class="error-card">
        <strong>❌ Error:</strong> {message}
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_nav_breadcrumb(current_page):
    breadcrumbs = {
        "dashboard": "Dashboard",
        "invoice_method_selection": "Dashboard > Invoice Method",
        "search_seller": "Dashboard > Search Seller",
        "excel_seller_search": "Dashboard > Excel Upload > Search Seller",
        "invoice": "Dashboard > Create Invoice",
        "excel_invoice": "Dashboard > Excel Processing",
        "update": "Dashboard > Update Seller",
    }

    breadcrumb = breadcrumbs.get(current_page, "Dashboard")
    st.markdown(
        f"""
    <div class="nav-breadcrumb">
        <strong>📍 Navigation:</strong> {breadcrumb}
    </div>
    """,
        unsafe_allow_html=True,
    )


# Password Authentication (keeping original logic)
hashed_pw = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())

# Enhanced Password Authentication with dual login
hashed_pw = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())


def check_password():
    """Returns True if the user entered the correct password (admin or guest)."""
    if "password_ok" not in st.session_state:
        st.session_state.password_ok = False
        st.session_state.user_type = None
        st.session_state.guest_seller_id = None
        st.session_state.guest_seller_data = None

    if st.session_state.password_ok:
        return True

    # Enhanced login form with user type selection
    st.markdown(
        """
    <div style="text-align: center; padding: 3rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem; border-radius: 20px; color: white; max-width: 500px; 
                    margin: 0 auto; box-shadow: 0 15px 35px rgba(0,0,0,0.2);">
            <h1 style="margin-bottom: 2rem;">🔐 Invoice Management System</h1>
            <p style="opacity: 0.9; margin-bottom: 2rem;">Secure Access Portal</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # User type selection
    st.markdown("### 👤 Select Login Type")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-card" style="text-align: center;">
            <h4>🛡️ Admin Access</h4>
            <p>Full system access including seller management</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="custom-card" style="text-align: center;">
            <h4>👤 Guest Access</h4>
            <p>Invoice creation only with your NTN/CNIC</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    login_type = st.radio(
        "Choose your access level:", ["Admin", "Guest"], horizontal=True
    )

    with st.form("login_form"):
        st.markdown("### 🛡️ Authentication Required")

        if login_type == "Admin":
            pw = st.text_input(
                "🔑 Enter admin password",
                type="password",
                placeholder="Enter admin password",
            )
            submit_label = "🚀 Admin Login"
        else:
            pw = st.text_input(
                "🆔 Enter your NTN/CNIC",
                placeholder="Enter your registered NTN/CNIC number",
            )
            submit_label = "👤 Guest Login"

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button(submit_label, use_container_width=True)

        if submit:
            if login_type == "Admin":
                # Admin login check
                if bcrypt.checkpw(pw.encode(), hashed_pw):
                    st.session_state.password_ok = True
                    st.session_state.user_type = "admin"
                    st.rerun()
                else:
                    create_error_message("Invalid admin password. Please try again.")

            else:
                # Guest login check - validate NTN/CNIC against database
                if pw.strip():
                    conn = sqlite3.connect("sellers.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT * FROM sellers WHERE seller_ntn_cnic = ?", (pw.strip(),)
                    )
                    seller = cursor.fetchone()
                    conn.close()

                    if seller:
                        st.session_state.password_ok = True
                        st.session_state.user_type = "guest"
                        st.session_state.guest_seller_id = seller[0]
                        st.session_state.guest_seller_data = seller
                        create_success_message(
                            f"Welcome {seller[2]}! Guest access granted."
                        )
                        st.rerun()
                    else:
                        create_error_message(
                            "NTN/CNIC not found. Please contact administrator to register your business."
                        )
                else:
                    create_error_message("Please enter your NTN/CNIC number.")

    return False


# Enhanced main dashboard with role-based access
def show_dashboard():
    user_type = st.session_state.get("user_type", "admin")

    if user_type == "guest":
        show_guest_dashboard()
        return

    # Original admin dashboard code (keep existing implementation)
    create_nav_breadcrumb("dashboard")
    create_header(
        "Professional Invoice Management System",
        "Streamlined FBR invoice processing with modern interface",
    )

    # Statistics Dashboard
    sellers = get_all_sellers()

    st.markdown("### 📊 System Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        create_stats_card(len(sellers), "Total Sellers")
    with col2:
        create_stats_card("2", "Processing Methods")
    with col3:
        create_stats_card("100%", "FBR Compliance")
    with col4:
        create_stats_card("24/7", "System Availability")

    # Main Actions
    st.markdown("### 🎯 Quick Actions")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-card" style="height: 200px;">
            <h3>🧾 Create Invoice</h3>
            <p>Generate FBR-compliant invoices using our advanced processing methods</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button(
            "🚀 Start Invoice Creation",
            type="primary",
            use_container_width=True,
            key="admin_invoice_btn",
        ):
            go_to_method_selection()
            st.rerun()

    with col2:
        st.markdown(
            """
        <div class="custom-card" style="height: 200px;">
            <h3>✏️ Update Seller</h3>
            <p>Modify existing seller information and authentication tokens</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button(
            "📝 Update Seller Info", use_container_width=True, key="admin_update_btn"
        ):
            go_to_search_seller("update")
            st.rerun()

    # Seller Registration Sidebar (Admin only)
    with st.sidebar:
        st.markdown("### ➕ Register New Seller")
        st.markdown("*Add new sellers to the system*")

        with st.form("seller_form"):
            seller_ntn_cnic = st.text_input(
                "🆔 Seller NTN/CNIC", placeholder="Enter NTN or CNIC"
            )
            seller_business_name = st.text_input(
                "🏢 Business Name", placeholder="Enter business name"
            )
            seller_province = st.selectbox(
                "🌍 Province",
                [
                    "",
                    "Sindh",
                    "Punjab",
                    "Khyber Pakhtunkhwa",
                    "Balochistan",
                    "Gilgit-Baltistan",
                    "Azad Kashmir",
                    "Islamabad Capital Territory",
                ],
            )
            seller_address = st.text_area(
                "📍 Address", placeholder="Enter complete address"
            )
            bearer_token = st.text_input(
                "🔑 Bearer Token", placeholder="Enter API bearer token", type="password"
            )

            submitted = st.form_submit_button(
                "💾 Register Seller", use_container_width=True
            )

            if submitted:
                if (
                    seller_ntn_cnic
                    and seller_business_name
                    and seller_province
                    and seller_address
                    and bearer_token
                ):
                    seller_data = {
                        "seller_ntn_cnic": seller_ntn_cnic,
                        "seller_business_name": seller_business_name,
                        "seller_province": seller_province,
                        "seller_address": seller_address,
                        "bearer_token": bearer_token,
                    }

                    seller_id = save_seller(seller_data)
                    create_success_message(
                        f"Seller registered successfully! ID: {seller_id}"
                    )
                    st.rerun()
                else:
                    create_error_message("Please fill all required fields")

        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


    st.markdown(
            """
        <div style="height: 100px;"/>
        """,
            unsafe_allow_html=True,
        )

    # Sellers Table (existing code)
    st.markdown("### 📋 Registered Sellers")

    if sellers:
        df_data = []
        for seller in sellers:
            df_data.append(
                {
                    "ID": seller[0],
                    "NTN/CNIC": seller[1],
                    "Business Name": seller[2],
                    "Province": seller[3],
                    "Address": (
                        seller[4][:50] + "..." if len(seller[4]) > 50 else seller[4]
                    ),
                    "Created": seller[6] if len(seller) > 6 else "N/A",
                }
            )

        df = pd.DataFrame(df_data)

        

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "NTN/CNIC": st.column_config.TextColumn("NTN/CNIC", width="medium"),
                "Business Name": st.column_config.TextColumn(
                    "Business Name", width="large"
                ),
                "Province": st.column_config.TextColumn("Province", width="medium"),
                "Address": st.column_config.TextColumn("Address", width="large"),
                "Created": st.column_config.TextColumn("Created", width="medium"),
            },
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.info(
            "💡 Use the Quick Actions above to create invoices or update seller information"
        )
    else:
        st.markdown(
            """
        <div class="custom-card" style="text-align: center; padding: 3rem;">
            <h3>📝 No Sellers Registered</h3>
            <p>Get started by registering your first seller using the sidebar form</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# New Guest Dashboard
def show_guest_dashboard():
    guest_seller = st.session_state.guest_seller_data

    create_nav_breadcrumb("dashboard")
    create_header(f"Welcome {guest_seller[2]}", "Guest Invoice Creation Portal")

    # Guest info display
    st.markdown(
        f"""
    <div class="success-card">
        <h4>👤 Your Business Information</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem;">
            <div><strong>Business Name:</strong> {guest_seller[2]}</div>
            <div><strong>NTN/CNIC:</strong> {guest_seller[1]}</div>
            <div><strong>Province:</strong> {guest_seller[3]}</div>
        </div>
        <div style="margin-top: 1rem;">
            <strong>Address:</strong> {guest_seller[4]}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Guest actions (invoice creation only)
    st.markdown("### 🎯 Available Actions")

    st.markdown(
        """
    <div class="custom-card" style="text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🧾</div>
        <h3>Create Invoice</h3>
        <p>Generate FBR-compliant invoices for your business</p>
        <p style="color: #6b7280; font-size: 0.9rem;">Choose between manual form entry or bulk Excel processing</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🚀 Start Invoice Creation",
        type="primary",
        use_container_width=True,
        key="guest_invoice_btn",
    ):
        go_to_method_selection()
        st.rerun()

    # Guest sidebar
    with st.sidebar:
        st.markdown("### 👤 Guest Session")
        st.markdown(f"**Logged in as:** {guest_seller[2]}")
        st.markdown(f"**NTN/CNIC:** {guest_seller[1]}")

        st.markdown("---")
        st.markdown("### ℹ️ Guest Limitations")
        st.info(
            "As a guest user, you can:\n- Create invoices\n- Use form and Excel methods\n- Download PDFs\n\nFor administrative access, contact the system administrator."
        )

        if st.button(
            "🚪 Logout", use_container_width=True, type="secondary", key="guest_logout"
        ):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# Enhanced search seller for guest users
def show_search_seller():
    user_type = st.session_state.get("user_type", "admin")

    if user_type == "guest":
        # Guest users automatically use their own seller data
        go_to_invoice_page(st.session_state.guest_seller_id)
        st.rerun()
        return

    # Original admin search functionality (keep existing code)
    purpose_title = (
        "Create Invoice"
        if st.session_state.search_purpose == "invoice"
        else "Update Seller"
    )
    create_nav_breadcrumb("search_seller")
    create_header(
        f"Find Seller - {purpose_title}", "Search through registered sellers to proceed"
    )

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("⬅️ Dashboard", use_container_width=True, key="search_dash_btn"):
            go_to_dashboard()
            st.rerun()

    st.markdown("### 🔍 Search Sellers")

    col1, col2 = st.columns([4, 1])
    with col1:
        search_term = st.text_input(
            "🔎 Search by NTN/CNIC, Business Name, or Province",
            placeholder="Type to search...",
            help="Enter any part of NTN/CNIC, business name, or province",
        )

    with col2:
        st.markdown("<div style='margin-top: 1.8rem;'>", unsafe_allow_html=True)
        search_button = st.button(
            "🔍 Search",
            type="primary",
            disabled=not search_term,
            key="admin_search_btn",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if search_term:
        with st.spinner("🔍 Searching sellers..."):
            sellers = search_sellers(search_term)

        if sellers:
            create_success_message(
                f"Found {len(sellers)} seller(s) matching your criteria"
            )

            st.markdown("### 📋 Search Results")

            for seller in sellers:
                st.markdown(
                    f"""
                <div class="custom-card slide-up">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{seller[2]}</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #6b7280;">
                                <div><strong>NTN/CNIC:</strong> {seller[1]}</div>
                                <div><strong>Province:</strong> {seller[3]}</div>
                            </div>
                            <div style="margin-top: 0.5rem; color: #6b7280;">
                                <strong>Address:</strong> {seller[4][:80]}{'...' if len(seller[4]) > 80 else ''}
                            </div>
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                action_label = (
                    "Create Invoice"
                    if st.session_state.search_purpose == "invoice"
                    else "Update Info"
                )
                action_icon = (
                    "🧾" if st.session_state.search_purpose == "invoice" else "✏️"
                )

                if st.button(
                    f"{action_icon} {action_label}",
                    key=f"admin_select_{seller[0]}",
                    use_container_width=True,
                ):
                    if st.session_state.search_purpose == "invoice":
                        go_to_invoice_page(seller[0])
                    else:
                        go_to_update_page(seller[0])
                    st.rerun()

                st.markdown(
                    "<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">🔍</div>
                <h3>No Results Found</h3>
                <p>No sellers found matching your search criteria. Try different terms or register a new seller.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
        <div class="custom-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
            <h3>Enter Search Terms</h3>
            <p>Use the search box above to find sellers by NTN/CNIC, business name, or province</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# Initialize session state for processed invoices
if "processed_invoices" not in st.session_state:
    st.session_state.processed_invoices = []
if "validation_results" not in st.session_state:
    st.session_state.validation_results = []
if "posting_results" not in st.session_state:
    st.session_state.posting_results = []


# Enhanced excel seller search for guest users
def show_excel_seller_search():
    user_type = st.session_state.get("user_type", "admin")

    if user_type == "guest":
        # Guest users automatically use their own seller data for Excel processing
        go_to_excel_invoice(st.session_state.guest_seller_id)
        st.rerun()
        return

    # Original admin functionality (keep existing code)
    create_nav_breadcrumb("excel_seller_search")
    create_header(
        "Excel Processing - Select Seller", "Choose seller for bulk invoice processing"
    )

    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button(
            "⬅️ Back to Methods", use_container_width=True, key="excel_back_btn"
        ):
            go_to_method_selection()
            st.rerun()

    st.markdown("### 🔍 Find Seller for Excel Processing")

    col1, col2 = st.columns([4, 1])
    with col1:
        search_term = st.text_input(
            "🔎 Search by NTN/CNIC, Business Name, or Province",
            placeholder="Type to search...",
            help="Find the seller for bulk Excel processing",
        )

    with col2:
        st.markdown("<div style='margin-top: 1.8rem;'>", unsafe_allow_html=True)
        search_button = st.button(
            "🔍 Search",
            type="primary",
            disabled=not search_term,
            key="excel_search_btn",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if search_term:
        with st.spinner("🔍 Searching sellers..."):
            sellers = search_sellers(search_term)

        if sellers:
            create_success_message(
                f"Found {len(sellers)} seller(s) for Excel processing"
            )

            st.markdown("### 📋 Available Sellers")

            for seller in sellers:
                st.markdown(
                    f"""
                <div class="custom-card slide-up">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{seller[2]}</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #6b7280;">
                                <div><strong>NTN/CNIC:</strong> {seller[1]}</div>
                                <div><strong>Province:</strong> {seller[3]}</div>
                            </div>
                            <div style="margin-top: 0.5rem; color: #6b7280;">
                                <strong>Address:</strong> {seller[4][:80]}{'...' if len(seller[4]) > 80 else ''}
                            </div>
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "📊 Start Excel Processing",
                    key=f"excel_process_{seller[0]}",
                    use_container_width=True,
                    type="primary",
                ):
                    go_to_excel_invoice(seller[0])
                    st.rerun()

                st.markdown(
                    "<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
            <div class="custom-card" style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">📊</div>
                <h3>No Sellers Found</h3>
                <p>No sellers found matching your criteria. Please register sellers first or try different search terms.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
        <div class="custom-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h3>Excel Bulk Processing</h3>
            <p>Select a seller to begin bulk invoice processing from Excel files</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# PDF Generation Function (keeping original functionality)
def generate_invoice_pdf(invoice_data, fbr_response=None):
    """Generate PDF invoice matching the exact FBR format from sample"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles to match sample PDF exactly
    title_style = ParagraphStyle(
        "CustomTitle",
        fontName="Times-Bold",
        fontSize=16,
        spaceAfter=24,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    section_style = ParagraphStyle(
        "SectionHeader",
        fontName="Times-Bold",
        fontSize=12,
        spaceAfter=8,
        spaceBefore=16,
        textColor=colors.black,
        alignment=TA_LEFT,
    )

    # Story elements
    story = []

    # Title - exactly as in sample
    story.append(Paragraph("Sales Tax Invoice", title_style))
    story.append(Spacer(1, 12))

    # Seller Information Section
    story.append(Paragraph("Seller Information", section_style))

    # Clean seller address formatting
    seller_address = invoice_data.get("sellerAddress", "N/A")

    seller_info_data = [
        [
            Paragraph("<b>Business Name</b>", styles["Normal"]),
            Paragraph(invoice_data.get("sellerBusinessName", "N/A"), styles["Normal"]),
        ],
        [
            Paragraph("<b>Registration No.</b>", styles["Normal"]),
            Paragraph(invoice_data.get("sellerNTNCNIC", "N/A"), styles["Normal"]),
        ],
        [
            Paragraph("<b>Address</b>", styles["Normal"]),
            Paragraph(seller_address, styles["Normal"]),
        ],
    ]

    seller_table = Table(seller_info_data, colWidths=[1.5 * inch, 4.5 * inch])
    seller_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    story.append(seller_table)
    story.append(Spacer(1, 12))

    # Buyer Information Section
    story.append(Paragraph("Buyer Information", section_style))

    # Handle buyer registration display
    buyer_display_name = invoice_data.get("buyerBusinessName", "N/A")
    if invoice_data.get("buyerRegistrationType") == "Unregistered":
        buyer_display_name = "Un-Registered"

    buyer_reg_no = invoice_data.get("buyerNTNCNIC", "")
    if not buyer_reg_no or invoice_data.get("buyerRegistrationType") == "Unregistered":
        buyer_reg_no = "9999999"

    buyer_info_data = [
        [
            Paragraph("<b>Business Name</b>", styles["Normal"]),
            Paragraph(buyer_display_name, styles["Normal"]),
        ],
        [
            Paragraph("<b>Registration No.</b>", styles["Normal"]),
            Paragraph(buyer_reg_no, styles["Normal"]),
        ],
        [
            Paragraph("<b>Address</b>", styles["Normal"]),
            Paragraph(invoice_data.get("buyerAddress", "N/A"), styles["Normal"]),
        ],
    ]

    buyer_table = Table(buyer_info_data, colWidths=[1.5 * inch, 4.5 * inch])
    buyer_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    story.append(buyer_table)
    story.append(Spacer(1, 12))

    # Invoice Summary Section
    story.append(Paragraph("Invoice Summary", section_style))

    # Get FBR Invoice No from response if available
    fbr_invoice_no = "Pending"
    if fbr_response and isinstance(fbr_response, dict):
        if "invoiceNumber" in fbr_response:
            fbr_invoice_no = fbr_response["invoiceNumber"]
        elif "data" in fbr_response and fbr_response["data"]:
            fbr_invoice_no = fbr_response["data"].get("invoiceNumber", "Pending")

    summary_info_data = [
        [
            Paragraph("<b>FBR Invoice No.</b>", styles["Normal"]),
            Paragraph(fbr_invoice_no, styles["Normal"]),
        ],
        [
            Paragraph("<b>Date</b>", styles["Normal"]),
            Paragraph(
                invoice_data.get("invoiceDate", date.today().strftime("%Y-%m-%d")),
                styles["Normal"],
            ),
        ],
    ]

    summary_table = Table(summary_info_data, colWidths=[1.5 * inch, 4.5 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 12))

    # Details of Goods Section
    story.append(Paragraph("Details of Goods", section_style))

    # Items table header - exactly as in sample
    items_header = [
        "Description",
        "HS Code",
        "Qty",
        "Value",
        "Rate",
        "Sales Tax",
        "Amount",
    ]
    items_data = [items_header]

    total_value_excluding_st = 0
    total_sales_tax = 0
    total_amount = 0

    for item in invoice_data.get("items", []):
        qty = item.get("quantity", 0)
        value = item.get("valueSalesExcludingST", 0)
        rate = item.get("rate", "0")
        sales_tax = item.get("salesTaxApplicable", 0)
        amount = item.get("totalValues", 0)

        # Format rate exactly as in sample (18%)
        if not str(rate).endswith("%"):
            rate = f"{rate}%"

        # Format description - use "No details" if empty like sample
        description = item.get("productDescription", "No details")
        if not description.strip():
            description = "No details"

        items_data.append(
            [
                description,
                item.get("hsCode", ""),
                str(int(qty)),  # Remove decimal for quantity
                f"{int(value):,}",  # Format as in sample: 6,000
                rate,
                f"{int(sales_tax):,}",  # Format as in sample: 1,080
                f"{int(amount):,}",  # Format as in sample: 7,080
            ]
        )

        total_value_excluding_st += value
        total_sales_tax += sales_tax
        total_amount += amount

    # Create items table with exact column widths to match sample
    items_table = Table(
        items_data,
        colWidths=[
            1.4 * inch,
            0.9 * inch,
            0.5 * inch,
            0.7 * inch,
            0.6 * inch,
            0.8 * inch,
            0.8 * inch,
        ],
    )
    items_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),  # Bold headers
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),  # Description left aligned
                ("ALIGN", (2, 0), (-1, -1), "CENTER"),  # Numbers centered
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    story.append(items_table)
    story.append(Spacer(1, 16))

    # Summary totals - exactly as in sample format
    totals_data = [
        ["Value (Excluding Sales Tax)", f"{int(total_value_excluding_st):,}"],
        ["Sales Tax", f"{int(total_sales_tax):,}"],
        ["Value (Including Sales Tax)", f"{int(total_amount):,}"],
    ]

    totals_table = Table(totals_data, colWidths=[2.5 * inch, 1.5 * inch])
    totals_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),  # Labels left aligned
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),  # Values right aligned
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    story.append(totals_table)

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


# API call functions (keeping original functionality)
def validate_invoice_api(invoice_data, bearer_token):
    """Send invoice data to FBR validation API endpoint"""
    try:
        api_url = "https://gw.fbr.gov.pk/di_data/v1/di/validateinvoicedata_sb"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }
        response = requests.post(api_url, json=invoice_data, headers=headers)
        return response.status_code, response.json()
    except Exception as e:
        return None, {"error": str(e)}


def post_invoice_api(invoice_data, bearer_token):
    """Send invoice data to FBR post API endpoint"""
    try:
        api_url = "https://gw.fbr.gov.pk/di_data/v1/di/postinvoicedata_sb"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }
        response = requests.post(api_url, json=invoice_data, headers=headers)
        return response.status_code, response.json()
    except Exception as e:
        return None, {"error": str(e)}


# Database setup (keeping original logic)
def init_database():
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_ntn_cnic TEXT NOT NULL,
            seller_business_name TEXT NOT NULL,
            seller_province TEXT NOT NULL,
            seller_address TEXT NOT NULL,
            bearer_token TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_seller_ntn_cnic ON sellers(seller_ntn_cnic)"""
    )
    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_seller_business_name ON sellers(seller_business_name)"""
    )
    cursor.execute(
        """CREATE INDEX IF NOT EXISTS idx_seller_province ON sellers(seller_province)"""
    )

    conn.commit()
    conn.close()


# Database operations (keeping original functionality)
def save_seller(seller_data):
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sellers (seller_ntn_cnic, seller_business_name, seller_province, seller_address, bearer_token)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            seller_data["seller_ntn_cnic"],
            seller_data["seller_business_name"],
            seller_data["seller_province"],
            seller_data["seller_address"],
            seller_data["bearer_token"],
        ),
    )
    conn.commit()
    seller_id = cursor.lastrowid
    conn.close()
    return seller_id


def update_seller(seller_id, seller_data):
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE sellers 
        SET seller_ntn_cnic = ?, seller_business_name = ?, seller_province = ?, seller_address = ?, bearer_token = ?
        WHERE id = ?
    """,
        (
            seller_data["seller_ntn_cnic"],
            seller_data["seller_business_name"],
            seller_data["seller_province"],
            seller_data["seller_address"],
            seller_data["bearer_token"],
            seller_id,
        ),
    )
    conn.commit()
    conn.close()


def get_all_sellers():
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers ORDER BY created_at DESC")
    sellers = cursor.fetchall()
    conn.close()
    return sellers


def get_seller_by_id(seller_id):
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id,))
    seller = cursor.fetchone()
    conn.close()
    return seller


def search_sellers(search_term):
    conn = sqlite3.connect("sellers.db")
    cursor = conn.cursor()
    search_query = f"%{search_term.lower()}%"
    cursor.execute(
        """
        SELECT * FROM sellers 
        WHERE LOWER(seller_ntn_cnic) LIKE ? 
        OR LOWER(seller_business_name) LIKE ? 
        OR LOWER(seller_province) LIKE ?
        ORDER BY seller_business_name
    """,
        (search_query, search_query, search_query),
    )
    sellers = cursor.fetchall()
    conn.close()
    return sellers


# Initialize database
init_database()

# Streamlit app configuration
st.set_page_config(
    page_title="Professional Invoice Management",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

# Load CSS
load_css()

# Session state management
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "selected_seller_id" not in st.session_state:
    st.session_state.selected_seller_id = None
if "search_purpose" not in st.session_state:
    st.session_state.search_purpose = None
if "invoice_method" not in st.session_state:
    st.session_state.invoice_method = None
if "excel_data" not in st.session_state:
    st.session_state.excel_data = None
if "column_mapping" not in st.session_state:
    st.session_state.column_mapping = {}
if "invoices_prepared" not in st.session_state:
    st.session_state.invoices_prepared = []


# Navigation functions
def go_to_dashboard():
    st.session_state.page = "dashboard"
    st.session_state.selected_seller_id = None
    st.session_state.search_purpose = None
    st.session_state.invoice_method = None
    st.session_state.excel_data = None
    st.session_state.column_mapping = {}
    st.session_state.invoices_prepared = []


def go_to_method_selection():
    st.session_state.page = "invoice_method_selection"


def go_to_search_seller(purpose):
    st.session_state.page = "search_seller"
    st.session_state.search_purpose = purpose


def go_to_excel_seller_search():
    st.session_state.page = "excel_seller_search"


def go_to_invoice_page(seller_id):
    st.session_state.page = "invoice"
    st.session_state.selected_seller_id = seller_id


def go_to_update_page(seller_id):
    st.session_state.page = "update"
    st.session_state.selected_seller_id = seller_id


def go_to_excel_invoice(seller_id):
    st.session_state.page = "excel_invoice"
    st.session_state.selected_seller_id = seller_id


# Auto-detection mapping for common column patterns
COLUMN_MAPPINGS = {
    # Buyer Information
    "buyer_reg_no": [
        "registration no",
        "buyer registration no",
        "buyerntnccnic",
        "buyer ntn",
        "buyer cnic",
        "ntn",
        "cnic",
        "registration number",
        "reg no",
        "buyer reg no",
    ],
    "buyer_name": [
        "name",
        "buyer name",
        "buyer business name",
        "business name",
        "buyerbusinessname",
        "customer name",
        "client name",
        "party name",
    ],
    "buyer_type": [
        "type",
        "buyer type",
        "registration type",
        "buyer registration type",
        "registered",
        "unregistered",
        "reg type",
    ],
    "buyer_province": [
        "sale origination province",
        "buyer province",
        "province",
        "buyerprovince",
        "origination province",
        "buyer state",
        "state",
    ],
    "buyer_address": [
        "destination of supply",
        "buyer address",
        "address",
        "buyeraddress",
        "destination",
        "supply destination",
        "delivery address",
    ],
    # Invoice Details
    "invoice_date": [
        "document date",
        "invoice date",
        "date",
        "invoicedate",
        "doc date",
        "transaction date",
        "sale date",
    ],
    "invoice_ref": [
        "document number",
        "invoice reference no",
        "invoice ref no",
        "invoice number",
        "doc number",
        "ref no",
        "reference",
        "invoicerefno",
    ],
    "hs_code": [
        "hs code description",
        "hs code",
        "hscode",
        "commodity code",
        "product code",
        "item code",
    ],
    "product_desc": [
        "product description",
        "description",
        "item description",
        "productdescription",
        "product name",
        "item name",
        "goods description",
    ],
    # Item Values
    "quantity": ["quantity", "qty", "amount", "units", "pieces", "nos"],
    "uom": [
        "uom",
        "unit of measure",
        "unit",
        "measure",
        "units",
        "numbers, pieces, units",
        "kg",
        "pcs",
        "pieces",
    ],
    "rate": [
        "rate",
        "tax rate",
        "st rate",
        "sales tax rate",
        "%",
        "percentage",
        "tax percentage",
    ],
    "value_excl_st": [
        "value of sales excluding sales tax",
        "value excluding sales tax",
        "value excl st",
        "base value",
        "taxable value",
        "net value",
        "valuesalesexcludingst",
        "amount before tax",
    ],
    "sales_tax": [
        "sales tax/fed in st mode",
        "sales tax",
        "st amount",
        "tax amount",
        "salestaxapplicable",
        "sales tax applicable",
        "tax",
    ],
    # Optional Fields
    "further_tax": ["further tax", "additional tax", "extra tax", "other tax"],
    "discount": ["discount", "rebate", "deduction", "less"],
    "sale_type": [
        "sale type",
        "transaction type",
        "saletype",
        "type of sale",
        "3rd schedule goods",
        "standard",
        "exempt",
    ],
}


def auto_detect_columns(df_columns):
    """Automatically detect and map Excel columns to required fields"""
    detected_mapping = {}
    df_columns_lower = [str(col).lower().strip() for col in df_columns]

    for field_key, possible_names in COLUMN_MAPPINGS.items():
        best_match = None
        best_score = 0

        for col_idx, col_name in enumerate(df_columns_lower):
            for pattern in possible_names:
                pattern_lower = pattern.lower()

                # Exact match gets highest score
                if col_name == pattern_lower:
                    best_match = df_columns[col_idx]
                    best_score = 100
                    break

                # Partial match scoring
                if pattern_lower in col_name or col_name in pattern_lower:
                    # Calculate similarity score
                    score = len(set(pattern_lower.split()) & set(col_name.split())) * 10
                    if col_name.startswith(
                        pattern_lower[:5]
                    ) or pattern_lower.startswith(col_name[:5]):
                        score += 5

                    if score > best_score:
                        best_match = df_columns[col_idx]
                        best_score = score

        if best_match and best_score >= 5:  # Minimum confidence threshold
            detected_mapping[field_key] = best_match

    return detected_mapping


def process_excel_row_auto(row, mapping, seller, idx):
    """Process a single Excel row using auto-detected mapping"""
    try:
        # Extract buyer info with safe string conversion
        buyer_registration_no = str(
            row.get(mapping.get("buyer_reg_no", ""), "")
        ).strip()
        buyer_business_name = str(row.get(mapping.get("buyer_name", ""), "")).strip()
        buyer_registration_type = str(
            row.get(mapping.get("buyer_type", ""), "Unregistered")
        ).strip()
        buyer_province_value = str(
            row.get(mapping.get("buyer_province", ""), "Sindh")
        ).strip()
        buyer_address_value = str(
            row.get(mapping.get("buyer_address", ""), "N/A")
        ).strip()

        # Handle unregistered buyers
        if (
            "unregistered" in buyer_registration_type.lower()
            or "un-register" in buyer_business_name.lower()
            or buyer_registration_no == "9999999"
        ):
            buyer_registration_no = "9999999"
            buyer_business_name = "Un-Registered"
            buyer_registration_type = "Unregistered"

        # Extract invoice details
        invoice_date_value = row.get(mapping.get("invoice_date", ""), date.today())
        if isinstance(invoice_date_value, str):
            try:
                invoice_date_value = pd.to_datetime(invoice_date_value).date()
            except:
                invoice_date_value = date.today()
        elif hasattr(invoice_date_value, "date"):
            invoice_date_value = invoice_date_value.date()

        invoice_ref_no = str(
            row.get(mapping.get("invoice_ref", ""), f"REF-{idx+1}")
        ).strip()

        # Extract item details
        hs_code_value = str(row.get(mapping.get("hs_code", ""), "")).strip()
        product_description = str(
            row.get(mapping.get("product_desc", ""), "No details")
        ).strip()

        # Safe numeric conversions
        def safe_float_convert(value, default=0.0):
            try:
                if pd.isna(value) or value == "":
                    return default
                return float(str(value).replace(",", "").replace("%", "").strip())
            except (ValueError, TypeError):
                return default

        quantity = safe_float_convert(row.get(mapping.get("quantity", ""), 1), 1.0)
        uom_value = str(row.get(mapping.get("uom", ""), "PCS")).strip()

        # Handle rate value
        rate_raw = row.get(mapping.get("rate", ""), "18")
        rate_value = str(rate_raw).strip()
        if "%" not in rate_value:
            rate_clean = rate_value.replace("%", "").replace(" ", "")
            try:
                rate_num = float(rate_clean)
                rate_value = f"{rate_num}%"
            except:
                rate_value = "18%"

        value_excluding_st = safe_float_convert(
            row.get(mapping.get("value_excl_st", ""), 0)
        )
        sales_tax_applicable = safe_float_convert(
            row.get(mapping.get("sales_tax", ""), 0)
        )

        # Optional fields
        further_tax = safe_float_convert(row.get(mapping.get("further_tax", ""), 0))
        extra_tax = 0.0  # Not commonly in Excel formats
        st_withheld = 0.0  # Not commonly in Excel formats
        fed_payable = 0.0  # Not commonly in Excel formats
        discount = safe_float_convert(row.get(mapping.get("discount", ""), 0))
        sale_type_value = str(row.get(mapping.get("sale_type", ""), "")).strip()

        # Calculate total
        total_values = (
            value_excluding_st
            + sales_tax_applicable
            + further_tax
            + extra_tax
            - discount
        )

        # Validation
        if value_excluding_st <= 0:
            return None, f"Row {idx+1}: Value excluding ST must be greater than 0"

        if not buyer_business_name:
            return None, f"Row {idx+1}: Buyer name is required"

        # Create invoice data structure
        invoice_data = {
            "sellerNTNCNIC": seller[1],
            "sellerBusinessName": seller[2],
            "sellerProvince": seller[3],
            "sellerAddress": seller[4],
            "invoiceType": "Sale Invoice",
            "invoiceDate": invoice_date_value.strftime("%Y-%m-%d"),
            "buyerNTNCNIC": buyer_registration_no,
            "buyerBusinessName": buyer_business_name,
            "buyerProvince": buyer_province_value,
            "buyerAddress": buyer_address_value,
            "buyerRegistrationType": buyer_registration_type,
            "invoiceRefNo": invoice_ref_no,
            "scenarioId": "SN002",  # Default scenario
            "items": [
                {
                    "hsCode": hs_code_value,
                    "productDescription": product_description,
                    "rate": rate_value,
                    "uoM": uom_value,
                    "quantity": quantity,
                    "valueSalesExcludingST": value_excluding_st,
                    "salesTaxApplicable": sales_tax_applicable,
                    "furtherTax": further_tax,
                    "extraTax": extra_tax,
                    "salesTaxWithheldAtSource": st_withheld,
                    "fixedNotifiedValueOrRetailPrice": 0.00,
                    "fedPayable": fed_payable,
                    "discount": discount,
                    "totalValues": total_values,
                    "saleType": sale_type_value,
                    "sroScheduleNo": "",
                    "sroItemSerialNo": "",
                }
            ],
        }

        return {
            "row_number": idx + 1,
            "invoice_data": invoice_data,
            "buyer_name": buyer_business_name,
            "amount": total_values,
        }, None

    except Exception as e:
        return None, f"Row {idx+1}: {str(e)}"


# Enhanced Pages
# def show_dashboard():
#     create_nav_breadcrumb('dashboard')
#     create_header("Professional Invoice Management System", "Streamlined FBR invoice processing with modern interface")

#     # Statistics Dashboard
#     sellers = get_all_sellers()

#     st.markdown("### 📊 System Overview")
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         create_stats_card(len(sellers), "Total Sellers")
#     with col2:
#         create_stats_card("2", "Processing Methods")
#     with col3:
#         create_stats_card("100%", "FBR Compliance")
#     with col4:
#         create_stats_card("24/7", "System Availability")

#     # Main Actions
#     st.markdown("### 🎯 Quick Actions")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("""
#         <div class="custom-card">
#             <h3>🧾 Create Invoice</h3>
#             <p>Generate FBR-compliant invoices using our advanced processing methods</p>
#         </div>
#         """, unsafe_allow_html=True)
#         if st.button("🚀 Start Invoice Creation", type="primary", use_container_width=True):
#             go_to_method_selection()
#             st.rerun()

#     with col2:
#         st.markdown("""
#         <div class="custom-card">
#             <h3>✏️ Update Seller</h3>
#             <p>Modify existing seller information and authentication tokens</p>
#         </div>
#         """, unsafe_allow_html=True)
#         if st.button("📝 Update Seller Info", use_container_width=True):
#             go_to_search_seller('update')
#             st.rerun()

#     # Seller Registration Sidebar
#     with st.sidebar:
#         st.markdown("### ➕ Register New Seller")
#         st.markdown("*Add new sellers to the system*")

#         with st.form("seller_form"):
#             seller_ntn_cnic = st.text_input("🆔 Seller NTN/CNIC", placeholder="Enter NTN or CNIC")
#             seller_business_name = st.text_input("🏢 Business Name", placeholder="Enter business name")
#             seller_province = st.selectbox("🌍 Province", [
#                 "", "Sindh", "Punjab", "Khyber Pakhtunkhwa", "Balochistan",
#                 "Gilgit-Baltistan", "Azad Kashmir", "Islamabad Capital Territory"
#             ])
#             seller_address = st.text_area("📍 Address", placeholder="Enter complete address")
#             bearer_token = st.text_input("🔑 Bearer Token", placeholder="Enter API bearer token", type="password")

#             submitted = st.form_submit_button("💾 Register Seller", use_container_width=True)

#             if submitted:
#                 if seller_ntn_cnic and seller_business_name and seller_province and seller_address and bearer_token:
#                     seller_data = {
#                         'seller_ntn_cnic': seller_ntn_cnic,
#                         'seller_business_name': seller_business_name,
#                         'seller_province': seller_province,
#                         'seller_address': seller_address,
#                         'bearer_token': bearer_token
#                     }

#                     seller_id = save_seller(seller_data)
#                     create_success_message(f"Seller registered successfully! ID: {seller_id}")
#                     st.rerun()
#                 else:
#                     create_error_message("Please fill all required fields")

#     # Sellers Table
#     st.markdown("### 📋 Registered Sellers")

#     if sellers:
#         # Create enhanced table data
#         df_data = []
#         for seller in sellers:
#             df_data.append({
#                 'ID': seller[0],
#                 'NTN/CNIC': seller[1],
#                 'Business Name': seller[2],
#                 'Province': seller[3],
#                 'Address': seller[4][:50] + '...' if len(seller[4]) > 50 else seller[4],
#                 'Created': seller[6] if len(seller) > 6 else 'N/A'
#             })

#         df = pd.DataFrame(df_data)

#         # Display with enhanced styling
#         st.markdown("""
#         <div class="custom-card">
#         """, unsafe_allow_html=True)

#         st.dataframe(
#             df,
#             use_container_width=True,
#             hide_index=True,
#             column_config={
#                 "ID": st.column_config.NumberColumn("ID", width="small"),
#                 "NTN/CNIC": st.column_config.TextColumn("NTN/CNIC", width="medium"),
#                 "Business Name": st.column_config.TextColumn("Business Name", width="large"),
#                 "Province": st.column_config.TextColumn("Province", width="medium"),
#                 "Address": st.column_config.TextColumn("Address", width="large"),
#                 "Created": st.column_config.TextColumn("Created", width="medium")
#             }
#         )

#         st.markdown("</div>", unsafe_allow_html=True)
#         st.info("💡 Use the Quick Actions above to create invoices or update seller information")
#     else:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center; padding: 3rem;">
#             <h3>📝 No Sellers Registered</h3>
#             <p>Get started by registering your first seller using the sidebar form</p>
#         </div>
#         """, unsafe_allow_html=True)


def show_method_selection():
    create_nav_breadcrumb("invoice_method_selection")
    create_header(
        "Select Invoice Creation Method",
        "Choose the best approach for your invoicing needs",
    )

    # Fixed button positioning with CSS
    st.markdown(
        """
    <style>
    .dashboard-button-container {
        display: flex;
        justify-content: flex-end;
        margin: -1rem 0 2rem 0;
        padding: 0;
    }
    .dashboard-button-container .stButton {
        width: 150px;
    }
    .dashboard-button-container .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .dashboard-button-container .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(239, 68, 68, 0.4);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="dashboard-button-container">', unsafe_allow_html=True)

    # Create columns for button positioning
    _, _, _, col_button = st.columns([2, 2, 1, 1])
    with col_button:
        if st.button("⬅️ Dashboard", key="dash_btn_method"):
            go_to_dashboard()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🎯 Choose Processing Method")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-card" style="height: 600px;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📝</div>
                <h3>Manual Form Entry</h3>
            </div>
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
                <h4>✨ Features:</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Step-by-step form filling</li>
                    <li>Real-time validation</li>
                    <li>Single invoice creation</li>
                    <li>Immediate FBR feedback</li>
                    <li>PDF generation</li>
                </ul>
            </div>
            <div style="color: #6b7280;">
                <strong>Best for:</strong> Individual invoices, detailed control, learning the system
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📝 Use Form Method",
            type="primary",
            use_container_width=True,
            key="form_method_btn",
        ):
            st.session_state.invoice_method = "form"
            go_to_search_seller("invoice")
            st.rerun()

    with col2:
        st.markdown(
            """
        <div class="custom-card" style="height: 600px;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                <h3>Excel File Upload</h3>
            </div>
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;">
                <h4>🚀 Features:</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Bulk invoice processing</li>
                    <li>Smart column detection</li>
                    <li>Multiple invoices at once</li>
                    <li>Batch FBR submission</li>
                    <li>ZIP file PDF output</li>
                </ul>
            </div>
            <div style="color: #6b7280;">
                <strong>Best for:</strong> High volume processing, bulk operations, efficiency
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📊 Use Excel Method", use_container_width=True, key="excel_method_btn"
        ):
            st.session_state.invoice_method = "excel"
            go_to_excel_seller_search()
            st.rerun()

    # Comparison table
    st.markdown(
        """
        <div style="height: 100px;"/>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 Method Comparison")

    comparison_data = {
        "Feature": [
            "Speed",
            "Volume",
            "Learning Curve",
            "Flexibility",
            "Error Detection",
            "PDF Output",
        ],
        "Manual Form": [
            "Moderate",
            "Single Invoice",
            "Easy",
            "High",
            "Real-time",
            "Individual",
        ],
        "Excel Upload": [
            "Fast",
            "Bulk Processing",
            "Moderate",
            "Moderate",
            "Batch",
            "ZIP Archive",
        ],
    }

    comparison_df = pd.DataFrame(comparison_data)

    # st.markdown("""
    # <div class="custom-card">
    # """, unsafe_allow_html=True)

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Feature": st.column_config.TextColumn("Feature", width="medium"),
            "Manual Form": st.column_config.TextColumn(
                "📝 Manual Form", width="medium"
            ),
            "Excel Upload": st.column_config.TextColumn(
                "📊 Excel Upload", width="medium"
            ),
        },
    )

    st.markdown("</div>", unsafe_allow_html=True)


# def show_search_seller():
#     purpose_title = "Create Invoice" if st.session_state.search_purpose == 'invoice' else "Update Seller"
#     create_nav_breadcrumb('search_seller')
#     create_header(f"Find Seller - {purpose_title}", "Search through registered sellers to proceed")

#     col1, col2 = st.columns([5, 1])
#     with col2:
#         if st.button("⬅️ Dashboard", use_container_width=True):
#             go_to_dashboard()
#             st.rerun()

#     st.markdown("### 🔍 Search Sellers")

#     col1, col2 = st.columns([4, 1])
#     with col1:
#         search_term = st.text_input(
#             "🔎 Search by NTN/CNIC, Business Name, or Province",
#             placeholder="Type to search...",
#             help="Enter any part of NTN/CNIC, business name, or province"
#         )

#     with col2:
#         st.markdown("<div style='margin-top: 1.8rem;'>", unsafe_allow_html=True)
#         search_button = st.button("🔍 Search", type="primary", disabled=not search_term)
#         st.markdown("</div>", unsafe_allow_html=True)

#     if search_term:
#         with st.spinner("🔍 Searching sellers..."):
#             sellers = search_sellers(search_term)

#         if sellers:
#             create_success_message(f"Found {len(sellers)} seller(s) matching your criteria")

#             st.markdown("### 📋 Search Results")

#             for seller in sellers:
#                 st.markdown(f"""
#                 <div class="custom-card slide-up">
#                     <div style="display: flex; justify-content: space-between; align-items: center;">
#                         <div style="flex: 1;">
#                             <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{seller[2]}</h4>
#                             <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #6b7280;">
#                                 <div><strong>NTN/CNIC:</strong> {seller[1]}</div>
#                                 <div><strong>Province:</strong> {seller[3]}</div>
#                             </div>
#                             <div style="margin-top: 0.5rem; color: #6b7280;">
#                                 <strong>Address:</strong> {seller[4][:80]}{'...' if len(seller[4]) > 80 else ''}
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 action_label = "Create Invoice" if st.session_state.search_purpose == 'invoice' else "Update Info"
#                 action_icon = "🧾" if st.session_state.search_purpose == 'invoice' else "✏️"

#                 if st.button(f"{action_icon} {action_label}", key=f"select_{seller[0]}", use_container_width=True):
#                     if st.session_state.search_purpose == 'invoice':
#                         go_to_invoice_page(seller[0])
#                     else:
#                         go_to_update_page(seller[0])
#                     st.rerun()

#                 st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="custom-card" style="text-align: center; padding: 3rem;">
#                 <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">🔍</div>
#                 <h3>No Results Found</h3>
#                 <p>No sellers found matching your search criteria. Try different terms or register a new seller.</p>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center; padding: 3rem;">
#             <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
#             <h3>Enter Search Terms</h3>
#             <p>Use the search box above to find sellers by NTN/CNIC, business name, or province</p>
#         </div>
#         """, unsafe_allow_html=True)

# # Initialize session state for processed invoices
# if 'processed_invoices' not in st.session_state:
#     st.session_state.processed_invoices = []
# if 'validation_results' not in st.session_state:
#     st.session_state.validation_results = []
# if 'posting_results' not in st.session_state:
#     st.session_state.posting_results = []

# def show_excel_seller_search():
#     create_nav_breadcrumb('excel_seller_search')
#     create_header("Excel Processing - Select Seller", "Choose seller for bulk invoice processing")

#     col1, col2 = st.columns([5, 1])
#     with col2:
#         if st.button("⬅️ Back to Methods", use_container_width=True):
#             go_to_method_selection()
#             st.rerun()

#     st.markdown("### 🔍 Find Seller for Excel Processing")

#     col1, col2 = st.columns([4, 1])
#     with col1:
#         search_term = st.text_input(
#             "🔎 Search by NTN/CNIC, Business Name, or Province",
#             placeholder="Type to search...",
#             help="Find the seller for bulk Excel processing"
#         )

#     with col2:
#         st.markdown("<div style='margin-top: 1.8rem;'>", unsafe_allow_html=True)
#         search_button = st.button("🔍 Search", type="primary", disabled=not search_term)
#         st.markdown("</div>", unsafe_allow_html=True)

#     if search_term:
#         with st.spinner("🔍 Searching sellers..."):
#             sellers = search_sellers(search_term)

#         if sellers:
#             create_success_message(f"Found {len(sellers)} seller(s) for Excel processing")

#             st.markdown("### 📋 Available Sellers")

#             for seller in sellers:
#                 st.markdown(f"""
#                 <div class="custom-card slide-up">
#                     <div style="display: flex; justify-content: space-between; align-items: center;">
#                         <div style="flex: 1;">
#                             <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{seller[2]}</h4>
#                             <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #6b7280;">
#                                 <div><strong>NTN/CNIC:</strong> {seller[1]}</div>
#                                 <div><strong>Province:</strong> {seller[3]}</div>
#                             </div>
#                             <div style="margin-top: 0.5rem; color: #6b7280;">
#                                 <strong>Address:</strong> {seller[4][:80]}{'...' if len(seller[4]) > 80 else ''}
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 if st.button("📊 Start Excel Processing", key=f"excel_{seller[0]}", use_container_width=True, type="primary"):
#                     go_to_excel_invoice(seller[0])
#                     st.rerun()

#                 st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="custom-card" style="text-align: center; padding: 3rem;">
#                 <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">📊</div>
#                 <h3>No Sellers Found</h3>
#                 <p>No sellers found matching your criteria. Please register sellers first or try different search terms.</p>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="custom-card" style="text-align: center; padding: 3rem;">
#             <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
#             <h3>Excel Bulk Processing</h3>
#             <p>Select a seller to begin bulk invoice processing from Excel files</p>
#         </div>
#         """, unsafe_allow_html=True)


# MAIN APPLICATION LOGIC
def main():
    if st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "invoice_method_selection":
        show_method_selection()
    elif st.session_state.page == "excel_seller_search":
        show_excel_seller_search()
    elif st.session_state.page == "search_seller":
        show_search_seller()
    elif st.session_state.page == "update":
        show_update_seller()
    elif st.session_state.page == "invoice":
        show_invoice_form()
    elif st.session_state.page == "excel_invoice":
        show_excel_invoice_auto()
    else:
        show_dashboard()

    # Professional Footer
    st.markdown(
        """
    <div class="footer">
        <h3>Professional Invoice Management System</h3>
        <p>Streamlined FBR compliance • Advanced processing capabilities • Modern interface</p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            Built with Streamlit • Powered by Python • Enhanced UI/UX
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def show_update_seller():
    seller = get_seller_by_id(st.session_state.selected_seller_id)

    if seller:
        create_nav_breadcrumb("update")
        create_header(
            f"Update Seller Information", f"Modifying details for {seller[2]}"
        )

        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("⬅️ Back to Search", use_container_width=True):
                go_to_search_seller("update")
                st.rerun()

        # Current info display
        st.markdown(
            f"""
        <div class="custom-card">
            <h4>📋 Current Information</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin-top: 1rem;">
                <div>
                    <strong>Business Name:</strong><br>
                    <span style="color: #6b7280;">{seller[2]}</span>
                </div>
                <div>
                    <strong>NTN/CNIC:</strong><br>
                    <span style="color: #6b7280;">{seller[1]}</span>
                </div>
                <div>
                    <strong>Province:</strong><br>
                    <span style="color: #6b7280;">{seller[3]}</span>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <strong>Address:</strong><br>
                <span style="color: #6b7280;">{seller[4]}</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("### ✏️ Update Information")

        with st.form("update_seller_form", clear_on_submit=False):
            col1, col2 = st.columns(2)

            with col1:
                updated_ntn_cnic = st.text_input(
                    "🆔 Seller NTN/CNIC *", value=seller[1]
                )
                updated_business_name = st.text_input(
                    "🏢 Business Name *", value=seller[2]
                )

                provinces = [
                    "",
                    "Sindh",
                    "Punjab",
                    "Khyber Pakhtunkhwa",
                    "Balochistan",
                    "Gilgit-Baltistan",
                    "Azad Kashmir",
                    "Islamabad Capital Territory",
                ]
                current_province_index = 0
                if seller[3] in provinces:
                    current_province_index = provinces.index(seller[3])

                updated_province = st.selectbox(
                    "🌍 Province *", provinces, index=current_province_index
                )

            with col2:
                updated_address = st.text_area(
                    "📍 Address *", value=seller[4], height=100
                )
                updated_bearer_token = st.text_input(
                    "🔑 Bearer Token *", value=seller[5], type="password"
                )

            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                update_submitted = st.form_submit_button(
                    "💾 Update Seller", type="primary", use_container_width=True
                )

            if update_submitted:
                if (
                    updated_ntn_cnic
                    and updated_business_name
                    and updated_province
                    and updated_address
                    and updated_bearer_token
                ):
                    updated_seller_data = {
                        "seller_ntn_cnic": updated_ntn_cnic,
                        "seller_business_name": updated_business_name,
                        "seller_province": updated_province,
                        "seller_address": updated_address,
                        "bearer_token": updated_bearer_token,
                    }

                    update_seller(seller[0], updated_seller_data)
                    create_success_message("Seller information updated successfully!")

                    # Show updated info
                    st.markdown(
                        f"""
                    <div class="success-card">
                        <h4>✅ Updated Information</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                            <div><strong>Business Name:</strong> {updated_business_name}</div>
                            <div><strong>NTN/CNIC:</strong> {updated_ntn_cnic}</div>
                            <div><strong>Province:</strong> {updated_province}</div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    create_error_message("Please fill all required fields")
    else:
        st.error("Seller not found!")
        if st.button("⬅️ Back to Dashboard"):
            go_to_dashboard()
            st.rerun()


def show_invoice_form():
    seller = get_seller_by_id(st.session_state.selected_seller_id)

    if seller:
        create_nav_breadcrumb("invoice")
        create_header(f"Create Invoice", f"Manual invoice creation for {seller[2]}")

        # Check user type to show appropriate back button
        user_type = st.session_state.get("user_type", "admin")

        col1, col2 = st.columns([5, 1])
        with col2:
            if user_type == "guest":
                # Guest users go back to dashboard
                if st.button(
                    "⬅️ Back", use_container_width=True, key="guest_invoice_back_btn"
                ):
                    go_to_dashboard()
                    st.rerun()
            else:
                # Admin users go back to search
                if st.button(
                    "⬅️ Back to Search",
                    use_container_width=True,
                    key="admin_invoice_back_btn",
                ):
                    go_to_search_seller("invoice")
                    st.rerun()

        # Seller info display
        st.markdown(
            f"""
        <div class="success-card">
            <h4>🏢 Selected Seller</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem;">
                <div><strong>Name:</strong> {seller[2]}</div>
                <div><strong>NTN/CNIC:</strong> {seller[1]}</div>
                <div><strong>Province:</strong> {seller[3]}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Main form
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            <div class="custom-card">
                <h4>🛒 Buyer Information</h4>
            </div>
            """,
                unsafe_allow_html=True,
            )

            buyer_ntn_cnic = st.text_input(
                "🆔 Buyer NTN/CNIC", placeholder="Enter buyer NTN/CNIC"
            )
            buyer_business_name = st.text_input(
                "🏢 Buyer Business Name", placeholder="Enter business name"
            )
            buyer_province = st.selectbox(
                "🌍 Buyer Province",
                [
                    "",
                    "Sindh",
                    "Punjab",
                    "Khyber Pakhtunkhwa",
                    "Balochistan",
                    "Gilgit-Baltistan",
                    "Azad Kashmir",
                    "Islamabad Capital Territory",
                ],
            )
            buyer_address = st.text_input(
                "📍 Buyer Address", placeholder="Enter buyer address"
            )
            buyer_registration_type = st.selectbox(
                "📋 Registration Type", ["", "Unregistered", "Registered"]
            )

        with col2:
            st.markdown(
                """
            <div class="custom-card">
                <h4>📄 Invoice Information</h4>
            </div>
            """,
                unsafe_allow_html=True,
            )

            invoice_type = st.selectbox("📑 Invoice Type", ["Sale Invoice"], index=0)
            invoice_date = st.date_input("📅 Invoice Date", value=date.today())
            invoice_ref_no = st.text_input(
                "🔢 Invoice Reference No", placeholder="Enter reference number"
            )
            scenario_id = st.text_input(
                "🎯 Scenario ID", placeholder="Enter scenario ID"
            )

        # Items section
        st.markdown("### 📦 Product Items")

        with st.expander("➕ Item Details", expanded=True):
            st.markdown(
                """
            <div class="custom-card">
            """,
                unsafe_allow_html=True,
            )

            col3, col4 = st.columns(2)

            with col3:
                hs_code = st.text_input("🏷️ HS Code", placeholder="Enter HS code")
                product_description = st.text_input(
                    "📝 Product Description", placeholder="Enter product description"
                )
                rate = st.text_input(
                    "📊 Tax Rate", placeholder="Enter tax rate (e.g., 18%)"
                )
                uom = st.text_input(
                    "📏 Unit of Measure", placeholder="Enter unit of measure"
                )
                quantity = st.number_input("🔢 Quantity", min_value=1, value=1)
                value_sales_excluding_st = st.number_input(
                    "💰 Value (Excluding Sales Tax)", min_value=0.0, value=0.0
                )

            with col4:
                sales_tax_applicable = st.number_input(
                    "🏛️ Sales Tax Applicable", min_value=0.0, value=0.0
                )
                further_tax = st.number_input(
                    "➕ Further Tax", min_value=0.0, value=0.0
                )
                extra_tax = st.number_input("📈 Extra Tax", min_value=0.0, value=0.0)
                sales_tax_withheld = st.number_input(
                    "⚖️ Sales Tax Withheld at Source", min_value=0.0, value=0.0
                )
                fed_payable = st.number_input(
                    "🏦 FED Payable", min_value=0.0, value=0.0
                )
                discount = st.number_input("💸 Discount", min_value=0.0, value=0.0)

            # Calculate total
            total_values = (
                value_sales_excluding_st
                + sales_tax_applicable
                + further_tax
                + extra_tax
                - discount
            )

            st.markdown(
                f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
                <h3 style="margin: 0;">💰 Total Invoice Value</h3>
                <h2 style="margin: 0.5rem 0 0 0;">₨ {total_values:,.2f}</h2>
            </div>
            """,
                unsafe_allow_html=True,
            )

            sale_type = st.text_input("🏪 Sale Type", placeholder="Enter sale type")
            sro_schedule_no = st.text_input(
                "📋 SRO Schedule No", placeholder="Enter SRO schedule number"
            )
            sro_item_serial_no = st.text_input(
                "🔢 SRO Item Serial No", placeholder="Enter SRO item serial number"
            )

            st.markdown("</div>", unsafe_allow_html=True)

        # Action buttons
        st.markdown("### 🚀 Invoice Actions")

        col5, col6 = st.columns(2)

        with col5:
            if st.button(
                "✅ Validate Invoice", use_container_width=True, type="secondary"
            ):
                # Create invoice data structure
                invoice_data = {
                    "sellerNTNCNIC": seller[1],
                    "sellerBusinessName": seller[2],
                    "sellerProvince": seller[3],
                    "sellerAddress": seller[4],
                    "invoiceType": invoice_type,
                    "invoiceDate": invoice_date.strftime("%Y-%m-%d"),
                    "buyerNTNCNIC": buyer_ntn_cnic,
                    "buyerBusinessName": buyer_business_name,
                    "buyerProvince": buyer_province,
                    "buyerAddress": buyer_address,
                    "buyerRegistrationType": buyer_registration_type,
                    "invoiceRefNo": invoice_ref_no,
                    "scenarioId": scenario_id,
                    "items": [
                        {
                            "hsCode": hs_code,
                            "productDescription": product_description,
                            "rate": rate,
                            "uoM": uom,
                            "quantity": quantity,
                            "valueSalesExcludingST": value_sales_excluding_st,
                            "salesTaxApplicable": sales_tax_applicable,
                            "furtherTax": further_tax,
                            "extraTax": extra_tax,
                            "salesTaxWithheldAtSource": sales_tax_withheld,
                            "fixedNotifiedValueOrRetailPrice": 0.00,
                            "fedPayable": fed_payable,
                            "discount": discount,
                            "totalValues": total_values,
                            "saleType": sale_type,
                            "sroScheduleNo": sro_schedule_no,
                            "sroItemSerialNo": sro_item_serial_no,
                        }
                    ],
                }

                # Local validation
                errors = []
                required_fields = [
                    (buyer_business_name, "Buyer Business Name"),
                    (buyer_province, "Buyer Province"),
                    (buyer_address, "Buyer Address"),
                    (buyer_registration_type, "Buyer Registration Type"),
                    (scenario_id, "Scenario ID"),
                    (hs_code, "HS Code"),
                    (product_description, "Product Description"),
                    (rate, "Tax Rate"),
                    (uom, "Unit of Measure"),
                ]

                for field_value, field_name in required_fields:
                    if not field_value:
                        errors.append(f"{field_name} is required")

                if value_sales_excluding_st <= 0:
                    errors.append("Value (Excluding Sales Tax) must be greater than 0")

                if errors:
                    st.markdown(
                        """
                    <div class="error-card">
                        <h4>❌ Validation Failed</h4>
                        <ul style="margin: 0.5rem 0;">
                    """,
                        unsafe_allow_html=True,
                    )
                    for error in errors:
                        st.markdown(f"<li>{error}</li>", unsafe_allow_html=True)
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                else:
                    # Call FBR validation API
                    with st.spinner("🔄 Validating with FBR API..."):
                        status_code, response = validate_invoice_api(
                            invoice_data, seller[5]
                        )

                        if status_code == 200:
                            create_success_message("FBR Validation Successful!")
                            st.json(response)
                        else:
                            create_error_message("FBR Validation Failed")
                            if response:
                                st.json(response)

        with col6:
            if st.button("📤 Post to FBR", use_container_width=True, type="primary"):
                # Same validation and posting logic
                invoice_data = {
                    "sellerNTNCNIC": seller[1],
                    "sellerBusinessName": seller[2],
                    "sellerProvince": seller[3],
                    "sellerAddress": seller[4],
                    "invoiceType": invoice_type,
                    "invoiceDate": invoice_date.strftime("%Y-%m-%d"),
                    "buyerNTNCNIC": buyer_ntn_cnic,
                    "buyerBusinessName": buyer_business_name,
                    "buyerProvince": buyer_province,
                    "buyerAddress": buyer_address,
                    "buyerRegistrationType": buyer_registration_type,
                    "invoiceRefNo": invoice_ref_no,
                    "scenarioId": scenario_id,
                    "items": [
                        {
                            "hsCode": hs_code,
                            "productDescription": product_description,
                            "rate": rate,
                            "uoM": uom,
                            "quantity": quantity,
                            "valueSalesExcludingST": value_sales_excluding_st,
                            "salesTaxApplicable": sales_tax_applicable,
                            "furtherTax": further_tax,
                            "extraTax": extra_tax,
                            "salesTaxWithheldAtSource": sales_tax_withheld,
                            "fixedNotifiedValueOrRetailPrice": 0.00,
                            "fedPayable": fed_payable,
                            "discount": discount,
                            "totalValues": total_values,
                            "saleType": sale_type,
                            "sroScheduleNo": sro_schedule_no,
                            "sroItemSerialNo": sro_item_serial_no,
                        }
                    ],
                }

                # Quick validation
                required_fields = [
                    buyer_business_name,
                    buyer_province,
                    buyer_address,
                    buyer_registration_type,
                    scenario_id,
                    hs_code,
                    product_description,
                    rate,
                    uom,
                ]

                if not all(required_fields) or value_sales_excluding_st <= 0:
                    create_error_message(
                        "Cannot post: Please validate the form first and fix all errors!"
                    )
                else:
                    with st.spinner("📤 Posting to FBR API..."):
                        status_code, response = post_invoice_api(
                            invoice_data, seller[5]
                        )

                        if status_code == 200:
                            create_success_message(
                                "Invoice posted successfully to FBR!"
                            )
                            st.json(response)

                            # Generate PDF after successful posting
                            try:
                                pdf_buffer = generate_invoice_pdf(
                                    invoice_data, response
                                )
                                invoice_filename = f"Invoice_{seller[1]}_{invoice_date.strftime('%Y-%m-%d')}.pdf"

                                st.download_button(
                                    label="📄 Download Invoice PDF",
                                    data=pdf_buffer.getvalue(),
                                    file_name=invoice_filename,
                                    mime="application/pdf",
                                    type="secondary",
                                )

                            except Exception as e:
                                create_error_message(f"PDF generation failed: {str(e)}")

                        else:
                            create_error_message("FBR post failed")
                            if response:
                                st.json(response)
    else:
        st.error("Seller not found!")
        if st.button("⬅️ Back to Dashboard"):
            go_to_dashboard()
            st.rerun()


def show_excel_invoice_auto():
    seller = get_seller_by_id(st.session_state.selected_seller_id)

    if not seller:
        st.error("Seller not found!")
        if st.button("⬅️ Back to Dashboard"):
            go_to_dashboard()
            st.rerun()
        return

    create_nav_breadcrumb("excel_invoice")
    create_header("Smart Excel Processing", f"Bulk invoice processing for {seller[2]}")

    # Check user type to show appropriate back button
    user_type = st.session_state.get("user_type", "admin")

    col1, col2 = st.columns([5, 1])
    with col2:
        if user_type == "guest":
            # Guest users go back to dashboard
            if st.button(
                "⬅️ Back", use_container_width=True, key="guest_excel_back_btn"
            ):
                go_to_dashboard()
                st.rerun()
        else:
            # Admin users go back to excel seller search
            if st.button(
                "⬅️ Back to Search", use_container_width=True, key="admin_excel_back_btn"
            ):
                go_to_excel_seller_search()
                st.rerun()

    # Display seller info
    st.markdown(
        f"""
    <div class="success-card">
        <h4>🏢 Processing for Seller</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem;">
            <div><strong>Name:</strong> {seller[2]}</div>
            <div><strong>NTN/CNIC:</strong> {seller[1]}</div>
            <div><strong>Province:</strong> {seller[3]}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Excel upload section
    st.markdown("### 📁 Smart Excel File Processing")

    st.markdown(
        """
    <div class="custom-card">
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h3>Auto-Detection Enabled</h3>
            <p>The system will automatically detect and map your Excel columns!</p>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "📂 Choose Excel file (.xlsx or .xls)",
        type=["xlsx", "xls"],
        help="Upload your Excel file with invoice data for automatic processing",
    )

    if uploaded_file is not None:
        try:
            # Read Excel file
            df_dict = pd.read_excel(
                uploaded_file, sheet_name=None, dtype={"hsCode": str, "rate": str}
            )

            # Find main data sheet
            main_df = None
            sheet_name = None

            if isinstance(df_dict, dict):
                for name, sheet_df in df_dict.items():
                    if len(sheet_df) > 0:
                        cols_lower = [str(col).lower() for col in sheet_df.columns]
                        if any(
                            keyword in " ".join(cols_lower)
                            for keyword in [
                                "buyer",
                                "invoice",
                                "registration",
                                "name",
                                "amount",
                                "value",
                                "tax",
                            ]
                        ):
                            sheet_name = name
                            main_df = sheet_df
                            break

                if main_df is None:
                    for name, sheet_df in df_dict.items():
                        if len(sheet_df) > 0:
                            sheet_name = name
                            main_df = sheet_df
                            break
            else:
                main_df = df_dict
                sheet_name = "Main Sheet"

            if main_df is None or len(main_df) == 0:
                create_error_message("No data found in the Excel file")
                return

            create_success_message(
                f"File uploaded successfully! Found {len(main_df)} rows"
            )
            if sheet_name:
                st.info(f"📋 Using sheet: **{sheet_name}**")

            # Clean column names
            main_df.columns = [str(col).strip() for col in main_df.columns]

            # Auto-detect columns
            st.markdown("### 🤖 Auto-Detection Results")
            with st.spinner("🔍 Analyzing your Excel columns..."):
                detected_mapping = auto_detect_columns(main_df.columns)

            if detected_mapping:
                create_success_message(
                    f"Automatically detected {len(detected_mapping)} column mappings!"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        """
                    <div class="custom-card">
                        <h4>🎯 Detected Mappings</h4>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    for field_key, excel_col in detected_mapping.items():
                        field_display = field_key.replace("_", " ").title()
                        st.markdown(f"**{field_display}:** {excel_col}")

                with col2:
                    st.markdown(
                        """
                    <div class="custom-card">
                        <h4>📊 Detection Status</h4>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    required_fields = [
                        "buyer_name",
                        "hs_code",
                        "product_desc",
                        "value_excl_st",
                    ]
                    detected_required = [
                        field for field in required_fields if field in detected_mapping
                    ]

                    create_stats_card(
                        f"{len(detected_required)}/4", "Required Fields Detected"
                    )

                    if len(detected_required) < 4:
                        missing = [
                            field.replace("_", " ").title()
                            for field in required_fields
                            if field not in detected_mapping
                        ]
                        st.warning(f"⚠️ Missing: {', '.join(missing)}")
            else:
                st.markdown(
                    """
                <div class="custom-card" style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
                    <h3>Auto-Detection Issue</h3>
                    <p>Could not auto-detect column mappings. Please check your Excel format.</p>
                    <p><strong>Tip:</strong> Make sure your Excel has columns like: Name, Registration No, Value, Rate, etc.</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Show data preview
            st.markdown("### 📋 Data Preview")

            st.markdown(
                """
            <div class="custom-card">
            """,
                unsafe_allow_html=True,
            )

            st.dataframe(main_df.head(10), use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

            if len(main_df) > 10:
                st.info(f"Showing first 10 rows. Total rows: {len(main_df)}")

            # Process data button
            if st.button(
                "🚀 Process Excel Data Automatically",
                type="primary",
                use_container_width=True,
            ):
                required_fields = ["buyer_name", "value_excl_st"]
                missing_required = [
                    field
                    for field in required_fields
                    if field not in detected_mapping or not detected_mapping[field]
                ]

                if missing_required:
                    missing_display = [
                        field.replace("_", " ").title() for field in missing_required
                    ]
                    create_error_message(
                        f"Cannot process: Missing required fields: {', '.join(missing_display)}"
                    )
                    st.info(
                        "💡 Please ensure your Excel has at least Buyer Name and Value columns"
                    )
                else:
                    processed_invoices = []
                    processing_errors = []

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for idx, row in main_df.iterrows():
                        status_text.text(f"Processing row {idx + 1} of {len(main_df)}")
                        progress_bar.progress((idx + 1) / len(main_df))

                        invoice_result, error = process_excel_row_auto(
                            row, detected_mapping, seller, idx
                        )

                        if invoice_result:
                            processed_invoices.append(invoice_result)
                        elif error:
                            processing_errors.append(error)

                    progress_bar.empty()
                    status_text.empty()

                    # Store processed data
                    st.session_state.processed_invoices = processed_invoices

                    # Show processing results
                    if processed_invoices:
                        create_success_message(
                            f"Successfully processed {len(processed_invoices)} invoices!"
                        )

                        st.markdown("### 📊 Processing Summary")
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            create_stats_card(len(processed_invoices), "Total Invoices")
                        with col2:
                            total_amount = sum(
                                [inv["amount"] for inv in processed_invoices]
                            )
                            create_stats_card(f"₨ {total_amount:,.0f}", "Total Amount")
                        with col3:
                            create_stats_card(
                                len(processing_errors), "Processing Errors"
                            )

                        if processing_errors:
                            with st.expander(
                                f"⚠️ Processing Errors ({len(processing_errors)})"
                            ):
                                for error in processing_errors:
                                    st.error(f"• {error}")
                    else:
                        create_error_message("No valid invoices could be processed")
                        if processing_errors:
                            st.error("**Errors encountered:**")
                            for error in processing_errors:
                                st.error(f"• {error}")

        except Exception as e:
            create_error_message(f"Error reading Excel file: {str(e)}")
            st.info("Please ensure your file is a valid Excel (.xlsx or .xls) format")

    # Action buttons for processed invoices
    if st.session_state.processed_invoices:
        st.markdown("### 🚀 Bulk Invoice Actions")

        col5, col6, col7 = st.columns(3)

        with col5:
            if st.button("✅ Validate All Invoices", use_container_width=True):
                validation_results = []

                progress_bar = st.progress(0)
                status_text = st.empty()

                for idx, invoice_item in enumerate(st.session_state.processed_invoices):
                    status_text.text(
                        f"Validating invoice {idx + 1} of {len(st.session_state.processed_invoices)}"
                    )
                    progress_bar.progress(
                        (idx + 1) / len(st.session_state.processed_invoices)
                    )

                    try:
                        status_code, response = validate_invoice_api(
                            invoice_item["invoice_data"], seller[5]
                        )
                        validation_results.append(
                            {
                                "row_number": invoice_item["row_number"],
                                "buyer_name": invoice_item["buyer_name"],
                                "status_code": status_code,
                                "response": response,
                                "success": status_code == 200,
                            }
                        )
                    except Exception as e:
                        validation_results.append(
                            {
                                "row_number": invoice_item["row_number"],
                                "buyer_name": invoice_item["buyer_name"],
                                "status_code": None,
                                "response": {"error": str(e)},
                                "success": False,
                            }
                        )

                progress_bar.empty()
                status_text.empty()

                st.session_state.validation_results = validation_results

                successful_validations = sum(
                    1 for r in validation_results if r["success"]
                )
                failed_validations = len(validation_results) - successful_validations

                # Display results
                st.markdown("### 📋 Validation Results")

                col_success, col_failed = st.columns(2)
                with col_success:
                    create_stats_card(successful_validations, "Successful Validations")
                with col_failed:
                    create_stats_card(failed_validations, "Failed Validations")

                if successful_validations > 0:
                    create_success_message(
                        f"FBR Validation successful for {successful_validations} invoices!"
                    )

                    with st.expander(
                        f"✅ Successful Validations ({successful_validations})",
                        expanded=True,
                    ):
                        for result in validation_results:
                            if result["success"]:
                                st.success(
                                    f"**Row {result['row_number']} - {result['buyer_name']}** ✅"
                                )
                                st.json(result["response"])
                                st.divider()

                if failed_validations > 0:
                    create_error_message(
                        f"FBR Validation failed for {failed_validations} invoices"
                    )

                    with st.expander(
                        f"❌ Validation Failures ({failed_validations})", expanded=True
                    ):
                        for result in validation_results:
                            if not result["success"]:
                                st.error(
                                    f"**Row {result['row_number']} - {result['buyer_name']}** ❌"
                                )
                                if result["status_code"]:
                                    st.write(
                                        f"**Status Code:** {result['status_code']}"
                                    )
                                st.json(result["response"])
                                st.divider()

        with col6:
            if st.button(
                "📤 Post All to FBR", use_container_width=True, type="primary"
            ):
                posting_results = []

                progress_bar = st.progress(0)
                status_text = st.empty()

                for idx, invoice_item in enumerate(st.session_state.processed_invoices):
                    status_text.text(
                        f"Posting invoice {idx + 1} of {len(st.session_state.processed_invoices)}"
                    )
                    progress_bar.progress(
                        (idx + 1) / len(st.session_state.processed_invoices)
                    )

                    try:
                        status_code, response = post_invoice_api(
                            invoice_item["invoice_data"], seller[5]
                        )
                        posting_results.append(
                            {
                                "row_number": invoice_item["row_number"],
                                "buyer_name": invoice_item["buyer_name"],
                                "invoice_data": invoice_item["invoice_data"],
                                "status_code": status_code,
                                "response": response,
                                "success": status_code == 200,
                            }
                        )
                    except Exception as e:
                        posting_results.append(
                            {
                                "row_number": invoice_item["row_number"],
                                "buyer_name": invoice_item["buyer_name"],
                                "invoice_data": invoice_item["invoice_data"],
                                "status_code": None,
                                "response": {"error": str(e)},
                                "success": False,
                            }
                        )

                progress_bar.empty()
                status_text.empty()

                st.session_state.posting_results = posting_results

                successful_posts = sum(1 for r in posting_results if r["success"])
                failed_posts = len(posting_results) - successful_posts

                st.markdown("### 📤 FBR Posting Results")

                col_success, col_failed = st.columns(2)
                with col_success:
                    create_stats_card(successful_posts, "Successfully Posted")
                with col_failed:
                    create_stats_card(failed_posts, "Failed Posts")

                if successful_posts > 0:
                    create_success_message(
                        f"{successful_posts} invoices posted successfully to FBR!"
                    )

                    with st.expander(
                        f"✅ Successfully Posted Invoices ({successful_posts})",
                        expanded=True,
                    ):
                        for result in posting_results:
                            if result["success"]:
                                st.success(
                                    f"**Row {result['row_number']} - {result['buyer_name']}** ✅"
                                )

                                invoice_number = "N/A"
                                if isinstance(result["response"], dict):
                                    if "invoiceNumber" in result["response"]:
                                        invoice_number = result["response"][
                                            "invoiceNumber"
                                        ]
                                    elif (
                                        "data" in result["response"]
                                        and result["response"]["data"]
                                    ):
                                        invoice_number = result["response"]["data"].get(
                                            "invoiceNumber", "N/A"
                                        )

                                st.write(f"**FBR Invoice Number:** {invoice_number}")
                                st.json(result["response"])
                                st.divider()

                if failed_posts > 0:
                    create_error_message(
                        f"{failed_posts} invoices failed to post to FBR"
                    )

                    with st.expander(
                        f"❌ Failed Posts ({failed_posts})", expanded=True
                    ):
                        for result in posting_results:
                            if not result["success"]:
                                st.error(
                                    f"**Row {result['row_number']} - {result['buyer_name']}** ❌"
                                )
                                if result["status_code"]:
                                    st.write(
                                        f"**Status Code:** {result['status_code']}"
                                    )
                                st.json(result["response"])
                                st.divider()

        with col7:
            if st.session_state.posting_results and any(
                r["success"] for r in st.session_state.posting_results
            ):
                if st.button("📄 Generate PDF Package", use_container_width=True):
                    successful_posts = [
                        r for r in st.session_state.posting_results if r["success"]
                    ]

                    if successful_posts:
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(
                            zip_buffer, "w", zipfile.ZIP_DEFLATED
                        ) as zip_file:

                            progress_bar = st.progress(0)
                            status_text = st.empty()

                            for idx, result in enumerate(successful_posts):
                                status_text.text(
                                    f"Generating PDF {idx + 1} of {len(successful_posts)}"
                                )
                                progress_bar.progress((idx + 1) / len(successful_posts))

                                try:
                                    pdf_buffer = generate_invoice_pdf(
                                        result["invoice_data"], result["response"]
                                    )
                                    safe_buyer_name = "".join(
                                        c
                                        for c in result["buyer_name"]
                                        if c.isalnum() or c in (" ", "-", "_")
                                    ).rstrip()
                                    filename = f"Invoice_Row_{result['row_number']}_{safe_buyer_name[:20]}.pdf"
                                    zip_file.writestr(filename, pdf_buffer.getvalue())

                                except Exception as e:
                                    st.error(
                                        f"Failed to generate PDF for row {result['row_number']}: {str(e)}"
                                    )

                            progress_bar.empty()
                            status_text.empty()

                        zip_buffer.seek(0)

                        st.download_button(
                            label="📦 Download All Invoice PDFs",
                            data=zip_buffer.getvalue(),
                            file_name=f"Invoices_{seller[1]}_{date.today().strftime('%Y-%m-%d')}.zip",
                            mime="application/zip",
                            type="secondary",
                        )

                        create_success_message(
                            f"Generated {len(successful_posts)} PDF invoices!"
                        )
            else:
                st.info("📄 Post invoices first to generate PDFs")

    # Show expected format when no file uploaded
    if uploaded_file is None:
        st.markdown("### 📋 Expected Excel Format")
        st.info(
            "🤖 **Smart Detection:** The system automatically recognizes these common column patterns:"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            <div class="custom-card">
                <h4>🔍 Auto-Detected Patterns</h4>
                <div style="font-size: 0.9rem; line-height: 1.6;">
                    <strong>Buyer Information:</strong><br>
                    • Registration No, Buyer Registration No, NTN, CNIC<br>
                    • Name, Buyer Name, Business Name, Customer Name<br>
                    • Type, Registration Type, Registered/Unregistered<br>
                    • Province, Buyer Province, State<br>
                    • Address, Buyer Address, Destination of Supply
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div class="custom-card">
                <h4>💰 Financial Fields</h4>
                <div style="font-size: 0.9rem; line-height: 1.6;">
                    <strong>Invoice & Values:</strong><br>
                    • Document Date, Invoice Date, Date<br>
                    • Document Number, Invoice Number, Reference<br>
                    • HS Code, Commodity Code, Product Code<br>
                    • Value Excluding Sales Tax, Base Value<br>
                    • Sales Tax, Tax Amount, ST Amount<br>
                    • Rate, Tax Rate, Percentage
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Sample data format
        st.markdown("### 📄 Sample Data Format")
        sample_data = {
            "invoiceType": ["Sale Invoice"],
            "invoiceDate": ["8/21/2025"],
            "buyerNTNC": ["Un-Register"],
            "buyerBusinessName": ["Un-Register"],
            "buyerProvince": ["Sindh"],
            "buyerAddress": ["Karachi"],
            "buyerRegistrationType": ["Unregistered"],
            "invoiceRefNo": ["SN002"],
            "scenarioId": ["0101.21"],
            "item_1_hsCode": ["Test Product"],
            "item_1_productDescription": ["18%"],
            "item_1_rate": ["Numbers, pieces, units"],
            "item_1_uoM": ["1"],
            "item_1_quantity": ["1000"],
            "item_1_valueSalesExcludingST": ["180"],
        }

        sample_df = pd.DataFrame(sample_data)

        st.markdown(
            """
        <div class="custom-card">
        """,
            unsafe_allow_html=True,
        )

        st.dataframe(sample_df, use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
            <h3 style="margin: 0;">🎯 Ready to Process</h3>
            <p style="margin: 0.5rem 0 0 0;">Just upload your Excel file - the system will handle column detection automatically!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# Main execution
if check_password():
    main()
else:
    st.stop()
