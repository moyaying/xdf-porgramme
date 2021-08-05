import argparse
import sys
from logistic import handle_data2
from logistic import logistic


def logistic_modules(namespace):
    if namespace.t == "run":
        logistic.run()
    elif namespace.t == "handle_data":
        handle_data2.handle_data()
    else:
        print("please type `-t run` or `-t handle_data`")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="types of logistic")
    logistic_parser = subparsers.add_parser("logistic")
    logistic_parser.add_argument("-t", help="run or handle_data")
    logistic_parser.set_defaults(func=logistic_modules)

    # -db DATABSE -u USERNAME -p PASSWORD -size 20
    # parser.add_argument("-db", "--hostname", help="Database name")
    # parser.add_argument("-u", "--username", help="User name")
    # parser.add_argument("-p", "--password", help="Password")
    # parser.add_argument("-size", "--size", help="Size", type=int)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)
