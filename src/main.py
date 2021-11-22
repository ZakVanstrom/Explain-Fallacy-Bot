import copy
import time
import praw
import explain_fallacy


def check_new_call(n):
    app = app_list[n]
    inbox = app['reddit'].inbox.unread()
    for msg in inbox:
        print("Calling next function", msg)
        msg.mark_read()
        app['function'](app, msg)


def generate_details(n_app_name, n_bucket, n_prefix, n_function):
    details = copy.deepcopy({
        'bucket': n_bucket,
        'prefix': n_prefix,
        'reddit': praw.Reddit(n_app_name),
        'function': n_function,
    })
    return details


bucket = 'crowdy-llc-reddit-bots'
app_list = {
    'Explain-Fallacy-Script': generate_details('Explain-Fallacy-Script', bucket, 'explain-fallacy', explain_fallacy.start_handling),
}

while True:
    print("1. Handle for new calls")
    for n in app_list:
        check_new_call(n)
    print("2. Sleep for 30 seconds")
    time.sleep(30)
