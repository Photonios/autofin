import argparse

from autofin import user, models


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configures a creditor for a user.")

    parser.add_argument(
        "--user-id", dest="user_id", action="store", type=int, required=True
    )
    parser.add_argument(
        "--creditor-id", dest="creditor_id", action="store", type=int, required=True
    )
    parser.add_argument("--username", dest="username", action="store", required=True)
    parser.add_argument("--password", dest="password", action="store", required=True)

    args = parser.parse_args()

    user.configure_creditor(
        user=models.User.select().where(models.User.id == args.user_id).first(),
        creditor_id=args.creditor_id,
        username=args.username,
        password=args.password,
    )
