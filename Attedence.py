import datetime
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D6)

req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)



import gspread 
from oauth2client.service_account import ServiceAccountCredentials
scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds=ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)

sheet = client.open('MyAttendance').sheet1


def attend(uid):
    col = 1
    flag = 0 
    uida=str(uid)
    for row in range (4,7):
        res = sheet.cell(row,1).value
        if uida == res:
            print('student found')
            flag = 1 
            return row,col

    if flag == 0:
        print('student not found')
        return 0,0

def getdate():
    now = datetime.datetime.now()
    month = str(now.month)
    day = str(now.day) 
    date = month+'/'+day
    row = 2 
    for col in range (3,22):
        res = sheet.cell(row,col).value
        if date == res :
            return row,col

def update_attend(row,col):
    res=sheet.cell(row,col).value
    if res!='P':
        sheet.update_cell(row,col,'P')
        print('Attendance Given successfully')
    else :
        print('Already present for today!!')



ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

pn532.SAM_configuration()
print('Waiting for RFID/NFC card...')
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is None:
        continue
    #print('Found card with UID:', [hex(i) for i in uid])
    uid_a=int.from_bytes(uid, byteorder='big', signed=False)
    row_S , col_S = attend(uid_a)
    if col_S == 0 not row_S == 0:
        continue
    row_D , col_D = getdate()
    update_attend(row_S,col_D)




    






