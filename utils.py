import re
import requests
import json

def extract_terabox_link(url):
    try:
        match = re.search(r'(https?://)?(www\.)?(terabox|4funbox)\.com/s/[a-zA-Z0-9]+', url)
        if not match:
            return None

        share_url = match.group(0)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        session = requests.Session()
        res = session.get(share_url, headers=headers)
        page_text = res.text

        file_name_match = re.search(r'"fs_name":"(.*?)"', page_text)
        fs_id_match = re.search(r'"fs_id":"(.*?)"', page_text)
        uk_match = re.search(r'"uk":"(.*?)"', page_text)
        shareid_match = re.search(r'"shareid":"(.*?)"', page_text)

        if not all([file_name_match, fs_id_match, uk_match, shareid_match]):
            return None

        fs_id = fs_id_match.group(1)
        uk = uk_match.group(1)
        shareid = shareid_match.group(1)

        data = {
            "product": "share",
            "nozip": 0,
            "fid_list": f"[{fs_id}]",
            "uk": uk,
            "shareid": shareid
        }

        api_url = f"https://www.terabox.com/share/list?app_id=250528&clienttype=0"
        api_headers = {
            "User-Agent": headers["User-Agent"],
            "Referer": share_url,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        response = session.post(api_url, headers=api_headers, data=data)
        json_data = response.json()

        dlink = json_data['list'][0].get('dlink', '')
        if not dlink:
            return None

        return dlink

    except Exception as e:
        print("Error extracting Terabox link:", e)
        return None
