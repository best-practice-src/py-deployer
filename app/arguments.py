from . import settings
from argparse import ArgumentParser, Namespace


def get_arguments() -> Namespace:
    """
    Return the input arguments
    :return: A Namespace
    """
    arg_parser = __get_argument_parser()
    args = arg_parser.parse_args()

    if args.version:
        print('v' + str(settings.VERSION))
        arg_parser.exit(0)

    if not args.stage:
        arg_parser.print_help()
        arg_parser.exit(0)

    return args


def __get_argument_parser() -> ArgumentParser:
    """
    Make a new ArgumentParser
    :return: An ArgumentParser
    """
    argument_parser = ArgumentParser(
        description="[OF - Institutional] City Coverage Update v"+str(settings.VERSION)+" (Py Microservice)\n"
    )
    # --- Optional arguments ---#
    argument_parser.add_argument("-v", "--version", help="show program's version number and exit", action="store_true")
    argument_parser.add_argument("-s", "--stage", help="The stage to deploy", type=str)
    return argument_parser
