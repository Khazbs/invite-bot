ERROR_UNKNOWN_COMMAND = 'Command `{}` is unknown, please check out the **help** section to see available commands.\n'
ERROR_NOT_SELECTED = 'No invite code selected, please **select** an existing one or **create** a new one.\n'
ERROR_CODE_MISSING = 'Invite code not specified, please write which code to **select**.\n'
ERROR_NOT_FOUND = 'Invite code `{}` not found, please **list all** codes to look for an existing one or **create** a new one.\n'
ERROR_NO_INVITES = 'No invite codes yet... a great time to **create** one!\n'
ERROR_EXISTS = 'Invite code `{}` already exists, please choose another code or leave it blank to generate one.\n'
ERROR_ACTIVE = 'Invite code `{}` is already active, maybe you want to **deactivate** it?\n'
ERROR_INACTIVE = 'Invite code `{}` is already inactive, maybe you want to **activate** it?\n'
ERROR_NUMBER = '`{}` is not a valid number of users, it must be a natural number, e.g. 1, 2, 3...\n'
ERROR_DATETIME = '`{}` was not recognized as date or time, please try to write it in another way.\n'
ERROR_SERVER = 'Sorry, something went wrong on our end, please try again later.'

SUCCESS_CREATE = 'Invite code `{}` created, selected.\n\nYou can **limit** its number of users, set its time to **begin** or **expire**, and **activate** it.'
SUCCESS_SELECT = 'Invite code `{}` selected.\n\nCheck out the **help** section to see what you can do with it.'
SUCCESS_ACTIVATE = 'Invite code `{}` activated.\n\nIf you need, you can **deactivate** it.'
SUCCESS_DEACTIVATE = 'Invite code `{}` deactivated.\n\nIf you need, you can **activate** it.'
SUCCESS_BEGIN = 'Invite code `{}` will begin working at {}.\n\nIf you need, you can set it to **begin anytime**.'
SUCCESS_BEGIN_ANYTIME = 'Invite code `{}` will begin working anytime.\n\nIf you need, you can set it to **begin** at certain time.'
SUCCESS_EXPIRE = 'Invite code `{}` will expire at {}.\n\nIf you need, you can set it to **never expire**.'
SUCCESS_NEVER_EXPIRE = 'Invite code `{}` will never expire.\n\nIf you need, you can set it to **expire** at certain time.'
SUCCESS_LIMIT = 'Invite code `{}` will work for {} users.\n\nIf you need, you can **unlimit** this number.'
SUCCESS_UNLIMIT = 'Invite code `{}` will work for any number of users.\n\nIf you need, you can **limit** this number.'

PURPOSE_CREATE = '**Create** and select a new invite code, either specified, or generated if left blank.'
PURPOSE_SELECT = '**Select** an existing invite code to modify.'
PURPOSE_ACTIVATE = '**Activate** the selected invite code to allow its usage.'
PURPOSE_DEACTIVATE = '**Deactivate** the selected invite code to suspend its usage.'
PURPOSE_BEGIN = 'Set the date and time for the selected invite code to **begin** working.'
PURPOSE_BEGIN_ANYTIME = 'Set the selected invite code to **begin** working **anytime** without the time limitation.'
PURPOSE_EXPIRE = 'Set the date and time for the selected invite code to **expire** and stop working.'
PURPOSE_NEVER_EXPIRE = 'Set the selected invite code to **never expire** and continue working without the time limitation.'
PURPOSE_LIMIT = '**Limit** the selected invite code to only work for a certain number of users.'
PURPOSE_UNLIMIT = 'Set the selected invite code to work for an **unlimit**ed number of users.'
PURPOSE_LIST_ALL = '**List all** existing invite codes in order of their creation.'
PURPOSE_HELP = 'How did you open this **help** section, you reckon?'

USAGE_CREATE = '\nUsage: `!create` or `!create <code>`, e.g. `!create IDDQD1337`'
USAGE_SELECT = '\nUsage: `!select <code>`, e.g. `!select IDDQD1337`'
USAGE_ACTIVATE = '\nUsage: `!activate`'
USAGE_DEACTIVATE = '\nUsage: `!deactivate`'
USAGE_BEGIN = '\nUsage: `!begin <datetime>`, e.g. `!begin tomorrow at 00:00 UTC` or `!begin on September 8`'
USAGE_BEGIN_ANYTIME = '\nUsage: `!begin_anytime`'
USAGE_EXPIRE = '\nUsage: `!expire <datetime>`, e.g. `!expire on Friday` or `!expire on October 31 at 18:00 MSK`'
USAGE_NEVER_EXPIRE = '\nUsage: `!never_expire`'
USAGE_LIMIT = '\nUsage: `!limit <n_users>`, e.g. `!limit 10`'
USAGE_UNLIMIT = '\nUsage: `!unlimit`'
USAGE_LIST_ALL = '\nUsage: `!list_all`'
USAGE_HELP = '\nUsage: `!help`'

INVITE_GUILD = 'Want to become a verified member? React in this channel and DM me your invite code to receive the role!'
INVITE_DM = 'Hello! Want to become a verified member on `{}`? Send me your invite code to receive the role!'
INVITE_VALID = 'Congratulations! You have just become a verified member.'
INVITE_INVALID = 'Sorry! This invite code is not valid.'


def invite_guild():
	return (INVITE_GUILD)


def invite_dm(guild_name):
	return (INVITE_DM.format(guild_name))


def invite_valid():
	return (INVITE_VALID)


def invite_invalid():
	return (INVITE_INVALID)


def error_unknown_command(command):
	return (ERROR_UNKNOWN_COMMAND.format(command)
		+ USAGE_HELP)


def error_not_selected():
	return (ERROR_NOT_SELECTED
		+ USAGE_SELECT
		+ USAGE_CREATE)


def error_code_missing():
	return (ERROR_CODE_MISSING
		+ USAGE_SELECT)


def error_not_found(code):
	return (ERROR_NOT_FOUND.format(code)
		+ USAGE_LIST_ALL
		+ USAGE_CREATE)


def error_exists(code):
	return (ERROR_EXISTS.format(code)
		+ USAGE_CREATE)


def error_active(code):
	return (ERROR_ACTIVE.format(code)
		+ USAGE_DEACTIVATE)


def error_inactive(code):
	return (ERROR_INACTIVE.format(code)
		+ USAGE_ACTIVATE)


def error_begin_datetime(dt_string):
	return (ERROR_DATETIME.format(dt_string)
		+ USAGE_BEGIN)


def error_expire_datetime(dt_string):
	return (ERROR_DATETIME.format(dt_string)
		+ USAGE_EXPIRE)


def error_limit_number(n_string):
	return (ERROR_NUMBER.format(n_string)
		+ USAGE_LIMIT)


def error_no_invites():
	return (ERROR_NO_INVITES
		+ USAGE_CREATE)


def success_create(code):
	return (SUCCESS_CREATE.format(code)
		+ USAGE_LIMIT
		+ USAGE_BEGIN
		+ USAGE_EXPIRE
		+ USAGE_ACTIVATE)


def error_server():
	return (ERROR_SERVER)


def success_select(code):
	return (SUCCESS_SELECT.format(code)
		+ USAGE_HELP)


def success_activate(code):
	return (SUCCESS_ACTIVATE.format(code)
		+ USAGE_DEACTIVATE)


def success_deactivate(code):
	return (SUCCESS_DEACTIVATE.format(code)
		+ USAGE_ACTIVATE)


def success_begin(code, dt):
	return (SUCCESS_BEGIN.format(code, dt)
		+ USAGE_BEGIN_ANYTIME)


def success_begin_anytime(code):
	return (SUCCESS_BEGIN_ANYTIME.format(code)
		+ USAGE_BEGIN)


def success_expire(code, dt):
	return (SUCCESS_EXPIRE.format(code, dt)
		+ USAGE_NEVER_EXPIRE)


def success_never_expire(code):
	return (SUCCESS_NEVER_EXPIRE.format(code)
		+ USAGE_EXPIRE)


def success_limit(code, n):
	return (SUCCESS_LIMIT.format(code, n)
		+ USAGE_UNLIMIT)


def success_unlimit(code):
	return (SUCCESS_UNLIMIT.format(code)
		+ USAGE_LIMIT)


def help():
	return (
		PURPOSE_CREATE + USAGE_CREATE + '\n\n' +
		PURPOSE_SELECT + USAGE_SELECT + '\n\n' +
		PURPOSE_ACTIVATE + USAGE_ACTIVATE + '\n\n' +
		PURPOSE_DEACTIVATE + USAGE_DEACTIVATE + '\n\n' +
		PURPOSE_BEGIN + USAGE_BEGIN + '\n\n' +
		PURPOSE_BEGIN_ANYTIME + USAGE_BEGIN_ANYTIME + '\n\n' +
		PURPOSE_EXPIRE + USAGE_EXPIRE + '\n\n' +
		PURPOSE_NEVER_EXPIRE + USAGE_NEVER_EXPIRE + '\n\n' +
		PURPOSE_LIMIT + USAGE_LIMIT + '\n\n' +
		PURPOSE_UNLIMIT + USAGE_UNLIMIT + '\n\n' +
		PURPOSE_LIST_ALL + USAGE_LIST_ALL + '\n\n' +
		PURPOSE_HELP + USAGE_HELP
	)
