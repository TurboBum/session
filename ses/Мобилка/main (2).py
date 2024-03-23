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

# ??????????? ??????? ??? ??????? ????
class Window1(GridLayout):
    def __init__(self, **kwargs):
        super(Window1, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="???????? \n ??????", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # ???????? ?????? ? ??????? ??????? ??????
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # ???????? ????? ??? ????????? ? ?????????? ??????
        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)
    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno1')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # ??????? ?????????? ????? ???????????
        # ??????? ?????? GridLayout ? ????? ????????? ??? ???????
        grid_layout = GridLayout(cols=4, size_hint=(1, None))
        # ?????? ?????? ?????? ?????? ???????
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        row_height = 30  # ??????
        grid_layout.row_default_height = row_height
        # ????????? ??????? Label ? ???????
        labels = [
            Label(text='????? ?????????:'),
            Label(text='???????? ?????????:'),
            Label(text='??????:'),
            Label(text='????? ??:')]
        for label in labels:
            grid_layout.add_widget(label)
        # ????????? ??????? ? ??????? layout'?
        self.data_layout.add_widget(grid_layout)
        for i in dict:
            if i[2]:
                true_or_false = "???????? ????????????"
            else:
                true_or_false = "???????? ???????????"
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
        # ????????????? ??????? ? ?????? ? GridLayout
        self.cols = 2
        self.rows = 6

        # ????????? ??????? Label ? TextInput ??? ??????? ????
        self.add_widget(Label(text='???????? ?????????:'))
        self.name_input = TextInput(multiline=False)
        self.add_widget(self.name_input)

        self.add_widget(Label(text='??? ??????????:'))
        self.supplier_input = TextInput(multiline=False)
        self.add_widget(self.supplier_input)
        #
        self.add_widget(Label(text='???? ????????:'))
        self.expiry_date_input = TextInput(multiline=False)
        self.add_widget(self.expiry_date_input)
        #
        self.add_widget(Label(text='????? ?????:'))
        self.warehouse_input = TextInput(multiline=False)
        self.add_widget(self.warehouse_input)

        self.add_widget(Label(text='???-?? ??????:'))
        self.kol_tof_input = TextInput(multiline=False)
        self.add_widget(self.kol_tof_input)

        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

        button_back = Button(text="?????????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.update_DB)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_DB(self, instance):
        # ?????????? ?????? ?? API
        response = requests.post('http://127.0.0.1:8000/okno2', data={
            'name_preparat': self.name_input.text,
            'name_postawchik': self.supplier_input.text,
            'srok': self.expiry_date_input.text,
            'number_sklad': self.warehouse_input.text,
            'kol_tof_input': self.kol_tof_input.text
        })
        popup_content = Label(
            text='?????? ??????? ?????????? ?? API' if response.status_code == 200 else '????????? ?????? ??? ???????? ?????? ?? API'
        )
        popup = Popup(
            title='?????????',
            content=popup_content,
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
class Window3(GridLayout):
    def __init__(self, **kwargs):
        super(Window3, self).__init__(**kwargs)
        # ????????????? ??????? ? ?????? ? GridLayout
        self.cols = 2
        self.rows = 6

        # ????????? ??????? Label ? TextInput ??? ??????? ????
        self.add_widget(Label(text='????????????? ????????:'))
        self.medicinal_product = TextInput(multiline=False)
        self.add_widget(self.medicinal_product)


        self.add_widget(Label(text='??????? ???????? ?????????:'))
        self.write_offs = TextInput(multiline=False)
        self.add_widget(self.write_offs)


        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

        button_back = Button(text="???????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.update_DB)
        self.add_widget(button_back)

    def switch_to_main(self, instance):
        app.switch_to_main()

    def update_DB(self, instance):
        # ?????????? ?????? ?? API
        response = requests.post('http://127.0.0.1:8000/okno3', data={
            'medicinal_product': self.medicinal_product.text,
            'write_offs': self.write_offs.text,

        })
        popup_content = Label(
            text='?????? ??????? ???????' if response.status_code == 200 else '????????? ?????? ??? ???????? ??????'
        )
        popup = Popup(
            title='?????????',
            content=popup_content,
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()




class Window4(GridLayout):
    def __init__(self, **kwargs):
        super(Window4, self).__init__(**kwargs)
        self.cols = 1

        self.data_list = []

        self.update_back = Button(text="???????? ??????", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)
        self.add_widget(self.update_back)

        self.data_layout = GridLayout(cols=2, spacing=10)
        self.add_widget(self.data_layout)

        self.update_data()

        button_send = Button(text="?????????", size_hint=(None, None), size=(100, 50))
        button_send.bind(on_press=self.send_data)
        self.add_widget(button_send)

        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

    def switch_to_main(self, instance):
        app.switch_to_main()

    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno4')
        data = r.json()

        self.data_layout.clear_widgets()
        self.data_list = []
        for item in data:
            id = item[0]
            name = item[1]
            key = item[2]
            self.g_key = key
            label = Label(text=f'id{id}: ????????-{name}, ???-??({key}):', size_hint=(None, None), size=(300, 40))
            self.data_layout.add_widget(label)

            text_input = TextInput(text='', multiline=False, size_hint=(None, None), size=(300, 30))
            self.data_layout.add_widget(text_input)

            self.data_list.append([id, text_input])

    def send_data(self, instance):
        data_to_send = []
        for item in self.data_list:
            id = item[0]
            try:
                value = int(item[1].text)
                print(value)
                print(type(value))
                if value <= self.g_key:
                    data_to_send.append({"id": id, "decrease_value": value})
                else:
                    popup_content = Label(
                        text='???????? ?? ????????? '
                    )
                    popup = Popup(
                        title='??????',
                        content=popup_content,
                        size_hint=(None, None),
                        size=(400, 200)
                    )
                    popup.open()
                    return

            except:
                pass

        print(data_to_send)

        response = requests.post('http://127.0.0.1:8000/send_data4', json=data_to_send)
        # self.data_list.clear()

        if response.status_code == 200:
            print('?????? ??????? ?????????? ?? API')
        else:
            print('????????? ?????? ??? ???????? ?????? ?? API')


class Window5(GridLayout):
    def __init__(self, **kwargs):
        super(Window5, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="???????? \n ??????", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # ???????? ?????? ? ??????? ??????? ??????
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # ???????? ????? ??? ????????? ? ?????????? ??????
        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)

    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno5')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # ??????? ?????????? ????? ???????????
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))








class Window6(GridLayout):
    def __init__(self, **kwargs):
        super(Window6, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="???????? \n ??????", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # ???????? ?????? ? ??????? ??????? ??????
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # ???????? ????? ??? ????????? ? ?????????? ??????
        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno6')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # ??????? ?????????? ????? ???????????
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))

class Window7(GridLayout):

    def __init__(self, **kwargs):
        super(Window7, self).__init__(**kwargs)
        self.cols = 1
        self.update_back = Button(text="???????? \n ??????", size_hint=(None, None), size=(100, 50))
        self.update_back.bind(on_press=self.update_data)  # ???????? ?????? ? ??????? ??????? ??????
        self.add_widget(self.update_back)
        self.data_layout = GridLayout(cols=1)
        self.add_widget(self.data_layout)
        self.update_data()  # ???????? ????? ??? ????????? ? ?????????? ??????
        button_back = Button(text="?????", size_hint=(None, None), size=(100, 50))
        button_back.bind(on_press=self.switch_to_main)
        self.add_widget(button_back)


    def switch_to_main(self, instance):
        app.switch_to_main()
    def update_data(self, *args):
        r = requests.get('http://127.0.0.1:8000/okno7')
        dict = json.loads(r.text)
        self.data_layout.clear_widgets()  # ??????? ?????????? ????? ???????????
        for i in dict:
            self.data_layout.add_widget(Label(text=f'{i} - {dict[i]}', size_hint=(1, 0.1)))


# ??????????? ?????? ???????? ??????????
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
        layout.add_widget(self.create_button("???? 1", self.show_window1))
        layout.add_widget(self.create_button("???? 2", self.show_window2))
        layout.add_widget(self.create_button("???? 3", self.show_window3))
        layout.add_widget(self.create_button("???? 4", self.show_window4))
        layout.add_widget(self.create_button("???? 5", self.show_window5))
        layout.add_widget(self.create_button("???? 6", self.show_window6))
        layout.add_widget(self.create_button("???? 7", self.show_window7))

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
