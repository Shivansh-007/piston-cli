from pygments.style import Style
from pygments.token import (
    Comment,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    String,
    Token,
)


class GruvboxStyle(Style):
    """Configure Gruvbox Theme."""

    styles = {
        Comment.Preproc: "noinherit #8ec07c",
        Comment: "#928374 italic",
        Generic.Deleted: "noinherit #282828",
        Generic.Emph: "#83a598 underline",
        Generic.Error: "bold",
        Generic.Heading: "#b8bb26 bold",
        Generic.Inserted: "noinherit #282828",
        Generic.Output: "noinherit #504945",
        Generic.Prompt: "#ebdbb2",
        Generic.Strong: "#ebdbb2",
        Generic.Subheading: "#b8bb26 bold",
        Generic.Traceback: "#fb4934 bold",
        Generic: "#ebdbb2",
        Keyword.Type: "noinherit #fabd2f",
        Keyword: "noinherit #fe8019",
        Name.Attribute: "#b8bb26 bold",
        Name.Builtin: "#fabd2f",
        Name.Constant: "noinherit #d3869b",
        Name.Entity: "noinherit #fabd2f",
        Name.Exception: "noinherit #fb4934",
        Name.Function: "#fabd2f",
        Name.Label: "noinherit #fb4934",
        Name.Tag: "noinherit #fb4934",
        Name.Variable: "noinherit #ebdbb2",
        Name: "#ebdbb2",
        Number.Float: "noinherit #d3869b",
        Number: "noinherit #d3869b",
        Operator: "#fe8019",
        String.Symbol: "#83a598",
        String: "noinherit #b8bb26",
        Token: "noinherit #ebdbb2",
    }
