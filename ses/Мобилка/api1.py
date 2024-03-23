from fastapi import FastAPI, Request, Form
import psycopg2
import uvicorn
from random import randint
from pydantic import BaseModel

app = FastAPI()
connectionSQL = psycopg2.connect(dbname="test_api", host="127.0.0.1", user="postgres", password="root", port='')


@app.get('/okno1')
def okno1():
    with connectionSQL.cursor() as cursor:
        connectionSQL.rollback()
        cursor.execute("SELECT * FROM preparat")
        cone = cursor.fetchall()
        return cone


@app.post('/okno2')
def okno2(request: Request,
          name_preparat=Form(),
          name_postawchik=Form(),
          srok=Form(),
          number_sklad=Form(),
          kol_tof_input=Form()
          ):
    with connectionSQL.cursor() as cursor:
        connectionSQL.rollback()
        cursor.execute(f"SELECT name FROM sklad WHERE name = '{number_sklad}'")
        name_sklad = cursor.fetchall()
        print(name_sklad)
        if len(name_sklad) == 0:
            cursor.execute(
                f"INSERT INTO sklad (name) VALUES ('{number_sklad}') RETURNING *")
            sklad = cursor.fetchone()
            print(1)
        else:
            cursor.execute(f"SELECT id FROM sklad WHERE  name = '{number_sklad}'")
            sklad = cursor.fetchall()
            sklad = sklad[0]
            print(2)
        print(sklad)
        print(sklad[0])
        print("---------------------------------------------")

        cursor.execute(f"SELECT name FROM postawchik WHERE name = '{name_postawchik}'")
        postawchik = cursor.fetchall()
        print(postawchik)
        if len(postawchik) == 0:
            cursor.execute(
                f"INSERT INTO postawchik (name) VALUES ('{name_postawchik}') RETURNING *")
            postaw = cursor.fetchone()
            postaw = postaw[0]
            print(1)
            print(postaw)
        else:
            cursor.execute(f"SELECT id FROM postawchik WHERE  name = '{name_postawchik}'")
            postaw = cursor.fetchone()
            postaw = postaw[0]
            print(2)
            print(postaw)

        cursor.execute(
            f"INSERT INTO preparat (name, est_net, nomer_sklada, cod_postafchika, srok_godnosti, kol_wo) VALUES ('{name_preparat}', 'true', '{sklad[0]}', '{postaw}', '{srok}', '{kol_tof_input}')")
        connectionSQL.commit()
    return {200}


@app.post('/okno3')
def okno3(request: Request,
          medicinal_product=Form(),
          write_offs=Form(),
          ):
    with connectionSQL.cursor() as cursor:
        connectionSQL.rollback()
        cursor.execute(f"SELECT id FROM preparat WHERE name = '{medicinal_product}'")
        id_preparat = cursor.fetchall()
        if len(id_preparat) != 0:
            print(id_preparat)
            print(id_preparat[0])
            print(id_preparat[0][0])
            cursor.execute(f"DELETE FROM preparat WHERE id = '{id_preparat[0][0]}'")
            connectionSQL.commit()

    return {200}


@app.get('/okno4')
def okno4():
    with connectionSQL.cursor() as cursor:
        connectionSQL.rollback()
        cursor.execute("SELECT id, name, kol_wo FROM preparat")
        cone = cursor.fetchall()
        return cone


# Маршрут POST для обработки отправки данных
# Модель данных для вложенного списка
class DataItem(BaseModel):
    id: int
    decrease_value: int


@app.post('/send_data4')
def send_data4(request: Request, data_to_send: list[DataItem]):
    try:
        with connectionSQL.cursor() as cursor:
            connectionSQL.rollback()
            for item in data_to_send:
                id = item.id
                decrease_value = item.decrease_value
                query = f"UPDATE preparat SET kol_wo = kol_wo - {decrease_value} WHERE id = {id}"
                cursor.execute(query)
        connectionSQL.commit()
        data_to_send.clear()
        return {"message": "Данные успешно обновлены"}
    except Exception as e:
        connectionSQL.rollback()
        return {"message": f"Произошла ошибка при обновлении данных: {str(e)}"}


@app.get('/okno5')
def okno5():
    id = 'id'
    return {id: randint(1, 999999999), 'srt1': "doctor"}


@app.get('/okno6')
def okno6():
    id = 'id'
    return {id: randint(1, 999999999), 'srt1': "doctor"}


@app.get('/okno7')
def okno7():
    id = 'id'
    return {id: randint(1, 9999999), 'srt1': "doctor"}


if __name__ == "__main__":
    uvicorn.run("api1:app", reload=True)
