from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from operator import itemgetter
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget, IconLeftWidgetWithoutTouch
from database import DatabaseManager

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Indigo"
        self.lista_list_dialog = None
        self.items = []
        self.sort_direction = "ascendente"
        self.db_manager = DatabaseManager('items.db')
        
    def load_items(self):
        self.items = self.db_manager.get_items()
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
                title="Adicionar itens à lista.", type="custom", content_cls=DialogContent()
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
        self.show_list()

    def calcular_total(self):
        valor_total = sum(item[1] * item[2] for item in self.items)
        self.total_widget.text = f"[b]VALOR TOTAL: R$ {valor_total:.2f}[/b]"

    def show_list(self):
        self.root.ids["container"].clear_widgets()
        for item in self.items:
            list_text = f"{item[0]}    R$ {item[1]:.2f}    {item[2]}x"
            list_item = OneLineAvatarIconListItem(text=list_text)
            trash_icon = IconRightWidget(icon="trash-can-outline", theme_text_color="Custom", text_color=(1, 0, 0, 1))
            trash_icon.bind(on_release=lambda x, li=list_item: self.delete_item(li))
            list_item.add_widget(trash_icon)
            self.root.ids["container"].add_widget(list_item)
        self.total_widget = OneLineAvatarIconListItem(text="")
        total_icon = IconLeftWidgetWithoutTouch(icon="equal")
        self.total_widget.add_widget(total_icon)
        self.root.ids["container"].add_widget(self.total_widget)
        self.calcular_total()

    def delete_item(self, list_item):
        for idx, item in enumerate(self.items):
            if item[0] == list_item.text.split()[0]:
                self.items.pop(idx)
                self.root.ids.container.remove_widget(list_item)
                self.db_manager.delete_item(item)
                break
        self.calcular_total()

    def switch_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    MainApp().run()
