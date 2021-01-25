from piston.colorschemes.nord import NordStyle
from piston.colorschemes.gruvbox import GruvboxStyle
from piston.colorschemes.dracula import DraculaStyle


scheme_dict = {
    "nord": NordStyle.get_nord,
    "gruvbox": GruvboxStyle.get_gruvbox,
    "dracula": DraculaStyle.get_dracula,
}

schemes = list(scheme_dict.keys())
