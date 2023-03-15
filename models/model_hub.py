from transformers import pipeline
from transformers.pipelines import Pipeline


ROBERTA = "deepset/roberta-base-squad2"
DEBERTA = "deepset/deberta-v3-large-squad2"
DISTILBERT = 'distilbert-base-cased-distilled-squad'


def get_nlp(model_name: str) -> Pipeline:
    nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
    return nlp


names = ['roberta', 'deberta', 'distilbert']
models = {name:get_nlp(eval(name.upper())) for name in names}