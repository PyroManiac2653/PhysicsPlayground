import nextcord

def cmd_has_bot_role (ctx, roles, error_handler = None):
    def decorator_has_bot_role(func):
        @functools.wraps(func)
        def wrapper_has_bot_role(ctx, *args, **kwargs):
            member = ctx.author
            if not any (member.roles in []):
                if error_handler != None:
                    error_handler()
                else:
                    raise Exception("Unauthorized")
            return func(*args, **kwargs)
        return wrapper_has_bot_role
    return decorator_has_bot_role

def cmd_mod_only (user, error_handler=None):
    return has_bot_role(user, ["moderator"], error_handler)