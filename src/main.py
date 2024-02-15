import draw
import neis as ns
import utility as util
import schedule
import time
from instagrapi import Client
from datetime import datetime


account_data = util.get_id()
ACCOUNT_USERNAME = account_data["id"]
ACCOUNT_PASSWORD = account_data["pw"]

cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
print("Login Successful")

def fetch_image():
    school_name = "능주고등학교"
    schedules, meal_data = ns.get_info(school_name, ns.get_current_date())
    draw.create_meal_image(schedules, meal_data)
    draw.create_schedule_image(school_name)


def upload_instagram():
    fetch_image()
    upload_img = ["images/아침_menu.jpeg", "images/점심_menu.jpeg", "images/저녁_menu.jpeg", "images/schedule.jpeg"]
    cl.album_upload(paths=upload_img, caption=f'{datetime.now().strftime("%Y/%m/%d")}의 학사일정입니다.')
    time.sleep(5)
    print("Upload Completed in ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


schedule.every().day.at("01:00").do(upload_instagram)


try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    pass
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"An error occurred: {e}")
finally:
    cl.logout()
    print("Logout Successful")
