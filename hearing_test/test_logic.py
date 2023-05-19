"""Class to govern the logic of the hearing test."""

from enum import Enum


class STATUS(Enum):
    """Enum to represent the status of the test."""

    INIT = 0
    INCREASE = 1
    DECREASE = 2


class DigitInNoise:
    """Class to govern the logic of the digit-in-noise test."""

    def __init__(
        self,
        correct_threshold: int,
        incorrect_threshold: int,
        step_size: list[int],
        reversal_limit: int,
    ):
        """Initilize the DigitInNoise class.

        Args:
            correct_threshold (int): how many correct answers before decreasing the SNR
            incorrect_threshold (int): how many incorrect answers
                                            before increasing the SNR.
            step_size (list[int]): In what steps to increase/decrease the SNR
            reversal_limit (int): How many reversals before stopping the test.
        """
        self._correct_threshold = correct_threshold
        self._incorrect_threshold = incorrect_threshold
        self._step_size = step_size
        self._reversal_count = 0
        self._previous_action = STATUS.INIT
        self._reversal_limit = reversal_limit

    def _is_reversing(self, new_status: STATUS) -> bool:
        """Check if the test is reversing.

        Args:
            new_status (STATUS): the new STATUS of the test in this iteration

        Returns:
            bool: True if the test is reversing, False otherwise
        """
        if self._previous_action == STATUS.INIT:
            return False

        if self._previous_action == new_status:
            return False
        else:
            return True

    def _get_step_size(self) -> int:
        """Get the step size to for changing the SNR.

        Returns:
            int: The amount to change the SNR.
        """
        if self._reversal_count > 2:
            return self._step_size[1]
        elif self._reversal_count > 4:
            return self._step_size[2]
        else:
            return self._step_size[0]

    def get_next_snr(
        self, correct_count: int, incorrect_count: int, snr_db: int
    ) -> int:
        """Get the next SNR value.

        The SNR value is calculated based on the number of correct and incorrect.

        Args:
            correct_count (int): the number of correct answers
            incorrect_count (int): the number of incorrect answers
            snr_db (int): the current snr value

        Returns:
            int: new snr to use
        """
        if correct_count >= self._correct_threshold:
            if self._is_reversing(STATUS.DECREASE):
                self._reversal_count += 1
            self._previous_action = STATUS.DECREASE
            snr_change = self._get_step_size()
            return snr_db - snr_change

        elif incorrect_count >= self._incorrect_threshold:
            if self._is_reversing(STATUS.INCREASE):
                self._reversal_count += 1
            self._previous_action = STATUS.INCREASE
            snr_change = self._get_step_size()
            return snr_db + snr_change

        return snr_db

    def stop_condition(self) -> bool:
        """Check if the test should stop.

        Returns:
            bool: True if the test should stop, False otherwise.
        """
        if self._reversal_count > self._reversal_limit:
            return True
        else:
            return False
