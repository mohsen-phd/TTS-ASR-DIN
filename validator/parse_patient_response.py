"""Module to extract information from patient response."""
import spacy


class Extractor:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")

    def yes_no_extractor(self, answer: str) -> dict[str]:
        if "yes" in answer.lower():
            return {"agree": True}
        elif "no" in answer.lower():
            return {"agree": False}

    def keyword_extractor(
        self, answer: str, question_key_words: list[str]
    ) -> list[str]:
        doc_answer = self.nlp(answer)
        doc_question = self.nlp(question_key_words[0])

        question_nps = []
        for np in doc_question.noun_chunks:
            question_nps.append([(token.text, token.pos_) for token in np])

        answer_nps = []
        for np in doc_answer.noun_chunks:
            answer_nps.append(
                [
                    (token.text, token.pos_)
                    for token in np
                    if token.pos_ == question_nps[0][0]
                ]
            )

        answer_nps
