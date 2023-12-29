"""Main entry point of the program."""
import sys

from colorama import Fore, Back, Style
from loguru import logger

from util import get_test_manager, play_stimuli, read_conf

logger.remove(0)
logger.add(sys.stderr, level="INFO")


def main():
    """Code entry point."""
    participant_id = input(Fore.GREEN + "Enter The ID: ")
    logger.debug(f"Participant ID: {participant_id}")
    configs = read_conf("config.yaml")

    manager = get_test_manager(configs)

    snr_db = manager.start_snr
    correct_count = incorrect_count = 0
    while not manager.hearing_test.stop_condition():
        question = manager.stimuli_generator.get_stimuli()
        print(Fore.YELLOW + "Listen to the numbers")

        play_stimuli(manager.sound_generator, snr_db, question, manager.noise)

        print(Fore.GREEN + "Repeat the number you heard")
        transcribe = manager.get_response()

        matched = manager.stimuli_generator.check_answer(transcribe)
        logger.debug(f"Matched: {matched}")

        if matched:
            correct_count += 1
        else:
            incorrect_count += 1

        new_snr_db = manager.hearing_test.get_next_snr(
            correct_count, incorrect_count, snr_db
        )
        manager.hearing_test.update_variables(matched, snr_db)
        logger.debug(f"New SNR: {new_snr_db}")
        if new_snr_db != snr_db:
            snr_db = new_snr_db
            correct_count = incorrect_count = 0

    logger.debug(f"SRT: {manager.hearing_test.srt}")
    print(Fore.RED + "End of the test")


if __name__ == "__main__":
    main()
