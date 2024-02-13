import sys
import logging


def install_excepthook():
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logging.debug("", exc_info=(exc_type, exc_value, exc_traceback))
        logging.critical(
            "Erreur inattendue, veuillez prévenir le développeur.\n"
            "Le programme va maintenant se fermer sans avoir terminé."
        )

    sys.excepthook = handle_exception
