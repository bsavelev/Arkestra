from django import template
from django.db.models import Q
from django.template import loader, Context
from contacts_and_people.templatetags.entity_tags import entity_for_page, work_out_entity
from datetime import datetime
from news_and_events.models import NewsArticle

register = template.Library()

@register.simple_tag(takes_context=True)
def news(context, format="all_info", max_items=20, entity=None, template='newslist.html'):
    """
    Publishes a date-ordered list of news items
    """
    if not entity:
        entity = work_out_entity(context, entity)
    news = NewsArticle.objects.filter(
        Q(hosted_by=entity)|Q(publish_to=entity),
        date__lte=datetime.now()
    )[0: max_items]
    t = loader.get_template(template)
    c = Context({
        'entity': entity,
        'news': news,
        'format': format,
    })
    return t.render(c)

@register.inclusion_tag('newslist.html', takes_context=True)
def news_for_this_page(context, max_items):
    request=context['request']
    page = request.current_page
    entity = entity_for_page(page)
    if entity:
        news = NewsArticle.objects.filter(
            Q(hosted_by=entity)|Q(publish_to=entity),
            date__lte=datetime.now()
        )[0: max_items]
        return {
            'news': news,
        }
    else:
        return {
            'news': "No news is good news",
        }
