# Physics Playground Bot
From Tanmay and Pyro

## About

This is a hastily assemble Discord bot made primarily for the PhyiscsPlayground guild.

## Technical Setup Notes

The four segments to set this up are:
- **Python environment**

    To ensure this can be adapted on other machines
- **Application code**

    All in one place:  source code
- **Database file (SQLite)**

    To be kept where you thing best
- **Configuration**
    Some in-app, but also in config files outside app code (to allow for differing environments)

## Function

There are two aspects of functionality that should be meaningful on their own but must work together for the bot to be most useful.

- **Discord interaction**

    Reacting to messages, posting messages, opening threads, and so on.

- **Guild item updates**

    Manually update things like "question of the day" questions, solutions.

- **Guild item interaction** (combining the two)

    Allowing guild staff and guild members to update items and settings through discord interactions
    Guild staff and members should also be able to use the bot to create posts and threads as spaces to update the guild items.

## Wishlist

Some future improvements:

- **Automated Scheduling** - have the bot choose and schedule items from the backlog automatically
- **Notifiacation Overrides** - instead of helpers getting pings for their role, have the bot send them a DM.

    This will extend to providing a collection of pings hourly, including all pings from the last hour if any. The time period doesn't have to be hourly, but can be set otherwise like half hour, three hours, 12 hours, or daily.

    Furthermore, perhaps this can extend to allowing the guild member to use a command to get the latest pings, or DM the bot with a server name (or not) to get those pings.