from resources.Globals import platform, os

consts = {}

consts['context'] = 'cli'
consts['os_name'] = platform.system()
consts['pc_name'] = os.getenv('COMPUTERNAME', 'NoName-PC')
consts['pc_user'] = os.getlogin()
consts['pc_fullname'] = consts['pc_name'] + ', ' + consts['pc_user']
consts['cwd'] = os.getcwd()
consts["executable"] = os.path.join(consts["cwd"], "executables")
consts["net.global_timeout"] = 1000
consts["logger.skip_categories"] = ["AsyncDownloadManager"]
consts["config.hidden"] = 1

# Executables consts
consts["vk.user_fields"] = "first_name_gen,first_name_acc,last_name_gen,last_name_acc,first_name_ins,last_name_ins,first_name_abl,last_name_abl,about,activities,bdate,blacklisted,blacklisted_by_me,books,can_see_all_posts,career,city,common_count,connections,contacts,counters,country,cover,crop_photo,domain,education,can_write_private_message,exports,employee_mark,employee_working_state,is_service_account,educational_profile,name,type,reposts_disabled,followers_count,friend_status,games,has_photo,has_mobile,has_mail,house,home_town,interests,is_subscribed,is_no_index,is_nft,is_favorite,is_friend,is_followers_mode_on,bdate_visibility,is_dead,image_status,is_hidden_from_feed,is_verified,last_seen,maiden_name,movies,music,military,nickname,online,online_info,occupation,owner_state,personal,photo_200,photo_50,photo_max_orig,quotes,relatives,relation,schools,sex,site,status,tv,universities,verified,wall_default"
consts["vk.group_fields"] = "activity,addresses,age_limits,ban_info,can_create_topic,can_message,can_post,can_suggest,can_see_all_posts,can_upload_doc,can_upload_story,can_upload_video,city,contacts,counters,country,cover,crop_photo,description,fixed_post,has_photo,is_favorite,is_hidden_from_feed,is_subscribed,is_messages_blocked,links,main_album_id,main_section,member_status,members_count,place,photo_50,photo_200,photo_max_orig,public_date_label,site,start_date,finish_date,status,trending,verified,wall,wiki_page"
