import instaloader
import pandas as pd
import time
import logging
import os

logging.basicConfig(filename='instaloader.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

def login_instaloader(username, password):
    
    L = instaloader.Instaloader()
    try:
        L.login(username, password)
    except instaloader.exceptions.BadCredentialsException:
        logging.error("Invalid username or password.")
        print("Invalid username or password. Check log for details.")
        return None
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        logging.error("Two-factor authentication is required.")
        print("Two-factor authentication is required. Check log for details.")
        return None
    except Exception as e:
        logging.error(f"Error logging in: {e}")
        print(f"Failed to login. Check log for details: {e}")
        return None
    return L

def download_posts(L, profile_name):
 
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
    except Exception as e:
        logging.error(f"Error loading profile: {e}")
        print("Failed to load profile. Check log for details.")
        return []

    posts_info = []
    for post in profile.get_posts():
        try:
        
            L.download_post(post, target=f"{profile_name}_posts")

            posts_info.append({
                'url': post.url,
                'caption': post.caption,
                'likes': post.likes,
                'date': post.date,
            })

            time.sleep(5)
        except Exception as e:
            logging.error(f"Error downloading post: {e}")
            print("Failed to download post. Check log for details.")
    
    return posts_info

def save_to_csv(posts_info, filename='instagram_posts.csv'):
    
    try:
        df = pd.DataFrame(posts_info)
        df.to_csv(filename, index=False)
        print(f"Saved {len(posts_info)} posts to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")
        print("Failed to save to CSV. Check log for details.")

def main(username, password, profile_name):
   
    L = login_instaloader(username, password)
    if L:
        posts_info = download_posts(L, profile_name)
        if posts_info:
            save_to_csv(posts_info)

if __name__ == "__main__":
    username = ''
    password = ''
    profile_name = ''

    main(username,password,profile_name)
