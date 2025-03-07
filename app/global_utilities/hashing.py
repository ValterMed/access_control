from argon2 import PasswordHasher, low_level


def get_password_hasher():
    ph = PasswordHasher(
        time_cost=2,
        memory_cost=19 * 1024,
        parallelism=1,
        hash_len=16,
        salt_len=16,
        type=low_level.Type.D,
    )
    return ph
