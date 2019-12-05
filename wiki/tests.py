from django.test import TestCase

from django.test import TestCase, Client
from django.contrib.auth.models import User
from wiki.models import Page

#Unit test, one thing: dates, length, slug, username
#Integration test, test lots of things. status codes

class WikiTestCase(TestCase):
    def test_true_is_true(self):
        """ Tests that True == True """
        self.assertEqual(True, True)

    def test_page_slugify_on_save(self):
        """ Tests the slug generated when saving a Page. """
        #Create a user as author is req
        user = User()
        user.save()

        #Create and save a page to DB
        page = Page(title="Test Page", content="test", author=user)
        page.save()
    
        self.assertEqual(page.slug, 'test-page')

class PageListViewTest(TestCase):
    """ Tests that the homepage works. """
    def test_multiple_pages(self):
        #Create a user as Pages; this way saves as one line
        user = User.objects.create()

        Page.objects.create(title="Test Page", content="test", author=user)
        Page.objects.create(title="another Test Page", content="test2", author=user)
        Page.objects.create(title="Crash page", content="test13", author=user)

        #Make a GET request
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

        #Errors look like:
        # AssertionError: 3 != 2
        responses = response.context['pages']
        self.assertEqual(len(responses), 3)

        #Errors look like: 
        # AssertionError: Count[22 chars]': 1, '<Page: another Test Page>': 1, '<Page: Crash page>': 1}) != Count[22 chars]': 1, '<Page: another Test Page>': 1})
        self.assertQuerysetEqual(
            responses, 
            ['<Page: Test Page>', '<Page: another Test Page>'],
            ordered=False
        )