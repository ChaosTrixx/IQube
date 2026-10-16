import streamlit as st
import streamlit.components.v1 as components
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import datetime
import hashlib
import html
import json
import os
import secrets
import threading

# --- 1. MUST BE THE VERY FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="IQube - Secure Multi-Source Discovery Engine",
    page_icon="⚡",
    layout="wide",
)

# --- THREAD LOCK FOR SAFE CONCURRENCY ---
DB_LOCK = threading.Lock()
USER_DB_FILE = "iqube_secure_db.json"
PREMIUM_KEY_VALID = "IQUBE-PRO-2026"

# --- SUPER-ADMIN CONFIGURATION ---
ADMIN_USERNAME = "lala"
ADMIN_GOOGLE_EMAIL = os.getenv("ADMIN_GOOGLE_EMAIL", "lala@gmail.com")

# --- MULTI-LANGUAGE TRANSLATION DICTIONARIES (EN & DE) ---
TRANSLATIONS = {
    "English (EN)": {
        "title": "🟢 IQUBE // MULTI-SOURCE DISCOVERY ENGINE",
        "access_portal": "🟢 IQUBE // SECURE ACCESS PORTAL",
        "matrix_access": "Access Matrix",
        "login": "Log In",
        "create_account": "Create Account",
        "user_id": "User ID",
        "security_key": "Security Key",
        "auth_node": "Authenticate Node",
        "init_node": "Initialize Node",
        "confirm_key": "Confirm Security Key",
        "active_node": "Active Node",
        "status_std": "Status: Standard Tier",
        "terminate_session": "Terminate Session",
        "admin_center": "👑 ADMIN CONTROL CENTER",
        "manage_accounts": "Manage Registered Accounts",
        "select_node": "Select User Node",
        "toggle_pro": "Toggle Pro",
        "delete_user": "Delete User",
        "promote_all": "Promote All Users to Pro",
        "ip_security": "IP Security & Banning",
        "enter_ip": "Enter IP to Ban",
        "execute_ban": "Execute IP Ban",
        "remove_ban": "Remove IP Ban",
        "lift_ban": "Lift IP Ban",
        "feedback_inbox": "User Feedback & Bug Reports",
        "broadcast_alert": "System Broadcast Alert",
        "broadcast_msg": "Broadcast Message",
        "publish_alert": "Publish Alert",
        "clear_alert": "Clear Alert",
        "db_maint": "Database Maintenance",
        "download_backup": "📥 Download Full DB Backup",
        "restore_db": "Restore DB from Backup",
        "raw_inspector": "Raw DB Inspector",
        "source_platform": "Source Platform",
        "audio_saver": "📻 Audio-Only Background Data Saver Mode",
        "import_sub": "📥 Subscriptions & Playlist Export",
        "upload_json": "Import Channel Export (.json)",
        "export_profile": "📤 Export IQube Profile (.json)",
        "unlock_pro": "💎 Unlock IQube Pro",
        "enter_license": "Enter License Key",
        "activate_pro": "Activate Pro Node",
        "global_search": "🔍 GLOBAL SPOKEN TRANSCRIPT VECTOR SEARCH",
        "search_placeholder": "Type any search term to scan transcripts...",
        "tab_recs": "🏠 Recommendations Matrix",
        "tab_deep": "⚡ Deep Scan Engine",
        "tab_pro": "💎 Pro Features",
        "normal_feed": "🎬 Normal Feed",
        "shorts_feed": "⚡ Shorts Feed",
        "live_feed": "🔴 Live Feed",
        "execute_search": "Execute Deep Search Query",
        "train_profile": "Train Profile",
        "calibrate": "Calibrate 👍",
        "stream_adfree": "▶ Stream Ad-Free",
        "ai_summary": "🧠 Generate Neural AI Summary",
        "custom_genre_name": "Custom Genre Name",
        "custom_genre_query": "Custom Search Query",
        "add_matrix": "Add Custom Genre Matrix",
        "diagnostics": "🛠️ SYSTEM DIAGNOSTICS & CONTROL PANEL",
        "patchnotes_tab": "📜 Up-To-Date Patchnotes (v2.9.14 - 2FA Removed for Admin)",
        "directory_tab": "📋 Complete IQube Functionality Directory",
        "feedback_title": "🐛 Send Feedback / Bug Report",
        "feedback_placeholder": "Describe bug or request...",
        "submit_admin": "Submit to Admin",
    },
    "German (DE) - Deutsch": {
        "title": "🟢 IQUBE // MULTI-SOURCE DISCOVERY ENGINE",
        "access_portal": "🟢 IQUBE // SICHERES ZUGANGSPORTAL",
        "matrix_access": "Zugangsmatrix",
        "login": "Anmelden",
        "create_account": "Konto erstellen",
        "user_id": "Benutzername",
        "security_key": "Sicherheitsschlüssel",
        "auth_node": "Knoten authentifizieren",
        "init_node": "Knoten initialisieren",
        "confirm_key": "Schlüssel bestätigen",
        "active_node": "Aktiver Knoten",
        "status_std": "Status: Standard-Stufe",
        "terminate_session": "Sitzung beenden",
        "admin_center": "👑 ADMIN-KONTROLLZENTRUM",
        "manage_accounts": "Registrierte Konten verwalten",
        "select_node": "Benutzerknoten auswählen",
        "toggle_pro": "Pro umschalten",
        "delete_user": "Benutzer löschen",
        "promote_all": "Alle Benutzer auf Pro stufen",
        "ip_security": "IP-Sicherheit & Sperren",
        "enter_ip": "IP zum Sperren eingeben",
        "execute_ban": "IP-Sperre ausführen",
        "remove_ban": "IP-Sperre entfernen",
        "lift_ban": "Sperre aufheben",
        "feedback_inbox": "Benutzer-Feedback & Fehlerberichte",
        "broadcast_alert": "System-Rundschreiben",
        "broadcast_msg": "Nachricht senden",
        "publish_alert": "Warnung veröffentlichen",
        "clear_alert": "Löschen",
        "db_maint": "Datenbank-Wartung",
        "download_backup": "📥 Vollständiges Backup herunterladen",
        "restore_db": "DB aus Backup wiederherstellen",
        "raw_inspector": "Roh-DB-Inspektor",
        "source_platform": "Quellplattform",
        "audio_only": "Nur-Audio-Datenparmodus",
        "import_sub": "📥 Abonnements & Playlist-Export",
        "upload_json": "Kanal-Export importieren (.json)",
        "export_profile": "📤 IQube-Profil exportieren (.json)",
        "unlock_pro": "💎 IQube Pro freischalten",
        "enter_license": "Lizenzschlüssel eingeben",
        "activate_pro": "Pro-Knoten aktivieren",
        "global_search": "🔍 GLOBALE SPRACHTRANSKRIPT-VEKTORSUCHE",
        "search_placeholder": "Suchbegriff eingeben...",
        "tab_recs": "🏠 Empfehlungsmatrix",
        "tab_deep": "⚡ Deep-Scan-Engine",
        "tab_pro": "💎 Pro-Funktionen",
        "normal_feed": "🎬 Normaler Feed",
        "shorts_feed": "⚡ Shorts-Feed",
        "live_feed": "🔴 Live-Feed",
        "execute_search": "Deep-Suchanfrage ausführen",
        "train_profile": "Profil trainieren",
        "calibrate": "Kalibrieren 👍",
        "stream_adfree": "▶ Werbefrei streamen",
        "ai_summary": "🧠 KI-Zusammenfassung generieren",
        "custom_genre_name": "Benutzerdefinierter Genre-Name",
        "custom_genre_query": "Benutzerdefinierte Suchanfrage",
        "add_matrix": "Genre-Matrix hinzufügen",
        "diagnostics": "🛠️ SYSTEMDIAGNOSE & KONTROLLPANEL",
        "patchnotes_tab": "📜 Aktuelle Patchnotes (v2.9.14)",
        "directory_tab": "📋 Funktionsverzeichnis",
        "feedback_title": "🐛 Feedback / Fehlerbericht senden",
        "feedback_placeholder": "Fehler oder Wunsch beschreiben...",
        "submit_admin": "An Admin senden",
    },
}

def t(key: str) -> str:
    lang = st.session_state.get("app_language", "English (EN)")
    return TRANSLATIONS.get(lang, TRANSLATIONS["English (EN)"]).get(key, key)

st.markdown("""
    <style>
        .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #0b0f19; border-right: 1px solid rgba(0, 243, 255, 0.1); }
        div.stExpander, div.stForm { background: rgba(17, 24, 39, 0.6) !important; border: 1px solid rgba(0, 243, 255, 0.15) !important; border-radius: 12px !important; backdrop-filter: blur(12px); }
        .stButton>button { background: linear-gradient(135deg, #00f3ff 0%, #0066ff 100%) !important; color: #030712 !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; box-shadow: 0 0 15px rgba(0, 243, 255, 0.3); transition: all 0.3s ease; width: 100%; }
        .stButton>button:hover { box-shadow: 0 0 25px rgba(0, 243, 255, 0.7); transform: translateY(-2px); }
        input { background-color: #111827 !important; color: #00f3ff !important; border: 1px solid rgba(0, 243, 255, 0.3) !important; border-radius: 8px !important; }
        h1, h2, h3 { color: #00f3ff !important; letter-spacing: 0.05em; text-shadow: 0 0 10px rgba(0, 243, 255, 0.2); }
        hr { border-color: rgba(0, 243, 255, 0.1) !important; }
        .premium-badge { background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%); color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .admin-badge { background: linear-gradient(135deg, #ff4b4b 0%, #ff0000 100%); color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .broadcast-banner { background: rgba(0, 243, 255, 0.1); border: 1px solid #00f3ff; padding: 10px; border-radius: 8px; margin-bottom: 20px; color: #00f3ff; font-weight: bold; }
        .feedback-card { background: rgba(17, 24, 39, 0.8); border-left: 3px solid #00f3ff; padding: 10px; margin-bottom: 10px; border-radius: 4px; font-size: 0.9em; }
        
        /* Hover-to-Play Thumbnail Container */
        .thumb-hover-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(0, 243, 255, 0.2);
        }
        .thumb-hover-container img {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            object-fit: cover;
            transition: opacity 0.3s ease;
            z-index: 2;
        }
        .thumb-hover-container iframe {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
            border: none;
        }
        .thumb-hover-container:hover img {
            opacity: 0;
            pointer-events: none;
        }
    </style>
""", unsafe_allow_html=True)

def hash_password(password: str, salt_hex: str = None) -> tuple[str, str]:
    if not salt_hex:
        salt = secrets.token_bytes(16)
        salt_hex = salt.hex()
    else:
        salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return key.hex(), salt_hex

def load_database() -> dict:
    with DB_LOCK:
        db_data = {"users": {}, "banned_ips": [], "system_announcement": "", "feedback_reports": []}
        if os.path.exists(USER_DB_FILE):
            try:
                with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                    db_data = json.load(f)
            except Exception:
                pass
        
        if "users" not in db_data: db_data["users"] = {}
        if "banned_ips" not in db_data: db_data["banned_ips"] = []
        if "system_announcement" not in db_data: db_data["system_announcement"] = ""
        if "feedback_reports" not in db_data: db_data["feedback_reports"] = []

        if ADMIN_USERNAME not in db_data["users"]:
            default_pass_hash, default_salt = hash_password("admin2026!secure")
            db_data["users"][ADMIN_USERNAME] = {
                "password_hash": default_pass_hash,
                "salt": default_salt,
                "email": ADMIN_GOOGLE_EMAIL,
                "history": [],
                "playlists": [],
                "is_premium": True,
                "is_admin": True,
                "custom_genres": {}
            }
            with open(USER_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(db_data, f, indent=4)
        return db_data

def save_database(db: dict):
    with DB_LOCK:
        with open(USER_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

def sanitize(text: str) -> str:
    return html.escape(str(text))

def get_client_ip() -> str:
    try:
        ctx = st.runtime.scriptrunner.get_script_run_ctx()
        if ctx and hasattr(ctx, "headers"):
            forwarded = ctx.headers.get("X-Forwarded-For")
            if forwarded: return forwarded.split(",")[0].strip()
            return ctx.headers.get("Remote-Addr", "127.0.0.1")
    except Exception:
        pass
    return "127.0.0.1"

def fetch_sponsor_segments(video_id: str) -> list:
    url = f"https://sponsor.ajay.app/api/skipSegments?videoID={video_id}"
    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 200: return res.json()
    except Exception:
        pass
    return []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
if "feed_type" not in st.session_state: st.session_state.feed_type = "normal"
if "audio_only" not in st.session_state: st.session_state.audio_only = False
if "platform_source" not in st.session_state: st.session_state.platform_source = "YouTube"
if "app_language" not in st.session_state: st.session_state.app_language = "English (EN)"

db_master = load_database()
client_ip = get_client_ip()
if client_ip in db_master.get("banned_ips", []):
    st.error("🛑 ACCESS DENIED: Your IP address has been restricted.")
    st.stop()

def auth_screen():
    selected_lang = st.selectbox("🌍 Language / Sprache", list(TRANSLATIONS.keys()))
    st.session_state.app_language = selected_lang
    st.title(t("access_portal"))
    choice = st.radio(t("matrix_access"), [t("login"), t("create_account")])

    if choice == t("login"):
        with st.form("login_form"):
            username_input = sanitize(st.text_input(t("user_id")).strip().lower())
            password_input = st.text_input(t("security_key"), type="password")
            submit = st.form_submit_button(t("auth_node"))
            if submit:
                db = load_database()
                users = db.get("users", {})
                if username_input in users:
                    stored_hash = users[username_input]["password_hash"]
                    salt_hex = users[username_input]["salt"]
                    calc_hash, _ = hash_password(password_input, salt_hex)
                    if secrets.compare_digest(stored_hash, calc_hash):
                        st.session_state.logged_in = True
                        st.session_state.username = username_input
                        st.rerun()
                    else:
                        st.error("Authentication failed: Invalid credentials.")
                else:
                    st.error("Authentication failed: User node does not exist.")
    else:
        with st.form("register_form"):
            new_user = sanitize(st.text_input(t("user_id")).strip().lower())
            new_pass = st.text_input(t("security_key"), type="password")
            confirm_pass = st.text_input(t("confirm_key"), type="password")
            reg_submit = st.form_submit_button(t("init_node"))
            if reg_submit:
                db = load_database()
                users = db.setdefault("users", {})
                if not new_user or not new_pass: st.error("Fields cannot be empty.")
                elif new_user in users: st.error("User node ID already exists.")
                elif new_pass != confirm_pass: st.error("Security keys do not match.")
                elif new_user == ADMIN_USERNAME: st.error("Reserved node ID.")
                else:
                    p_hash, salt_hex = hash_password(new_pass)
                    users[new_user] = {
                        "password_hash": p_hash,
                        "salt": salt_hex,
                        "history": [],
                        "playlists": [],
                        "is_premium": False,
                        "is_admin": False,
                        "custom_genres": {}
                    }
                    save_database(db)
                    st.success("Account successfully initialized! Switch to Log In.")

if not st.session_state.logged_in:
    auth_screen()
else:
    current_user = st.session_state.username
    db = load_database()
    users = db.setdefault("users", {})

    if current_user == ADMIN_USERNAME and current_user in users:
        users[current_user]["is_admin"] = True
        users[current_user]["is_premium"] = True
        save_database(db)

    user_data = users.get(current_user, {"history": [], "playlists": [], "is_premium": False, "is_admin": False, "custom_genres": {}})
    is_premium = user_data.get("is_premium", False)
    is_admin = user_data.get("is_admin", False) or (current_user == ADMIN_USERNAME)

    if "user_history" not in st.session_state:
        st.session_state.user_history = user_data.get("history", [])

    with st.sidebar:
        selected_lang = st.selectbox("🌍 Language / Sprache", list(TRANSLATIONS.keys()))
        st.session_state.app_language = selected_lang

        st.write(f"{t('active_node')}: **{current_user.upper()}**")
        if is_admin: st.markdown('<span class="admin-badge">SUPER ADMIN</span>', unsafe_allow_html=True)
        elif is_premium: st.markdown('<span class="premium-badge">PRO ACTIVE</span>', unsafe_allow_html=True)
        else: st.write(t("status_std"))

        if st.button(t("terminate_session")):
            db = load_database()
            if current_user in db.get("users", {}):
                db["users"][current_user]["history"] = st.session_state.user_history
                save_database(db)
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.pop("user_history", None)
            st.rerun()

        if is_admin:
            st.divider()
            st.markdown(f"### {t('admin_center')}")
            with st.expander(t("manage_accounts"), expanded=False):
                all_users = list(db.get("users", {}).keys())
                target_user = st.selectbox(t("select_node"), all_users)
                if target_user and target_user != ADMIN_USERNAME:
                    t_data = db["users"][target_user]
                    current_status = "Pro" if t_data.get("is_premium") else "Standard"
                    st.write(f"Target Status: **{current_status}**")
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        if st.button(t("toggle_pro")):
                            db["users"][target_user]["is_premium"] = not t_data.get("is_premium", False)
                            save_database(db)
                            st.success("Updated status!")
                            st.rerun()
                    with col_a2:
                        if st.button(t("delete_user"), type="primary"):
                            del db["users"][target_user]
                            save_database(db)
                            st.warning("Deleted account.")
                            st.rerun()
                st.markdown("---")
                if st.button(t("promote_all")):
                    for u in db["users"]: db["users"][u]["is_premium"] = True
                    save_database(db)
                    st.success("All promoted to Pro!")
                    st.rerun()

            with st.expander(t("ip_security"), expanded=False):
                st.write(f"Current IP: `{client_ip}`")
                banned_list = db.setdefault("banned_ips", [])
                ban_input = st.text_input(t("enter_ip"))
                if st.button(t("execute_ban")):
                    if ban_input and ban_input not in banned_list:
                        banned_
