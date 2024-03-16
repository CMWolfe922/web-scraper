#! /usr/bin/python

from __future__ import absolute_import, division, print_function
from builtins import *

import sys
import json
from http.server import BaseHTTPRequestHandler
from io import StringIO
import os
# import ColorizePython
import mimetypes


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        # request_text = str(request_text).encode('utf-')
        request_text = request_text.decode('utf-8')
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1000.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, 'Yb', suffix)


def loadConfig(fileName):
    try:
        with open(fileName, 'r') as d:
            jsn = json.load(d)
            jsn['PUBLIC_HTML'] = os.path.normpath(
                jsn['PUBLIC_HTML'])  # Normalize path
            jsn['ERROR_DIR'] = os.path.normpath(
                jsn['ERROR_DIR'])  # Normalize path
            jsn['OTHER_TEMPLATES'] = os.path.normpath(
                jsn['OTHER_TEMPLATES'])  # Normalize path
            return jsn
    except IOError:
        print("Error: File does not appear to exist.")
        sys.exit(1)
    except ValueError:
        print("Error: Config file format not correct.")
        sys.exit(1)
    except:
        print("Error: Something went wrong trying to load the settings.")
        sys.exit(1)


# def colorizeLog(shouldColorize, log_level, msg):
#     # Higher is the log_level in the log() argument, the lower is its priority.
#     colorize_log = {
#         "NORMAL": ColorizePython.pycolors.ENDC,
#         "WARNING": ColorizePython.pycolors.WARNING,
#         "SUCCESS": ColorizePython.pycolors.OKGREEN,
#         "FAIL": ColorizePython.pycolors.FAIL,
#         "RESET": ColorizePython.pycolors.ENDC
#     }
#
#     if shouldColorize.lower() == "true":
#         if log_level in colorize_log:
#             return colorize_log[str(log_level)] + msg + colorize_log['RESET']
#         return colorize_log["NORMAL"] + msg + colorize_log["RESET"]
#     return msg
#
#
# def guessMIME(filename):
#     return mimetypes.guess_type(filename)[0]
#

def isvalidPath(location):
    """ Check if file/directory exists """
    if os.path.exists(location):
        return True
    return False


def isvalidFile(location):
    """ Check if file exists """
    if isvalidPath(location) and os.path.isfile(location):
        return True
    return False


def isvalidDirectory(location):
    """ Check if directory exists """
    if (isvalidPath(location)) and (not os.path.isfile(location)):
        return True
    return False


def isReadable(location):
    """ Check if file/directory is readable """
    if os.access(location, os.R_OK):
        return True
    return False


# Add the HTML Elements and Attribute Dictionary in here:
# Create a method to check the elements and attributes lists to see if the user
# put a valid element or attribute in the input prompt:
# If the element is valid, continue to the next step

element_attribute_examples = {
    'Elements': [
        "!DOCTYPE", "html", "head", "title", "base", "link", "meta", "style", "script", "noscript", "body", "section",
        "nav",
        "article", "aside", "h1", "h2", "h3", "h4", "h5", "h6", "header", "footer", "address", "main", "p", "hr", "pre",
        "blockquote", "ol", "ul", "li", "dl", "dt", "dd", "figure", "figcaption", "div", "a", "em", "strong", "small",
        "s", "cite",
        "q", "dfn", "abbr", "ruby", "rt", "rp", "data", "time", "code", "var", "samp", "kbd", "sub", "sup", "i", "b",
        "u",
        "mark", "bdi", "bdo", "span", "br", "wbr", "ins", "del", "image", "img", "iframe", "embed", "object", "param",
        "video",
        "audio", "source", "track", "canvas", "map", "area", "svg", "math", "table", "caption", "colgroup", "col",
        "tbody", "thead",
        "tfoot", "tr", "td", "th", "form", "fieldset", "legend", "label", "input", "button", "select", "datalist",
        "optgroup", "option",
        "textarea", "keygen", "output", "progress", "meter", "details", "summary", "menu", "menuitem", "dialog"
    ],
    'Attributes': [
        "id", "class", "style", "title", "alt", "src", "href", "target", "rel", "type", "value", "name", "placeholder",
        "disabled", "checked", "readonly", "selected", "multiple", "required", "pattern", "min", "max", "step",
        "data-*",
        "aria-*", "role", "async", "defer", "srcset", "sizes", "hreflang", "charset", "autofocus", "autocomplete",
        "novalidate",
        "method", "action", "enctype", "formmethod", "formaction", "headers", "for", "form", "width", "height",
        "frameborder",
        "allow", "allowfullscreen", "autoplay", "loop", "muted", "controls", "download", "accesskey", "contenteditable",
        "dir",
        "draggable", "hidden", "lang", "spellcheck", "tabindex", "translate", "reversed", "start", "colspan", "rowspan",
        "headers",
        "scope", "align", "nowrap", "border", "cellpadding", "cellspacing", "summary", "usemap", "shape", "coords",
        "poster",
        "preload", "kind", "srclang", "sandbox", "integrity", "crossorigin", "referrerpolicy", "loading"
    ],
}

xpath_examples={
    "Select all elements with `//tagName`": '`//tagName`',
    "Select all elements with `//tagName` with `attribute` with specific `value`: ": "`//tagName[@attribute='value']`",
    "Select all elements with `//tagName` containing specific 'text content': ": "`//tagName[contains(text(),'text content')]`",
    "Select nth `tagName` element in doc: ": '`//tagName[position()=n]`',
    "Select first|last `childTagName` within `parentTagName`: ": '`//parentTagName/childTagName[1]` or `//parentTagName/childTagName[last()]`',
    "Select elements that `attribute` = 'substring': ": "`//tagName[contains(@attribute, 'substring')]`",
    "Select `tagName` ancestor|sibling element, showcasing XPath axes to navigate element relationships: ": '`//tagName/ancestor::ancestorTagName` or `//tagName/following-sibling::siblingTagName`',
    "Use logical operators (and, or) to select elements that meet multiple conditions: ": "`//tagName[@attribute1='value1' and @attribute2='value2']`",
    "Selects all tags with `className`, accounting for potential multiple class names.": "`//*[contains(concat(' ', normalize-space(@class), ' '), ' className ')]`",
    "Select elements without certain `attribute` or select 'attribute' that exceeds the len of `n`( demonstrating the use of XPath functions for more complex filtering) :": '`//tagName[not(@attribute)]` or `//tagName[string-length(@attribute) > n]`'
}

def check_html_elements_and_attributes(html_dict:dict, user_input):
    """ Check if the user input is a valid HTML element or attribute """
    for key in html_dict:
        if user_input in html_dict[key]:
            return True
    return False
