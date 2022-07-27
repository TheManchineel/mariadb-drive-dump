from cryptography.fernet import Fernet


def new_key():
    return Fernet.generate_key()


if __name__ == "__main__":
    print("Generating key...\n")
    key = new_key().decode()

    print(
        "=" * (len(key) + 10) + "\n" + "Your key: " + key + "\n" + "=" * (len(key) + 10)
    )

    print("\nNow you can copy the key to the config file.")
