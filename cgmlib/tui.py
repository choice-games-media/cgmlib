import msvcrt
import os

import keyboard
from colorama import Fore, Style


def sinput(
    prompt: object = "", sep: object = " ", end: object = ">>", mode: str = None
) -> input:
    """
    A function ripped directly from one of my projects, Make Money.
    :param prompt: Optional. The input prompt.
    :param sep: Optional. String which goes in between the prompt and the end.
    :param end: Optional. String which goes at the end of the prompt.
    :param mode: Optional. Input mode.
        'compare' for case-insensitive comparison.
        'compare-validated' to return a boolean value of the response's approval.
        'interrupt' for press Enter to continue.
    :return: The user's input.
    """
    match mode:
        case "compare":
            return input(f"{prompt}{sep}{end}").casefold().strip()

        case "compare-validated":
            return affirmative(input(f"{prompt}{sep}{end}").casefold().strip())

        case "interrupt":
            if prompt == "":
                prompt = "Press any key to continue."
            print(prompt, end="", flush=True)
            msvcrt.getch()  # Todo: This solution only works for Windows devices
            print()
            return None

        case _:
            return input(f"{prompt}{sep}{end}")


def clear() -> None:
    """
    Clears the console screen.
    :return: None
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pick(options: list, title: str = None) -> str:
    """
    Present a list of options to the user and return their selected option.
    :param options: List of options.
    :param title: Optional. String displayed above the options.
    :return: The selected option.
    """
    current_option = 0

    def print_options():
        if title:
            print(title)
        for i, option in enumerate(options):
            if i == current_option:
                print(f"> {Fore.GREEN}{option}{Style.RESET_ALL}")
            else:
                print(f"  {option}")

    print_options()

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "down" and current_option < len(options) - 1:
                current_option += 1
                clear()
                print_options()
            elif event.name == "up" and current_option > 0:
                current_option -= 1
                clear()
                print_options()
            elif event.name == "enter":
                break

    input()
    return options[current_option]


def affirmative(response) -> bool:
    """
    Determine if a given response expresses agreement or approval.
    :param response: The response.
    :return: True if affirmative, False otherwise.
    """
    # https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python/715455#715455
    # https://github.com/pypa/pipx/blob/0cfcdc1781d6bc366e7f72af5b3c59513d9ec118/src/pipx/emojis.py#L5
    if response in [
        "true",
        "1",
        "t",
        "y",
        "yes",
        "yeah",
        "yup",
        "certainly",
        "uh-huh",
        "on",
    ]:
        return True
    else:
        return False
