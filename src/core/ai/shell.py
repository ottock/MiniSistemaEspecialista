# imports
import yaml

# constants
_DIAGNOSIS_PREFIXES = ("diagnóstico", "recomendação", "alerta")


# class
class Shell:
    def __init__(self, yaml_path: str):
        """Carrega a base de conhecimento e inicializa fatos e diagnósticos."""
        self.knowledge = self._load_shell(yaml_path)
        self.questions = self.knowledge["questions"]
        self.rules = self.knowledge["rules"]
        self.facts = set()
        self.diagnoses = list()


    # functions
    def _load_shell(self, file_path: str):
        """Lê e retorna o conteúdo do arquivo YAML da base de conhecimento."""
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)


    def _infer_facts(self):
        """Aplica encadeamento progressivo até não haver novos fatos ou diagnósticos."""
        new_facts = True
        while new_facts:
            new_facts = False
            for rules in self.rules:
                premises = set(rules["if"])
                consequences = rules["then"]
                if premises.issubset(self.facts) and consequences not in self.facts and consequences not in self.diagnoses:
                    if str(consequences).lower().startswith(_DIAGNOSIS_PREFIXES):
                        self.diagnoses.append(consequences)
                    else:
                        self.facts.add(consequences)
                        new_facts = True