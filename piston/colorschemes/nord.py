from prompt_toolkit.styles import Style, style_from_pygments_dict
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Whitespace,
)


class NordStyle:
    """Configuration for Nord Theme."""

    def __init__(self) -> None:
        self.nord0 = "#2e3440"
        self.nord1 = "#3b4252"
        self.nord2 = "#434c5e"
        self.nord3 = "#4c566a"
        self.nord3_bright = "#616e87"

        self.nord4 = "#d8dee9"
        self.nord5 = "#e5e9f0"
        self.nord6 = "#eceff4"

        self.nord7 = "#8fbcbb"
        self.nord8 = "#88c0d0"
        self.nord9 = "#81a1c1"
        self.nord10 = "#5e81ac"

        self.nord11 = "#bf616a"
        self.nord12 = "#d08770"
        self.nord13 = "#ebcb8b"
        self.nord14 = "#a3be8c"
        self.nord15 = "#b48ead"

        self.background_color = self.nord0
        self.default = self.nord4

    def get_nord(self) -> Style:
        """Configuration for Nord Theme."""
        return style_from_pygments_dict(
            {
                Whitespace: self.nord4,
                Comment: f"italic {self.nord3_bright}",
                Comment.Preproc: self.nord10,
                Keyword: f"bold {self.nord9}",
                Keyword.Pseudo: f"nobold {self.nord9}",
                Keyword.Type: f"nobold {self.nord9}",
                Operator: self.nord9,
                Operator.Word: f"bold {self.nord9}",
                Name: self.nord4,
                Name.Builtin: self.nord9,
                Name.Function: self.nord8,
                Name.Class: self.nord7,
                Name.Namespace: self.nord7,
                Name.Exception: self.nord11,
                Name.Variable: self.nord4,
                Name.Constant: self.nord7,
                Name.Label: self.nord7,
                Name.Entity: self.nord12,
                Name.Attribute: self.nord7,
                Name.Tag: self.nord9,
                Name.Decorator: self.nord12,
                Punctuation: self.nord6,
                String: self.nord14,
                String.Doc: self.nord3_bright,
                String.Interpol: self.nord14,
                String.Escape: self.nord13,
                String.Regex: self.nord13,
                String.Symbol: self.nord14,
                String.Other: self.nord14,
                Number: self.nord15,
                Generic.Heading: f"bold {self.nord8}",
                Generic.Subheading: f"bold {self.nord8}",
                Generic.Deleted: self.nord11,
                Generic.Inserted: self.nord14,
                Generic.Error: self.nord11,
                Generic.Emph: "italic",
                Generic.Strong: "bold",
                Generic.Prompt: f"bold {self.nord3}",
                Generic.Output: self.nord4,
                Generic.Traceback: self.nord11,
                Error: self.nord11,
            }
        )


NordStyle = NordStyle()
