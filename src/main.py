# imports
from pathlib import Path
from datetime import date

# project imports
from presentation.gui.app import App
from core.logger.logger import setup_logger

# constants
logger = setup_logger(log_filename=f"log_{date.today()}.log")
YAML_PATH = Path(__file__).parent / "core" / "ai" / "diagnostic.yaml"


# functions
def main():
    """Instancia e executa a aplicação."""
    app = App(yaml_path=str(YAML_PATH))
    app.run()



if __name__ == "__main__":
    logger.info("Inicializando Mini Sistema Especialista")
    try:
        main()
    except Exception as e:
        raise e
    finally:
        logger.info("Finalizando Mini Sistema Especialista")