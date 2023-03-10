"""Check answers against wordnet."""
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from parse_patient_response import Extractor

nltk.download("wordnet")
nltk.download("omw-1.4")
lemmatizer = WordNetLemmatizer()


class Wordnet:
    """Compare user response to the response inferred from WordNet."""

    def _get_lemma(self, words: list[str]) -> list[str]:
        """Convert list of words to their lemmas.

        Args:
            words (list[str]): list of input words.

        Returns:
            list[str]: list words containg the lemma of the input words.
        """
        return [lemmatizer.lemmatize(word) for word in words]

    def synonym_check(
        self, answer: str, question_main_words: list, self_check: bool
    ) -> bool:
        """Check the answer of the synonym question.

            Extract words from user response and compare
              it to the answered inferred from WordNet.

        Args:
            answer (str): Answer given by the patient.
            question_main_words (list): Words of interest in the question.
            self_check (bool): should the could check if the words in question are
                synonym or it should check if words givven by the patient is
                synonyms of the words in the question.
        """
        extractor = Extractor()
        is_synonym_truth = False
        lemma_words = self._get_lemma(question_main_words)

        if self_check:
            syns = wn.synsets(lemma_words[0])
            for syn in syns:
                for lemma in syn.lemmas():
                    if (
                        lemma.name() != lemma_words[0]
                        and lemma.name() == lemma_words[1]
                    ):
                        is_synonym_truth = True

            answer = extractor.yes_no_extractor(answer=answer)

            if answer is None:
                print("bad Input")
            if answer["agree"] == is_synonym_truth:
                print("OK")
            else:
                print("No")
        # todo: finish this function by adding synonym chech for condition when we want
        # to check for the condition when the similarity is checked between a word and
        # the one words in the patients response.


w = Wordnet()
w.synonym_check("No They are not", ["rejects", "decline"], self_check=True)
