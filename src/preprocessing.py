import pandas as pd
import numpy as np
import re
from sklearn.base import BaseEstimator, TransformerMixin
from .rules import PatternRules

class TextCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
        
    def transform(self, X, y=None):
        # X espera-se ser uma Series ou Lista
        if isinstance(X, pd.DataFrame):
            # Garante pegar a coluna de texto se vier como DF
            text_data = X.iloc[:, 0].astype(str)
        else:
            text_data = pd.Series(X).astype(str)
            
        # Limpeza básica: lower, remoção de espaços duplos
        return text_data.apply(lambda t: re.sub(r'\s+', ' ', t.lower().strip()))

class RuleFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Transforma texto cru em vetor de features baseado nas regras de RegEx.
    Saída numérica: [tem_cpf, tem_email, tem_tel, tem_rg]
    """
    def __init__(self):
        self.matcher = PatternRules()
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        features = []
        for text in X:
            matches = self.matcher.check_sensitive_patterns(text)
            # Extraindo features binárias (contém/não contém) e contagem total
            # Isso ajuda o modelo a aprender que CPF é muito forte para decisão.
            row = [
                1 if matches['match_cpf'] > 0 else 0,
                1 if matches['match_email'] > 0 else 0,
                1 if matches['match_phone'] > 0 else 0,
                1 if matches['match_rg'] > 0 else 0
            ]
            features.append(row)
        return np.array(features)