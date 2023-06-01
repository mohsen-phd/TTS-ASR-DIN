"""Main entry point of the program."""
from loguru import logger

from util import initialize, listen, play_stimuli


def main():
    """Code entry point."""
    (
        hearing_test,
        stimuli_generator,
        asr,
        recorder,
        sound_generator,
        noise,
    ) = initialize()

    snr_db = 5
    correct_count = incorrect_count = 0
    while not hearing_test.stop_condition():
        question = stimuli_generator.get_stimuli()
        play_stimuli(sound_generator, snr_db, question, noise)

        transcribe = listen(asr, recorder)

        matched = stimuli_generator.check_answer(transcribe)
        logger.info(f"Matched: {matched}")

        if matched:
            correct_count += 1
        else:
            incorrect_count += 1

        new_snr_db = hearing_test.get_next_snr(correct_count, incorrect_count, snr_db)
        logger.info(f"New SNR: {new_snr_db}")
        if new_snr_db != snr_db:
            snr_db = new_snr_db
            correct_count = incorrect_count = 0

    logger.info(f"SRT: {hearing_test.srt}")


if __name__ == "__main__":
    main()
