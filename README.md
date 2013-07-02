User definable forms with CKEditor
==================================

The POC uses Django 1.2.4. 

You'll need to tweak the hardcoded paths in settings.py and urls.py, and put a version of CKEditor in /static/ckeditor. This code was first written early 2011, so there might be some config/setting changes to get CKEditor loaded also.

This is a proof of concept app. I shoved a lot of stuff into one place, and it's a little hacky. You'll be able to break it if you try. 

Django HTML used in an app is called a "template". To reduce name confusion, I called the user created templates-from-documents "user forms" in this application.

The basic idea is to use the left side to enter a "document" and replace any needed areas with placeholders using the [[placeholder]] markup. Note that this POC app requires a placeholder to have only alphanumeric or underscores in the name (no spaces or other special chars). Placeholder names breaking this rule are ignored and treated as text (won't be treated as a form field).

You can then give this document a title (required) and save it as a user form (i.e., template). It will then appear in the list on the right hand side. Choose a user form from the list and you'll see your original document with form fields for input instead of placeholders. You can enter data into these fields and save this form to the database. After saving, you'll see what the completed form looks like with the filled in data at the bottom of the right pane.

Note that I use eval() to get the fields dictionary back out of the definition in the db. Perhaps not something you'd want to do in production. In general, there are questions of user trust with this kind of application.

