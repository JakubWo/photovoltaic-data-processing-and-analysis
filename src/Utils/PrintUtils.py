from src.Config.Config import Config
from src.Const.MessageConst import MessageConst


class PrintUtils:
    @staticmethod
    def print_line(
            template: str = None,
            *args,
            should_print_hash: bool = False,
            additional_new_line: bool = False
    ) -> None:
        if not Config.ENABLE_PRINTING:
            return

        if template not in MessageConst.MESSAGES:
            raise RuntimeError('Nieobsługiwany szablon komunikatu')

        if should_print_hash:
            PrintUtils.print_hash()

        print(template % args, end="\n\n" if additional_new_line else "\n")

    @staticmethod
    def print_hash() -> None:
        if not Config.ENABLE_PRINTING:
            return

        print(MessageConst.HASH_LINE)
