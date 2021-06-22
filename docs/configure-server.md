# Configure your Server

You need to configure Cyberon's settings using the cyb!config command. You can see all config commands using `cyb!help config`

- setwarnthresh | setwarnthreshold
Sets the warning threshold for the server, beyond which the member gets banned
Usage: `cyb!setwarnthresh <integer>`

- clearwanthresh(old) | delwarnthresh(old)
Clears the warning threshold of the server
Usage: `cyb!clearwarnthresh`

- serverconfig | config | serversetup | setup
Configures the channels for moderation logging, welcome and depart messages, deleted or edited messages, mute role for muting messages for that role
Usage: `cyb!config`

- showconfig
Shows channels that are for logging
Usage: `cyb!showconfig <args>`
Args can be optional (type help to get a list)

## Resetting a Setting

If you want to change the config settings, re run `cyb!config`.
