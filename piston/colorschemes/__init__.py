from piston.colorschemes.dracula import DraculaStyle
from piston.colorschemes.gruvbox import GruvboxStyle
from piston.colorschemes.nord import NordStyle


scheme_dict = {
    "nord": NordStyle,
    "gruvbox": GruvboxStyle,
    "dracula": DraculaStyle,
}

schemes = list(scheme_dict.keys())
