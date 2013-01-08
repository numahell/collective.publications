from five import grok
from zope import schema
from zope.interface import implements, alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from Products.ATContentTypes.interfaces.file import IATFile

from plone.app.dexterity.behaviors.metadata import IDublinCore

from plone.formwidget.autocomplete import AutocompleteFieldWidget
try:
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines.textlines import TextLinesFieldWidget

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from collective.publications import MessageFactory as _

class IPublication(form.Schema):

    dcterm_abstract = RichText(
            title=_(u"Abstract"),
            description=_(u"A short summary of the content."),
            required=False,
        )

    creators = schema.Tuple(
        title = _(u'label_creators', u'Creators'),
        description = _(u'help_creators',
                          default=u"Persons responsible for creating the content of "
                                   "this item. Please enter a list of user names, one "
                                   "per line. The principal creator should come first."),
        value_type = schema.TextLine(),
        required = False,
        missing_value = (),
        )
    form.widget(creators = TextLinesFieldWidget)
    
    dcterm_issue = schema.TextLine(
            title=_(u"Issue"),
            description=_(u"Publication issue."),
            required=False,
        )

    number_of_pages = schema.Int(
        title=_(u"Number of pages"),
        required=False,
        )
        
    dcterm_bibliographicCitation = schema.TextLine(
            title=_(u"Bibliographic citation"),
            required=False,
        )

    cover = NamedBlobImage(
            description=_(u"Cover picture."),
            required=False,
            title=_(u"Cover"),
    )

alsoProvides(IPublication, form.IFormFieldProvider)
    
class Publication(dexterity.Container):
    grok.implements(IPublication)


class View(grok.View):
    grok.context(IPublication)
    grok.require('zope2.View')

    grok.name('view')
    
    def getFiles(self):
        """Return the files contained in the publication."""
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=IATFile.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title')