def main():
    """Print a Hello, World! message."""
    name = input("Enter your name (leave blank for 'World'): ").strip()
    if not name:
        name = "World"
    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()