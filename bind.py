#!/usr/bin/env python3
# Garena Account Management Tool
# Credits: SenkuCodex (Modified by SOURAV)
# Modified: Auto-install missing modules + New Theme

import subprocess
import sys
import os

# ------------------- Auto Install Missing Modules -------------------
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Module '{package}' not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Module '{package}' installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to install '{package}'. Please install it manually with: pip install {package}")
            sys.exit(1)
        try:
            __import__(package)
        except ImportError:
            print(f"Module '{package}' still not available. Exiting.")
            sys.exit(1)

required_modules = ['requests']
for mod in required_modules:
    install_and_import(mod)

import requests
import json

# ==================== NEW COLOR SCHEME ====================
class Colors:
    GREEN = '\033[92m'      # Success
    RED = '\033[91m'        # Error
    YELLOW = '\033[93m'     # Warning
    BLUE = '\033[94m'       # Info
    MAGENTA = '\033[95m'    # Accent
    CYAN = '\033[96m'       # Highlight
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ==================== NEW BANNER (SOURAV) ====================
def print_banner():
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════╗
║{Colors.BOLD}{Colors.MAGENTA}                 A L P H A                     {Colors.END}{Colors.CYAN}║
║{Colors.BOLD}{Colors.YELLOW}           Garena Account Manager               {Colors.END}{Colors.CYAN}║
╚══════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

def show_header():
    print(f"{Colors.BOLD}{Colors.CYAN}=== Garena Account Management Tool by ALPHA ==={Colors.END}\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_response(response_text, title="Response"):
    print(f"\n{Colors.CYAN}{'-'*55}{Colors.END}")
    print(f"{Colors.BOLD}{title}:{Colors.END}")
    try:
        if response_text.strip().startswith('{') or response_text.strip().startswith('['):
            parsed = json.loads(response_text)
            print(json.dumps(parsed, indent=2, ensure_ascii=False))
            if isinstance(parsed, dict):
                if parsed.get("result") == 0:
                    print(f"\n{Colors.GREEN}✓ SUCCESS{Colors.END} (Result: 0)")
                elif parsed.get("result") != 0:
                    print(f"\n{Colors.RED}✗ FAILED (Result: {parsed.get('result')}){Colors.END}")
        else:
            print(response_text)
            if '"result": 0' in response_text:
                print(f"\n{Colors.GREEN}✓ SUCCESS{Colors.END}")
            elif '"result":' in response_text:
                print(f"\n{Colors.RED}✗ FAILED{Colors.END}")
    except:
        print(response_text)
    print(f"{Colors.CYAN}{'-'*55}{Colors.END}\n")

# ==================== BIND INFO (via API) ====================
def check_bind_info(access_token=None, show_raw=True):
    if not access_token:
        access_token = input("Enter access token: ").strip()
    print(f"\n{Colors.GREEN}[✓]{Colors.END} Checking bind info...")
    
    url = f"https://bind-info-senku.vercel.app/bind_info?access_token={access_token}"
    
    try:
        response = requests.get(url, timeout=30)
        print(f"\n{Colors.BLUE}{'='*55}{Colors.END}")
        print(f"{Colors.GREEN}✓ Account Information:{Colors.END}")
        print(f"{Colors.BLUE}{'='*55}{Colors.END}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                info = data.get("data", {})
                current_email = info.get("current_email", "")
                pending_email = info.get("pending_email", "")
                countdown_human = info.get("countdown_human", "0")
                countdown_seconds = info.get("countdown_seconds", 0)
                
                print(f"  {Colors.CYAN}Current Email:{Colors.END} {current_email}")
                if pending_email:
                    print(f"  {Colors.CYAN}Pending Email:{Colors.END} {pending_email}")
                print(f"  {Colors.CYAN}Countdown:{Colors.END} {countdown_human} ({countdown_seconds} seconds)")
                
                summary = data.get("summary", "")
                if summary:
                    print(f"\n  {Colors.YELLOW}Summary:{Colors.END} {summary}")
                
                if show_raw:
                    raw_response = info.get("raw_response", {})
                    if raw_response:
                        print(f"\n  {Colors.MAGENTA}Raw Response:{Colors.END}")
                        print(f"{Colors.MAGENTA}{'-'*50}{Colors.END}")
                        print(json.dumps(raw_response, indent=2, ensure_ascii=False))
                
                print(f"\n  {Colors.CYAN}Status:{Colors.END} success")
                print(f"  {Colors.CYAN}Status Code:{Colors.END} {response.status_code}")
            else:
                print(f"  {Colors.RED}✗ API returned error: {data.get('message', 'Unknown')}{Colors.END}")
        else:
            print(f"  {Colors.RED}✗ Error: API returned status code {response.status_code}{Colors.END}")
            if response.text:
                print(f"  Response: {response.text[:500]}")
    except Exception as e:
        print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")
    
    print(f"{Colors.BLUE}{'='*55}{Colors.END}")

# ==================== EAT TO ACCESS (using API) ====================
def eat_to_access():
    print(f"\n{Colors.BOLD}{Colors.GREEN}[ EAT TO ACCESS ]{Colors.END}")
    print(f"{'='*55}")
    eat_token = input("Enter EAT token: ").strip()
    if not eat_token:
        print(f"{Colors.RED}✗ Token cannot be empty!{Colors.END}")
        input("Press Enter to continue...")
        return

    api_url = f"https://eat-to-access-beta.vercel.app/eat_to_access?eat_token={eat_token}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}✗ API request failed: {e}{Colors.END}")
        input("Press Enter to continue...")
        return
    except ValueError:
        print(f"{Colors.RED}✗ Invalid JSON response from API{Colors.END}")
        input("Press Enter to continue...")
        return

    if data.get("status") == "success" and "access_token" in data:
        print(f"\n{Colors.GREEN}✓ Success!{Colors.END}")
        print(f"  {Colors.CYAN}Access Token:{Colors.END} {data['access_token']}")
        if data.get("region"):
            print(f"  {Colors.CYAN}Region:{Colors.END} {data['region']}")
        if data.get("game_uid"):
            print(f"  {Colors.CYAN}Game UID:{Colors.END} {data['game_uid']}")
        if data.get("nickname"):
            print(f"  {Colors.CYAN}Nickname:{Colors.END} {data['nickname']}")
    else:
        print(f"{Colors.RED}✗ Failed to get access token.{Colors.END}")
        print("  API response:", json.dumps(data, indent=2))

    input("\nPress Enter to continue...")

# ==================== GARENA ACCOUNT BINDER CLASS ====================
class GarenaAccountBinder:
    def __init__(self, access_token, email):
        self.access_token = access_token
        self.email = email
        self.app_id = "100067"
        self.base_url = "https://100067.connect.garena.com/game/account_security"
        self.headers = {
            'User-Agent': 'GarenaMSDK/4.0.39(GFY-LX3 ;Android 13;en;HK;)',
            'Connection': 'Keep-Alive',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'datadome=XjUykstNTPfQcRhQ6hLhjpqgsuvxVM8gvP59Zsfahr4DRCkZSSQzvYZUmslLlknS9AS3aPFG3S3Z_~SMn7ulGH9cawYoziogCS5sTm6hoW35ctShDcf7U90fYTkaSEaA'
        }
        self.verifier_token = None
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def is_success(self, result):
        return result.get('result') == 0 or result.get('error') == 0
    
    def send_otp(self):
        url = f"{self.base_url}/bind:send_otp"
        data = {
            'app_id': self.app_id,
            'access_token': self.access_token,
            'email': self.email,
            'locale': 'en_HK'
        }
        try:
            response = self.session.post(url, data=data)
            result = response.json()
            print(f"\n[SEND OTP to {self.email}] Status: {response.status_code}")
            format_response(json.dumps(result), "API Response - Send OTP")
            if response.status_code == 200 and self.is_success(result):
                print(f"{Colors.GREEN}✓ OTP sent successfully!{Colors.END}")
                return True
            else:
                error = result.get('message') or result.get('error_msg') or result.get('result') or 'Unknown'
                print(f"{Colors.RED}✗ OTP send failed: {error}{Colors.END}")
                return False
        except Exception as e:
            print(f"{Colors.RED}✗ Error: {str(e)}{Colors.END}")
            return False
    
    def verify_otp(self, otp):
        url = f"{self.base_url}/bind:verify_otp"
        data = {
            'app_id': self.app_id,
            'access_token': self.access_token,
            'otp': otp,
            'email': self.email
        }
        try:
            response = self.session.post(url, data=data)
            result = response.json()
            print(f"\n[VERIFY OTP for {self.email}] Status: {response.status_code}")
            format_response(json.dumps(result), "API Response - Verify OTP")
            if response.status_code == 200 and self.is_success(result):
                self.verifier_token = (result.get('data', {}).get('verifier_token') or
                                      result.get('verifier_token') or
                                      result.get('token') or
                                      result.get('data', {}).get('token'))
                if self.verifier_token:
                    print(f"{Colors.GREEN}✓ OTP verified!{Colors.END}")
                    print(f"  {Colors.CYAN}Verifier Token:{Colors.END} {self.verifier_token[:60]}...")
                    return True
                else:
                    print(f"{Colors.RED}✗ No verifier token received{Colors.END}")
                    return False
            else:
                error = result.get('message') or result.get('error_msg') or result.get('result') or 'Unknown'
                print(f"{Colors.RED}✗ Verification failed: {error}{Colors.END}")
                return False
        except Exception as e:
            print(f"{Colors.RED}✗ Error: {str(e)}{Colors.END}")
            return False
    
    def create_bind_request(self, secondary_password):
        if not self.verifier_token:
            print(f"{Colors.RED}✗ No verifier token{Colors.END}")
            return False
        url = f"{self.base_url}/bind:create_bind_request"
        data = {
            'app_id': self.app_id,
            'access_token': self.access_token,
            'verifier_token': self.verifier_token,
            'secondary_password': secondary_password,
            'email': self.email
        }
        try:
            response = self.session.post(url, data=data)
            result = response.json()
            print(f"\n[CREATE BIND] Status: {response.status_code}")
            format_response(json.dumps(result), "API Response - Create Bind")
            if response.status_code == 200 and self.is_success(result):
                print(f"{Colors.GREEN}✓ Email binding successful!{Colors.END}")
                return True
            else:
                error = result.get('message') or result.get('error_msg') or result.get('result') or 'Unknown'
                print(f"{Colors.RED}✗ Bind failed: {error}{Colors.END}")
                return False
        except Exception as e:
            print(f"{Colors.RED}✗ Error: {str(e)}{Colors.END}")
            return False

# ==================== OPTION FUNCTIONS (with updated colors) ====================
def bind_recovery_email():
    print(f"\n{Colors.BOLD}{Colors.GREEN}[ BIND RECOVERY EMAIL ]{Colors.END}")
    print(f"{'='*55}")
    email = input("Enter email: ").strip()
    if not email:
        print(f"{Colors.RED}✗ Email cannot be empty!{Colors.END}")
        input("Press Enter to continue...")
        return
    access_token = input("Enter access token: ").strip()
    if not access_token:
        print(f"{Colors.RED}✗ Access Token cannot be empty!{Colors.END}")
        input("Press Enter to continue...")
        return
    
    DEFAULT_SECONDARY = "3A43F5AE7A96BAE91481F6225AC98A378CA08EBE92DAC680AAABE41E82102179"
    sec = input("Enter secondary password (default: 3A43F5...): ").strip()
    secondary = sec if sec else DEFAULT_SECONDARY
    
    binder = GarenaAccountBinder(access_token, email)
    print(f"\n{'='*55}")
    print(f"📧 {Colors.CYAN}Email:{Colors.END} {email}")
    print(f"🔑 {Colors.CYAN}Access Token:{Colors.END} {access_token[:25]}...")
    print(f"{'='*55}")
    
    if not binder.send_otp():
        input("Press Enter to continue...")
        return
    otp = input(f"Enter OTP from {email}: ").strip()
    if not otp:
        print(f"{Colors.RED}✗ OTP cannot be empty!{Colors.END}")
        input("Press Enter to continue...")
        return
    if not binder.verify_otp(otp):
        input("Press Enter to continue...")
        return
    print("\nCreating request...")
    if not binder.create_bind_request(secondary):
        input("Press Enter to continue...")
        return
    print(f"\n{Colors.GREEN}✓ Email binding successful!{Colors.END}")
    input("Press Enter to continue...")

def change_bind_email():
    print(f"\n{Colors.BOLD}{Colors.GREEN}[ CHANGE BIND EMAIL ]{Colors.END}")
    print(f"{'='*55}")
    access_token = input("Access Token: ").strip()
    old_email = input("Old Email: ").strip()
    new_email = input("New Email: ").strip()
    if not access_token or not old_email or not new_email:
        print(f"{Colors.RED}✗ All fields are required!{Colors.END}")
        input("Press Enter to continue...")
        return
    
    check_bind_info(access_token, show_raw=False)
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    print(f"\n[Step 1/5] Sending OTP to {old_email}...")
    url_send = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
    data = {"email": old_email, "locale": "en_PK", "region": "PK", "app_id": "100067", "access_token": access_token}
    r = requests.post(url_send, headers=headers, data=data)
    format_response(r.text, "API Response - Old Email")
    if r.status_code != 200 or (r.json().get("result") != 0 if r.text else False):
        print(f"{Colors.RED}✗ Failed to send OTP to old email{Colors.END}")
        input("Press Enter to continue...")
        return
    
    otp_old = input(f"Enter OTP from {old_email}: ").strip()
    
    print(f"\n[Step 2/5] Verifying OTP...")
    url_verify = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
    data = {"email": old_email, "app_id": "100067", "access_token": access_token, "otp": otp_old}
    r = requests.post(url_verify, headers=headers, data=data)
    format_response(r.text, "API Response - Verify Identity")
    try:
        identity_token = r.json().get("identity_token")
        if not identity_token:
            print(f"{Colors.RED}✗ No identity token received{Colors.END}")
            input("Press Enter to continue...")
            return
        print(f"\n{Colors.GREEN}✓ Identity Token:{Colors.END} {identity_token}")
    except:
        print(f"{Colors.RED}✗ Failed to parse response{Colors.END}")
        input("Press Enter to continue...")
        return
    
    print(f"\n[Step 3/5] Sending OTP to {new_email}...")
    data = {"email": new_email, "locale": "en_PK", "region": "PK", "app_id": "100067", "access_token": access_token}
    r = requests.post(url_send, headers=headers, data=data)
    format_response(r.text, "API Response - New Email")
    if r.status_code != 200 or (r.json().get("result") != 0 if r.text else False):
        print(f"{Colors.RED}✗ Failed to send OTP to new email{Colors.END}")
        input("Press Enter to continue...")
        return
    
    otp_new = input(f"Enter OTP from {new_email}: ").strip()
    
    print(f"\n[Step 4/5] Verifying OTP...")
    url_verify_otp = "https://100067.connect.garena.com/game/account_security/bind:verify_otp"
    data = {"email": new_email, "app_id": "100067", "access_token": access_token, "otp": otp_new}
    r = requests.post(url_verify_otp, headers=headers, data=data)
    format_response(r.text, "API Response - Verify OTP")
    try:
        verifier_token = r.json().get("verifier_token")
        if not verifier_token:
            print(f"{Colors.RED}✗ No verifier token received{Colors.END}")
            input("Press Enter to continue...")
            return
        print(f"\n{Colors.GREEN}✓ Verifier Token:{Colors.END} {verifier_token}")
    except:
        print(f"{Colors.RED}✗ Failed to parse response{Colors.END}")
        input("Press Enter to continue...")
        return
    
    print(f"\n[Step 5/5] Creating request...")
    url_rebind = "https://100067.connect.garena.com/game/account_security/bind:create_rebind_request"
    data = {
        "identity_token": identity_token,
        "email": new_email,
        "app_id": "100067",
        "verifier_token": verifier_token,
        "access_token": access_token
    }
    r = requests.post(url_rebind, headers=headers, data=data)
    format_response(r.text, "API Response - Rebind")
    if r.status_code == 200 and '"result": 0' in r.text:
        print(f"\n{Colors.GREEN}✓ Email change request submitted!{Colors.END}")
    else:
        print(f"\n{Colors.RED}✗ Email change failed!{Colors.END}")
    input("Press Enter to continue...")

def unbind_email():
    print(f"\n{Colors.BOLD}[ UNBIND EMAIL ]{Colors.END}")
    print(f"{'='*55}")
    email = input("Enter email: ").strip()
    access_token = input("Enter access token: ").strip()
    if not email or not access_token:
        print(f"{Colors.RED}✗ All fields are required!{Colors.END}")
        input("Press Enter to continue...")
        return
    
    check_bind_info(access_token, show_raw=False)
    
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    print(f"\n[Step 1/3] Sending OTP to {email}...")
    send_url = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
    data = {"email": email, "locale": "en_PK", "region": "PK", "app_id": "100067", "access_token": access_token}
    r = requests.post(send_url, headers=headers, data=data)
    format_response(r.text, "API Response - Send OTP")
    if r.status_code != 200 or (r.json().get("result") != 0 if r.text else False):
        print(f"{Colors.RED}✗ OTP send failed{Colors.END}")
        input("Press Enter to continue...")
        return
    print(f"{Colors.GREEN}✓ OTP sent!{Colors.END}")
    
    otp = input("Enter OTP: ").strip()
    
    print(f"\n[Step 2/3] Verifying OTP...")
    verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
    data = {"email": email, "app_id": "100067", "access_token": access_token, "otp": otp}
    r = requests.post(verify_url, headers=headers, data=data)
    format_response(r.text, "API Response - Verify Identity")
    try:
        identity_token = r.json().get("identity_token")
        if not identity_token:
            print(f"{Colors.RED}✗ No identity token{Colors.END}")
            input("Press Enter to continue...")
            return
        print(f"\n{Colors.GREEN}✓ Identity Token:{Colors.END} {identity_token}")
    except:
        print(f"{Colors.RED}✗ Failed to parse response{Colors.END}")
        input("Press Enter to continue...")
        return
    
    print(f"\n[Step 3/3] Creating request...")
    unbind_url = "https://100067.connect.garena.com/game/account_security/bind:create_unbind_request"
    data = {"app_id": "100067", "access_token": access_token, "identity_token": identity_token}
    r = requests.post(unbind_url, headers=headers, data=data)
    format_response(r.text, "API Response - Unbind")
    if r.status_code == 200 and '"result": 0' in r.text:
        print(f"\n{Colors.GREEN}✓ Unbind request created!{Colors.END}")
    else:
        print(f"\n{Colors.RED}✗ Unbind failed!{Colors.END}")
    input("Press Enter to continue...")

def cancel_bind():
    print(f"\n{Colors.BOLD}[ CANCEL BIND REQUEST ]{Colors.END}")
    print(f"{'='*55}")
    access_token = input("Enter access token: ").strip()
    if not access_token:
        print(f"{Colors.RED}✗ Access Token cannot be empty!{Colors.END}")
        input("Press Enter to continue...")
        return
    
    check_bind_info(access_token, show_raw=False)
    print("\nCreating request...")
    url = "https://100067.connect.gopapi.io/game/account_security/bind:cancel_request"
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {"app_id": "100067", "access_token": access_token}
    r = requests.post(url, headers=headers, data=data)
    print(f"Status Code: {r.status_code}")
    format_response(r.text, "API Response - Cancel")
    if '"result": 0' in r.text:
        print(f"\n{Colors.GREEN}✓ Cancel successful!{Colors.END}")
    else:
        print(f"\n{Colors.RED}✗ Cancel failed!{Colors.END}")
    input("Press Enter to continue...")

def bind_info_only():
    print(f"\n{Colors.BOLD}[ BIND INFO ]{Colors.END}")
    print(f"{'='*55}")
    access_token = input("Enter access token: ").strip()
    check_bind_info(access_token, show_raw=True)
    input("Press Enter to continue...")

# ==================== MAIN ====================
def main():
    while True:
        clear_screen()
        print_banner()
        show_header()
        print("Available Options:")
        print(f"{Colors.GREEN}1. BIND RECOVERY EMAIL{Colors.END}")
        print(f"{Colors.GREEN}2. CHANGE BIND EMAIL{Colors.END}")
        print(f"{Colors.GREEN}3. UNBIND EMAIL{Colors.END}")
        print(f"{Colors.GREEN}4. CANCEL BIND REQUEST{Colors.END}")
        print(f"{Colors.GREEN}5. BIND INFO{Colors.END}")
        print(f"{Colors.GREEN}6. EAT TO ACCESS{Colors.END}")
        print(f"{Colors.GREEN}7. EXIT{Colors.END}")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        choice = input("Choose option (1-7): ").strip()
        
        if choice == "1":
            clear_screen(); print_banner(); show_header(); bind_recovery_email()
        elif choice == "2":
            clear_screen(); print_banner(); show_header(); change_bind_email()
        elif choice == "3":
            clear_screen(); print_banner(); show_header(); unbind_email()
        elif choice == "4":
            clear_screen(); print_banner(); show_header(); cancel_bind()
        elif choice == "5":
            clear_screen(); print_banner(); show_header(); bind_info_only()
        elif choice == "6":
            clear_screen(); print_banner(); show_header(); eat_to_access()
        elif choice == "7":
            print(f"\n{Colors.GREEN}Allah Hafez! 👋{Colors.END}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}✗ Invalid option! Please try again.{Colors.END}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}Allah Hafez! 👋{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
        input("Press Enter to exit...")
