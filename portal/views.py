from django.shortcuts import render
import json
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.sessions.backends.db import SessionStore


def assignment1(request):
    return render(request, 'assignment1.html', {})


def assignment2(request):
    print('yes')
    return render(request, 'assignment2.html', {})


def execute_json_function_1(request):
    request.session.modified = True
    print('yes,', request.session.keys())
    for key in request.session.keys():
        print("key:=>", request.session[key])

    json_file = 'assignment_1_input_1.json'

    count = int(request.POST.get('count'))
    response = request.POST.get('response')

    if response != '' and request.session['previous_var']:
        request.session[request.session['previous_var']] = str(response)

    if count == 1:
        count = request.session.get('count')
    else:
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]

    with open(json_file) as f:
        json_content = json.load(f)

    final_message = {
        'instructions': [],
        'var': '',
        'options': [],
    }

    status = True
    rows = [0, 0, 0]

    while status and len(json_content['questions']) > count:
        query = json_content['questions'][count]
        if 'instruction' in query:
            query_instruction = query['instruction']
            if '%s' in query['instruction']:
                if 'list_length' in query:
                    for i in range(int(query['list_length'])):
                        for var in query['instruction_var']:
                            for key in request.session.keys():
                                if key in var:
                                    print(key)
                                    exec('%s = %s') % (key, request.session.get(key))
                                    query_instruction = query_instruction.replace('%s', request.session.get(key), 1)
                                else:
                                    print(key)
                                    query_instruction = query_instruction.replace('%s', str(eval(var)), 1)
                else:
                    for var in query['instruction_var']:
                        query_instruction = query_instruction.replace('%s', request.session.get(var), 1)
            final_message['instructions'].append(query_instruction)
        elif 'calculated_variable' in query:
            temp_session = request.session.keys()
            for key in temp_session:
                if key == 'rows':
                    continue
                try:
                    exec('%s = %s') % (key, request.session[key])
                except:
                    exec(key + ' = "' + str(request.session[key]) + '"')

            request.session[query['var']] = eval(query['formula'])
            # Load all the session variables because we don't know what is actually used
        elif 'conditions' in query:
            condition_status = False
            exec(query['var'] + ' = "' + request.session[query['var']] + '"')
            for condition in query['conditions']:
                flag = 0
                for statement in condition:
                    print('eval', eval(statement))
                    if not eval(statement):
                        flag = 1
                        break

                # Any statement is true, then the given condition is met
                if flag == 0:
                    condition_status = True
            if condition_status:
                count += 1
        elif 'text' in query:
            final_message['instructions'].append(query['text'])
            final_message['var'] = query['var']
            request.session['previous_var'] = query['var']
            status = False

            if 'options' in query:
                final_message['options'] = query['options']

        count = int(count)
        count += 1
        request.session['count'] = count

    request.session['count'] = count
    print(final_message)

    return JsonResponse(final_message, content_type="application/json")





# Just 1 hack

def execute_json_function_2(request):
    request.session.modified = True
    print('yes,', request.session.keys())
    for key in request.session.keys():
        print("key:=>", request.session[key])

    json_file = 'assignment_1_input_2.json'

    count = int(request.POST.get('count'))
    response = request.POST.get('response')

    if response != '' and request.session['previous_var']:
        request.session[request.session['previous_var']] = str(response)

    if count == 1:
        count = request.session.get('count')
    else:
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]

    with open(json_file) as f:
        json_content = json.load(f)

    final_message = {
        'instructions': [],
        'var': '',
        'options': [],
    }

    status = True
    rows = [0, 0, 0]

    while status and len(json_content['questions']) > count:
        query = json_content['questions'][count]
        if 'instruction' in query:
            query_instruction = query['instruction']
            if '%s' in query['instruction']:
                if 'list_length' in query:
                    for i in range(int(query['list_length'])):
                        for var in query['instruction_var']:
                            for key in request.session.keys():
                                if key in var:
                                    exec('%s = %s') % (key, request.session.get(key))
                                    try:
                                        query_instruction = query_instruction.replace('%s', request.session.get(key), 1)
                                    except:
                                        query_instruction = query_instruction.replace('%s', str(eval(key)), 1)
                else:
                    for var in query['instruction_var']:
                        query_instruction = query_instruction.replace('%s', request.session.get(var), 1)
            final_message['instructions'].append(query_instruction)
        elif 'calculated_variable' in query:
            temp_session = request.session.keys()
            for key in temp_session:
                if key == 'rows':
                    continue
                try:
                    exec('%s = %s') % (key, request.session[key])
                except:
                    exec(key + ' = "' + str(request.session[key]) + '"')

            request.session[query['var']] = eval(query['formula'])
            # Load all the session variables because we don't know what is actually used
        elif 'conditions' in query:
            condition_status = False
            exec(query['var'] + ' = "' + request.session[query['var']] + '"')
            for condition in query['conditions']:
                flag = 0
                for statement in condition:
                    print('eval', eval(statement))
                    if not eval(statement):
                        flag = 1
                        break

                # Any statement is true, then the given condition is met
                if flag == 0:
                    condition_status = True
            if condition_status:
                count += 1
        elif 'text' in query:
            final_message['instructions'].append(query['text'])
            final_message['var'] = query['var']
            request.session['previous_var'] = query['var']
            status = False

            if 'options' in query:
                final_message['options'] = query['options']

        count = int(count)
        count += 1
        request.session['count'] = count

    request.session['count'] = count
    print(final_message)

    return JsonResponse(final_message, content_type="application/json")