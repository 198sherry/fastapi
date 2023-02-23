from typing import List
from app import schemas
import pytest

# def test_get_all_posts(authorized_client, test_posts):
#     res = authorized_client.get("/posts/")
#     print (res.json())

#     def validate(post):
#         return schemas.PostOut(**post)
    
#     posts_map = map(validate, res.json())
#     posts_list = list(posts_map)
    
#     assert len(res.json()) == len(test_posts)
#     #assert posts_list[0].Post.id == test_posts[0].id #order matters
#     assert res.status_code == 200

# def test_unauthorized_user_get_all_posts(client, test_posts):
#     res = client.get('/posts/')
#     assert res.status_code ==401

# def test_unauthorized_user_get_one_posts(client, test_posts):
#     res = client.get(f'/posts/{test_posts[0].id}')
#     assert res.status_code ==401

# def test_get_one_post_not_exist(authorized_client, test_posts):
#     res = authorized_client.get(f'/posts/9999') #post 9999 doesn't exist
#     assert res.status_code ==404

def test_authorized_user_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code ==200

    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

# @pytest.mark.parametrize("title, content, published", [
#     ("title1", "content1", True),
#     ("title2", "content2", False),
#     ("title3", "content3", True)
# ])
# def test_authorized_user_create_posts(authorized_client, test_user, test_posts, title, content, published):
#     res = authorized_client.post('/posts/', json={"title":title, "content":content, "published":published})
#     created_post = schemas.Post(**res.json())
#     assert res.status_code ==201
#     assert created_post.title == title
#     assert created_post.content == content
#     assert created_post.published == published
#     assert created_post.owner_id == test_user['id']

# def test_authorized_user_create_posts_default_published_true(authorized_client):
#     res = authorized_client.post('/posts/', json={"title":"1title", "content":"1content"})
#     created_post = schemas.Post(**res.json())
#     assert res.status_code ==201
#     assert created_post.published == True

# def test_unauthorized_user_create_posts(client):
#     res = client.post('/posts/', json={"title":"1title", "content":"1content"})
#     assert res.status_code ==401

# def test_unauthorized_user_create_posts(client, test_posts):
#     res = client.delete(f'/posts/{test_posts[0].id}')
#     assert res.status_code ==401

# def test_authorized_user_delete_posts_success(authorized_client, test_posts):
#     res = authorized_client.delete(f'/posts/{test_posts[0].id}')
#     assert res.status_code ==204

# def test_authorized_user_delete_non_exist_posts(authorized_client, test_posts):
#     res = authorized_client.delete('/posts/9999')
#     assert res.status_code ==404

# def test_authorized_user_delete_other_user_posts(authorized_client, test_posts):
#     res = authorized_client.delete(f'/posts/{test_posts[3].id}')
#     assert res.status_code ==403

# def test_authorized_user_update_posts(authorized_client, test_user, test_posts):
#     data = {
#         "title": "updated title",
#         "content": "updated content",
#         "id": test_posts[0].id
#     }

#     res = authorized_client.put(f'/posts/{test_posts[0].id}', json = data)
#     assert res.status_code ==200
    
# def test_update_other_user_posts(authorized_client, test_user, test_user2, test_posts):
#     post_data = {
#         "title": "updated title",
#         "content": "updated content",
#         "id": test_posts[3].id
#     }

#     res = authorized_client.put(f'/posts/{test_posts[3].id}', json = post_data)
#     assert res.status_code ==403

# def test_update_non_exist_posts(authorized_client, test_user, test_user2, test_posts):
#     post_data = {
#         "title": "updated title",
#         "content": "updated content",
#         "id": 9999
#     }

#     res = authorized_client.put(f'/posts/9999', json = post_data)
#     assert res.status_code ==404
