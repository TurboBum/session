from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from qr_code import qrcode_new, read_qrcode
import os
import psycopg2
from random import randint
from datetime import date, timedelta

app = FastAPI()
templates = Jinja2Templates(directory="./")
connectionSQL = psycopg2.connect(dbname="postgres", host="127.0.0.1", user="postgres", password="root",port='')


@app.get("/")
def root():
    return FileResponse("./index.html")
##############################################
@app.get("/registration")
def registration():
    return FileResponse("./registration.html")


@app.post("/proverkaREG")
#функцию Form() помещаем в название тех переменныхБ которые указаны в поле name в input`ах в форме для передачи на бэк
def proverkaREG(
    request: Request, 
    insurance_company = Form(), 
    expiry_date = Form(), 
    policy_number = Form(), 
    workplace = Form(), 
    passport = Form(), 
    full_name = Form(),
    birthday = Form(),
    gender = Form(),
    Place_of_residence = Form(),
    tel = Form(),
    mail = Form()
    
    ):
    name = full_name.split(' ')#Ф И О
    passport_date = passport.split(' ')#Паспортные данные
    with connectionSQL.cursor() as cursor:
        try:
            connectionSQL.rollback()
            # выполнение запроса для получения максимального значения id
            cursor.execute("SELECT MAX(id_patients) FROM patients")
            max_id = cursor.fetchone()[0]
            if max_id is None:
                max_id = 0
            next_id = int(max_id) + 1
            id_medical_cart = next_id*randint(123,473)
            print(type(tel))
            cursor.execute(f"INSERT INTO list_of_phones (phone) VALUES ('{tel}') RETURNING *")
            connectionSQL.commit()
            # id_patients  = cursor.fetchone()
            # print(id_patients[0])
            cursor.execute(f"INSERT INTO list_of_emails (email) VALUES ('{mail}')")
            connectionSQL.commit()
            cursor.execute(f"INSERT INTO insurance_company (insurance_company) VALUES ('{insurance_company}') RETURNING *")
            connectionSQL.commit()
            id_company  = cursor.fetchone()
            print(id_company)

            #проблемное место
            cursor.execute(f"SELECT number_of_insurance_policy FROM list_of_insurance_policy WHERE number_of_insurance_policy = '{policy_number}'")
            policy_id = cursor.fetchall()
            print("sss" + str(policy_id))
            # проверка на полис номер Должна быть. Если нет ретурном запомнить его ключ к полюсу привязать страх. комп. елис комп. нет создаю получаю айди и добавляю к полису.
            cursor.execute(f"INSERT INTO list_of_insurance_policy (number_of_insurance_policy, dateoff_insurance_policy, fk_insurance_company) VALUES ('{policy_number}','{expiry_date}','{id_company[0]}')")
            connectionSQL.commit()

            if len(name) == 2 :
                cursor.execute(f"INSERT INTO patients (lastname, firstname, seria_passport, number_passport, birthday, gender, fk_insurance_policy) VALUES ('{name[0]}', '{name[1]}', '{passport_date[0]}', '{passport_date[1]}', '{birthday}', '{gender}', '{policy_number}') RETURNING *" )
            else:
                cursor.execute(f"INSERT INTO patients (lastname, firstname, secondname, seria_passport, number_passport, birthday, gender, fk_insurance_policy) VALUES ('{name[0]}', '{name[1]}', '{name[2]}', '{passport_date[0]}', '{passport_date[1]}', '{birthday}', '{gender}', '{policy_number}') RETURNING *" )
            test = connectionSQL.commit()
            patient_id = cursor.fetchone()[0]
            print(patient_id)

            cursor.execute(f"INSERT INTO medical_cart (number_medical_cart) VALUES ('{patient_id}') RETURNING *")
            connectionSQL.commit()
            medcard_id = cursor.fetchone()[0]
            print(medcard_id)

            cursor.execute(f"UPDATE patients SET fk_id_medical_cart = ('{medcard_id}') WHERE id_patients = '{patient_id}'")
            connectionSQL.commit()

            print(test)
        except IndexError:
            return {"ERROR":'Были введены некоректные данные'}

    qrcode = qrcode_new(full_name, passport)
    app.mount("/qr-cods", StaticFiles(directory="./qr-cods"), name="static")
    status = 200
    return templates.TemplateResponse('./qr_code_display.html', {'request': request, 'status': status, 'qrcode': f"qr-cods/{qrcode}",'policy_number':policy_number,'qrcode_name':qrcode})

@app.get("/download-the-qr-code/{qrcode_name}")
def download_the_qr_code(request: Request, qrcode_name: str):
    file_path = os.path.join("qr-cods", qrcode_name)
    return FileResponse(file_path, media_type="application/octet-stream")


@app.post("/viewing-the-QR-code")
async  def upload_image(upload_file: UploadFile = File(...)):
    # Создаем путь до файла на основе имени файла, загруженного пользователем
    # file_path = f"download_qr_cods/{upload_file.filename}"#проблема с русскими символами в названии файла
    file_path = f"download_qr_cods/test.png"#проблема Решена
    # Сохраняем файл на диск
    with open(file_path, "wb") as file:
        file.write(await upload_file.read())
    text = read_qrcode(file_path)
    os.remove(os.path.join('download_qr_cods', 'test.png'))#решение проблемы
    return {"message": text}



@app.get("/download-the-document/{policy_number}")
def download_the_document(request: Request, policy_number: str):
    # Здесь может быть логика обработки и формирования файла
    filename = f"{policy_number}.docx"
    file_path = f"./documents/{filename}"  # Путь к файлу, который нужно скачать
    with open(file_path, 'w') as file:
        file.write('''(заполнение) необходимых сопутствующих документов: 
                   договор на медицинское обслуживание и согласие на обработку персональных данных
                    в формате .docx (шаблоны будут предоставлены в ресурсах).
                   ''')
    return FileResponse(file_path, filename=filename, media_type="application/octet-stream")


##############################################




#########################################
@app.get('/hospitalization')
def hospitalization():
    return FileResponse("Hospitalizacia/index.html")
@app.get('/hospitalizationREG')
def hospitalization():
    return FileResponse("Hospitalizacia/hospitalization.html")
@app.get('/Viewing_information_about_the_patients_code')
def Viewing_information_about_the_patients_code():
    return (FileResponse("Hospitalizacia/Viewing_information_about_the_patients_code.html"))
@app.get('/Refusal_of_hospitalization')
def Refusal_of_hospitalization():
    return FileResponse("Hospitalizacia/Refusal_of_hospitalization.html")
@app.get('/rejection_as_a_therapist')
def rejection_as_a_therapist():
    return FileResponse("Hospitalizacia/the_reason_for_the_therapists_refusal.html")




@app.post('/proverkaGOS')
def proverkaGOS(request: Request,
                full_name = Form(),
                passport = Form(), 
                workplace = Form(),
                policy_number = Form(),
                expiry_date = Form(),
                insurance_company = Form(),
                hospitalization = Form(),
                date_and_time = Form(),
                ):
    with connectionSQL.cursor() as cursor:
        try:
            passport_date = passport.split(' ')#Паспортные данные
            connectionSQL.rollback()
            cursor.execute(f"SELECT number_of_insurance_policy FROM list_of_insurance_policy WHERE number_of_insurance_policy = '{policy_number}'")
            policy_id = cursor.fetchone()
            cursor.execute(f"SELECT id_patients FROM patients WHERE seria_passport = '{passport_date[0]}' AND number_passport = '{passport_date[1]}' OR ='{policy_id}'")
            result = cursor.fetchone()
        except IndexError:
            return {"ERROR":'Были введены некоректные данные'}
        return {"Результат:", result[0]}

                    # id_patients  = cursor.fetchone()
            # print(id_patients[0])
    # status = "Сохранение"
    # js_code = 'alert("Данные БЫЛИ сохранены");'
    # return templates.TemplateResponse('./service_notification.html',
    #                                   {'request': request, 'status': status, 'js_code': js_code})




@app.post('/TrueCode')
def TrueCode(request: Request, code = Form()):
    try:
        Intcode = int(code)
        status = Intcode
        js_code = 'alert("Данные Просмотренны");'
    except:
        status = "Ошибка кода"
        js_code = 'alert("Данные невозможно прочитать");'
    return templates.TemplateResponse('./service_notification.html',
                                          {'request': request, 'status': status, 'js_code': js_code})
@app.get('/rejection_as_a_customer')
def rejection_as_a_customer(request: Request):
    status = "Вы отказались как клиент"
    js_code = 'alert("Госпитализация была отменена");'
    return templates.TemplateResponse('./service_notification.html',
                                      {'request': request, 'status': status, 'js_code': js_code})
@app.post('/failure_report')
def failure_report(request: Request, eason_for_the_refusal=Form()):
    status = "Вы отказали как терапевт"
    js_code = f'alert("Госпитализация была отменена терапевтом по причине {eason_for_the_refusal}");'
    return templates.TemplateResponse('./service_notification.html',
                                      {'request': request, 'status': status, 'js_code': js_code})
###############################################



@app.get('/therapeutic_and_diagnostic_measures')
def therapeutic_and_diagnostic_measures():
    return FileResponse("therapeutic_and_diagnostic_measures/index.html")
@app.get('/Working_ith_a_medical_card')
def Working_ith_a_medical_card():
    return FileResponse("therapeutic_and_diagnostic_measures/Working_ith_a_medical_card.html")
@app.get('/id_user')
def id_user():
    return FileResponse("therapeutic_and_diagnostic_measures/id_user.html")
########################################################################################################################
@app.post('/vibor_destfij')
def vibor_destfij(request: Request,login=Form(),password=Form()):
    with connectionSQL.cursor() as cursor:
        connectionSQL.rollback()
        cursor.execute(f"SELECT id_doctor FROM doctors WHERE login = '{login}' AND password = '{password}'")
        policy_id = cursor.fetchone()
        if policy_id is None:
            status = "УЧ неверные"
            js_code = f'alert("Вы ввели неверные данные");'
            return templates.TemplateResponse('./service_notification.html',
                                          {'request': request, 'status': status, 'js_code': js_code})
        else:
            return FileResponse("therapeutic_and_diagnostic_measures/vibor_destfij.html")
    
       
                                          
@app.post('/Viewing_of_Available_Information')
def dd(request: Request,id=Form()):
    with connectionSQL.cursor() as cursor:
        connectionSQL.rollback()
        cursor.execute(f"SELECT * FROM patients WHERE id_patients = '{id}'")
        patient = cursor.fetchone()
        print(patient)
        return templates.TemplateResponse('./information_for_patient.html',
                                          {'request': request, 'id_patient': patient[0], 'familija': patient[2], 'Imja': patient[1], 'otchestfo': patient[3], 'serija_pasport': patient[4], 'nomer_passport': patient[5], 'day_roj': patient[6], 'pol': patient[7], 'id_cart': patient[10], 'polis': patient[11], 'addres': patient[12]})


@app.post('/medical_card_proverka')
async def medical_card_proverka(
    request: Request,
    anamnesis: str = Form(...),
    symptoms: str = Form(...),
    diagnosis: str = Form(...),
    recommendations: str = Form(...),
    medicine: list = Form(...),#
    dosage: list = Form(...),
    format: list = Form(...),
    referral: list = Form(...),
    investigations: str = Form(...),
    procedures: str = Form(...),
    fk_medical_cart: str = Form(...),
    code_for_hospitalization: str = Form(...),
    fk_doctor: str = Form(...),
):
    #medicine, dosage, format - НЕ ИСПОЛЬЗУЮТСЯ
    print(anamnesis,symptoms,diagnosis,recommendations,medicine,dosage,format,referral,investigations,procedures)
    with connectionSQL.cursor() as cursor:
        try:
            connectionSQL.rollback()
            cursor.execute(f"INSERT INTO medical_checkup (anamnesis, symptoms, diagnosis, recomendation_for_treatment, date_of_visit, date_of_next_visit, fk_medical_cart, code_for_hospitalization, fk_doctor) VALUES ('{anamnesis}', '{symptoms}', '{diagnosis}', '{recommendations}', '{date.today()}', '{date.today() + timedelta(days=10)}', '{fk_medical_cart}', '{code_for_hospitalization}','{fk_doctor}') RETURNING *" )        
            test = connectionSQL.commit()

        except IndexError:
            return {"ERROR":'Были введены некоректные данные'}
    status = 206
    js_code = 'alert("Данные успешно внесены в базу");'
    return templates.TemplateResponse(
        "./service_notification.html",
        {"request": request, "status": status, "js_code": js_code},
    )
   