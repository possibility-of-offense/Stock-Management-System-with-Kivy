import kivy
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.lang import Builder

Window.clearcolor = get_color_from_hex('#03A9F4')
Window.size = (1000, 650)

# Simple Product class
class Product:
    def __init__(self, name, qnt):
        self.name = name
        self.qnt = qnt


class Management_System(GridLayout, Widget):
    # Define Object Properties for linking with the widgets in the KV file (text input fields)
    whole_grain_flour_price_value = ObjectProperty('')
    whole_grain_flour_qnt_value = ObjectProperty('')
    rice_price_value = ObjectProperty('')
    rice_qnt_value = ObjectProperty('')
    pinto_beans_price_value = ObjectProperty('')
    pinto_beans_qnt_value = ObjectProperty('')
    red_lentils_price_value = ObjectProperty('')
    red_lentils_qnt_value = ObjectProperty('')

    # Define Object Properties for linking with the widgets in the KV file (label outputs for product quantities)
    whole_grain_flour_quantity_output = ObjectProperty(None)
    rice_quantity_output = ObjectProperty(None)
    pinto_beans_quantity_output = ObjectProperty(None)
    red_lentils_quantity_output = ObjectProperty(None)

    output_label_id = ObjectProperty(None)

    show_temp_products_switch = ObjectProperty(None)
    temp_products_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        '''
            Constructor function calling the __init__ method from the class it is inheriting
        '''
        super(Management_System, self).__init__(**kwargs)

    # Products Dictionary with products like objects of Product class
    products = {
        'whole-grain-flour': Product('whole grain flour', 30),
        'rice': Product('rice', 15),
        'pinto-beans': Product('pinto beans', 55),
        'red-lentils': Product('red lentils', 7),
    }

    # Temp products dictionary and missing input fields values list
    temp_products = {}
    missing_input_fields = list()

    # Available Sum
    available_sum = NumericProperty(400)

    # Boolean property to check if the button for adding/removing has been clicked
    being_added_or_removed_from_stock = BooleanProperty(False)

    # 
    # METHODS
    # 

    # HELPER METHODS
    def change_the_output_label_size_and_color(self, size, color):
        '''
            Change the output label size and color

            @params:
                size
                color
        '''
        self.output_label_id.color = get_color_from_hex(color)
        self.output_label_id.font_size = size
    

    def get_product_qnt_by_key(self, key):
        '''
            Retrieve quantity via dictionary key

            @params:
                key
            @return:
                product in the products dictionary
        '''
        return self.products[key].qnt


    def check_for_missing_prop_and_update_total(self, items, type_of_operation):
        '''
            Check if price and quantity is missing:
            if they are available
                create or update total prop
            else if one of them is missing
                update the output label

            @params:
                items - some dictionary with items; e.g. self.products/self.temp_products
                type_of_operation - 'add', 'remove', etc.
            @helper-functions:

        '''
        for key, val in items.items():
            if len(list(val.items())) == 1:
                get_prop = list(val.items())[0]
                original_key = key.replace('-', '_')
                key = key.replace('-', ' ')

                list_dict = list(self.ids.items())

                if get_prop[0] == 'price':
                    self.output_label_id.text = f'The quantity for {key} is missing!'

                    for ind in range(len(list_dict)):
                        if f'{original_key}_price_value' in list_dict[ind][0]:
                            list_dict[ind + 1][1].background_color = (1, 0, 0, 1)
                            self.missing_input_fields.append(list_dict[ind + 1])
                            break
                else:
                    self.output_label_id.text = f'The price for {key} is missing!'

                    for ind in range(len(list_dict)):
                        if f'{original_key}_qnt_value' in list_dict[ind][0]:
                            list_dict[ind - 1][1].background_color = (1, 0, 0, 1)
                            self.missing_input_fields.append(list_dict[ind - 1])
                            break

                self.change_the_output_label_size_and_color('20sp', '#ff051a')
            else:
                if type_of_operation == 'add':
                    self.temp_products[key].update({
                        'total': self.products[key].qnt + int(val['qnt'])
                    })
                else:
                    if val['qnt']:
                        temp_val = self.products[key].qnt - int(val['qnt'])

                    if temp_val <= 0:
                        self.being_added_or_removed_from_stock = False
                        self.check_for_certain_word(key)
                        self.output_label_id.text = 'You cannot remove more than you have! Try again!'
                        self.change_the_output_label_size_and_color('20sp', '#ff051a')
                    else:
                        self.temp_products[key].update({
                            'total': self.products[key].qnt - int(val['qnt'])
                        })


    def check_for_certain_word(self, word):
        '''
            Check if a certain word exists in the self.ids dictionary
            If it exists and there is no `output` in the word, clear the text input field

            @params:
                word
        '''
        word = word.replace('-', '_')
        for key, val in self.ids.items():
            if word in key and 'output' not in key:
                val.text = ''

    
    def update_output_field_by_existing_key(self, key):
        '''
            Update output input field by checking if the key exists in the id name

            @params:
                key
        '''
        # Replace the `-` with `_` to match the output label id
        original_key = key
        modified_key = key.replace('-', '_')

        if modified_key in 'whole_grain_flour_quantity_output':
            self.whole_grain_flour_quantity_output.text = str(self.products[original_key].qnt)
        elif modified_key in 'rice_quantity_output':
            self.rice_quantity_output.text = str(self.products[original_key].qnt)
        elif modified_key in 'pinto_beans_quantity_output':
            self.pinto_beans_quantity_output.text = str(self.products[original_key].qnt)
        elif modified_key in 'red_lentils_quantity_output':
            self.red_lentils_quantity_output.text = str(self.products[original_key].qnt)

    
    def check_if_available_sum_is_positive(self, sum):
        '''
            Check if the available sum is positive

            @params:
                sum - temporal sum
        '''
        if sum <= 0: 
            Factory.CustomAlertPopup().open()
                
            self.output_label_id.text = 'Not enough money'
            self.change_the_output_label_size_and_color('20sp', '#ff051a')
            return False


    # MAIN METHODS
    def handle_operation_click(self, type_of_operation, items = {}):
        '''
            Handle button click

            @params:
                type_of_operation - 'add', 'remove', etc.
                items - some dictionary with items; e.g. self.products/self.temp_products
            @return:

            @helper-functions:
                check_for_certain_word
                check_for_missing_prop_and_update_total
                update_output_field_by_existing_key
        '''

        self.output_label_id.text = ''

        for field in self.missing_input_fields:
            field[1].background_color = (1, 1, 1, 1)

        if type_of_operation == 'add':
            self.check_for_missing_prop_and_update_total(items, type_of_operation)
            self.being_added_or_removed_from_stock = True
        elif type_of_operation == 'subtr':
            self.check_for_missing_prop_and_update_total(items, type_of_operation)   
            self.being_added_or_removed_from_stock = True
        elif type_of_operation == 'clear':
            self.whole_grain_flour_price_value = ''

            for key, val in self.temp_products.items():
                self.check_for_certain_word(key)

            self.temp_products = {}
            self.being_added_or_removed_from_stock = False
        elif type_of_operation == 'finalize':
            if self.being_added_or_removed_from_stock is True:
                for key, val in self.temp_products.items():
                    if 'total' in val:
                        val_to_subtr = int(val['qnt']) * int(val['price'])
                        subtr_from_available = self.available_sum - val_to_subtr

                        if self.check_if_available_sum_is_positive(subtr_from_available) is not False:
                            self.available_sum -= val_to_subtr
                            self.products[key].qnt = int(val['total'])
                            self.update_output_field_by_existing_key(key)
            else:
                # self.output_label = 'You should add or remove something before finalizing the order!'
                self.output_label_id.text = 'You should add or remove something before finalizing the order!'
                self.change_the_output_label_size_and_color('20sp', '#ff051a')

            self.being_added_or_removed_from_stock = False
            for key, val in self.temp_products.items():
                self.check_for_certain_word(key)

            self.temp_products = {}

    # Function when text is being changed

    def handle_text_changing(self, inst, val, item, prop):
        '''
            Function to trigger when the text input text is being updated

            @params:
                inst - instance
                val - value of the text input
                item - the item for which the text input is referring to
                prop - 'price' or 'qnt'
        '''
        if item not in self.temp_products:
            self.temp_products[item] = {
                prop: val
            }
        else:
            self.temp_products[item].update({prop: val})


    def handle_show_temp_products(self, inst):
        # I know it does not make sense :D
        if inst.active is False:
            temp_out = list()

            if len(self.temp_products.items()):
                for key, val in self.temp_products.items():
                    if 'qnt' in val and 'price' in val:
                        qnt = val['qnt']
                        temp_out.append(f'{key} -> quantity: {qnt}')
                    
                    self.temp_products_input.text = ' || '.join(temp_out)
            else:
                self.temp_products_input.text = 'No products to order yet!'
        else:
            if len(self.temp_products.items()):
                self.temp_products_input.text = ''
            else:
                self.temp_products_input.text = 'No products to order yet!'


class MainApp(App):
    def close_window(self):
        Window.close()


    def build(self):
        manage = Management_System()
        return manage

if __name__ == '__main__':
    MainApp().run()