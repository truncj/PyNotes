import json
import re
from ConfigParser import ConfigParser

import requests

from releaseissue import ReleaseIssue

config = ConfigParser()
config.read("./config.ini")
url = config.get('instance', 'url')
token = config.get('instance', 'token')
project_name = config.get('instance', 'project_name')
version = config.get('instance', 'version')
image_host = config.get('instance', 'image_host')
header_text = config.get('instance', 'header_text')


# Get release notes by pulling Jira issues tagged with the fix version
def get_issues():
    query = '/rest/api/2/search?jql=fixVersion=%s' % version
    resp = requests.get(url + query, headers={'Authorization': 'Basic %s' % token})
    resp = json.loads(resp.text)
    if 'issues' in resp:
        issues = process_issues(resp['issues'])
        return issues
    else:
        return


def process_issues(issues):

    release_issues = []
    for issue in issues:

        release_issues.append(ReleaseIssue(issue['id'],
                                           issue['key'],
                                           issue['fields']['summary'],
                                           truncate_field(issue['fields']['description']),
                                           check_exists(issue, ('fields', 'assignee', 'displayName')),
                                           '%s/browse/%s' % (url, issue['key'])))
    return release_issues


# dealing with nested dict/json throwing KeyErrors if the key doesn't exist
def check_exists(d, l):
    try:  # try to get the value
        return reduce(dict.__getitem__, l, d)
    except KeyError:  # failed
        return None
    except TypeError:
        return None


# formatting fix for long descriptions with hyperlinks, images, etc..
def truncate_field(d):
    if d:

        regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        urls = re.findall(regex, d)

        for url in urls:
            url_link = "<a href='%s'>%s...</a>" % (url, url[:20])
            d = d.replace(str(url), str(url_link))

        d = (d[:1021] + ' ...') if len(d) > 1024 and d else d

    return d
