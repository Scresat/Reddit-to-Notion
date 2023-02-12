import praw
import config
import pprint
import requests
import html

def score_add_comma(score):
    score = str(score)
    if len(score) > 3:
        score = score[:-3] + ',' + score[-3:]
    return score


def fetch_posts(subreddit_to_scrape, r):
    if subreddit_to_scrape == 'popular':
        top_posts = r.subreddit(subreddit_to_scrape).hot(limit=config.number_of_posts_to_fetch)
    else:
        top_posts = r.subreddit(subreddit_to_scrape).top(limit=config.number_of_posts_to_fetch, time_filter='day')


    test_p = 0
    image_links_prefix = [
        'https://i.redd.it',
        'https://preview.redd.it/',
        'https://external-preview.redd.it/',
        'https://imgur.com/',
        'https://i.imgur.com'
    ]
    video_links_prefix = [
        'https://v.redd.it/',
        'https://www.youtube.com/watch?v='
    ]

    post_objects = []
    for post in top_posts:
        test_p += 1
        post_object = {
            'type': 'other',
            'content': {
                'title': post.title,
                'permalink': post.permalink,
                'votes': score_add_comma(post.score),
                'url': post.url,
                'text': ''
            }
        }

        
        post_object['content']['comments'] = []

        comment_range = range(0)
        comments_obj_list = get_comments(post.permalink)
        for comment in comments_obj_list:
            if (len(post_object['content']['comments'])) > 2:
                break
            if comment['author'] != 'automoderator':
                post_object['content']['comments'].append(comment['body'] + '\n⬆️ ' + score_add_comma(str(comment['score'])) + ' votes')
     

        if post.url.startswith('https://www.reddit.com/r/'):
            post_object['type'] = 'text'
            post_object['content']['text'] = post.selftext[:1996] + '...' if len(post.selftext) > 1995 else post.selftext
            
        elif any(map(post.url.startswith, image_links_prefix)):
            post_object['type'] = 'image'
            
        elif any(map(post.url.startswith, video_links_prefix)):
            post_object['type'] = 'video'
            if post.url.startswith('https://v.redd.it'):
                try:
                    post_object['content']['video_url'] = post.secure_media['reddit_video']['fallback_url']
                
                except:
                    try:
                        print(post.media['reddit_video']['fallback_url'][-13:-16].lower())
                        if post.media['reddit_video']['fallback_url'][-13:-16].lower() == 'mp4':
                            post_object['content']['video_url'] = post.media['reddit_video']['fallback_url']
                        else:
                            post_object['type'] = 'other'
                    except:
                        post_object['type'] = 'other'
            else:
                post_object['content']['video_url'] = post.url
            
        elif post.url.startswith('https://'):
            post_object['type'] = 'link'
        else:
            post_object['type'] = 'other'
            post_object['content']['text'] = post.selftext
            
        post_objects.append(post_object)

    # print('fetched ' + str(test_p) + ' posts')
    return post_objects


def get_subreddit_details(subreddit_name, r):
    reddit_subreddit = r.subreddit(subreddit_name)
    if subreddit_name not in ['popular', 'all']:
        subreddit_details = {
            'name': reddit_subreddit.url[3:-1] ,
            'icon': reddit_subreddit.community_icon,
            'icon2': reddit_subreddit.icon_img,
            'cover': reddit_subreddit.banner_background_image
        }
    else:
        subreddit_details = {
            'name': subreddit_name,
            'icon': '',
            'icon2': '',
            'cover': ''
        }
    return subreddit_details


def get_comments(permalink):
    endpoint = 'https://www.reddit.com' + permalink + '.json?sort=top&limit=6'
   
    r = requests.get(endpoint, headers = {'User-agent': 'your bot 0.1'})
    comments = []
    try:
        for i in r.json()[1]['data']['children']:
            if i['kind'] == 't1' and i['data']['author'] != 'AutoModerator' and not i['data']['stickied']:
                comments.append({
                    'author': i['data']['author'],
                    'body': html.unescape(i['data']['body']),
                    'score': i['data']['score']
                })
        return comments
    except Exception as e:
        return []
  