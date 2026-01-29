from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from .preprocessing import TextCleaner, RuleFeatureExtractor

class AccessInfoClassifier:
    def __init__(self):
        # Definição do Modelo
        # Usamos FeatureUnion para combinar a análise semântica (NLP) com as Regras rígidas
        
        self.model_pipeline = Pipeline([
            ('union', FeatureUnion(
                transformer_list=[
                    # Ramo 1: NLP Puro (contexto, nomes, endereços não estruturados)
                    ('nlp', Pipeline([
                        ('cleaner', TextCleaner()),
                        ('tfidf', TfidfVectorizer(
                            ngram_range=(1, 3), # Unigramas, bigramas e trigramas para contexto
                            max_features=5000,
                            min_df=2
                        )),
                    ])),
                    
                    # Ramo 2: Regras Explícitas (CPF, Email, Tel)
                    ('rules', Pipeline([
                        ('cleaner', TextCleaner()),
                        ('rule_extractor', RuleFeatureExtractor())
                    ]))
                ]
            )),
            
            # Modelo de Classificação: LogisticRegression
            # Escolhido pela alta explicabilidade (pesos das features) e robustez.
            # class_weight='balanced': Crucial para priorizar Recall em classes desbalanceadas.
            ('clf', LogisticRegression(
                C=1.0, 
                solver='liblinear', 
                class_weight='balanced',
                random_state=42
            ))
        ])

    def train(self, X_train, y_train):
        print(">> Treinando modelo híbrido...")
        self.model_pipeline.fit(X_train, y_train)
        
    def predict(self, X):
        return self.model_pipeline.predict(X)
        
    def predict_proba(self, X):
        return self.model_pipeline.predict_proba(X)