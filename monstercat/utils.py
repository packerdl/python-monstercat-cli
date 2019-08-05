from click import echo, style


def pretty_dict(d, indent=0, indent_size=2, key_fg="blue", value_fg="green"):
    for key, value in d.items():
        if isinstance(value, dict):
            echo(" " * (indent + indent_size) + style("%s: " % key, fg=key_fg, bold=True))
            pretty_dict(value, indent + indent_size)
        else:
            key_txt = style("%s:" % key, fg=key_fg, bold=True)
            val_txt = style("%s" % value, fg=value_fg)
            echo(" " * (indent + indent_size) + "%s %s" % (key_txt, val_txt))
