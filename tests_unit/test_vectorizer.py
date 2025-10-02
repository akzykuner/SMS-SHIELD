import pytest
from vectorizer import Vectorizer

class TestVectorizer(unittest.TestCase):
    def setUp(self):
        self.vectorizer = Vectorizer()

    def test_vector_size_and_structure(self):
        text1 = "Texto de prueba uno!"
        text2 = "Otro texto para prueba."
        
        vec1 = self.vectorizer.vectorize(text1)
        vec2 = self.vectorizer.vectorize(text2)
        
        self.assertEqual(len(vec1), len(vec2))
        
        caps_ratio = vec1[-3]
        exclam_count = vec1[-2]
        token_len = vec1[-1]
        self.assertIsInstance(caps_ratio, float)
        self.assertIsInstance(exclam_count, int)
        self.assertIsInstance(token_len, int)
