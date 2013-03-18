import os
import random
import time
from behave import when, then
from behaving.personas.persona import persona_vars


@when(u'I fill in "{name}" with "{value}"')
@persona_vars
def i_fill_in_field(context, name, value):
    context.browser.fill(name, value)


@when(u'I type "{value}" to "{name}"')
@persona_vars
def i_type_to(context, name, value):
    for key in context.browser.type(name, value, slowly=True):
        assert key


@when(u'I slowly type "{value}" to "{name}"')
@persona_vars
def i_slowly_type_to(context, name, value):
    for key in context.browser.type(name, value, slowly=True):
        assert key
        time.sleep(random.random() * 0.15)


@when(u'I choose "{value}" from "{name}"')
@persona_vars
def i_choose_in_radio(context, name, value):
    context.browser.choose(name, value)


@when(u'I check "{name}"')
def i_check(context, name):
    context.browser.check(name)


@when(u'I uncheck "{name}"')
def i_uncheck(context, name):
    context.browser.uncheck(name)


@when(u'I select "{value}" from "{name}"')
@persona_vars
def i_select(context, value, name):
    context.browser.select(name, value)


@when(u'I press "{name}"')
def i_press(context, name):
    button = context.browser.find_by_id(name) or \
             context.browser.find_by_name(name) or \
             context.browser.find_by_xpath("//button[text()='%s']" % name) or \
             context.browser.find_by_xpath("//button[contains(text(), '%s')]" % name) or \
             context.browser.find_link_by_text(name) or \
             context.browser.find_link_by_partial_text(name)
    assert button, u'Element not found'
    button.mouseover()
    # Go figure why checking for button.first is necessary, but it seems to be for elements
    #that listen to onclick and change somehow
    if button.first:
        button.first.click()


@when(u'I press the element with xpath "{xpath}"')
def i_press_xpath(context, xpath):
    button = context.browser.find_by_xpath(xpath)
    assert button, u'Element not found'
    button.first.click()


@when('I attach the file "{path}" to "{name}"')
@persona_vars
def i_attach(context, name, path):
    if not os.path.exists(path):
        path = os.path.join(context.attachment_dir, path)
        if not os.path.exists(path):
            assert False
    context.browser.attach_file(name, path)


@when('I set the inner HTML of the element with id "{id}" to "{contents}"')
def set_html_content_to_element_with_id(context, id, contents):
    assert context.browser.evaluate_script("document.getElementById('%s').innerHTML = '%s'" % (id, contents)), u'Element not found or could not set HTML content'


@when('I set the inner HTML of the element with class "{klass}" to "{contents}"')
def set_html_content_to_element_with_class(context, klass, contents):
    assert context.browser.evaluate_script("document.getElementsByClassName('%s')[0].innerHTML = '%s'" % (klass, contents)), u'Element not found or could not set HTML content'


@then(u'field "{name}" should have the value "{value}"')
@persona_vars
def field_has_value(context, name, value):
    el = context.browser.find_by_id(name) or \
         context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert el.first.value == value, "Values do not match"


@then(u'"{name}" should be enabled')
def is_enabled(context, name):
    el = context.browser.find_by_id(name) or \
         context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert el.first._element.is_enabled()


@then(u'"{name}" should be disabled')
def is_disabled(context, name):
    el = context.browser.find_by_id(name) or \
         context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert not el.first._element.is_enabled()


@then(u'field "{name}" should be valid')
def field_is_valid(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert context.browser.evaluate_script("document.getElementsByName('%s')[0].checkValidity()" % name), \
        'Field is invalid'


@then(u'field "{name}" should be invalid')
@then(u'field "{name}" should not be valid')
def field_is_invalid(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert not context.browser.evaluate_script("document.getElementsByName('%s')[0].checkValidity()" % name), \
        'Field is valid'