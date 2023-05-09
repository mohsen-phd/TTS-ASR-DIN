"""Class to govern the logic of the hearing test."""


class DigitInNoise:
    """Class to govern the logic of the digit-in-noise test."""

    def __init__(
        self, correct_threshold: int, incorrect__threshold: int, step_size: list[int]
    ):
        """Initilize the DigitInNoise class.

        Args:
            correct_threshold (int): how many correct answers before decreasing the SNR
            incorrect__threshold (int): how many incorrect answers
                                            before increasing the SNR.
            step_size (list[int]): In what steps to increase/decrease the SNR
        """
        self.correct_threshold = correct_threshold
        self.incorrect__threshold = incorrect__threshold
        self.step_size = step_size

    def get_next_snr(
        self, correct_count: int, incorrect_count: int, test_stage: int
    ) -> int:
        """Get the next SNR value.

        The SNR value is calculated based on the number of correct and incorrect.

        Args:
            correct_count (int): the number of correct answers
            incorrect_count (int): the number of incorrect answers
            test_stage (int): how many phases of the test have been completed

        Returns:
            int: new snr to use
        """
        return 0
