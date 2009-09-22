def get_uuid():
    import uuid
    return str(uuid.uuid4())

def get_user_name(user):
    default_name = "%s %s" % (user.first_name, user.last_name)
    if default_name.strip():
        default_name = "%s - %s" % (default_name, user.email)
    else:
        default_name = user.email
    return default_name.strip()
