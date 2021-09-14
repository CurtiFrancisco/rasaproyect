# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#
#
import requests

class ActionRecibirNombre(Action):
#
     def name(self) -> Text:
         return "action_recibir_nombre"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         cliente = next(tracker.get_latest_entity_values("cliente"), None)
         message = "Perfecto, me acordare de tu nombre. "  
         dispatcher.utter_message(text=str(message))

         return [SlotSet("name", str(cliente))]


class ActionDecirNombre(Action):
#
     def name(self) -> Text:
         return "action_decir_nombre"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
         name = tracker.get_slot("name") 
         dispatcher.utter_message(text="Tu nombre es: " + str(name))

         return []

class ActionDespedidaNombre(Action):
#
     def name(self) -> Text:
         return "action_despedida_nombre"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
         name = tracker.get_slot("name") 
         dispatcher.utter_message(text="Nos vemos " + str(name) + "!")

         return []         

class ActionVerificarCliente(Action):
#
     def name(self) -> Text:
         return "action_verificar_cliente"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         name = tracker.get_slot("name")
         if (str(name) != str(None)):  
            with open('C:/Users/Tobias Romano/Desktop/Rasa/clientes.txt') as f_obj:  
                if (f_obj.read().find(str(name)) != -1):
                    message = str(name) + " quiza te equivocaste, ya eres cliente."
                else:
                    with open('C:/Users/Tobias Romano/Desktop/Rasa/clientes.txt', "a+") as f_obj:
                        f_obj.seek(0)
                        data = f_obj.read(100)
                        if len(data) > 0 :
                            f_obj.write("\n")
                        f_obj.write(str(name))    
                    message = "Perfecto, " + str(name) + " ya te agregamos como cliente del banco, bienvenido!"   
         else:
             message = "Aun no nos has dicho tu nombre!"  
         dispatcher.utter_message(text= str(message))             
         return []

class ActionInformacionTarjeta(Action):
#
     def name(self) -> Text:
         return "action_informacion_tarjeta"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         tarjeta = next(tracker.get_latest_entity_values("tipo_tarjeta"), None)
         SlotSet("tipo_tarjeta", str(tarjeta))
         if (str(tarjeta) == "DEBITO"):
             dispatcher.utter_message(text="Para solicitar una tarjeta de debito primero debes cumplir los siguientes requisitos: ")
             dispatcher.utter_message(text="• Ser cliente del banco.")
             dispatcher.utter_message(text="• Ser mayor de 18 años")
             dispatcher.utter_message(text="Una vez hecho eso podes solicitar tu tarjeta de debito, podes solicitar con las siguientes caracteristicas: ")
             dispatcher.utter_message(text="• Caja de ahorro en pesos y en dolares")
             dispatcher.utter_message(text="• Compras internacionales")
         else:
             dispatcher.utter_message(text="Para solicitar una tarjeta de credito primero debes cumplir los siguientes requisitos: ")
             dispatcher.utter_message(text="• Ser cliente del banco.")
             dispatcher.utter_message(text="• Ser mayor de 21 años")
             dispatcher.utter_message(text="Una vez hecho eso podes solicitar tu tarjeta de credito, podes solicitar con las siguientes caracteristicas: ")               
             dispatcher.utter_message(text="• El limite mensual: $50.000 o $100.000")
             dispatcher.utter_message(text="• Compras internacionales")
         return []

class ActionCotizacion(Action):
#
     def name(self) -> Text:
         return "action_cotizacion"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         url = 'https://api-dolar-argentina.herokuapp.com/api/dolaroficial'
         r = requests.get(url)
         datos = r.json()
         p_d_compra = datos['compra']
         p_d_venta = datos['venta']
         dispatcher.utter_message(text="Valor de compra: " + p_d_compra)
         dispatcher.utter_message(text="Valor de venta: " + p_d_venta)
         return []  

class ActionAyuda(Action):
#
     def name(self) -> Text:
         return "action_ayuda"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         dispatcher.utter_message(text="Te puedo ofrecer informacion de: ")    
         dispatcher.utter_message(text="• Tarjetas")
         dispatcher.utter_message(text="• Convertirte en cliente")
         dispatcher.utter_message(text="• Cotizacion de monedas")
         return []     