# Downloading script for your ideogram.ai image generation history.

## Rationale

I've generated a ton of images on ideogram. I find it pretty useful to have all of my historical prompts in a file, locally, so I can re-run them for testing new models that come out. I've been through this already with midjourney, dalle-3. Now that Ideogram is unquestionably the best AI image generation tool out there, I want to save up all my prompts.  

Note: here is a C# client for using the ideogram.ai API which is pretty good! (Paid API) https://github.com/ernop/IdeogramApiCSharp

## Instructions

1. You have to fill in a couple of values below to make this work
2. You have to have python3 installed and you will run this like python rip_ideogram_history.py or python3 rip_ideogram_history.py
3. You probably have to do things like 'pip install cloudscraper' or 'pip3 install cloudscraper' in your python environment to get that library installed.
4. But before that you have to fill in some private values related to your authentication on ideogram, within this very file itself.
5. I'm not going to copy or take advantage of your info, but in general, be very careful with the development tools tab. The data you are reading and entering is enough to authenticate as you, so don't share it if people ask for it.
6. For safety, whenever anyone asks for that, please think about maybe posting the whole script or situation to an LLM for analysis, like claude/chatgpt, asking if this is safe to run or if it will leak your data.  
7. That includes this case - please check this script out and validate it's safe.  

That out of the way, here is what you have to get:

1. Your "bearer" authentication token from being logged in to ideogram.
2. Your cookies from the browser, in a development tools window, opened from a logged-in ideogram page you are on.

How to do this

1. Visit ideogram.ai, say in chrome or firefox (my choice)
2. Hit F12 to pop up 'development tools'.
3. Don't get intimidated - you are all right. Step by step.
4. Go to the "Network" tab.
5. Now click back to the browser window and scroll down say on your profile view, or any other page so that your browser will send a request to ideogram
6. then in dev tools, a new row will appear in the list of requests to ideogram.ai
7. If you click on it you can see details on the right, like Headers, Cookies, etc.
8. On the right side within that, there is a tab for the "request headers" section and Authorization part.
9. Copy the entire value of the Authorization header which starts "Bearer" and put that below into YOUR_BEARER
10. Copy the entire value of the Cookie header. (right-click and do "copy value" or similar.  Put that into this script below where it says YOUR_COOKIE
11. Also update your username like below, by replacing YOUR_USERNAME with your actual username
12. Then you can run this script. It'll create a subfolder which will have the json files for all your public/private history of requests to ideogram.

![image](https://github.com/user-attachments/assets/d9d19b54-d538-4281-939b-539cdcd50815)

