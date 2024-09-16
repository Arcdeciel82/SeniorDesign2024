# simulationUI.py
# Curt Lynch
# This program will host a ui that will help with collecting and storing data from CytonDaisy, UE5, and Tubi.

from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from collection import dataCollection, cytonCollection, ue5Collection, tobiCollection


def CollectionSwitch(event:ValueChangeEventArguments, agent:dataCollection):
    if event.value:
        ui.notify(f"Starting {event.sender._text}!")
        agent.startCollection()
    else:
        ui.notify(f"Stopping {event.sender._text}!")
        agent.stopCollection()

cyton = cytonCollection("/dev/ttyUSB0")
ue5 = ue5Collection()
tobi = tobiCollection()

ui.dark_mode(True)
ui.page_title("Data Collection")
with ui.row():
    ui.switch('Cyton Collection', on_change=lambda e: CollectionSwitch(e, cyton))
    ui.switch('Tobi Collection', on_change=lambda e: CollectionSwitch(e, tobi))
    ui.switch('UE5 Simulation', on_change=lambda e: CollectionSwitch(e, ue5))

ui.run()
