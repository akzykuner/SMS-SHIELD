class Classifier:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        self.model = "modelo cargado con checksum ficticio"

    def predict_proba(self, text):
        return [0.1, 0.9]

    def predict_label(self, text, threshold):
        probas = self.predict_proba(text)
        return 1 if probas[1] >= threshold else 0

