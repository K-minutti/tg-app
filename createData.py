from faker import Faker
import pandas as pd
import random
fake = Faker()

#SCHEMA FOR USER BASED OFF https://developers.soundcloud.com/docs/api/explorer/open-api#/users/get_users__user_id_
#SCHEMA FOR TRACKS BASED OFF https://developers.soundcloud.com/docs/api/explorer/open-api#/tracks/get_tracks__track_id_
#SCHEMA FOR COMMENTS BASED OFF https://developers.soundcloud.com/docs/api/explorer/open-api#/users/get_users__user_id__comments


#USER 
p = 400000 #Total Population
#user - city, country, followers_count, followings_count, id, playlist_count, public_favorites_count,reposts_count, track_count
cities = [fake.city() for i in range(p)]
countries = [fake.country() for i in range(p)]
followers_count = [random.randint(1,87000) for i in range(p)]
followings_count = [random.randint(1,3000) for i in range(p)]
full_name = [fake.unique.name() for i in range(p)]
user_id = [i for i in range(p)]
playlist_count = [random.randint(1,30) for i in range(p)]
public_favorites_count = [random.randint(1,200) for i in range(p)]
reposts_count =  [random.randint(1,300) for i in range(p)]
track_count =  [random.randint(2,36) if i > 4000 and i % 113 == 0 else 0 for i in range(p)]

user_data = {'city': cities, 'country': countries, 'followers_count': followers_count, 'followings_count': followings_count, 'full_name': full_name, 'id': user_id, 'playlist_count': playlist_count, 'public_favorites_count': public_favorites_count, 'reposts_count': reposts_count, 'track_count': track_count}
user_df = pd.DataFrame(data=user_data)
user_df.to_csv('users.csv',index=False)


#TRACK
#track - comment_count, created_at,duration,favoritings_count, genre, id,title,user_id,user_playback_count
t = sum(track_count)
genres = ['rock', 'hip hop', 'pop', 'jazz', 'folk', 'blues', 'punk rock', 'rap', 'hip hop', 'pop', 'heavy metal', 'classical','rap', 'electronic', 'soul', 'electronic dance', 'rock', 'funk', 'reggae', 'house', 'disco', 'techno', 'indie rock', 'ambient','pop', 'heavy metal']
g_l = len(genres)-1

def user_id_to_match_tracks(tracks):
    ids = []
    for idx, t in enumerate(tracks):
        if t >= 2:
            count = t
            while count > 0:
                ids.append(idx)
                count-=1
    return ids
user_id_list = user_id_to_match_tracks(track_count)

comment_count = [random.randint(1,100) if i > 4000 else 0 for i in range(t)]
created_at = [fake.date_this_year() for i in range(t)]
duration = [random.randint(1000,12000) for i in range(t)]
favoritings_count = [random.randint(400,9000) for i in range(t)]
genre = [genres[random.randint(0,g_l)] for i in range(t)]
track_id = [i for i in range(t)] 
title = [fake.unique.company() for i in range(t)]
user_id_track = user_id_list
user_playback_count = [random.randint(2000,1800000) for i in range(t)]

track_data = {'comment_count':comment_count , 'created_at':created_at,'duration':duration,'favoritings_count': favoritings_count, 'genre':genre, 'id':track_id,'title':title,'user_id':user_id_track, 'user_playback_count': user_playback_count}
track_df = pd.DataFrame(data=track_data)
track_df.to_csv('tracks.csv',index=False)

#COMMENT
#comment - body, created_at, id,track_id, user_id
c = sum(comment_count)
def track_id_to_match_comments(comments):
    ids = []
    for idx, c in enumerate(comments):
        if c != 0:
            count = c
            while count > 0:
                ids.append(idx)
                count -=1
    return ids
track_id_list = track_id_to_match_comments(comment_count)
body = [fake.bs() for i in range(c)]
created_at_comment = [fake.date_this_year() for i in range(c)]
comment_id = [i for i in range(c)] 
track_id_comment = track_id_list
user_id_comment = [random.randint(1000,p) for i in range(c)]

print(c)
print(len(track_id_comment))
comment_data = {'body':body, 'created_at':created_at_comment, 'id':comment_id,'track_id':track_id_comment, 'user_id':user_id_comment}
comment_df = pd.DataFrame(data=comment_data)
comment_df.to_csv('comments.csv',index=False)

#FAVORITED 
def track_users_ids(favoritings_count, user_id):
    track_ids = []
    user_ids = []
    for idx, track in enumerate(favoritings_count):
        count = track
        while count > 0:
            track_ids.append(idx)
            l = len(user_id)
            user_ids.append(random.randint(0,l))
            count -=1
    return track_ids, user_ids

track_ids, user_ids = track_users_ids(favoritings_count,user_id)
track_id_fav = track_ids
user_id_fav = user_ids

favorite_data = {'track_id':track_id_fav , 'user_id':user_id_fav}
favorite_df = pd.DataFrame(data=favorite_data)
favorite_df.to_csv('favorites.csv',index=False)

#LIKES
# track_id_like = track_ids
# user_id_like = user_ids

#USER FOLLOWER
def user_followers_ids(followers_count, user_id):
    user_main_ids = []
    followers_main_ids = []
    for idx, followers in enumerate(followers_count):
        count = followers
        while count > 0:
            user_main_ids.append(idx)
            l = len(user_id)
            followers_main_ids.append(random.randint(0,l))
            count -=1
    return user_main_ids, followers_main_ids

user_main_ids, followers_main_ids = user_followers_ids(followers_count, user_id)

user_id_f = user_main_ids
follower_id_f = followers_main_ids

followers_data = {'user_id':user_id_f, 'folower_id':follower_id_f}
followers_df = pd.DataFrame(data=followers_data)
followers_df.to_csv('user_followers.csv',index=False)

#EXPORTING 
#users.csv, tracks.csv, favorites.csv, userfollowers.csv