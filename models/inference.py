from transformers.pipelines import Pipeline


def run_pipeline(nlp: Pipeline, question: str, context: str) -> str:
    """Running Hugging Face Pipeline (generic) 

    Parameters:
    nlp (Pipeline): The transformers' pipeline object intended to be run
    question: The questoin (from template) designed to summarise the review
    context: The (raw/preprocessed) review itself (subject to being summarised)
    
    Returns:
    res (str): The listed elements (anwser to given question) as string.

   """

    QA_input = {
        'context': context,
        'question': question
    }
    
    out = nlp(QA_input)
    res = out['answer']
    return res
