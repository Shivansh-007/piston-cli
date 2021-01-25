from pygments import lexers
from pygments.styles import get_all_styles
from piston.colorschemes import schemes
from piston.utilities.compilers import languages_


def init_lexers() -> None:
    lexers.find_lexer_class_by_name("nasm")
    lexers.find_lexer_class_by_name("awk")
    lexers.find_lexer_class_by_name("bash")
    lexers.find_lexer_class_by_name("brainfuck")
    lexers.find_lexer_class_by_name("c")
    lexers.find_lexer_class_by_name("lisp")
    lexers.find_lexer_class_by_name("csharp")
    lexers.find_lexer_class_by_name("cpp")
    lexers.find_lexer_class_by_name("d")
    lexers.find_lexer_class_by_name("ruby")
    lexers.find_lexer_class_by_name("emacs")
    lexers.find_lexer_class_by_name("elixir")
    lexers.find_lexer_class_by_name("haskell")
    lexers.find_lexer_class_by_name("go")
    lexers.find_lexer_class_by_name("java")
    lexers.find_lexer_class_by_name("javascript")
    lexers.find_lexer_class_by_name("julia")
    lexers.find_lexer_class_by_name("kotlin")
    lexers.find_lexer_class_by_name("perl")
    lexers.find_lexer_class_by_name("php")
    lexers.find_lexer_class_by_name("python3")
    lexers.find_lexer_class_by_name("python2")
    lexers.find_lexer_class_by_name("rust")
    lexers.find_lexer_class_by_name("swift")
    lexers.find_lexer_class_by_name("zig")


init_lexers()

# https://chromium.googlesource.com/external/bitbucket.org/birkenfeld/pygments-main/+/db08aaee269398020b08a388206b62b560a08665/pygments/lexers/_mapping.py
lexers_dict = {
    "nasm": lexers.asm.NasmLexer,
    "awk": lexers.textedit.AwkLexer,
    "bash": lexers.shell.BashLexer,
    "brainfuck": lexers.esoteric.BrainfuckLexer,
    "c": lexers.c_cpp.CLexer,
    "lisp": lexers.lisp.CommonLispLexer,
    "csharp": lexers.dotnet.CSharpLexer,
    "cpp": lexers.c_cpp.CppLexer,
    "d": lexers.d.DLexer,
    "ruby": lexers.ruby.RubyLexer,
    "emacs": lexers.lisp.CommonLispLexer,
    "elixir": lexers.erlang.ElixirLexer,
    "haskell": lexers.haskell.HaskellLexer,
    "go": lexers.go.GoLexer,
    "java": lexers.jvm.JavaLexer,
    "js": lexers.javascript.JavascriptLexer,
    "julia": lexers.julia.JuliaLexer,
    "kotlin": lexers.jvm.KotlinLexer,
    "perl": lexers.perl.PerlLexer,
    "php": lexers.php.PhpLexer,
    "python3": lexers.python.Python3Lexer,
    "python2": lexers.python.PythonLexer,
    "rust": lexers.rust.RustLexer,
    "swift": lexers.objective.SwiftLexer,
    "zig": lexers.zig.ZigLexer,
}

spinners = [
    "point",
    "dots",
    "dots12",
    "dots9",
    "dots2",
    "simpleDotsScrolling",
    "bouncingBall",
]

themes = list(get_all_styles()) + schemes
themes = [list(themes[style : style + 2]) for style in range(0, len(themes), 2)]

languages_table = zip(iter(languages_), iter(languages_))
