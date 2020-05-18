# Microsoft Teams notification plugin for Centreon

## Prerequisite
You must have generate a Incomming Webhook for your MS Teams channel (righ-click on the channel and go to Connectors).

## Installation
* Upload the script to the Centreon plugins directory (`/usr/lib/centreon/plugins/`).
* Go to Centreon / Commands / Notifications.
* Add a notification method called `service-notify-by-msteams` and configure it as below :

``python /usr/lib/centreon/plugins/msteams-notify.py <MSTeams Webhook> '$NOTIFICATIONTYPE$' '$HOSTNAME$' '$HOSTALIAS$' '$HOSTADDRESS$' '$SERVICESTATE$' '$SERVICEOUTPUT$' --service-description='$SERVICEDESC$'``

* Add a notification method called `host-notify-bymsteams` and configure it as below :

``python /usr/lib/centreon/plugins/msteams-notify.py <MSTeams Webhook> '$NOTIFICATIONTYPE$' '$HOSTNAME$' '$HOSTALIAS$' '$HOSTADDRESS$' '$HOSTSTATE$' '$HOSTOUTPUT$'``

* Then add the notifications methods to a single Centreon user with all notifications enabled.
