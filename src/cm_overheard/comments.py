"""Extract comments from tex file
"""
import re

long_comment_regexp = "^\s*(%.*)$"
short_comment_regexp = ".*?(%.*)$"


def long_comments_from_lines(lines):
    # State variable
    comment_started = False
    # Contains current comment
    comment = []
    # Contains list of all comments -- overall output
    result = []

    for line in lines:
        line_is_comment = re.search(long_comment_regexp, line)
        if not comment_started and line_is_comment:
            # beginning of comment
            comment = [line]
            comment_started = True
        elif comment_started and line_is_comment:
            # continuation of comment
            comment.append(line_is_comment.group(1))
        elif comment_started and not line_is_comment:
            # end of comment
            result.append(comment)
            comment_started = False
        elif not comment_started and not line_is_comment:
            # continuation of non-comment
            pass

    return result


def short_comments_from_lines(lines):

    result = []
    for line in lines:
        if not re.search(long_comment_regexp, line):
            match = re.search(short_comment_regexp, line)
            if match:
                result.append(match.group(1))
    return result


def find_tex_files(path):
    # TODO. fix paths
    import glob

    return [tex for tex in glob.iglob(path + "/**/*.tex", recursive=True)]


def get_comments(path_to_tex):

    with open(path_to_tex) as f:
        lines = f.readlines()

    short_comments = short_comments_from_lines(lines)
    long_comments = long_comments_from_lines(lines)

    return short_comments, long_comments


def extract_all(path):
    tex_files = find_tex_files(path)

    for tex in tex_files:
        short, long = get_comments(tex)

        print(short)
        print(long)
