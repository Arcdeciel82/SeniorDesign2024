# Collection.py

from datetime import datetime
from time import sleep
import brainflow as bf
import multiprocessing
from pathlib import Path

class dataCollection:
    """base class for different collection sources."""
    def __init__(self) -> None:
        self.exit = multiprocessing.Value('i', 0)
        self.thread = multiprocessing.Process(target=self._collectionLoop)
        self.path = Path(f"./{datetime.now().isoformat()}_default.csv")
        self.timer = None
        self.interval = 1

    def _collectionLoop(self):
        # self.file = open(self.path, "a")
        # while not self.exit.is_set():
        # do stuff
        # sleep(self.interval)
        pass

    def startCollection(self) -> None:
        if bool(self.exit.value):
            return
        self.exit.value = 0
        self.thread = multiprocessing.Process(target=self._collectionLoop)
        self.thread.start()
    
    def stopCollection(self) -> None:
        with self.exit.get_lock():
            self.exit.value = 1
        self.thread.join()
        self.thread.close()

class tobiCollection(dataCollection):
    """Insert Description here."""
    def __init__(self) -> None:
        super().__init__()
        self.path = Path(f"./{datetime.now().isoformat()}_tobi.csv")     

class cytonCollection(dataCollection):
    """Insert Description here."""
    def __init__(self, comPort) -> None:
        super().__init__()
        date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.path = Path(f"./{date_string}_cyton.csv")
        self.interval = 0.008
        params = bf.BrainFlowInputParams()
        params.serial_port = comPort
        self.board = bf.BoardShim(bf.BoardIds.CYTON_DAISY_BOARD, params)

    def _collectionLoop(self):
        file = open(self.path, "a+")
        self.board.prepare_session()
        self.board.start_stream()
        description = str(bf.BoardShim.get_board_descr(bf.BoardIds.CYTON_DAISY_BOARD))
        file.write(f"{description}\n")
        while not bool(self.exit.value):
            data = self.board.get_board_data()
            lines = []
            for sample in range(len(data[0])):
                line = []
                for signal in range(len(data)):
                    line.append(str(data[signal][sample]))
                lines.append(','.join(line) + '\n')
            file.writelines(lines)
            print("Cyton Collecting Data")
            sleep(1)
        file.close()

class ue5Collection(dataCollection):
    """Insert Description here."""
    def __init__(self) -> None:
        super().__init__()
        self.path = Path(f"./{datetime.now().isoformat()}_ue5.csv")
