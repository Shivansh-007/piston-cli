from piston.commands.base import Base
from piston.commands.from_file import FromFile
from piston.commands.from_input import FromInput
from piston.commands.from_link import FromLink
from piston.commands.from_shell import from_shell
from piston.commands.theme_list import theme_list

commands_dict = {
    "from_file": FromFile.run_file,
    "from_input": FromInput.ask_input,
    "base": Base.run,
    "from_link": FromLink.ask_input,
    "from_shell": from_shell.run_shell,
    "theme_list": theme_list,
}
