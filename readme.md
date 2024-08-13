# Sumerian dictionary with faceted tagging

Emedict is a dictionary of the Sumerian language; its main features are
1. The ability to tag each entry with an arbitrary number of categorized tags
1. The separation of each "word" into a lemma with an arbitrary number of optionally categorized forms.
    * For most parts of speech, only one uncategorized form is necessary. A noun like *ninda* will only have a single form.
    * For verbs, forms minimally represent ḫamtû and marû forms. Forms can have mutliple types to capture the distribution of more complex suppletive verbs such as ŋen/du/sub/ere or dug/e/di.

To get started, run `install.sh`. This script will create a virtual environment for Python, install the necessary packages, and load the data into the site.

Currently this web app is designed to be run locally, as it depends on the user being able to access the admin pages of each entry. Future versions will be made suitable to run on public servers.

Initial lexicographical data come from the Electronic Pennsylvania Sumerian Dictionary (ePSD2; http://oracc.iaas.upenn.edu/epsd2/).
