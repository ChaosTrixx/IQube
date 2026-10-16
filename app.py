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
import requests

# --- 1. MUST BE THE VERY FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="IQube // CYBER MATRIX DISCOVERY ENGINE",
    page_icon="⚡",
    layout="wide",
)

# --- THREAD LOCK & CONFIGURATION ---
DB_LOCK = threading.Lock()
USER_DB_FILE = "iqube_secure_db.json"
PREMIUM_KEY_VALID = "IQUBE-PRO-2026"
ADMIN_USERNAME = "lala"
ADMIN_GOOGLE_EMAIL = os.getenv("ADMIN_GOOGLE_EMAIL", "lala@gmail.com")

# --- MULTI-LANGUAGE TRANSLATION DICTIONARIES (EN & DE) ---
TRANSLATIONS = {
    "English (EN)": {
        "title": "⚡ [SYSTEM:// IQUBE MATRIX DISCOVERY CORE]",
        "access_portal": "🔒 [SECURE NEURAL ACCESS PORTAL]",
        "matrix_access": "Authentication Protocol",
        "login": "Access Node",
        "create_account": "Initialize New Node",
        "user_id": "Operator Handle (ID)",
        "security_key": "Neural Passkey",
        "auth_node": "Execute Access",
        "init_node": "Initialize Node",
        "confirm_key": "Confirm Passkey",
        "active_node": "Active Neural Node",
        "status_std": "STATUS: STANDARD AGENT",
        "terminate_session": "Terminate Neural Link",
        "admin_center": "👑 OVERSEER MATRIX CONTROL",
        "manage_accounts": "Manage Neural Nodes",
        "select_node": "Target Operator Node",
        "toggle_pro": "Toggle Elite Tier",
        "delete_user": "Purge Node",
        "promote_all": "Elevate All Nodes to Elite",
        "ip_security": "IP Firewall & Banning",
        "enter_ip": "Target IP Address",
        "execute_ban": "Execute Firewall Block",
        "remove_ban": "Remove Block",
        "lift_ban": "Lift Firewall Rule",
        "feedback_inbox": "Encrypted Anomaly Reports",
        "broadcast_alert": "Matrix Broadcast Override",
        "broadcast_msg": "System Broadcast Payload",
        "publish_alert": "Transmit Alert",
        "clear_alert": "Purge Alert",
        "db_maint": "Matrix Core Maintenance",
        "download_backup": "📥 Export Core DB Backup",
        "restore_db": "Restore DB from Backup",
        "source_platform": "Data Feed Vector",
        "audio_saver": "📻 Audio-Only Bandwidth Saver Mode",
        "import_sub": "📥 Subscriptions & Playlist Ingestion",
        "upload_json": "Import Data Manifest (.json)",
        "export_profile": "📤 Export Neural Profile (.json)",
        "unlock_pro": "💎 Unlock Elite Matrix Status",
        "enter_license": "Enter Elite License Key",
        "activate_pro": "Activate Elite Node",
        "global_search": "🔍 GLOBAL SPOKEN TRANSCRIPT NEURAL VECTOR SEARCH",
        "search_placeholder": "Scan transcript frequencies for keywords...",
        "tab_recs": "🏠 Matrix Cinema Rails",
        "tab_deep": "⚡ Deep Transcript Scanner",
        "tab_pro": "💎 Elite Features",
        "normal_feed": "🎬 Standard Feed",
        "shorts_feed": "⚡ Flash Feeds (Shorts)",
        "live_feed": "🔴 Live Matrix Streams",
        "execute_search": "Execute Neural Scan",
        "train_profile": "Calibrate Neural Weights",
        "calibrate": "Calibrate 👍",
        "not_interested": "🚫 Not Interested",
        "stream_adfree": "▶ Jack In (Theater Mode)",
        "back_to_feed": "← Disconnect / Return to Matrix Grid",
        "ai_summary": "🧠 Generate Neural AI Summary",
        "custom_genre_name": "Custom Matrix Rail Name",
        "custom_genre_query": "Target Query Vector",
        "add_matrix": "Compile Custom Cinema Rail",
        "diagnostics": "🛠️ SYSTEM DIAGNOSTICS & CHRONOLOGS",
        "patchnotes_tab": "📜 Cyberpunk Matrix Changelog",
        "directory_tab": "📋 System Functionality Directory",
        "feedback_title": "🐛 Transmit Bug Report / Anomaly",
        "feedback_placeholder": "Describe system anomaly...",
        "submit_admin": "Transmit to Overseer",
    },
    "German (DE) - Deutsch": {
        "title": "⚡ [SYSTEM:// IQUBE MATRIX DISCOVERY CORE]",
        "access_portal": "🔒 [SICHERES NEURONALES ZUGANGSPORTAL]",
        "matrix_access": "Authentifizierungs-Protokoll",
        "login": "Knoten betreten",
        "create_account": "Neuen Knoten initialisieren",
        "user_id": "Operator-Kennung (ID)",
        "security_key": "Neuronaler Schlüssel",
        "auth_node": "Zugriff ausführen",
        "init_node": "Knoten initialisieren",
        "confirm_key": "Schlüssel bestätigen",
        "active_node": "Aktiver neuraler Knoten",
        "status_std": "STATUS: STANDARD-AGENT",
        "terminate_session": "Neuronale Verbindung trennen",
        "admin_center": "👑 OVERSEER MATRIX-KONTROLLE",
        "manage_accounts": "Neuronale Knoten verwalten",
        "select_node": "Ziel-Operator",
        "toggle_pro": "Elite-Stufe umschalten",
        "delete_user": "Knoten löschen",
        "promote_all": "Alle Knoten zu Elite stufen",
        "ip_security": "IP-Firewall & Sperren",
        "enter_ip": "Ziel-IP-Adresse",
        "execute_ban": "Firewall-Sperre ausführen",
        "remove_ban": "Sperre entfernen",
        "lift_ban": "Firewall-Regel aufheben",
        "feedback_inbox": "Verschlüsselte Anormalitätsberichte",
        "broadcast_alert": "Matrix-Broadcast-Override",
        "broadcast_msg": "System-Broadcast-Nutzdaten",
        "publish_alert": "Alarm übertragen",
        "clear_alert": "Alarm löschen",
        "db_maint": "Matrix-Core-Wartung",
        "download_backup": "📥 Core-DB-Backup exportieren",
        "restore_db": "DB aus Backup wiederherstellen",
        "source_platform": "Datenstrom-Vektor",
        "audio_only": "Nur-Audio-Bandbreitensparmodus",
        "import_sub": "📥 Abonnements & Playlist-Ingestion",
        "upload_json": "Datenmanifest importieren (.json)",
        "export_profile": "📤 Neurales Profil exportieren (.json)",
        "unlock_pro": "💎 Elite-Matrix-Status freischalten",
        "enter_license": "Elite-Lizenzschlüssel eingeben",
        "activate_pro": "Elite-Knoten aktivieren",
        "global_search": "🔍 GLOBALE SPRACHTRANSKRIPT-NEURONALE VEKTORSUCHE",
        "search_placeholder": "Transkript-Frequenzen durchsuchen...",
        "tab_recs": "🏠 Matrix-Cinema-Rails",
        "tab_deep": "⚡ Deep-Transkript-Scanner",
        "tab_pro": "💎 Elite-Funktionen",
        "normal_feed": "🎬 Standard-Feed",
        "shorts_feed": "⚡ Flash-Feeds (Shorts)",
        "live_feed": "🔴 Live-Matrix-Streams",
        "execute_search": "Neuronalen Scan ausführen",
        "train_profile": "Neuronale Gewichte kalibrieren",
        "calibrate": "Kalibrieren 👍",
        "not_interested": "🚫 Kein Interesse",
        "stream_adfree": "▶ Einwählen (Theater-Modus)",
        "back_to_feed": "← Trennen / Zurück zum Matrix-Grid",
        "ai_summary": "🧠 Neuronale KI-Zusammenfassung generieren",
        "custom_genre_name": "Benutzerdefinierter Rail-Name",
        "custom_genre_query": "Ziel-Abfragevektor",
        "add_matrix": "Benutzerdefinierte Cinema-Rail",
        "diagnostics": "🛠️ SYSTEMDIAGNOSE & CHRONOLOGS",
        "patchnotes_tab": "📜 Cyberpunk-Matrix-Changelog",
        "directory_tab": "📋 System-Funktionsverzeichnis",
        "feedback_title": "🐛 Fehlerbericht / Anormalität senden",
        "feedback_placeholder": "Systemanormalität beschreiben...",
        "submit_admin": "An Overseer übertragen",
    }
}

def t(key: str) -> str:
    lang = st.session_state.get("app_language", "English (EN)")
    return TRANSLATIONS.get(lang, TRANSLATIONS["English (EN)"]).get(key, key)

st.markdown("""
    <!-- DNS Pre-fetching & Pre-connecting for Zero Latency -->
    <link rel="preconnect" href="https://www.youtube.com">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://i.ytimg.com">
    <link rel="dns-prefetch" href="https://www.youtube.com">
    <link rel="dns-prefetch" href="https://googlevideo.com">
    
    <style>
        .stApp {
            background-color: #000000 !important;
            background-image: 
                linear-gradient(rgba(0, 255, 102, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 102, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            color: #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        [data-testid="stSidebar"] {
            background-color: #020408 !important;
            border-right: 1px solid rgba(0, 255, 102, 0.2) !important;
            box-shadow: inset -5px 0 15px rgba(0, 255, 102, 0.05);
        }
        div.stExpander, div.stForm {
            background: rgba(2, 8, 4, 0.8) !important;
            border: 1px solid rgba(0, 255, 102, 0.3) !important;
            border-radius: 4px !important;
            box-shadow: 0 0 12px rgba(0, 255, 102, 0.1);
            backdrop-filter: blur(8px);
        }
        .stButton>button {
            background: linear-gradient(135deg, #001a0a 0%, #003311 100%) !important;
            color: #00ff66 !important;
            font-weight: 700 !important;
            font-family: 'Courier New', Courier, monospace !important;
            border: 1px solid #00ff66 !important;
            border-radius: 3px !important;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
            transition: all 0.2s ease-in-out;
            width: 100%;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .stButton>button:hover {
            background: #00ff66 !important;
            color: #000000 !important;
            box-shadow: 0 0 25px rgba(0, 255, 102, 0.8);
            transform: translateY(-1px);
        }
        input, textarea, select {
            background-color: #010a04 !important;
            color: #00ff66 !important;
            border: 1px solid rgba(0, 255, 102, 0.4) !important;
            border-radius: 3px !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        input:focus {
            border-color: #00f3ff !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.4);
        }
        h1, h2, h3 {
            color: #00ff66 !important;
            font-family: 'Courier New', Courier, monospace !important;
            letter-spacing: 0.15em;
            text-shadow: 0 0 12px rgba(0, 255, 102, 0.6);
            text-transform: uppercase;
        }
        hr { border-color: rgba(0, 255, 102, 0.2) !important; }
        
        .rail-header {
            font-size: 1.4rem;
            font-weight: 800;
            color: #00f3ff !important;
            margin-top: 30px;
            margin-bottom: 15px;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            border-left: 4px solid #00f3ff;
            padding-left: 12px;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.4);
        }
        
        .btn-desc {
            font-size: 0.75rem;
            color: rgba(0, 255, 102, 0.7);
            margin-bottom: 10px;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
        }
        
        .premium-badge {
            background: linear-gradient(135deg, #00f3ff 0%, #0066ff 100%);
            color: #000;
            padding: 2px 8px;
            border-radius: 2px;
            font-size: 0.8em;
            font-weight: bold;
            box-shadow: 0 0 8px rgba(0, 243, 255, 0.6);
        }
        .admin-badge {
            background: linear-gradient(135deg, #ff0055 0%, #990033 100%);
            color: #fff;
            padding: 2px 8px;
            border-radius: 2px;
            font-size: 0.8em;
            font-weight: bold;
            box-shadow: 0 0 8px rgba(255, 0, 85, 0.8);
        }
        .broadcast-banner {
            background: rgba(0, 255, 102, 0.08);
            border: 1px solid #00ff66;
            padding: 10px;
            border-radius: 3px;
            margin-bottom: 20px;
            color: #00ff66;
            font-weight: bold;
            box-shadow: 0 0 12px rgba(0, 255, 102, 0.2);
            font-family: 'Courier New', Courier, monospace;
        }
        .feedback-card {
            background: rgba(1, 10, 4, 0.9);
            border-left: 3px solid #00f3ff;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 2px;
            font-size: 0.9em;
        }
        .thumb-hover-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            background: #000;
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid rgba(0, 255, 102, 0.4);
            margin-bottom: 8px;
            box-shadow: 0 0 8px rgba(0, 255, 102, 0.15);
            transition: all 0.3s ease;
        }
        .thumb-hover-container:hover {
            border-color: #00f3ff;
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.5);
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
        else:
            db_data["users"][ADMIN_USERNAME]["is_admin"] = True
            db_data["users"][ADMIN_USERNAME]["is_premium"] = True

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

# --- PERSISTENT SESSION RESTORATION FIX ---
query_params = st.query_params
if "logged_in" not in st.session_state:
    persisted_user = query_params.get("session_user")
    db_check = load_database()
    if persisted_user and persisted_user in db_check.get("users", {}):
        st.session_state.logged_in = True
        st.session_state.username = persisted_user
    else:
        st.session_state.logged_in = False
        st.session_state.username = None

if "active_theater_video" not in st.session_state:
    st.session_state.active_theater_video = None
if "feed_type" not in st.session_state: st.session_state.feed_type = "normal"
if "audio_only" not in st.session_state: st.session_state.audio_only = False
if "platform_source" not in st.session_state: st.session_state.platform_source = "YouTube"
if "app_language" not in st.session_state: st.session_state.app_language = "English (EN)"

db_master = load_database()
client_ip = get_client_ip()
if client_ip in db_master.get("banned_ips", []):
    st.error("🛑 FIREWALL BREACH DETECTED: Your IP address has been locked out.")
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
                        st.query_params["session_user"] = username_input
                        st.rerun()
                    else:
                        st.error("Access Denied: Invalid Neural Passkey.")
                else:
                    st.error("Access Denied: Operator Node does not exist.")
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
                elif new_user in users: st.error("Operator Handle already registered.")
                elif new_pass != confirm_pass: st.error("Passkeys do not synchronize.")
                elif new_user == ADMIN_USERNAME: st.error("Reserved Overseer handle.")
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
                    st.success("Node successfully compiled! Switch to Access Node.")

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
    is_premium = user_data.get("is_premium",
