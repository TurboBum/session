import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import requests
import json

# Определение классов для каждого окна
class Window1(GridLayout):
    def __init__(self, **kwargs):
        super(Window1, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="Обновить \n данные", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # Привязка метода к событию нажатия кнопки
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # Вызываем метод для получения и обновления данных
        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)
    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno1')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # Очищаем содержимое перед обновлением
        # Создаем виджет GridLayout с двумя колонками для таблицы
        grid_layout = GridLayout(cols=4, size_hint=(1, None))
        # Задаем высоту каждой строки таблицы
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        row_height = 30  # строки
        grid_layout.row_default_height = row_height
        # Добавляем виджеты Label в таблицу
        labels = [
            Label(text='Номер препарата:'),
            Label(text='Название препарата:'),
            Label(text='Статус:'),
            Label(text='Годен до:'),
        ]
        for label in labels:
            grid_layout.add_widget(label)
        # Добавляем таблицу к нужному layout'у
        self.data_layout.add_widget(grid_layout)
        for i in dict:
            if i[2]:
                true_or_false = "препарат присутствует"
            else:
                true_or_false = "препарат отсутствует"
            labels1 = [
                Label(text=f'{i[0]}'),
                Label(text=f'{i[1]}'),
                Label(text=f'{true_or_false}'),
                Label(text=f'{i[5]}')
            ]
            for label in labels1:
                grid_layout.add_widget(label)














class Window2(GridLayout):
    def __init__(self, **kwargs):
        super(Window2, self).__init__(**kwargs)
        # Устанавливаем колонки и строки в GridLayout
        self.cols = 2
        self.rows = 6

        # Добавляем виджеты Label и TextInput для каждого поля
        self.add_widget(Label(text='Название препарата:'))
        self.name_input = TextInput(multiline=False)
        self.add_widget(self.name_input)

        self.add_widget(Label(text='Имя поставщика:'))
        self.supplier_input = TextInput(multiline=False)
        self.add_widget(self.supplier_input)
        #
        self.add_widget(Label(text='Срок годности:'))
        self.expiry_date_input = TextInput(multiline=False)
        self.add_widget(self.expiry_date_input)
        #
        self.add_widget(Label(text='Номер склад:'))
        self.warehouse_input = TextInput(multiline=False)
        self.add_widget(self.warehouse_input)

        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

        button_back = Button(text="Поступить", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.update_DB)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_DB(self, instance):
        # Отправляем данные на API
        response = requests.post('http://127.0.0.1:8000/okno2', data={
            'name_preparat': self.name_input.text,
            'name_postawchik': self.supplier_input.text,
            'srok': self.expiry_date_input.text,
            'number_sklad': self.warehouse_input.text
        })
        popup_content = Label(
            text='Данные успешно отправлены на API' if response.status_code == 200 else 'Произошла ошибка при отправке данных на API'
        )
        popup = Popup(
            title='Результат',
            content=popup_content,
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()









class Window3(GridLayout):
    def __init__(self, **kwargs):
        super(Window3, self).__init__(**kwargs)
        # Устанавливаем колонки и строки в GridLayout
        self.cols = 2
        self.rows = 6

        # Добавляем виджеты Label и TextInput для каждого поля
        self.add_widget(Label(text='лекарственный препарат:'))
        self.medicinal_product = TextInput(multiline=False)
        self.add_widget(self.medicinal_product)


        self.add_widget(Label(text='Причина списания препарата:'))
        self.write_offs = TextInput(multiline=False)
        self.add_widget(self.write_offs)


        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

        button_back = Button(text="Списать", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.update_DB)
        self.add_widget(button_back)

    def switch_to_main(self, instance):
        app.switch_to_main()

    def update_DB(self, instance):
        # Отправляем данные на API
        response = requests.post('http://127.0.0.1:8000/okno3', data={
            'medicinal_product': self.medicinal_product.text,
            'write_offs': self.write_offs.text,

        })
        popup_content = Label(
            text='Данные успешно удалены' if response.status_code == 200 else 'Произошла ошибка при удалении данных'
        )
        popup = Popup(
            title='Результат',
            content=popup_content,
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

class Window4(GridLayout):
    def __init__(self, **kwargs):
        super(Window4, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="Обновить \n данные", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # Привязка метода к событию нажатия кнопки
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # Вызываем метод для получения и обновления данных
        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno4')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # Очищаем содержимое перед обновлением
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))

class Window5(GridLayout):
    def __init__(self, **kwargs):
        super(Window5, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="Обновить \n данные", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # Привязка метода к событию нажатия кнопки
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # Вызываем метод для получения и обновления данных
        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno5')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # Очищаем содержимое перед обновлением
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))

class Window6(GridLayout):
    def __init__(self, **kwargs):
        super(Window6, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="Обновить \n данные", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # Привязка метода к событию нажатия кнопки
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # Вызываем метод для получения и обновления данных
        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno6')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # Очищаем содержимое перед обновлением
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))

class Window7(GridLayout):

    def __init__(self, **kwargs):
        super(Window7, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="Обновить \n данные", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # Привязка метода к событию нажатия кнопки
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # Вызываем метод для получения и обновления данных
        button_back = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno7')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # Очищаем содержимое перед обновлением
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))


# Определение класса главного приложения
class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.window1 = Window1()
        self.window2 = Window2()
        self.window3 = Window3()
        self.window4 = Window4()
        self.window5 = Window5()
        self.window6 = Window6()
        self.window7 = Window7()

        self.current_window = None

    def build(self):
        layout = GridLayout(cols=2, padding=10, spacing=10)
        layout.add_widget(self.create_button("Окно 1", self.show_window1))
        layout.add_widget(self.create_button("Окно 2", self.show_window2))
        layout.add_widget(self.create_button("Окно 3", self.show_window3))
        layout.add_widget(self.create_button("Окно 4", self.show_window4))
        layout.add_widget(self.create_button("Окно 5", self.show_window5))
        layout.add_widget(self.create_button("Окно 6", self.show_window6))
        layout.add_widget(self.create_button("Окно 7", self.show_window7))

        scroll_view = ScrollView(size_hint=(1, 0.9), do_scroll_x=False)
        scroll_view.add_widget(layout)

        return scroll_view

    def create_button(self, text, callback):
        button = Button(text=text, size_hint=(None, None), size=(100, 50))
        button.bind(on_press=callback)
        return button

    def switch_to_main(self):
        self.current_window = None
        self.root.clear_widgets()
        self.root.add_widget(self.build())

    def show_window1(self, instance):
        self.current_window = self.window1
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

    def show_window2(self, instance):
        self.current_window = self.window2
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

    def show_window3(self, instance):
        self.current_window = self.window3
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

    def show_window4(self, instance):
        self.current_window = self.window4
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

    def show_window5(self, instance):
        self.current_window = self.window5
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

    def show_window6(self, instance):
        self.current_window = self.window6
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

    def show_window7(self, instance):
        self.current_window = self.window7
        self.root.clear_widgets()
        self.root.add_widget(self.current_window)

if __name__ == '__main__':
    app = MyApp()
    app.run()
