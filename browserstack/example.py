import optparse
from browserstack.screenshot import Screenshot


def post(url, username, password, callback_url=None):
    """Post a screenshot
    """
    screenshot = Screenshot(username, password)
    browsers = [
        {"os": "Windows",
         "os_version": "7",
         "browser_version": "8.0",
         "browser": "ie"}
    ]
    res = screenshot.add_screenshot(url, browsers=browsers)
    print 'The job %s is running' % res['job_id']


def status(job_id, username, password):
    """Get the status of a screenshot
    """
    screenshot = Screenshot(username, password)
    res = screenshot.get_screenshot(job_id)
    print 'Status: %s ' % res['state']
    if 'screenshots' in res:
        for screenshot in res['screenshots']:
            if screenshot['image_url']:
                print 'Url:', screenshot['image_url']


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.usage = "usage: %prog [options] 'url'"
    parser.add_option(
        "-u", "--username",
        help="Browserstack url")
    parser.add_option(
        "-p", "--password",
        help="Browserstack password")
    parser.add_option(
        "-c", "--callback_url",
        help="A callback url called when the screenshots are generated",
        metavar="URL")
    parser.add_option(
        "-j", "--job_id",
        help="The job_id you want to get the status",
        metavar="URL")
    options, args = parser.parse_args()

    if not options.username and not options.password:
        parser.error('Please provide a username and a password')

    if options.job_id:
        dic = vars(options)
        dic.pop('callback')
        status(**dic)
        exit(0)

    if len(args) < 1:
        parser.error('Please provide the url you want to make the screenshot')

    dic = vars(options)
    dic.pop('job_id')
    post(args[0], **vars(options))
