import neispy
from datetime import datetime
from asyncio.events import get_event_loop


async def get_schedule(school_name, date):
    async with neispy.Neispy() as neis:
        school_info = await neis.schoolInfo(SCHUL_NM=school_name)
        row = school_info.schoolInfo[1].row[0]
        AE = row.ATPT_OFCDC_SC_CODE
        SE = row.SD_SCHUL_CODE
        try:
            row_schedule = await neis.SchoolSchedule(
                ATPT_OFCDC_SC_CODE=AE, SD_SCHUL_CODE=SE, AA_YMD=date
            )
            row = row_schedule.SchoolSchedule[1].row[0]
            schedule = row.EVENT_NM
        except neispy.error.DataNotFound:
            schedule = "일정이 없습니다."
    return schedule


async def get_meal(school_name, date):
    async with neispy.Neispy() as neis:
        school_info = await neis.schoolInfo(SCHUL_NM=school_name)
        row = school_info.schoolInfo[1].row[0]
        AE = row.ATPT_OFCDC_SC_CODE
        SE = row.SD_SCHUL_CODE
        meal_data = {}
        try:
            meal_info = await neis.mealServiceDietInfo(
                ATPT_OFCDC_SC_CODE=AE, SD_SCHUL_CODE=SE, MLSV_YMD=date
            )
        except neispy.error.DataNotFound:
            pass

        for i in range(3):
            try:
                meal_row = meal_info.mealServiceDietInfo[1].row[i]
                meal_data[i] = meal_row.DDISH_NM.split("<br/>")
            except IndexError:
                meal_data[i] = ['데이터가 없습니다']
            except NameError:
                meal_data = {0: ['데이터가 없습니다'], 1: ['데이터가 없습니다'], 2: ['데이터가 없습니다']}
    return meal_data


def get_info(school_name, date):
    try:
        schedule = get_event_loop().run_until_complete(get_schedule(school_name, date))
        meal_data = get_event_loop().run_until_complete(get_meal(school_name, date))
    except Exception as e:
        return f"Error: {e}", f"Error: {e}"
    return schedule, meal_data


def get_current_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")
    return formatted_date
