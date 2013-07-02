from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from userforms.models import UserForm, CompletedUserForm, CUFData
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
import re

# this code is not intended to be safe, not at all. this is proof of concept
# for internal use only.

def index(request, user_form_id=None):
    d = {}
    titles = dict([(uf.id, uf.title,) for uf in UserForm.objects.all()])
    d['titles'] = titles

    if user_form_id:
        d['user_form_id'] = int(user_form_id)
        d['user_form_html'] = get_user_form_html(user_form_id)

    cuf_id = request.session.get('new_cuf_id', 0)
    if cuf_id > 0:
        d['cuf_html'] = get_completed_user_form_html(cuf_id) 
        request.session['new_cuf_id'] = 0

    cuf_errors = request.session.get('cuf_errors', '')
    if cuf_errors:
        d['cuf_errors'] = cuf_errors 
        request.session['cuf_errors'] = ''

    return render_to_response('index.html', d) 

@csrf_exempt
def new_user_form(request):
    title = request.POST.get('title', '').strip()
    html = request.POST.get('uf_html', '')
    fields = get_ph_fields_from_html(html)
    
    if (not fields.keys() or not title):
        d = {}
        # probly should use session, like did with cuf_errors.
        d['uf_errors'] = 'User form must have a form title and at least ' \
            'one valid placeholder in the HTML.'
        
        return render_to_response('index.html', d) 
    else:
        uf = UserForm()
        uf.title = title
        uf.html = html
        uf.fields = str(fields)
        uf.save()

        return HttpResponseRedirect(reverse('ckpoc.userforms.views.index'))

@csrf_exempt
def complete_user_form(request):
    ufid = request.POST.get('ckpoc_userforms_user_form_id', '0')
    to_index = reverse('ckpoc.userforms.views.index', 
            kwargs={'user_form_id': ufid})
    try: 
        uf = UserForm.objects.get(pk=ufid)
        fields = eval(uf.fields)
        dbinsert = {}
        for field in fields.keys():
            val = request.POST.get(field, '')
            if val:
                dbinsert[field] = val
        #not bothering with tran for proof of concept.
        if dbinsert:
            cuf = CompletedUserForm()
            cuf.UserForm = uf
            cuf.save()
            for field in dbinsert.keys():
                cufd = CUFData()
                cufd.CompletedUserForm = cuf
                cufd.field = field
                cufd.value = dbinsert[field]
                cufd.save()
            request.session['new_cuf_id'] = cuf.id

            return HttpResponseRedirect(to_index)
        else:
            request.session['cuf_errors'] = 'POC app requires at least one ' \
                + 'completed field for user forms.'
            return HttpResponseRedirect(to_index)
    except UserForm.DoesNotExist:
        request.session['cuf_errors'] = 'Could not find user form with id ' \
                + ufid + '.'
        return HttpResponseRedirect(to_index)

def get_ph_fields_from_html(html):
    # if invalid chars in placeholder, ignore that PH completely. 
    phs = re.findall(r'\[\[(?P<field>\w+)\]\]', html) 
    fields = {}
    for f in phs:
        if f in fields:
            return {}     # no dupe field names allowed, send {}, i.e. failure. 
        else:
            fields[f] = 'text'  # later, might do more complex options.

    return fields

def get_user_form_html(user_form_id):
    try: 
        uf = UserForm.objects.get(pk=user_form_id)
        html = uf.html
        fields = eval(uf.fields)

        for field in fields.keys():
            #if we don't make field dict values meaningful, use fields list instead.
            ph = '[[' + field + ']]'
            ff = '<input type="text" name="' + field + '" />'
            html = html.replace(ph, ff)

        return html
    except UserForm.DoesNotExist:
        return ''

def get_completed_user_form_html(cuf_id):
    try:
        cuf = CompletedUserForm.objects.get(pk=cuf_id)
        cufds = CUFData.objects.filter(CompletedUserForm=cuf)
        dbvalues = dict([(f.field, f.value,) for f in cufds])
        uf_fields = eval(cuf.UserForm.fields)
        uf_html = cuf.UserForm.html

        for field in uf_fields.keys():
            ph = '[[' + field + ']]'
            if field in dbvalues:
                uf_html = uf_html.replace(ph, escape(dbvalues[field]))
            else:
                uf_html = uf_html.replace(ph, '')

        return uf_html

    except CompletedUserForm.DoesNotExist:
        return ''

