import sys
import tinify


def main():
    tinify.key = sys.argv[1]
    try:
        tinify.validate()
        print(sys.argv[1])
    except tinify.Error:
        print("ERROR")


if __name__ == "__main__":
    main()
