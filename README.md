# WoVBot
A discord bot made for WoW Classic Guilds.  Made with <3 by Swooperior!

## Commands

### DKP System
#### Admin / Officer Commands:
!givedkp <@User> <Amt>
Gives x dkp to the user.

!takedkp <@User> <Amt>
Takes x dkp from the user.

!dkp_a
Shows all players DKP balances.

----------
#### User Commands:

!setmain <Character Name>
Sets the player's main toon name in the database.

!dkp
Shows your current dkp balance

!transferdkp <@User> <Amt>
Transfers amount to the given user.

### Guild Events System
Allows guild officers to create guild events (Raids, dungeon runs etc) and will notify players that join the event when the event is about to start.

#### Administrator / Officer Commands:

!newEvent <Event Name> <Event start time> <Event end time> <Max Players> <Event Description>
Returns the event ID after event has been created.

!cancelEvent <Event ID>
Cancels the event at the given ID.

!completeEvent <Event ID>
Completes the event at the given ID.

----------
#### User Commands:

!joinEvent <Event ID>
Joins the event at the given ID.

!leaveEvent <Event ID>
Removes you from the event at the given ID.

 
### ClassicDB System (Originally by Mikestr8s)
The code contained in the ClassicDB cog is mostly writted by Mikestr8, however has been adapted and cogified by myself.

Usage:
!classicdb <Database> <Search Query>

Example:
Looking for 'Blizzard'
!classicdb spell Blizzard

Looking for 'Thunderfury'
!classicdb item Thunderfury