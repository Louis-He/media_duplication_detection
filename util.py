class DEBUG_LEVEL:
    none = 0
    warning = 1
    info = 2
    debug = 3
    debug_verbose = 4
    debug_super_verbose = 5
    all = 6

GLOBAL_DEBUG_LEVEL = DEBUG_LEVEL.debug


def msg_debug(level, *args):
    if level <= GLOBAL_DEBUG_LEVEL:
        if level == DEBUG_LEVEL.warning:
            print("[Warning]", end=" ")
        elif level == DEBUG_LEVEL.info:
            print("[Info]", end=" ")
        else:
            print("[DEBUG]", end=" ")

        print(*args)
