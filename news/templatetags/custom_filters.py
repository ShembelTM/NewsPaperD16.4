from django import template

register = template.Library()


bad_words = [
        "редиска",
        "плохой",
        "неприличный",
        'статьи'
    ]


@register.filter()
def censor(text):
    for bad_word in bad_words:
        if bad_word in text:
            filtered_word = bad_word[0] + "*" * (len(bad_word) - 1)
            text = text.replace(bad_word, filtered_word)

    return text