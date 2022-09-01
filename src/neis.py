# @author: seungw0n
from datetime import datetime
from excel import openExcel, readNeis

def isWeekday(d: str) -> bool:
    """ 주말인지 아닌지 확인 """
    date = datetime.strptime(d, "%Y.%m.%d")
    return True if date.weekday() <= 4 else False

def isValidStartTime(targetHour: int, targetMin: int, startHour: int, startMin: int) -> bool:
    """ targetHour:targetMin 일과시간 후 부터만 특근매식비 지원 """
    if startHour > targetHour:
        return True
    
    if startHour == targetHour and startMin >= targetMin:
        return True
    
    return False

def isValid(date: str, totalHour: int, targetHour: int, targetMin: int, startHour: int, startMin: int) -> bool:
    """ 특근매식비를 받을 수 있는 조건인지 확인 함
    조건
        평일: 일과시간 이후 초과근무 1시간 이상
        주말: 초과근무 1시간 이상
    """
    if totalHour >= 1:
        if isWeekday(date) and isValidStartTime(targetHour, targetMin, startHour, startMin):
            return True
    
    return False

def overworkLog(filename: str, targetHour: int, targetMin: int) -> tuple:
    """ NEIS 초과근무확인에서 특근매식비 지급여부를 나눔 """
    wb, _ = openExcel(filename)
    total = readNeis(wb)

    correctLog = dict()
    wrongLog = dict()

    for key, val in total.items():
        correctValues = []
        wrongValues = []

        for v in val:  # [이름, 시작시간, 끝난시간, 총합]
            startHour = int(v[1].split(":")[0])
            startMin = int(v[1].split(":")[1])
            totalHour = int(v[3].split(':')[0])
            # totalMin = int(v[3].split(':')[1])

            validation = isValid(key, totalHour, targetHour, targetMin, startHour, startMin)

            if validation:
                correctValues.append(v)
            else:
                wrongValues.append(v)

        correctLog[key] = correctValues
        wrongLog[key] = wrongValues
    
    return correctLog, wrongLog



c, w = overworkLog("초과근무확인(7월분_나이스원본).xlsx", 16, 50)
print(c)