#!/bin/bash

import discord

from discord.ext import commands
from qabc.qubit import Qubit


if __name__ == "__main__":
    TOKEN = os.environ["QUBIT_TOKEN"]

    client = Qubit(
        case_insensitive = True,
        strip_after_prefix = True,
        intents = discord.Intents.all(),
    )

    client.run(TOKEN)
