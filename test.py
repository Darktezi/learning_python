from migration import *
from currencies_controller import *

def main():
    names = CC.get_all_names()
    print(names)
if __name__ == "__main__":
    main()