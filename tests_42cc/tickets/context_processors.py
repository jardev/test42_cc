from tests_42cc import settings

def project_settings(request):
    return {
        'settings' : settings,
        'request'  : request
    }

