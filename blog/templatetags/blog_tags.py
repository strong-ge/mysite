from django import template
import mistune, markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class HighlightMixin(object):
    def block_code(self, text, lang):
        # renderer has an options
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inlinestyles, linenos)


class TocRenderer(HighlightMixin, mistune.Renderer):
    pass


@register.filter
def markdown_list(value):
    renderer = TocRenderer(linenos=False, inlinestyles=False)
    mdp = mistune.Markdown(escape=True, renderer=renderer)
    # print mdp(value)
    return mdp(value)


@register.filter
def markdown_detail(value):
    renderer = TocRenderer(linenos=True, inlinestyles=False)
    mdp = mistune.Markdown(escape=True, renderer=renderer)
    # print mdp(value)
    return mdp(value)