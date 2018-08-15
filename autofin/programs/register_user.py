import argparse

from autofin import user


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Registers a new user.")

    parser.add_argument(
        "--first-name", dest="first_name", action="store", required=True
    )
    parser.add_argument(
        "--middle-name", dest="middle_name", action="store", default="", required=False
    )
    parser.add_argument("--last-name", dest="last_name", action="store", required=True)
    parser.add_argument("--email", dest="email", action="store", required=True)
    parser.add_argument("--password", dest="password", action="store", required=True)
    parser.add_argument(
        "--phone-number", dest="phone_number", action="store", required=False
    )

    args = parser.parse_args()
    user.create(
        args.first_name,
        args.middle_name,
        args.last_name,
        args.email,
        args.password,
        args.phone_number,
    )
