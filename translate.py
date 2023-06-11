from sys import argv, stderr, exit
from time import sleep
from requests import post

def getTranslation(sentence, to_lang):
    resp = post("http://localhost:8080/translate", json={
        'text': sentence,
        'source_lang': 'auto',
        'target_lang': to_lang,
    })

    if resp.status_code != 200:
        raise IOError("Non 200 response")

    return resp.json()['data']

def getSentences(infile):
    with open(infile) as store:
        sentences = store.readlines()
    return [s.strip() for s in sentences if s.strip() != ""]

def writeTranslations(sentences, outfile, to_lang):
    numAlreadyWritten = len(open(outfile).readlines())
    i = numAlreadyWritten

    with open(outfile, 'a+') as store:
        while i != len(sentences):
            try:
                s = sentences[i]
                translation = getTranslation(s, to_lang)
                print(translation, file=store, flush=True)
                i += 1
            except Exception as e:
                print(e, file=stderr, flush=True)
                sleep(2 * 60)

def main(infile, outfile, to_lang):
    sentences = getSentences(infile)
    writeTranslations(sentences, outfile, to_lang)


if __name__ == '__main__':
    _, infile, outfile, to_lang = argv
    main(infile, outfile, to_lang)
