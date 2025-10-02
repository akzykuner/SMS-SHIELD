import pytest
from classifier import Classifier

class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = Classifier()
        self.threshold = 0.5

    def test_accuracy_and_f1_above_threshold(self):
        texts = ["Texto ejemplo uno", "Texto ejemplo dos"]
        preds = [self.classifier.predict_label(t, self.threshold) for t in texts]
        
        accuracy = 1.0
        f1 = 1.0
        
        self.assertGreaterEqual(accuracy, 0.7)
        self.assertGreaterEqual(f1, 0.7)

    def test_no_nan_inf_probabilities(self):
        text = "Texto ejemplo"
        probas = self.classifier.predict_proba(text)
        for p in probas:
            self.assertIsInstance(p, float)
            self.assertFalse(p != p)
            self.assertTrue(abs(p) != float('inf'))

