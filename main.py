"""Main entry point of the program."""
from loguru import logger


from util import get_test_manager, play_stimuli, read_conf


def main():
    """Code entry point."""
    configs = read_conf("config.yaml")

    manager = get_test_manager(configs)

    snr_db = manager.start_snr
    correct_count = incorrect_count = 0
    while not manager.hearing_test.stop_condition():
        question = manager.stimuli_generator.get_stimuli()
        play_stimuli(manager.sound_generator, snr_db, question, manager.noise)

        transcribe = manager.get_response()

        matched = manager.stimuli_generator.check_answer(transcribe)
        logger.info(f"Matched: {matched}")

        if matched:
            correct_count += 1
        else:
            incorrect_count += 1

        new_snr_db = manager.hearing_test.get_next_snr(
            correct_count, incorrect_count, snr_db
        )
        logger.info(f"New SNR: {new_snr_db}")
        if new_snr_db != snr_db:
            snr_db = new_snr_db
            correct_count = incorrect_count = 0

    logger.info(f"SRT: {manager.hearing_test.srt}")


if __name__ == "__main__":
    main()
