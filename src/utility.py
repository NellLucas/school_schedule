import json
import re
import os

def save_id():
    while True:
        username = input("사용자 이름(USERNAME)을 입력하세요 : ")
        password = input("비밀번호를 입력하세요 : ")
        data = {"id": username, "pw": password}
        with open("account.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("사용자 이름과 비밀번호가 저장되었습니다.\n")
        return data


def get_id():
    try:
        with open("account.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return json_data
    except:
        return save_id()


def remove_numbers(items):
    return re.sub(r'\s*\([0-9.]*\)', '', items)


def get_fomatted_date(date):
    formatted_date = date.strftime("%Y%m%d")
    return formatted_date


def remove_files(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
