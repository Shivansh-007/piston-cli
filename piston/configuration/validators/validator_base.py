from piston.utilities.constants import Configuration, console


class Validator:
    
    def __init__(self, config, config_default, name) -> None:
        self.config = config
        self.config_default = config_default
        self.current_type = type(config)
        self.target_type = type(config_default)

        self.name = name

    def validate_type(self) -> bool:
        if self.current_type is not self.target_type and self.current_type is not list:
            console.print(
                f"[red]Configuration \"{self.config.__name__}\" invalid, use type {self.target_type.__name__}, "
                f"not {self.current_type.__name__}. Using default setting.[/red]"
            )
            return False

        if self.current_type is list:
            for item in self.config:
                if type(item) is not self.target_type:
                    console.print(
                        f"[red]A possible \"{type(item).__name__}\" in the list of configurations specified has an invalid type, use type {self.target_type.__name__}. "
                        f"not {type(item).__name__}. Using default setting.[/red]"
                    )
                    return False

            console.print(
                f"[blue]A list of possible configurations was found for the \"{self.name}\" option. Choosing a random one."
            )

        return True 

