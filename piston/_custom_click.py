import typing as t

from click import Command, Context, Group, UsageError


class DefaultCommandGroup(Group):
    """Allow a default command for a click group."""

    def command(self, *args: t.Any, **kwargs: t.Any) -> t.Callable[[t.Callable[..., t.Any]], Command]:
        """
        A shortcut decorator for declaring and attaching a command to the group.

        This takes the same arguments as :func:`command` and  immediately registers the created
        command with this group. If `default_command` is set to True (as a keyword argument),
        it would be the "fallback" command which would be executed in case the passed command
        isn't registered for the group.
        """
        default_command = kwargs.pop("default_command", False)
        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<default_command>")
        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f: t.Callable[..., t.Any]) -> Command:
                """Create a custom decorator for `default_command` command."""
                cmd = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(
        self, ctx: Context, args: t.List[str]
    ) -> t.Tuple[t.Optional[str], t.Optional[Command], t.List[str]]:
        """Try resolving the command, if the command isn't registered run the default command, if any."""
        try:
            # test if the command parses
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except UsageError:
            # command did not parse, assume it is the default command
            args.insert(0, self.default_command)
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
