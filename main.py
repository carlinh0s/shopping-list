from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from operator import itemgetter
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget, IconLeftWidgetWithoutTouch, IconLeftWidget
from database import DatabaseManager

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Indigo"
        self.lista_list_dialog = None
        self.items = []
        self.item_states = {}
        self.sort_direction = "ascendente"
        self.db_manager = DatabaseManager('items.db')

    def load_items(self):
        self.items = self.db_manager.get_items()
        self.item_states = self.db_manager.get_item_states()
        self.show_list()

    def on_start(self):
        self.load_items()

    def sort_list(self, key):
        if key == "Nome":
            self.items = sorted(self.items, key=itemgetter(0), reverse=self.sort_direction=="descendente")
        elif key == "Valor":
            self.items = sorted(self.items, key=itemgetter(1), reverse=self.sort_direction=="descendente")
        elif key == "Quantidade":
            self.items = sorted(self.items, key=itemgetter(2), reverse=self.sort_direction=="descendente")
        self.show_list()
        self.sort_direction = "descendente" if self.sort_direction=="ascendente" else "ascendente"

    def show_lista_dialog(self):
        if not self.lista_list_dialog:
            self.lista_list_dialog = MDDialog(
                title="[color=808080]Adicionar itens à lista.[/color]", type="custom", content_cls=DialogContent()
            )
        self.lista_list_dialog.open()

    def close_dialog(self, *args):
        self.lista_list_dialog.dismiss()

    def add_list(self):
        item_name_field = self.lista_list_dialog.content_cls.ids.item_name
        item_value_field = self.lista_list_dialog.content_cls.ids.item_value
        item_quantity_field = self.lista_list_dialog.content_cls.ids.item_quantity
        item_name = item_name_field.text if item_name_field else ""
        item_value = item_value_field.text if item_value_field else ""
        item_quantity = item_quantity_field.text if item_quantity_field else ""

        if not item_name or not item_value or not item_quantity:
            error_dialog = MDDialog(
                title=f"[b]Erro[/b]",
                text="Por favor, preencha todos os campos antes de adicionar um item.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: error_dialog.dismiss()
                    )
                ]
            )
            error_dialog.open()
            return
        item = (item_name, float(item_value), int(item_quantity))
        self.items.append(item)
        self.db_manager.add_item(item)
        self.item_states[item_name] = False
        self.db_manager.update_item_state(item_name, False)
        self.show_list()
        item_name_field.text = ""
        item_value_field.text = ""
        item_quantity_field.text = ""

    def calcular_total(self):
        valor_total = sum(item[1] * item[2] for item in self.items)
        self.total_widget.text = f"VALOR TOTAL: R$ {valor_total:.2f}"

    def show_list(self):
        self.root.ids["container"].clear_widgets()
        theme_text_color = "Primary" if self.theme_cls.theme_style == "Light" else "Secondary"
        for item in self.items:
            list_text = f"{item[0]:<10} R$ {item[1]:<24.2f} {item[2]:<1}x"
            list_item = ListItemWithCheckbox(text=list_text, checked=self.item_states.get(item[0], False), theme_text_color=theme_text_color)
            trash_icon = IconRightWidget(icon="trash-can-outline", theme_text_color="Custom", text_color=(1, 0, 0, 1))
            trash_icon.bind(on_release=lambda x, li=list_item: self.delete_item(li))
            list_item.add_widget(trash_icon)
            self.root.ids["container"].add_widget(list_item)
        self.total_widget = OneLineAvatarIconListItem(text="", theme_text_color=theme_text_color)
        total_icon = IconLeftWidgetWithoutTouch(icon="equal")
        self.total_widget.add_widget(total_icon)
        self.root.ids["container"].add_widget(self.total_widget)
        self.calcular_total()

    def delete_item(self, list_item):
        item_name = list_item.text.split()[0]
        for idx, item in enumerate(self.items):
            if item[0] == item_name:
                self.items.pop(idx)
                self.root.ids.container.remove_widget(list_item)
                self.db_manager.delete_item(item)
                break
        if item_name in self.item_states:
            del self.item_states[item_name]
            self.db_manager.delete_item_state(item_name)
        self.calcular_total()

    def switch_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
        self.show_list()

class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ListItemWithCheckbox(OneLineAvatarIconListItem):

    def __init__(self, **kwargs):
        self.checked = kwargs.pop("checked", False)
        super().__init__(**kwargs)
        self.icon_left = IconLeftWidget(icon='checkbox-outline' if self.checked else 'checkbox-blank-outline')
        self.icon_left.bind(on_release=self.toggle_checkbox)
        self.add_widget(self.icon_left)

    def toggle_checkbox(self, *args):
        self.checked = not self.checked
        self.icon_left.icon = 'checkbox-outline' if self.checked else 'checkbox-blank-outline'
        app = MDApp.get_running_app()
        item_name = self.text.split()[0]
        app.item_states[item_name] = self.checked
        app.db_manager.update_item_state(item_name, self.checked)

if __name__ == "__main__":
    MainApp().run()
