import argparse
import json

import struct_diff


def main():

    parser = argparse.ArgumentParser(description='this is first cli')

    parser.add_argument("first_json_file", help='input first json file')
    parser.add_argument("second_json_file", help='input second json file')
    parser.add_argument("-s", "--syntax", action="store", type=str, default="compact")
    # parser.add_argument("-i", "--indent", action="store", type=int, default=None)
    # parser.add_argument("x", type=int)
    # parser.add_argument("second", help='second file')
    parser.add_argument('-v', '--version', help='版本号', action="store_true")

    args = parser.parse_args()

    # y = args.x
    # z=y**3+y+1
    # print(z)

    if args.version:
        print("0.1.0")

    if args.syntax:
        print(args.syntax)

    # if args.indent:
    #     print(args.indent)

    if args.first_json_file:
        with open(args.first_json_file, "r",  encoding='utf-8') as f:
            with open(args.second_json_file, "r",  encoding='utf-8') as s:
                f = f.read()
                s = s.read()
                first_json_file = json.loads(f)
                second_json_file = json.loads(s)
                x = struct_diff.diff(
                    first_json_file,
                    second_json_file
                )
                print(x)


if __name__ == '__main__':
    main()