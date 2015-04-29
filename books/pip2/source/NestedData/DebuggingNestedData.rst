..  Copyright (C)  Paul Resnick.  Permission is granted to copy, distribute
    and/or modify this document under the terms of the GNU Free Documentation
    License, Version 1.3 or any later version published by the Free Software
    Foundation; with Invariant Sections being Forward, Prefaces, and
    Contributor List, no Front-Cover Texts, and no Back-Cover Texts.  A copy of
    the license is included in the section entitled "GNU Free Documentation
    License".

.. _debug_nested_chap:

Extracting from Nested Data
===========================

A common problem, especially when dealing with data returned from a web site, is to extract certain elements from deep inside a nested data structure. In principle, there's nothing more difficult about pulling something out from deep inside a nested data structure: with lists, you use [] to index or a for loop to get them them all; with dictionaries, you get the value associated with a particular key using []. But it's easy to get lost in the process and think you've extracted something different than you really have.

Follow the system described below and you will have success with extracting nested data. The process involves the following steps:

1. Understand the nested data object.
2. Extract one object at the next level down.
3. Repeat the process with the extracted object

Understand. Extract. Repeat.

To illustrate this, we will walk through extracting information from the data returned from the Twitter API. This nested dictionary results from querying Twitter, asking for three tweets matching "University of Michigan". As you'll see, it's quite a daunting data structure, even when printed with nice indentation as it's shown below. 

.. activecode:: extract_nested_data_1

   res = {
     "search_metadata": {
       "count": 3, 
       "completed_in": 0.015, 
       "max_id_str": "536624519285583872", 
       "since_id_str": "0", 
       "next_results": "?max_id=536623674942439424&q=University%20of%20Michigan&count=3&include_entities=1", 
       "refresh_url": "?since_id=536624519285583872&q=University%20of%20Michigan&include_entities=1", 
       "since_id": 0, 
       "query": "University+of+Michigan", 
       "max_id": 536624519285583872
     }, 
     "statuses": [
       {
         "contributors": None, 
         "truncated": False, 
         "text": "RT @mikeweber25: I'm decommiting from the university of Michigan thank you Michigan for the love and support I'll remake my decision at the\u2026", 
         "in_reply_to_status_id": None, 
         "id": 536624519285583872, 
         "favorite_count": 0, 
         "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", 
         "retweeted": False, 
         "coordinates": None, 
         "entities": {
           "symbols": [], 
           "user_mentions": [
             {
               "id": 1119996684, 
               "indices": [
                 3, 
                 15
               ], 
               "id_str": "1119996684", 
               "screen_name": "mikeweber25", 
               "name": "Mikey"
             }
           ], 
           "hashtags": [], 
           "urls": []
         }, 
         "in_reply_to_screen_name": None, 
         "in_reply_to_user_id": None, 
         "retweet_count": 2014, 
         "id_str": "536624519285583872", 
         "favorited": False, 
         "retweeted_status": {
           "contributors": None, 
           "truncated": False, 
           "text": "I'm decommiting from the university of Michigan thank you Michigan for the love and support I'll remake my decision at the army bowl", 
           "in_reply_to_status_id": None, 
           "id": 536300265616322560, 
           "favorite_count": 1583, 
           "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", 
           "retweeted": False, 
           "coordinates": None, 
           "entities": {
             "symbols": [], 
             "user_mentions": [], 
             "hashtags": [], 
             "urls": []
           }, 
           "in_reply_to_screen_name": None, 
           "in_reply_to_user_id": None, 
           "retweet_count": 2014, 
           "id_str": "536300265616322560", 
           "favorited": False, 
           "user": {
             "follow_request_sent": False, 
             "profile_use_background_image": True, 
             "profile_text_color": "666666", 
             "default_profile_image": False, 
             "id": 1119996684, 
             "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme9/bg.gif", 
             "verified": False, 
             "profile_location": None, 
             "profile_image_url_https": "https://pbs.twimg.com/profile_images/534465900343083008/A09dIq1d_normal.jpeg", 
             "profile_sidebar_fill_color": "252429", 
             "entities": {
               "description": {
                 "urls": []
               }
             }, 
             "followers_count": 5444, 
             "profile_sidebar_border_color": "FFFFFF", 
             "id_str": "1119996684", 
             "profile_background_color": "C0DEED", 
             "listed_count": 36, 
             "is_translation_enabled": False, 
             "utc_offset": None, 
             "statuses_count": 6525, 
             "description": "Mike Weber (U.S Army All American) DETROIT CTSENIOR State Champion", 
             "friends_count": 693, 
             "location": "", 
             "profile_link_color": "0084B4", 
             "profile_image_url": "http://pbs.twimg.com/profile_images/534465900343083008/A09dIq1d_normal.jpeg", 
             "following": False, 
             "geo_enabled": False, 
             "profile_banner_url": "https://pbs.twimg.com/profile_banners/1119996684/1416261575", 
             "profile_background_image_url": "http://abs.twimg.com/images/themes/theme9/bg.gif", 
             "name": "Mikey", 
             "lang": "en", 
             "profile_background_tile": False, 
             "favourites_count": 1401, 
             "screen_name": "mikeweber25", 
             "notifications": False, 
             "url": None, 
             "created_at": "Fri Jan 25 18:45:53 +0000 2013", 
             "contributors_enabled": False, 
             "time_zone": None, 
             "protected": False, 
             "default_profile": False, 
             "is_translator": False
           }, 
           "geo": None, 
           "in_reply_to_user_id_str": None, 
           "lang": "en", 
           "created_at": "Sat Nov 22 23:28:41 +0000 2014", 
           "in_reply_to_status_id_str": None, 
           "place": None, 
           "metadata": {
             "iso_language_code": "en", 
             "result_type": "recent"
           }
         }, 
         "user": {
           "follow_request_sent": False, 
           "profile_use_background_image": True, 
           "profile_text_color": "333333", 
           "default_profile_image": False, 
           "id": 2435537208, 
           "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", 
           "verified": False, 
           "profile_location": None, 
           "profile_image_url_https": "https://pbs.twimg.com/profile_images/532694075947110400/oZEP5XNQ_normal.jpeg", 
           "profile_sidebar_fill_color": "DDEEF6", 
           "entities": {
             "description": {
               "urls": []
             }
           }, 
           "followers_count": 161, 
           "profile_sidebar_border_color": "C0DEED", 
           "id_str": "2435537208", 
           "profile_background_color": "C0DEED", 
           "listed_count": 0, 
           "is_translation_enabled": False, 
           "utc_offset": None, 
           "statuses_count": 524, 
           "description": "Delasalle '17 Baseball & Football.", 
           "friends_count": 255, 
           "location": "", 
           "profile_link_color": "0084B4", 
           "profile_image_url": "http://pbs.twimg.com/profile_images/532694075947110400/oZEP5XNQ_normal.jpeg", 
           "following": False, 
           "geo_enabled": False, 
           "profile_banner_url": "https://pbs.twimg.com/profile_banners/2435537208/1406779364", 
           "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", 
           "name": "Andrew Brooks", 
           "lang": "en", 
           "profile_background_tile": False, 
           "favourites_count": 555, 
           "screen_name": "31brooks_", 
           "notifications": False, 
           "url": None, 
           "created_at": "Wed Apr 09 14:34:41 +0000 2014", 
           "contributors_enabled": False, 
           "time_zone": None, 
           "protected": False, 
           "default_profile": True, 
           "is_translator": False
         }, 
         "geo": None, 
         "in_reply_to_user_id_str": None, 
         "lang": "en", 
         "created_at": "Sun Nov 23 20:57:10 +0000 2014", 
         "in_reply_to_status_id_str": None, 
         "place": None, 
         "metadata": {
           "iso_language_code": "en", 
           "result_type": "recent"
         }
       }, 
       {
         "contributors": None, 
         "truncated": False, 
         "text": "RT @Plantedd: The University of Michigan moved a big Bur Oak yesterday. 65ft tall. 350+ tons. http://t.co/v2Y6vl3f9e", 
         "in_reply_to_status_id": None, 
         "id": 536624216305848320, 
         "favorite_count": 0, 
         "source": "<a href=\"http://tapbots.com/tweetbot\" rel=\"nofollow\">Tweetbot for i\u039fS</a>", 
         "retweeted": False, 
         "coordinates": None, 
         "entities": {
           "symbols": [], 
           "user_mentions": [
             {
               "id": 462890283, 
               "indices": [
                 3, 
                 12
               ], 
               "id_str": "462890283", 
               "screen_name": "Plantedd", 
               "name": "David Wong"
             }
           ], 
           "hashtags": [], 
           "urls": [], 
           "media": [
             {
               "source_status_id_str": "526276522374889472", 
               "expanded_url": "http://twitter.com/Plantedd/status/526276522374889472/photo/1", 
               "display_url": "pic.twitter.com/v2Y6vl3f9e", 
               "url": "http://t.co/v2Y6vl3f9e", 
               "media_url_https": "https://pbs.twimg.com/media/B021tLsIYAADq21.jpg", 
               "source_status_id": 526276522374889472, 
               "id_str": "526276519308845056", 
               "sizes": {
                 "small": {
                   "h": 191, 
                   "resize": "fit", 
                   "w": 340
                 }, 
                 "large": {
                   "h": 576, 
                   "resize": "fit", 
                   "w": 1024
                 }, 
                 "medium": {
                   "h": 337, 
                   "resize": "fit", 
                   "w": 600
                 }, 
                 "thumb": {
                   "h": 150, 
                   "resize": "crop", 
                   "w": 150
                 }
               }, 
               "indices": [
                 94, 
                 116
               ], 
               "type": "photo", 
               "id": 526276519308845056, 
               "media_url": "http://pbs.twimg.com/media/B021tLsIYAADq21.jpg"
             }
           ]
         }, 
         "in_reply_to_screen_name": None, 
         "in_reply_to_user_id": None, 
         "retweet_count": 27, 
         "id_str": "536624216305848320", 
         "favorited": False, 
         "retweeted_status": {
           "contributors": None, 
           "truncated": False, 
           "text": "The University of Michigan moved a big Bur Oak yesterday. 65ft tall. 350+ tons. http://t.co/v2Y6vl3f9e", 
           "in_reply_to_status_id": None, 
           "id": 526276522374889472, 
           "favorite_count": 25, 
           "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", 
           "retweeted": False, 
           "coordinates": None, 
           "entities": {
             "symbols": [], 
             "user_mentions": [], 
             "hashtags": [], 
             "urls": [], 
             "media": [
               {
                 "expanded_url": "http://twitter.com/Plantedd/status/526276522374889472/photo/1", 
                 "display_url": "pic.twitter.com/v2Y6vl3f9e", 
                 "url": "http://t.co/v2Y6vl3f9e", 
                 "media_url_https": "https://pbs.twimg.com/media/B021tLsIYAADq21.jpg", 
                 "id_str": "526276519308845056", 
                 "sizes": {
                   "small": {
                     "h": 191, 
                     "resize": "fit", 
                     "w": 340
                   }, 
                   "large": {
                     "h": 576, 
                     "resize": "fit", 
                     "w": 1024
                   }, 
                   "medium": {
                     "h": 337, 
                     "resize": "fit", 
                     "w": 600
                   }, 
                   "thumb": {
                     "h": 150, 
                     "resize": "crop", 
                     "w": 150
                   }
                 }, 
                 "indices": [
                   80, 
                   102
                 ], 
                 "type": "photo", 
                 "id": 526276519308845056, 
                 "media_url": "http://pbs.twimg.com/media/B021tLsIYAADq21.jpg"
               }
             ]
           }, 
           "in_reply_to_screen_name": None, 
           "in_reply_to_user_id": None, 
           "retweet_count": 27, 
           "id_str": "526276522374889472", 
           "favorited": False, 
           "user": {
             "follow_request_sent": False, 
             "profile_use_background_image": True, 
             "profile_text_color": "333333", 
             "default_profile_image": False, 
             "id": 462890283, 
             "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", 
             "verified": False, 
             "profile_location": None, 
             "profile_image_url_https": "https://pbs.twimg.com/profile_images/1791926707/Plantedd_Logo__square__normal.jpg", 
             "profile_sidebar_fill_color": "DDEEF6", 
             "entities": {
               "url": {
                 "urls": [
                   {
                     "url": "http://t.co/ZOnsCHvoKt", 
                     "indices": [
                       0, 
                       22
                     ], 
                     "expanded_url": "http://www.plantedd.com", 
                     "display_url": "plantedd.com"
                   }
                 ]
               }, 
               "description": {
                 "urls": []
               }
             }, 
             "followers_count": 2598, 
             "profile_sidebar_border_color": "C0DEED", 
             "id_str": "462890283", 
             "profile_background_color": "C0DEED", 
             "listed_count": 61, 
             "is_translation_enabled": False, 
             "utc_offset": 0, 
             "statuses_count": 8157, 
             "description": "Hello, I'm the supervillain behind Plantedd. We're an online market for plant lovers plotting to take over the world by making it simple to find and buy plants.", 
             "friends_count": 2664, 
             "location": "UK", 
             "profile_link_color": "0084B4", 
             "profile_image_url": "http://pbs.twimg.com/profile_images/1791926707/Plantedd_Logo__square__normal.jpg", 
             "following": False, 
             "geo_enabled": False, 
             "profile_banner_url": "https://pbs.twimg.com/profile_banners/462890283/1398254314", 
             "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", 
             "name": "David Wong", 
             "lang": "en", 
             "profile_background_tile": False, 
             "favourites_count": 371, 
             "screen_name": "Plantedd", 
             "notifications": False, 
             "url": "http://t.co/ZOnsCHvoKt", 
             "created_at": "Fri Jan 13 13:46:46 +0000 2012", 
             "contributors_enabled": False, 
             "time_zone": "Edinburgh", 
             "protected": False, 
             "default_profile": True, 
             "is_translator": False
           }, 
           "geo": None, 
           "in_reply_to_user_id_str": None, 
           "possibly_sensitive": False, 
           "lang": "en", 
           "created_at": "Sun Oct 26 07:37:55 +0000 2014", 
           "in_reply_to_status_id_str": None, 
           "place": None, 
           "metadata": {
             "iso_language_code": "en", 
             "result_type": "recent"
           }
         }, 
         "user": {
           "follow_request_sent": False, 
           "profile_use_background_image": True, 
           "profile_text_color": "2A48AE", 
           "default_profile_image": False, 
           "id": 104940733, 
           "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme17/bg.gif", 
           "verified": False, 
           "profile_location": None, 
           "profile_image_url_https": "https://pbs.twimg.com/profile_images/2878477539/78e20432088b5ee2addc9ce3362fd461_normal.jpeg", 
           "profile_sidebar_fill_color": "6378B1", 
           "entities": {
             "description": {
               "urls": []
             }
           }, 
           "followers_count": 149, 
           "profile_sidebar_border_color": "FBD0C9", 
           "id_str": "104940733", 
           "profile_background_color": "0C003D", 
           "listed_count": 18, 
           "is_translation_enabled": False, 
           "utc_offset": 0, 
           "statuses_count": 16031, 
           "description": "Have you any dreams you'd like to sell?", 
           "friends_count": 248, 
           "location": "", 
           "profile_link_color": "0F1B7C", 
           "profile_image_url": "http://pbs.twimg.com/profile_images/2878477539/78e20432088b5ee2addc9ce3362fd461_normal.jpeg", 
           "following": False, 
           "geo_enabled": False, 
           "profile_banner_url": "https://pbs.twimg.com/profile_banners/104940733/1410032966", 
           "profile_background_image_url": "http://abs.twimg.com/images/themes/theme17/bg.gif", 
           "name": "Heather", 
           "lang": "en", 
           "profile_background_tile": False, 
           "favourites_count": 777, 
           "screen_name": "froyoho", 
           "notifications": False, 
           "url": None, 
           "created_at": "Thu Jan 14 21:37:54 +0000 2010", 
           "contributors_enabled": False, 
           "time_zone": "London", 
           "protected": False, 
           "default_profile": False, 
           "is_translator": False
         }, 
         "geo": None, 
         "in_reply_to_user_id_str": None, 
         "possibly_sensitive": False, 
         "lang": "en", 
         "created_at": "Sun Nov 23 20:55:57 +0000 2014", 
         "in_reply_to_status_id_str": None, 
         "place": None, 
         "metadata": {
           "iso_language_code": "en", 
           "result_type": "recent"
         }
       }, 
       {
         "contributors": None, 
         "truncated": False, 
         "text": "RT @NotableHistory: Madonna, 18 year old freshman at the University of Michigan, 1976 http://t.co/x2dm1G67ea", 
         "in_reply_to_status_id": None, 
         "id": 536623674942439425, 
         "favorite_count": 0, 
         "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>", 
         "retweeted": False, 
         "coordinates": None, 
         "entities": {
           "symbols": [], 
           "user_mentions": [
             {
               "id": 844766941, 
               "indices": [
                 3, 
                 18
               ], 
               "id_str": "844766941", 
               "screen_name": "NotableHistory", 
               "name": "OnThisDay & Facts"
             }
           ], 
           "hashtags": [], 
           "urls": [], 
           "media": [
             {
               "source_status_id_str": "536610190334779392", 
               "expanded_url": "http://twitter.com/NotableHistory/status/536610190334779392/photo/1", 
               "display_url": "pic.twitter.com/x2dm1G67ea", 
               "url": "http://t.co/x2dm1G67ea", 
               "media_url_https": "https://pbs.twimg.com/media/B3EXbQkCMAEipwM.jpg", 
               "source_status_id": 536610190334779392, 
               "id_str": "536235587703812097", 
               "sizes": {
                 "small": {
                   "h": 487, 
                   "resize": "fit", 
                   "w": 340
                 }, 
                 "large": {
                   "h": 918, 
                   "resize": "fit", 
                   "w": 640
                 }, 
                 "medium": {
                   "h": 860, 
                   "resize": "fit", 
                   "w": 600
                 }, 
                 "thumb": {
                   "h": 150, 
                   "resize": "crop", 
                   "w": 150
                 }
               }, 
               "indices": [
                 86, 
                 108
               ], 
               "type": "photo", 
               "id": 536235587703812097, 
               "media_url": "http://pbs.twimg.com/media/B3EXbQkCMAEipwM.jpg"
             }
           ]
         }, 
         "in_reply_to_screen_name": None, 
         "in_reply_to_user_id": None, 
         "retweet_count": 9, 
         "id_str": "536623674942439425", 
         "favorited": False, 
         "retweeted_status": {
           "contributors": None, 
           "truncated": False, 
           "text": "Madonna, 18 year old freshman at the University of Michigan, 1976 http://t.co/x2dm1G67ea", 
           "in_reply_to_status_id": None, 
           "id": 536610190334779392, 
           "favorite_count": 13, 
           "source": "<a href=\"https://ads.twitter.com\" rel=\"nofollow\">Twitter Ads</a>", 
           "retweeted": False, 
           "coordinates": None, 
           "entities": {
             "symbols": [], 
             "user_mentions": [], 
             "hashtags": [], 
             "urls": [], 
             "media": [
               {
                 "expanded_url": "http://twitter.com/NotableHistory/status/536610190334779392/photo/1", 
                 "display_url": "pic.twitter.com/x2dm1G67ea", 
                 "url": "http://t.co/x2dm1G67ea", 
                 "media_url_https": "https://pbs.twimg.com/media/B3EXbQkCMAEipwM.jpg", 
                 "id_str": "536235587703812097", 
                 "sizes": {
                   "small": {
                     "h": 487, 
                     "resize": "fit", 
                     "w": 340
                   }, 
                   "large": {
                     "h": 918, 
                     "resize": "fit", 
                     "w": 640
                   }, 
                   "medium": {
                     "h": 860, 
                     "resize": "fit", 
                     "w": 600
                   }, 
                   "thumb": {
                     "h": 150, 
                     "resize": "crop", 
                     "w": 150
                   }
                 }, 
                 "indices": [
                   66, 
                   88
                 ], 
                 "type": "photo", 
                 "id": 536235587703812097, 
                 "media_url": "http://pbs.twimg.com/media/B3EXbQkCMAEipwM.jpg"
               }
             ]
           }, 
           "in_reply_to_screen_name": None, 
           "in_reply_to_user_id": None, 
           "retweet_count": 9, 
           "id_str": "536610190334779392", 
           "favorited": False, 
           "user": {
             "follow_request_sent": False, 
             "profile_use_background_image": True, 
             "profile_text_color": "333333", 
             "default_profile_image": False, 
             "id": 844766941, 
             "profile_background_image_url_https": "https://pbs.twimg.com/profile_background_images/458461302696837121/rGlGdWsc.png", 
             "verified": False, 
             "profile_location": None, 
             "profile_image_url_https": "https://pbs.twimg.com/profile_images/481243404320251905/gCr1cVP2_normal.png", 
             "profile_sidebar_fill_color": "DDFFCC", 
             "entities": {
               "url": {
                 "urls": [
                   {
                     "url": "http://t.co/9fTPk5A4wh", 
                     "indices": [
                       0, 
                       22
                     ], 
                     "expanded_url": "http://notablefacts.com/", 
                     "display_url": "notablefacts.com"
                   }
                 ]
               }, 
               "description": {
                 "urls": []
               }
             }, 
             "followers_count": 73817, 
             "profile_sidebar_border_color": "FFFFFF", 
             "id_str": "844766941", 
             "profile_background_color": "9AE4E8", 
             "listed_count": 485, 
             "is_translation_enabled": False, 
             "utc_offset": -21600, 
             "statuses_count": 38841, 
             "description": "On This Day in History, Historical Pictures & other Interesting Facts....Historyfollower@gmail.com", 
             "friends_count": 43594, 
             "location": "", 
             "profile_link_color": "0084B4", 
             "profile_image_url": "http://pbs.twimg.com/profile_images/481243404320251905/gCr1cVP2_normal.png", 
             "following": False, 
             "geo_enabled": False, 
             "profile_banner_url": "https://pbs.twimg.com/profile_banners/844766941/1411076349", 
             "profile_background_image_url": "http://pbs.twimg.com/profile_background_images/458461302696837121/rGlGdWsc.png", 
             "name": "OnThisDay & Facts", 
             "lang": "en", 
             "profile_background_tile": True, 
             "favourites_count": 1383, 
             "screen_name": "NotableHistory", 
             "notifications": False, 
             "url": "http://t.co/9fTPk5A4wh", 
             "created_at": "Tue Sep 25 03:08:59 +0000 2012", 
             "contributors_enabled": False, 
             "time_zone": "Central Time (US & Canada)", 
             "protected": False, 
             "default_profile": False, 
             "is_translator": False
           }, 
           "geo": None, 
           "in_reply_to_user_id_str": None, 
           "possibly_sensitive": False, 
           "lang": "en", 
           "created_at": "Sun Nov 23 20:00:13 +0000 2014", 
           "in_reply_to_status_id_str": None, 
           "place": None, 
           "metadata": {
             "iso_language_code": "en", 
             "result_type": "recent"
           }
         }, 
         "user": {
           "follow_request_sent": False, 
           "profile_use_background_image": True, 
           "profile_text_color": "333333", 
           "default_profile_image": False, 
           "id": 818185729, 
           "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", 
           "verified": False, 
           "profile_location": None, 
           "profile_image_url_https": "https://pbs.twimg.com/profile_images/486215801498640384/rz9o7LnF_normal.jpeg", 
           "profile_sidebar_fill_color": "DDEEF6", 
           "entities": {
             "description": {
               "urls": []
             }
           }, 
           "followers_count": 302, 
           "profile_sidebar_border_color": "C0DEED", 
           "id_str": "818185729", 
           "profile_background_color": "C0DEED", 
           "listed_count": 0, 
           "is_translation_enabled": False, 
           "utc_offset": None, 
           "statuses_count": 395, 
           "description": "Formerly with California Dept of General Services, now freelancing around the Sacramento area...", 
           "friends_count": 1521, 
           "location": "Citrus Heights, CA", 
           "profile_link_color": "0084B4", 
           "profile_image_url": "http://pbs.twimg.com/profile_images/486215801498640384/rz9o7LnF_normal.jpeg", 
           "following": False, 
           "geo_enabled": True, 
           "profile_banner_url": "https://pbs.twimg.com/profile_banners/818185729/1383764759", 
           "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", 
           "name": "M Duncan", 
           "lang": "en", 
           "profile_background_tile": False, 
           "favourites_count": 6544, 
           "screen_name": "MDuncan95814", 
           "notifications": False, 
           "url": None, 
           "created_at": "Tue Sep 11 21:02:09 +0000 2012", 
           "contributors_enabled": False, 
           "time_zone": None, 
           "protected": False, 
           "default_profile": True, 
           "is_translator": False
         }, 
         "geo": None, 
         "in_reply_to_user_id_str": None, 
         "possibly_sensitive": False, 
         "lang": "en", 
         "created_at": "Sun Nov 23 20:53:48 +0000 2014", 
         "in_reply_to_status_id_str": None, 
         "place": None, 
         "metadata": {
           "iso_language_code": "en", 
           "result_type": "recent"
         }
       }
     ]
   }   


Understand
----------

At any level of the extraction process, the first task is to make sure you understand the current object you have extracted. There are few options here.

1. Print the entire object. If it's small enough, you may be able to make sense of the printout directly. If it's a little bit larger, you may find it helpful to "pretty-print" it, with indentation showing the level of nesting of the data. We don't have a way to pretty-print in our online browser-based environment, but if you're running code with a full python interpreter, you can use the dumps function in the json module. For example:

.. sourcecode:: python

   import json
   json.dumps(res, indent = 2)

2. If printing the entire object gives you something that's too unwieldy, you have other options for making sense of it.

   * Print the type of the object.
   * If it's a dictionary:
      * print the keys
   * If it's a list:
      * print its length
      * print the type of the first item
      * print the first item if it's of manageable size

.. activecode:: extract_nested_data_2
   :include: extract_nested_data_1

   print type(res)
   print res.keys()

Extract
-------

In the extraction phase, you will be diving one level deeper into the nested data.

1. If it's a dictionary, figure out which key has the value you're looking for, and get its value. For example: ``res2 = res['statuses']``

2. If it's a list, you will typically be wanting to do something with each of the items (e.g., extracting something from each, and accumulating them in a list). For that you'll want a for loop, such as ``for res2 in res``. During your exploration phase, however, it will be easier to debug things if you work with just one item. One trick for doing that is to iterate over a slice of the list containing just one item. For example, ``for res2 in res[:1]``.

.. activecode:: extract_nested_data_3
   :include: extract_nested_data_1

   print type(res)
   print res.keys()
   res2 = res['statuses']


Repeat
------

Now you'll repeat the Understand and Extract processes at the next level.

Level 2
^^^^^^^

First understand.

.. activecode:: extract_nested_data_3a
   :include: extract_nested_data_1

   print type(res)
   print res.keys()
   res2 = res['statuses'] 
   print type(res2) # it's a list!
   print len(res2)  # looks like one item representing each of the three tweets
      
It's a list, with three items, so it's a good guess that each item represents one tweet.

Now extract. Since it's a list, we'll want to work with each item, but to keep things manageable for now, let's use the trick for just looking at the first item.

.. activecode:: extract_nested_data_4
   :include: extract_nested_data_1

   print type(res)
   print res.keys()
   res2 = res['statuses'] 
   print type(res2) # it's a list!
   print len(res2)  # looks like one item representing each of the three tweets
   for res3 in res2[:1]:
      print "working with a tweet, bound to variable res3"
  
Level 3
^^^^^^^

First understand.

.. activecode:: extract_nested_data_5
   :include: extract_nested_data_1

   print type(res)
   print res.keys()
   res2 = res['statuses'] 
   print type(res2) # it's a list!
   print len(res2)  # looks like one item representing each of the three tweets
   for res3 in res2[:1]:
      print type(res3) # it's a dictionary
      print res3.keys()

Then extract. Let's pull out the information about who sent each of the tweets. Probably that's the value associated with the 'user' key.

.. activecode:: extract_nested_data_6
   :include: extract_nested_data_1

   #print type(res)
   #print res.keys()
   res2 = res['statuses'] 
   #print type(res2) # it's a list!
   #print len(res2)  # looks like one item representing each of the three tweets
   for res3 in res2[:1]:
      #print type(res3) # it's a dictionary
      #print res3.keys()
      res4 = res3['user']
      
Now repeat.

Level 4
^^^^^^^

Understand.

.. activecode:: extract_nested_data_7
   :include: extract_nested_data_1

   #print type(res)
   #print res.keys()
   res2 = res['statuses'] 
   #print type(res2) # it's a list!
   #print len(res2)  # looks like one item representing each of the three tweets
   for res3 in res2[:1]:
      #print type(res3) # it's a dictionary
      #print res3.keys()
      res4 = res3['user']
      print type(res4) # it's a dictionary
      print res4.keys() 

Extract. Let's print out the user's screen name and when their account was created.

.. activecode:: extract_nested_data_8
   :include: extract_nested_data_1

   #print type(res)
   #print res.keys()
   res2 = res['statuses'] 
   #print type(res2) # it's a list!
   #print len(res2)  # looks like one item representing each of the three tweets
   for res3 in res2[:1]:
      #print type(res3) # it's a dictionary
      #print res3.keys()
      res4 = res3['user']
      #print type(res4) # it's a dictionary
      #print res4.keys()
      print res4['screen_name'], res4['created_at']

Now, we may want to go back have it extract for all the items rather than only the first item in res2.  

.. activecode:: extract_nested_data_9
   :include: extract_nested_data_1

   #print type(res)
   #print res.keys()
   res2 = res['statuses'] 
   #print type(res2) # it's a list!
   #print len(res2)  # looks like one item representing each of the three tweets
   for res3 in res2:
      #print type(res3) # it's a dictionary
      #print res3.keys()
      res4 = res3['user']
      #print type(res4) # it's a dictionary
      #print res4.keys()
      print res4['screen_name'], res4['created_at']


Reflections
^^^^^^^^^^^

Notice that each time we descend a level in a dictionary, we have a [] picking out a key. Each time we look inside a list, we will have a for loop. If there are lists at multiple levels, we will have nested for loops.

Once you've figured out how to extract everything you want, you *may* choose to collapse things with multiple extractions in a single expression. For example, we could have this shorter version.

.. activecode:: extract_nested_data_10
   :include: extract_nested_data_1

   for res3 in res['statuses']:
      print res3['user']['screen_name'], res3['user']['created_at']

Even with this compact code, we can still count off how many levels of nesting we have extracted from, in this case four. res['statuses'] says we have descended one level (in a dictionary). for res3 in... says we are have descended another level (in a list). ['user'] is descending one more level, and ['screen_name'] is descending one more level. 

 