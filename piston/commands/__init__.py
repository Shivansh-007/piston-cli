from piston.commands.base import Base
from piston.commands.from_file import FromFile
from piston.commands.from_input import FromInput
from piston.commands.from_link import FromLink
from piston.commands.from_shell import from_shell


commands_dict = {
    "from_file": FromFile.runfile,
    "from_input": FromInput.askinp,
    "base": Base.run,
    "from_link": FromLink.askinp,
    "from_shell": from_shell.run_shell,
}
