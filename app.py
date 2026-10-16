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
        "tab_recs": "🏠 Recommendations Dashboard",
        "tab_deep": "⚡ Deep Scan Engine",
        "tab_pro": "💎 Pro Features",
        "normal_feed": "🎬 Normal Feed",
        "shorts_feed": "⚡ Shorts Feed",
        "live_feed": "🔴 Live Feed",
        "execute_search": "
