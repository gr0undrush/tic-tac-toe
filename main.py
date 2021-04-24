import logging

from libs.gui import Ui

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    logger = logging.getLogger(__name__)

    ui = Ui()
    ui.start()


