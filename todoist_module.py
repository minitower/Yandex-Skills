from todoist.api import TodoistAPI

def start_todoist ():
    api = TodoistAPI ('544e9377b7715e54567c8fe64c3622be711c94c9')
    api.sync ()
    return api

def pars_responce (api):
    lst_projects = []
    for i in api.state ['projects']:
        lst_projects.append (i['name'])
    return lst_projects







