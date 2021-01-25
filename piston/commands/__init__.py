from piston.commands.frominput import FromInput
from piston.commands.fromfile import FromFile
from piston.commands.base import Base
from piston.commands.fromlink import FromLink

commands_dict = {
    "fromfile": FromFile.runfile,
    "frominput": FromInput.askinp,
    "base": Base.run,
    "fromlink": FromLink.askinp,
}
