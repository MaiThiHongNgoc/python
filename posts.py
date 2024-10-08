# biz app
# khai bao mot cau truc du lieu luu thong tin
posts = []

def get_posts():
    return posts

def add_post(title, content):
    # {expression}
    post = {'title': title, 'content':content}
    posts.append(post)