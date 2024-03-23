# import docx2txt

# def edit_contract(file_path, место, дата, организация, должность, фио, основание, потребитель):
#     try:
#         text = docx2txt.process(file_path)

#         text = text.replace('[место подписания договора]', место)
#         text = text.replace('[число, месяц, год]', дата)
#         text = text.replace('[Наименование медицинской организации/фамилия, имя и отчество (при наличии) индивидуального предпринимателя]', организация)
#         text = text.replace('[должность, Ф. И. О.]', f'{должность}, {фио}')
#         text = text.replace('[Устава, Положения, Доверенности]', основание)
#         text = text.replace('[фамилия, имя, отчество (при наличии)]', потребитель)

#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.write(text)

#         return True
#     except Exception as e:
#         print(f"Ошибка при редактировании договора: {e}")
#         return False
# edit_contract('./Форма_договора_предоставления_платных_медицинских_услуг1.docx', 'Омск', "0258", 'RaisQ', "Good", "Pasha J P ", 'len', 'ifi ofo afa')
Q = [4554545,4545]
print(len(Q))