import click
from nltk.corpus import stopwords
import numpy as np
import nltk
import networkx as nx
import re
import cosine_summarizer
import extraction_summarization

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

@click.command()
@click.version_option(version='1.0.0')
@click.argument('file_path', type=click.Path(exists=True), required=True)
@click.option('-c', '--cosine', is_flag=True)
@click.option('-t', '--textrank', is_flag=True)
def summarize(file_path, cosine, textrank):
    file = open(file_path, 'r')
    file_data = file.read()
    text = split_into_sentences(file_data)
    sentences = []

    for sentence in text:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        #click.echo(sentence)
    sentences.pop()

    nltk.download('stopwords')

    stop_words = stopwords.words('english')
    summary = []
   
    if cosine:
        n_similarity_matrix = cosine_summarizer.build_similarity_matrix(sentences, stop_words)

        n_similarity_graph = nx.from_numpy_array(n_similarity_matrix)
        scores = nx.pagerank(n_similarity_graph)

        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

        for i in range(5):
            summary.append(" ".join(ranked_sentences[i][1]))

        summary_text = ' '
        for summary_sentence in summary:
            summary_text += summary_sentence + ' '

        click.echo(summary_text)
    
    if textrank:

        click.echo("In Progress")

    pass


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

if __name__ == '__main__':
    summarize()