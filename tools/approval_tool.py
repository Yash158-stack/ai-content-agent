def approval_step(content: str):
    print("\nGenerated Content:\n")
    print(content)

    while True:
        choice = input("\nApprove? (y = yes / e = edit / n = reject): ").lower()

        if choice == "y":
            return content

        elif choice == "e":
            user_edit = input("\nEnter your changes:\n")
            return content + "\n\n" + user_edit

        elif choice == "n":
            print("Content rejected.")
            return None

        else:
            print("Invalid input. Try again.")