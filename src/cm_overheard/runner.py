# -*- coding: utf-8 -*-
"""Runner, i.e. code is run from here
"""
import argparse
import sys
import logging

from cm_overheard.fetch import get_today
from cm_overheard.comments import extract_all


_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest="command")

    add_fetch_subparser(subparser)
    add_comments_subparser(subparser)

    return parser.parse_args(args)


def setup_logging(loglevel=logging.INFO):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def add_fetch_subparser(subparser):
    parser = subparser.add_parser("fetch", help="fetch today's articles from arxiv")
    parser.add_argument(
        "-c",
        "--category",
        type=str,
        help="which arxiv category to consider",
        default="cond-mat.str-el",
    )
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help="path to the downloaded articles",
        default="data",
    )


def run_fetch(args):
    get_today(path=args.data)


def add_comments_subparser(subparser):
    parser = subparser.add_parser(
        "comments", help="extract comments from downloaded arxiv articles"
    )
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help="path to the downloaded articles",
        default="data",
    )


def run_comments(args):
    _logger.info("Extract all comments")
    extract_all(path=args.data)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging()

    entry_points = {
        "fetch": run_fetch,
        "comments": run_comments,
    }

    runner = entry_points.get(args.command)
    runner(args)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
