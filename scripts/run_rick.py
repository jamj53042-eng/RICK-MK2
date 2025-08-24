from rick.core.rick import Rick

def main():
    rick = Rick()
    rick.boot()

    # Demo loop
    while rick.alive:
        try:
            user_input = input('>> ').strip()
            if user_input:
                rick.commands.run(user_input)
        except KeyboardInterrupt:
            rick.shutdown()
            break

if __name__ == '__main__':
    main()
