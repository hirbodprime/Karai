from ippanel import Client
from ippanel import HTTPError, Error, ResponseCode

api_key = "i47UwgEM7u2I7l3ErpyXCgsooxkysAIBIR_5V4C43Gg="

sms = Client(api_key)
def send_sms_code(number,code):
    try:
        message_id = sms.send("3000505",[str(number)], f"کد ورود شما {code}",summary='some summary')
    except Error as e: # ippanel sms error
        print(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e: # http error like network error, not found, ...
        print(f"Error handled => code: {e}")
