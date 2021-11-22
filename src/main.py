import copy
import os
import praw
import explain_fallacy


def check_new_call(details):
    app = app_list[details]
    inbox = app['reddit'].inbox.unread()
    for msg in inbox:
        print("Calling next function", msg)
        msg.mark_read()
        app['function'](app, msg)


def generate_details(n_bucket, n_prefix, n_function):
    details = copy.deepcopy({
        'bucket': n_bucket,
        'prefix': n_prefix,
        'reddit': reddit,
        'function': n_function,
    })
    return details


reddit = praw.Reddit(
    client_id=os.environ['CLIENTID'],
    client_secret=os.environ['CLIENTSECRET'],
    user_agent=os.environ['USERAGENT'],
    username=os.environ['USERNAME'],
    password=os.environ['PASSWORD'],
)

app_list = {
    'Explain-Fallacy-Script': generate_details('crowdy-llc-reddit-bots', 'explain-fallacy',
                                               explain_fallacy.start_handling),
}


def lambda_handler(event, context):
    for n in app_list:
        check_new_call(n)

    response = {
        'headers': {
            "Content-Type": "application/json"
        },
        'statusCode': 200,
        'body': None,
        'isBase64Encoded': False
    }

    return response
