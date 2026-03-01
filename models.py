import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Optional

# --- Backend Models ---
class Ticket(BaseModel):
    id: str
    subject: str
    description: str
    category: str = "General"
    status: str = "open"
    comments: List[dict] = []
    chat_history: List[dict] = []
    solution: Optional[str] = None
    created_at: str = ""

class AgentSessionRequest(BaseModel):
    ticket_id: str
    call_id: str
    call_type: str = "default"

# --- Backend Data Store (In-memory for now) ---
TICKETS: Dict[str, Ticket] = {
    "TIC-DEMO01": Ticket(
        id="TIC-DEMO01",
        subject="Google Account Access on New Laptop",
        description="I bought a new laptop and I can't access my Google account. It keeps asking for verification / I forgot my password. How do I log in safely and restore everything?",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO02": Ticket(
        id="TIC-DEMO02",
        subject="Wi-Fi Connected but Internet Not Working",
        description="Wi-Fi is connected, but Chrome says 'No internet'. Other devices work. Need troubleshooting steps.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO03": Ticket(
        id="TIC-DEMO03",
        subject="Laptop Running Extremely Slow After Setup",
        description="New laptop is slow, apps take forever to open, fan is loud. How do I fix performance?",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO04": Ticket(
        id="TIC-DEMO04",
        subject="Microphone Not Working in Browser Calls",
        description="In Google Meet/Zoom, people can't hear me. Mic works in settings sometimes. Need a fix.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO05": Ticket(
        id="TIC-DEMO05",
        subject="Camera Not Detected / Black Screen",
        description="Camera shows black screen in apps. Works in some apps but not in browser.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO06": Ticket(
        id="TIC-DEMO06",
        subject="Admin Permission Required for Installation",
        description="Windows says I need admin rights to install apps. It's my personal laptop.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO07": Ticket(
        id="TIC-DEMO07",
        subject="Files Missing After Copying from Old Laptop",
        description="I transferred files using USB/Drive but some folders are missing. Need recovery steps.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO08": Ticket(
        id="TIC-DEMO08",
        subject="Google Drive Sync Not Working",
        description="Drive says syncing but files never upload / stuck on 'Preparing'. Need fix.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO09": Ticket(
        id="TIC-DEMO09",
        subject="Email Not Syncing on Outlook/Gmail App",
        description="Emails stopped syncing since yesterday. Need troubleshooting.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO10": Ticket(
        id="TIC-DEMO10",
        subject="Printer Not Printing / Offline",
        description="Printer shows 'offline'. I need to print urgently. Please guide.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO11": Ticket(
        id="TIC-DEMO11",
        subject="Payment Deducted but Subscription Inactive",
        description="I paid for a plan but it still shows free. Payment is successful in my bank.",
        category="Billing",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO12": Ticket(
        id="TIC-DEMO12",
        subject="Invoice Needed for Reimbursement",
        description="I need a GST/Tax invoice for my subscription for office reimbursement.",
        category="Billing",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO13": Ticket(
        id="TIC-DEMO13",
        subject="Auto-Renewal Charged Unexpectedly",
        description="Subscription renewed automatically and I was charged. I want to understand the charge.",
        category="Billing",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO14": Ticket(
        id="TIC-DEMO14",
        subject="Plan Upgrade Not Reflected",
        description="I upgraded from Basic to Pro but features aren't showing. How to fix?",
        category="Billing",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO15": Ticket(
        id="TIC-DEMO15",
        subject="How to Contact Support / Escalate",
        description="I want to escalate my issue and share screenshots/logs. What's the best way?",
        category="General",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO16": Ticket(
        id="TIC-DEMO16",
        subject="Account Security Check Request",
        description="I got a suspicious login alert. I want to secure my account and check recent activity.",
        category="General",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO17": Ticket(
        id="TIC-DEMO17",
        subject="Bluetooth Headphones Not Connecting",
        description="Pairing reset, remove device/re-pair, switch output device, disable hands-free mode tips.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO18": Ticket(
        id="TIC-DEMO18",
        subject="Gmail Not Receiving Emails",
        description="Spam filter, blocked addresses, storage full, forwarding rules, filters, check 'All Mail'.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO19": Ticket(
        id="TIC-DEMO19",
        subject="Windows Update Stuck",
        description="Restart, storage space, troubleshooter basics, safe 'wait vs restart' guidance.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    ),
    "TIC-DEMO20": Ticket(
        id="TIC-DEMO20",
        subject="Forgot Wi-Fi Password",
        description="Agent can walk them through finding Wi-Fi password on router, using another device.",
        category="Technical",
        status="open",
        created_at=datetime.now().isoformat()
    )
}

# --- Audio Buffer ---
SESSION_AUDIO: Dict[str, List[bytes]] = {}
