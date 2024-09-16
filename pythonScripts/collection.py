# Collection.py

from datetime import datetime
from time import sleep
import brainflow as bf
from multiprocessing import Process
from pathlib import Path

class dataCollection:
    """base class for different collection sources."""
    def __init__(self) -> None:
        self.running = False
        self.thread = Process(target=self._collectionLoop)
        self.path = Path(f"./{datetime.now().isoformat()}_default.csv")
        self.timer = None
        self.interval = 1

    def _collectionLoop(self):
        # self.file = open(self.path, "a")
        # while self.running:
        # do stuff
        # sleep(self.interval)
        pass

    def startCollection(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread.start()
    
    def stopCollection(self) -> None:
        if not self.running:
            return
        self.running = False
        self.thread.join()

class tobiCollection(dataCollection):
    """Insert Description here."""
    def __init__(self) -> None:
        super().__init__()
        self.path = Path(f"./{datetime.now().isoformat()}_tobi.csv")     

class cytonCollection(dataCollection):
    """Insert Description here."""
    def __init__(self, comPort) -> None:
        super().__init__()
        self.path = Path(f"./{datetime.now().isoformat()}_cyton.csv")
        params = bf.BrainFlowInputParams()
        params.serial_port = comPort
        self.board = bf.BoardShim(bf.BoardIds.CYTON_DAISY_BOARD, params)

    def _collectionLoop(self):
        file = open(self.path, "a")
        self.board.prepare_session()
        self.board.start_stream()
        while self.running:
            data = self.board.get_current_board_data(1)
            file.write(data)
        file.close()
        

class ue5Collection(dataCollection):
    """Insert Description here."""
    def __init__(self) -> None:
        super().__init__()
        self.path = Path(f"./{datetime.now().isoformat()}_ue5.csv")