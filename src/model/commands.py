
class Commands:

    WHO = "WHO"
    WHERE = "WHERE"
    WHY = "WHY"
    PADDING_CHARACTER = "x"

    _commands = {
        WHO,
        WHERE,
        WHY
    }

    @staticmethod
    def get_command_len():
        return len(Commands.WHERE)

    @staticmethod
    def pad_to_command_len(cmd):
        return cmd.ljust(Commands.get_command_len(),
                         Commands.PADDING_CHARACTER)

    @staticmethod
    def unpad_command(cmd):
        return cmd.replace(Commands.PADDING_CHARACTER, '')

    @staticmethod
    def assert_valid(command):
        if command not in Commands._commands:
            raise ValueError(
                f"Bad command, not registed in Commands {command}")
