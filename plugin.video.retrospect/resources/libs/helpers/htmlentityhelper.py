#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/
# or send a letter to Creative Commons, 171 Second Street, Suite 300,
# San Francisco, California 94105, USA.
#===============================================================================
import re
import urllib
import htmlentitydefs

from logger import Logger


class HtmlEntityHelper(object):
    """Used for HTML converting"""

    def __init__(self):
        """Initialises the class"""

        raise NotImplementedError("Just statics")

    @staticmethod
    def strip_amp(data):
        """Replaces the "&amp;" with "&"


        :param str data:     Data to search and replace in.

        :return: The data with replaced values.
        :rtype: str

        """

        return data.replace("&amp;", "&")

    @staticmethod
    def convert_html_entities(html):
        """Convert the HTML entities into their real characters

        :param str|None html: The HTML to convert.

        :return: The HTML with converted characters.
        :rtype: str

        """

        try:
            return HtmlEntityHelper.__convert_html_entities(html)
        except:
            Logger.error("Error converting: %s", html, exc_info=True)
            return html

    @staticmethod
    def url_encode(url):
        """Converts an URL in url encode characters

        :param str url: The data to URL encode.

        :return: Encoded URL like this. Example: '/~connolly/' yields '/%7econnolly/'.
        :rtype: str

        """

        if isinstance(url, unicode):
            Logger.trace("Unicode url: %s", url)
            return urllib.quote(url.encode())
        else:
            # this is the main time waster
            return urllib.quote(url)

    @staticmethod
    def url_decode(url):
        """Converts an URL encoded text in plain text

        :param str url:     The URL encoded text to decode to decode.

        :return: Decoded URL like this. Example: '/%7econnolly/' yields '/~connolly/'.
        :rtype: str

        """

        return urllib.unquote(url)

    @staticmethod
    def __convert_html_entities(html):
        """Convert the entities in HTML using the HTMLEntityConverter into
        their real characters.

        :param str html: The HTML to convert

        :return: The HTML with converted characters
        :rtype: str

        """

        return re.sub(r"&(#?x?)(\w+?);", HtmlEntityHelper.__html_entity_converter, html)

    @staticmethod
    def __html_entity_converter(entity):
        """Substitutes an HTML entity with the correct character

        :param re.MatchObject entity: Value of the HTML entity without the '&'

        :rtype: str
        :return: Replaces &#xx where 'x' is single digit, or &...; where '.' is a
        character into the real character. That character is returned.

        """

        # Logger.Debug("1:%s, 2:%s", entity.group(1), entity.group(2))
        try:
            if entity.group(1) == "#":
                # Logger.Trace("%s: %s", entity.group(2), chr(int(entity.group(2))))
                return unichr(int(entity.group(2), 10))

            elif entity.group(1) == "#x":
                # check for hex values
                return unichr(int(entity.group(2), 16))

            elif entity.group(2) == 'apos':
                # this one is not covert in name2codepoint
                return "'"

            else:
                # Logger.Trace("%s: %s", entity.group(2), htmlentitydefs.name2codepoint[entity.group(2)])
                return unichr(htmlentitydefs.name2codepoint[entity.group(2)])
        except:
            Logger.error("Error converting HTMLEntities: &%s%s", entity.group(1), entity.group(2), exc_info=True)
            return '&%s%s;' % (entity.group(1), entity.group(2))
