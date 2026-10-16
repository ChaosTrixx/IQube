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
        "import_sub":
