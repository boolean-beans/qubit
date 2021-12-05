#!/bin/bash
import os

import discord
from discord.ext import commands

from qabc.qubit import Qubit


if __name__ == "__main__":
    TOKEN = os.environ.get('QUBIT_TOKEN', None)

    assert TOKEN is not None
    client = Qubit(
        case_insensitive=True,
        strip_after_prefix=True,
        intents=discord.Intents.all(),
    )
    client.run(TOKEN)



