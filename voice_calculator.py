import re
import operator

class VoiceCalculator:
    def __init__(self):
        self.operations = {
            "plus": operator.add,
            "additionne": operator.add,
            "ajoute": operator.add,
            "additionner": operator.add,
            "et": operator.add,  # Exemple : "5 et 3"
            "moins": operator.sub,
            "soustrait": operator.sub,
            "retranche": operator.sub,
            "soustraire": operator.sub,
            "multiplie": operator.mul,
            "multiplié par": operator.mul,
            "fois": operator.mul,
            "x": operator.mul,
            "par": operator.mul,  # Exemple : "5 par 3" (contextuellement multiplicatif)
            "divise": operator.truediv,
            "divisé par": operator.truediv,
            "sur": operator.truediv,  # Exemple : "10 sur 2"
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }

    def parse_and_calculate(self, text):
        # Normalisation des espaces et mise en minuscules
        text = re.sub(r'\s+', ' ', text.lower())

        for op_text, op_func in self.operations.items():
            if op_text in text:
                try:
                    # Extraire les nombres (entiers ou flottants) dans le texte
                    numbers = list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", text)))
                    if len(numbers) == 2:
                        result = op_func(numbers[0], numbers[1])
                        return f"Le résultat est {result:.2f}"
                    else:
                        return "Je n'ai pas compris les nombres à utiliser. Veuillez réessayer."
                except ZeroDivisionError:
                    return "Erreur : division par zéro."
                except Exception as e:
                    return f"Erreur lors du calcul : {str(e)}"
        return "Je n'ai pas compris l'opération demandée. Veuillez utiliser des expressions comme '5 plus 3'."

    def validate_input(self, text):
        """
        Vérifie que l'entrée contient une opération valide.
        """
        if any(op in text for op in self.operations.keys()):
            return True
        return False
