from pygments import lexers


def init_lexers() -> None:
    """Declaring all lexers of the languages supported by piston API."""
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
    lexers.find_lexer_class_by_name("nim")
    lexers.find_lexer_class_by_name("scala")
    lexers.find_lexer_class_by_name("typescript")
    lexers.find_lexer_class_by_name("lua")
    lexers.find_lexer_class_by_name("crystal")
    lexers.find_lexer_class_by_name("text")


init_lexers()

# https://github.com/pydanny/pygments-custom/blob/master/pygments/lexers/_mapping.py
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
    "python": lexers.python.Python3Lexer,
    "python2": lexers.python.PythonLexer,
    "rust": lexers.rust.RustLexer,
    "swift": lexers.objective.SwiftLexer,
    "zig": lexers.zig.ZigLexer,
    "paradox": lexers.special.TextLexer,
    "crystal": lexers.crystal.CrystalLexer,
    "dash": lexers.special.TextLexer,
    "osabie": lexers.special.TextLexer,
    "nim": lexers.nimrod.NimrodLexer,
    "deno": lexers.javascript.JavascriptLexer,
    "scala": lexers.jvm.ScalaLexer,
    "typescript": lexers.javascript.TypeScriptLexer,
    "lua": lexers.scripting.LuaLexer,
}
