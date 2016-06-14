#! -*- coding: utf-8 -*-


def login(username, password):
    return {'__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'pagebody_0$left_0$txtUsername': username,
            'pagebody_0$left_0$txtPassword': password,
            'pagebody_0$left_0$btnSubmit': '',
            'elqFormName':	'RecruiterLoginAndRegister',
            'elqDefaultTargetURL': '',
            'elqPost': '',
            'elqCustomerGUID': '',
            'elqCookieWrite': '0',
            'pagebody_0$right_0$chkThirdPartyMarketing': 'on'}


def next_candidate(page_no):
    return {'__EVENTTARGET':
            'ctl00$cphCentralPanel$ucSearchResults$pgrPager',
            '__EVENTARGUMENT': page_no,
            'ctl00$cphCentralPanel$NewOrExistingSavedSearch':
                'rdoNewSavedSearch'}

def search(industry, timelimit):
    return {
        'ctl00$cphCentralPanel$ucSearchPart$ddlIndustries': industry,
        'ctl00$cphCentralPanel$ucSearchPart$ddlLastActivity': timelimit}


MAX_ENTRIES_PER_PAGE = 50

switch_to_max = lambda: {
    '__EVENTTARGET': 'ctl00$cphCentralPanel$ucSearchResults$ddlPageSize',
    '__EVENTARGUMENT': '',
    'ctl00$cphCentralPanel$ucSearchResults$ddlPageSize':
        str(MAX_ENTRIES_PER_PAGE),
}

switch_to_last = lambda: {
    '__EVENTTARGET': 'ctl00$cphCentralPanel$ucSearchResults$ddlSort',
    '__EVENTARGUMENT': '',
    'ctl00$cphCentralPanel$ucSearchResults$ddlSort': 'LastActivityDate#0'
}
