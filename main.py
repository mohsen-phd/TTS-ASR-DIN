"""Main entry point of the program."""
import os
import sys

from colorama import Fore, Back, Style
from loguru import logger

from util import get_test_manager, play_stimuli, read_conf

logger.remove(0)
logger.add(sys.stderr, level="INFO")


def preparation() -> tuple[str, str]:
    """prepare the test and logging system.

    Returns:
        tuple(str,str): save location of logs and audio recording. test number for logging.
    """
    participant_id = input(Fore.GREEN + "Enter The ID: ")
    test_number = input(Fore.GREEN + "Enter test number: ")

    save_dir = f"records/{participant_id}"
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(f"save_dir/{test_number}", exist_ok=True)

    logger.add(f"{save_dir}/{test_number}/out.log")
    logger.debug(f"\nParticipant ID: {participant_id}")
    input(Fore.RED + "Press enter to start the test ")
    return save_dir, test_number


def main():
    """Code entry point."""
    save_dir, test_number = preparation()

    configs = read_conf("config.yaml")
    configs["test"]["record_save_dir"] = f"{save_dir}/{test_number}"
    manager = get_test_manager(configs)

    snr_db = manager.start_snr
    correct_count = incorrect_count = 0
    while not manager.hearing_test.stop_condition():
        question = manager.stimuli_generator.get_stimuli()
        print(Fore.YELLOW + "Listen to the numbers")
        logger.debug(f"The stimuli is: {question}")
        play_stimuli(manager.sound_generator, snr_db, question, manager.noise)

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

    logger.debug(f"SRT: {manager.hearing_test.srt} \n")
    print(Fore.RED + "End of the test")


if __name__ == "__main__":
    main()
