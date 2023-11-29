# coding: utf-8
# import time
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import calculator

sys_function = calculator.SysFuntion()


def updata(_):
    if sys_function.get:
        sys_function.get = False
        sys_function.function(sys_function.args)



def massagebox(err, title='error'):
    content = BoxLayout(orientation='vertical')
    size1, size2 = Window.size
    dialog = Popup(title=title, content=content, size_hint=(None, None), size=(size1 / 1.2, size2 / 2))
    title_input = Label(text=str(err))
    submit_button = Button(text='确认',
                           on_release=dialog.dismiss)
    content.add_widget(title_input)
    content.add_widget(submit_button)
    dialog.open()


class DialogApp(App):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.dialog = None
        self.top_section = None
        self.title_input = None
        self.threas = None
        self.needs = {}
        self.translations = None
        self.buttons = None

    def lop_calculator(self, _):
        content = BoxLayout(orientation='vertical')
        size1, size2 = Window.size
        self.title_input = TextInput(text='正在计算')

        # print(size1,size2)
        content.add_widget(self.title_input)
        self.dialog = Popup(title='结果', content=content, size_hint=(None, None), size=(size1, size2))

        self.top_section = BoxLayout(orientation='horizontal', size_hint_y=None, height=size2 / 10)

        content.add_widget(self.top_section)
        self.clock = Clock.schedule_interval(updata, 0.01)
        t = Thread(target=self.calculator)
        t.start()
        self.dialog.open()

    def endlist(self, strs):
        self.title_input.text = strs
        submit_button = Button(text='确认',
                               on_release=self.dialog.dismiss)
        self.top_section.add_widget(submit_button)
        self.clock.cancel()

    def show(self, strs):
        self.title_input.text = strs

    def calculator(self):
        sys_function.function = self.show
        strs = calculator.main(self.needs, sys_function)
        sys_function.get = True
        sys_function.function = self.endlist
        sys_function.args = strs
        # print(strs)

    def clear(self, _):
        for i in range(1, len(calculator.de_dirc_list) - 2):
            button1 = self.buttons[i - 1][2]
            button1.text = self.buttons[i - 1][1]
        self.needs = {}

    def get_need(self, _):
        strs = ''
        for i in self.needs:
            strs += i + '\n' + str(self.needs[i]) + '\n'
        Clipboard.copy(strs)

    def lop_need(self, _):
        strs = Clipboard.paste()
        # print(strs)
        try:
            be = 0
            name = None
            for i in range(len(strs)):
                if strs[i] == '\n':
                    # print(name)
                    if name is not None:
                        for j in self.buttons:
                            # print(j[1][:-1])
                            if j[1][:-1] == name:
                                f = int(strs[be:i])
                                self.needs[name] = f
                                j[2].text = name + strs[be:i]
                                name = None
                                be = i + 1
                                break
                    else:
                        name = strs[be:i]
                        be = i + 1
            if name is not None:
                for j in self.buttons:
                    # print(j[1][:-1])
                    if j[1][:-1] == name:
                        f = int(strs[be:])
                        self.needs[name] = f
                        j[2].text = name + strs[be:]
                        break

        except (ValueError, KeyError):
            print(ValueError, KeyError)

    def build(self):
        # Create the main layout as a vertical BoxLayout
        # self.translations = gettext.translation('dialog_app', localedir='locales', languages=['zh_CN'], fallback=True)
        # self.translations.install()
        _, size2 = Window.size
        self.needs = {}
        main_layout = BoxLayout(orientation='vertical')

        top_section = BoxLayout(size_hint_y=None, height=size2 / 5)
        top_button = Button(text="计算")
        top_button.bind(on_release=self.lop_calculator)
        top_section.add_widget(top_button)

        top_button2 = Button(text="清除")
        top_button2.bind(on_release=self.clear)
        top_section.add_widget(top_button2)

        top_button3 = Button(text="退出")
        top_button3.bind(on_release=self.stop)
        top_section.add_widget(top_button3)

        top_section2 = BoxLayout(size_hint_y=None, height=size2 / 10)
        top_button2 = Button(text="导出到粘贴板")
        top_button2.bind(on_release=self.get_need)
        top_section2.add_widget(top_button2)

        top_button3 = Button(text="从粘贴板导入")
        top_button3.bind(on_release=self.lop_need)
        top_section2.add_widget(top_button3)

        bottom_section = GridLayout(cols=2)

        self.buttons = []

        for i in range(1, len(calculator.de_dirc_list) - 2):
            text = calculator.de_dirc_list[len(calculator.de_dirc_list) - 2 - i] + ':'
            button = Button(text=text)
            button.bind(on_release=lambda instance, num=i: self.open_dialog(num, self.submit_dialog))
            bottom_section.add_widget(button)
            self.buttons.append((i, text, button))

        top_section3 = BoxLayout(size_hint_y=None, height=size2 / 10)
        top_button3 = Button(text="价体比限制" + str(calculator.sets.value_type))
        i = len(calculator.de_dirc_list) - 2
        top_button3.bind(on_release=lambda instance, num=i: self.open_dialog(num, self.submit_dialog_float))
        self.buttons.append((i, "价体比限制", top_button3))
        top_section3.add_widget(top_button3)

        top_button4 = Button(text="计算复杂度" + str(calculator.sets.difficult))
        i = len(calculator.de_dirc_list) - 1
        top_button4.bind(on_release=lambda instance, num=i: self.open_dialog(num, self.submit_dialog_3))
        self.buttons.append((i, "计算复杂度", top_button4))
        top_section3.add_widget(top_button4)

        main_layout.add_widget(top_section)
        main_layout.add_widget(top_section2)
        main_layout.add_widget(top_section3)
        main_layout.add_widget(bottom_section)

        return main_layout

    def open_dialog(self, dialog_num, call_function):
        dialog_info = self.buttons[dialog_num - 1][1]
        content = BoxLayout(orientation='vertical')
        size1, size2 = Window.size
        # print(size1,size2)
        dialog = Popup(title=dialog_info, content=content, size_hint=(None, None), size=(size1 / 1.2, size2 / 2))

        title_input = TextInput()
        submit_button = Button(text='确认',
                               on_release=lambda instance: call_function(dialog_num, title_input.text, dialog))

        content.add_widget(title_input)
        content.add_widget(submit_button)

        dialog.open()

    def submit_dialog_float(self, dialog_num, f, dialog):
        try:
            sums = float(f)
        except ValueError:
            dialog.dismiss()
            massagebox('请输入浮点数或整数！')
            return
        calculator.sets.value_type = sums
        button1 = self.buttons[dialog_num - 1][2]
        button1.text = self.buttons[dialog_num - 1][1] + f
        dialog.dismiss()

    def submit_dialog(self, dialog_num, f, dialog):
        try:
            sums = int(f)
        except ValueError:
            dialog.dismiss()
            return
        key = calculator.de_dirc_list[len(calculator.de_dirc_list) - 2 - dialog_num]
        self.needs[key] = sums
        button1 = self.buttons[dialog_num - 1][2]
        button1.text = self.buttons[dialog_num - 1][1] + f
        dialog.dismiss()

    def submit_dialog_3(self, dialog_num, f, dialog):
        try:
            sums = int(f)
            if sums != 1 and sums != 2 and sums != 3:
                raise ValueError
        except ValueError:
            massagebox('请输入1/2/3\n其中1代表最低精确，2代表中等精确\n3代表最精确')
            dialog.dismiss()
            return
        calculator.sets.difficult = sums
        button1 = self.buttons[dialog_num - 1][2]
        button1.text = self.buttons[dialog_num - 1][1] + f
        dialog.dismiss()


if __name__ == '__main__':
    DialogApp().run()
