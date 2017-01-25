from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from subprocess32 import Popen
import subprocess32
import threading
import sql_man
import time


class ConfirmationPopup(Popup):
        def __init__(self,  transaction, userid, item_id, item_name,  **kwargs):
                self.title='Buchung bestaetigen:'
                self.transaction = str(transaction)
                self.userid = int(userid)
                self.item_id = int(item_id)
                self.item_name = str(item_name)

                self.return_name_output = ''
                self.return_credit_output = ''

                confirmation_content = BoxLayout(orientation='vertical')
                confirmation_content.add_widget(Label(text='Wirklich buchen?' ))
                confirmation_content.add_widget(Label(text='[color=00ff00]%s[/color]'%self.transaction, markup=True))
                #button_ok = Button(text='O.K.', on_press=
                button_ok = Button(text='O.K.', on_press=self.on_button_ok)
                button_cancel = Button(text='Abbrechen', on_press=self.on_button_cancel)
                confirmation_content.add_widget(button_ok)
                confirmation_content.add_widget(button_cancel)
                self.content=confirmation_content

                super(ConfirmationPopup, self).__init__(**kwargs)

        def on_button_ok(self, obj):
                self.buy(self.userid, self.item_id, self.item_name)
                self.dismiss()


        def on_button_cancel(self, obj):
                self.dismiss()

        def log_transaction(self, log_string):
                f = open('speziinvest_log.txt', 'a')
                f.write(time.strftime("%d/%m/%Y") + '\t' + time.strftime("%H:%M:%S") + '\t' + str(log_string)+'\n')
                f.close()

        def buy(self, uid, item_id, item_name):
                # item: 0 kaffee
                # item: 1 spezi
                # item: 2 schorle
                # item: 3 bier
                # item: 4 mate

                if sql_man.sql_man().check(uid):
                        l=sql_man.sql_man().book(item_id,uid)
                        l[0]+=' hat 1 %s gebucht.' %(str(item_name))
                elif uid<0:
                        l=["",""]
                else:
                        l=['User not found. NFC Tag ID is %i'%uid, 0]
                self.return_name_output = str(l[0])
                self.return_credit_output = str(l[1])
                logstring = str(l[0]) + '\t' + str(l[1])
                self.log_transaction(logstring)



class MainInterface(BoxLayout):
        name_output = ObjectProperty()
        credit_output = ObjectProperty()

        def confirmation_callback(self, confirmation_popup):
                self.name_output.text = confirmation_popup.return_name_output
                self.credit_output.text = confirmation_popup.return_credit_output
        def confirmation_box(self, uid, item_id, item_name):
                if sql_man.sql_man().check(uid):
                        l=sql_man.sql_man().read(uid)
                elif uid <0:
                        l=["",""]
                else:
                        l=['User not found. NFC Tag ID is %i'%uid, 0]
                transaction_name = str(l[0]) + ': %s'%(item_name)
                confirmation_popup = ConfirmationPopup(transaction=transaction_name, userid=uid, item_id=item_id, item_name=item_name)
                confirmation_popup.bind(on_dismiss=self.confirmation_callback)
                confirmation_popup.open()



        def read_out(self):
                process = Popen(["/home/pi/speziinvest/nfc"])
                (output, err) = process.communicate()
                uid = process.poll()
                process.kill()
                if uid is None:
                        uid = -1
                else:
                        uid = int(uid)

                if sql_man.sql_man().check(uid):
                        l=sql_man.sql_man().read(uid)
                elif uid <0:
                        l=["",""]
                else:
                        l=['User not found. NFC Tag ID is %i'%uid, 0]

                self.name_output.text = str(l[0])
                self.credit_output.text = str(l[1])




        def book_kaffee(self):
                process = Popen(["/home/pi/speziinvest/nfc"])
                (output, err) = process.communicate()
                uid = -1
                uid = int(process.wait(timeout=5))

                self.confirmation_box(uid, 0, "Kaffee")


        def book_spezi(self):
                process = Popen(["/home/pi/speziinvest/nfc"])
                (output, err) = process.communicate()
                uid = -1
                uid = int(process.wait(timeout=5))

                self.confirmation_box(uid, 1, "Spezi")


        def book_schorle(self):
                process = Popen(["/home/pi/speziinvest/nfc"])
                (output, err) = process.communicate()
                uid =-1
                uid = int(process.wait(timeout=5))

                self.confirmation_box(uid, 2, "Schorle")



        def book_bier(self):
                process = Popen(["/home/pi/speziinvest/nfc"])
                (output, err) = process.communicate()
                uid=-1
                uid = int(process.wait(timeout=5))

                self.confirmation_box(uid, 3, "Bier")

        def book_mate(self):
                process = Popen(["/home/pi/speziinvest/nfc"])
                (output, err) = process.communicate()
                uid=-1
                uid = int(process.wait(timeout=5))

                self.confirmation_box(uid, 4, "Mate")


class SpeziApp(App):
	def build(self):
                return MainInterface()


if __name__ == '__main__':
	SpeziApp().run()
