from .auth import login, logout, status
from .entry import entry
from .settings import settings
from .sync import sync

entry.add_command(login)
entry.add_command(logout)
entry.add_command(settings)
entry.add_command(status)
entry.add_command(sync)

entry()
