import json
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr

load_dotenv()  # Load environment variables


class GeminiAssistant:
    def __init__(self):
        genai.configure(api_key="AIzaSyDHHCM4jdLio7svg2c_KRupC93lvShT6fg")

        self.model = genai.GenerativeModel("gemini-pro")
        self.chat = self.model.start_chat(history=[])

    def get_gemini_response(self, template, question):
        prompt = f""" {template}

السؤال {question}
"""
        response = self.chat.send_message(prompt.format(question=question))
        return response.text

    @staticmethod
    def listen_for_wake_word():
        speech_recognizer = sr.Recognizer()
        print("Listening for wake word...")
        with sr.Microphone() as source:
            speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = speech_recognizer.listen(source, timeout=10, phrase_time_limit=10)
            try:
                speech_text = speech_recognizer.recognize_google(audio, language='ar-AR').lower()
                print(speech_text)
                return speech_text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                return None

    @staticmethod
    def get_num(amount):
        numbers = re.findall(r'\d+', amount)
        numbers = ''.join(numbers)
        if numbers:
            return numbers, True
        else:
            return "المبلغ غير صحيح يرجى اعادة مره اخرى", False

    @staticmethod
    def Wallet_cheak(wallte, pre, text):
        for i in pre:
            if i in str(text):
                return i + " كاش", True
                break
        else:
            for i in wallte:
                if i in str(text):
                    return i, True
                    break
            else:
                return "اسم المحفظة غير صحيح يرجى اختيار محفظة صحصحة   ", False

    @staticmethod
    def check_phone_number(phone_number):
        if len(phone_number) != 9:
            return "عذرا عزيزي رقم الهاتف غير صحيح يرجى نطق رقم الهاتف مره اخرى", False
        prefix = phone_number[:2]
        if prefix == "77" or prefix == "78":
            return "يمن موبايل ", True
        elif prefix == "71":
            return "سبأفون  ", True
        elif prefix == "73":
            return "يو ", True
        elif prefix == "70":
            return " واي ", True
        else:
            return "عذرا عزيزي رقم الهاتف غير صحيح يرجى نطق رقم الهاتف مره اخرى", False

    @staticmethod
    def update_json_file(file_name, updates):
        try:
            with open(file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
            return data

        data.update(updates)
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    @staticmethod
    def extract_data_within_braces_as_dict(text):
        pattern = r'\{([^}]*)\}'
        match = re.search(pattern, text)
        if match:
            data_within_braces = match.group(1).strip()
            return json.loads("{" + data_within_braces + "}")
        else:
            return {'amount': None,
                    'phone_number': None,
                    'wallet_name': None,
                    'opration_number': None,
                    'msg': None,
                    'mobile_companay': None
                    }

    @staticmethod
    def create_vir_json():
        data = {'amount': None,
                'phone_number': None,
                'wallet_name': None,
                'opration_number': None,
                'msg': None,
                'mobile_companay': None
                }
        file_name = 'data.json'
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def is_empty(value):
        return value is None or value == "" or value == "None" or value == "null"

    @staticmethod
    def process_Json(Data):
        assistant = GeminiAssistant()
        Data = assistant.extract_data_within_braces_as_dict(Data)
        file_name = "data.json"
        for key, valeu in Data.items():
            if assistant.is_empty(valeu):
                continue
            else:
                j = {key: valeu}
                assistant.update_json_file(file_name, j)
        with open(file_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data

    @staticmethod
    def check_conditions(data):

        is_canceled = data["is_canceled"]
        assistant = GeminiAssistant()
        company_phone = ["Yemen Mobail", "You", "Sabafon"]
        wallete = ["جوالي", "ون كاش", "كاش"]
        text = " وي  كاش  تسيبنم "
        pre = ["وي", "ون"]
        msg = ""
        op_num = 0
        company = ""

        amount = data["amount"]
        phone_number = data["phone_number"]
        wallet_name = data["wallet_name"]
        if not is_canceled:

            if assistant.is_empty(amount) and assistant.is_empty(phone_number) and assistant.is_empty(wallet_name):

                msg = "يرجى تحديد المبلغ ورقم الهاتف واسم المحفظة التي تريد الدفع منها لإكمال عملية السداد"
            elif assistant.is_empty(amount) and assistant.is_empty(phone_number) and not assistant.is_empty(
                    wallet_name):
                wallet_name, chk = assistant.Wallet_cheak(wallete, pre, wallet_name)
                if chk:
                    msg = "يرجى تحديد الملبغ ورقم الهاتف لإكمال عملية السداد"
                else:
                    msg = "يرجى تحديد الملبغ ورقم الهاتف لإكمال عملية السداد" + wallet_name

            elif assistant.is_empty(amount) and not assistant.is_empty(phone_number) and assistant.is_empty(
                    wallet_name):
                phone_number_co, chk = assistant.check_phone_number(assistant.get_num(str(phone_number))[0])
                if chk:
                    company = phone_number_co
                    msg = "يرجى تحديد اسم المحفظة والمبلغ الذي تريد دفعه لإكمال عملية السداد"
                else:
                    msg = "يرجى تحديد اسم المحفظة والمبلغ الذي تريد دفعه لإكمال عملية السداد" + phone_number

            elif not assistant.is_empty(amount) and assistant.is_empty(phone_number) and assistant.is_empty(
                    wallet_name):
                amount, chk = assistant.get_num(str(amount))
                if chk:

                    msg = "يرجى تحديد اسم المحفظة ورقم الهاتف لإكمال عملية السداد"
                else:
                    msg = "يرجى تحديد اسم المحفظة ورقم الهاتف لإكمال عملية السداد" + amount

            elif assistant.is_empty(amount) and not assistant.is_empty(phone_number) and not assistant.is_empty(
                    wallet_name):
                phone_number_co, chk_ph = assistant.check_phone_number(assistant.get_num(str(phone_number))[0])
                wallet_name, chk_wa = assistant.Wallet_cheak(wallete, pre, wallet_name)
                if chk_wa and chk_ph:
                    company = phone_number_co
                    msg = "يرجى تحديد المبلغ الذي تريد السداد به لاكمال عملية السداد"
                elif chk_wa and not chk_ph:
                    msg = "يرجى تحديد المبلغ الذي تريد السداد به لاكمال عملية السداد" + phone_number_co
                elif chk_ph and not chk_wa:
                    company = phone_number_co
                    msg = "يرجى تحديد المبلغ الذي تريد السداد به لاكمال عملية السداد" + wallet_name
                else:
                    msg = "يرجى تحديد المبلغ الذي تريد السداد به لاكمال عملية السداد" + wallet_name + phone_number

            elif not assistant.is_empty(amount) and assistant.is_empty(phone_number) and not assistant.is_empty(
                    wallet_name):
                wallet_name, chk_wa = assistant.Wallet_cheak(wallete, pre, wallet_name)
                amount, chk_am = assistant.get_num(str(amount))
                if chk_am and chk_wa:
                    msg = "يرجى تحديد رقم الهاتف الذي تريد السداد له لإكمال عملية السداد"
                elif chk_am and not chk_wa:
                    msg = "يرجى تحديد رقم الهاتف الذي تريد السداد له لإكمال عملية السداد" + wallet_name
                elif chk_wa and not chk_am:
                    msg = "يرجى تحديد رقم الهاتف الذي تريد السداد له لإكمال عملية السداد" + amount
                else:
                    msg = "يرجى تحديد رقم الهاتف الذي تريد السداد له لإكمال عملية السداد" + wallet_name + amount

            elif not assistant.is_empty(amount) and not assistant.is_empty(phone_number) and assistant.is_empty(
                    wallet_name):
                phone_number_co, chk_ph = assistant.check_phone_number(assistant.get_num(str(phone_number))[0])
                amount, ch_am = assistant.get_num(str(amount))
                if ch_am and chk_ph:
                    company = phone_number_co
                    msg = "يرجى تحديد اسم المحفظة لإكمال عملية السداد"
                elif chk_ph and not ch_am:
                    company = phone_number_co
                    msg = "يرجى تحديد اسم المحفظة لإكمال عملية السداد" + amount
                elif ch_am and not chk_ph:
                    msg = "يرجى تحديد اسم المحفظة لإكمال عملية السداد" + phone_number_co

            elif not assistant.is_empty(amount) and not assistant.is_empty(phone_number) and not assistant.is_empty(
                    wallet_name):
                phone_number_co, chk_ph = assistant.check_phone_number(assistant.get_num(str(phone_number))[0])
                amount, chk_am = assistant.get_num(str(amount))
                wallet_name, chk_wa = assistant.Wallet_cheak(wallete, pre, wallet_name)
                if chk_wa and chk_ph and chk_am:
                    op_num = 1
                    company = phone_number_co
                    msg = "يرجى التأكيد على البيانات المعروضة أمامك أو تعديلها لإكمال عملية السداد"
                elif chk_wa and chk_ph and not chk_am:
                    msg = amount
                elif chk_wa and not chk_ph and chk_am:
                    msg = phone_number_co
                elif not chk_wa and chk_ph and chk_am:
                    msg = wallet_name
                elif not chk_wa and not chk_ph and chk_am:
                    msg = phone_number_co + wallet_name
                elif not chk_wa and chk_ph and not chk_am:
                    msg = wallet_name + amount
                elif chk_wa and not chk_ph and not chk_am:
                    msg = phone_number_co + amount
                elif not chk_wa and not chk_ph and not chk_am:
                    msg = phone_number_co + wallet_name + amount

            # # Printing data        op_num = 1
            return msg, op_num, wallet_name, phone_number, amount, company, is_canceled
        else:
            msg = "تم الغاء الطلب. كيف يمكنني مساعدتك  "
            return msg, op_num, None, None, None, None, is_canceled

    @staticmethod
    def updeat_data(Question):
        template = """انت عبارة عن مساعد برمجي تقوم بتحويل السؤال الخاص بالمستخدم الى صيغية json  وتستخرج البيانات من سؤال المستخدم وتضعها في json وتعيدها  قم باستخراج البيانات التالي من السؤال  واذا كان السؤال عبارة عن الغاء العملية فقط في حالة وحود كلمة الغاء للعميلة  قم بعمل true في متغير الالغاء    
'json
'amount':""
'phone_number ': ""
'wallet_name':""
'is_canceled':""
'
واذا لم يتوفر اي من البيانات السابقة قم باعطاه قيمة null
"""
        file_name = "data.json"

        assistant = GeminiAssistant()
        Data = assistant.get_gemini_response(template, Question)
        data = assistant.process_Json(Data)
        msg, op_num, wallet_name, phone_number, amount, company, is_canceled = assistant.check_conditions(data)
        last_update = {
            "msg": msg,
            "opration_number": op_num,
            "wallet_name": wallet_name,
            "phone_number": phone_number,
            "amount": amount,
            "mobile_companay": company,
            "is_canceled": is_canceled
        }

        assistant.update_json_file(file_name, last_update)

    @staticmethod
    def secound_op(Quation):
        last_update_nun = {
            "msg": "تم الغاء العملية بنجاح ",
            "opration_number": 0,
            "wallet_name": "null",
            "phone_number": "null",
            "amount": "null",
            "mobile_companay": "null"
        }
        template = """
                انت عبارة عن مساعد برمجي تقوم بفهم وتحويل السؤال الخاص بالمستخدم الى ارقام فقط 
                اذا كان في صياغة السؤال التأكيد على العملية سوف تعيد رقم 1،
                 واذا كانت العملية عبارة عن الغاء سوف تعيد رقم 2،
                  واذا كان تعديل على البيانات او وجود نقص او خطأ سوف تعيد الرقم 3،
                  واذا ليس صياغة السؤال
                 أي من الانواع  السابقة سوف تعيد الرقم 0.

                قم بإرجاع كافة النتائج في ملف json
                    result:""
                """
        # Assuming GeminiAssistant and listen_for_wake_word are correctly implemented
        assistant = GeminiAssistant()
        Data = assistant.get_gemini_response(template, Quation)
        text_dict = assistant.extract_data_within_braces_as_dict(Data)
        print(text_dict)

        if text_dict['result'] == 1:
            print("=====================sadasd")
            last_update = {"opration_number": 0,
                           "msg": "تم تاكيد العملية بنجاح شكرا لك طلبك تحت المعالجة"
                           }
            assistant.update_json_file("data.json", last_update)
        elif text_dict['result'] == 2:

            assistant.update_json_file("data.json", last_update_nun)

        elif text_dict['result'] == 3:
            print("========================")
            last_update_ = {"opration_number": 0,
                            "msg": "قم باعطائنا البيانات التي تريد تعديلها ",
                            }
            assistant.update_json_file("data.json", last_update_)
        else:
            last_update = {
                "msg": "عذر عزيزي لم استطيع فهم السؤال لو سمحت قم باعادة السؤال"
            }
            assistant.update_json_file("data.json", last_update)

    @staticmethod
    def read_json():
        with open("data.json", 'r', encoding='utf-8') as json_file:
            last_Data = json.load(json_file)
        return last_Data
