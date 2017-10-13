# Author: Brian Hardenstein
# pixelatedbrian@gmail.com

# v0.51 detect the end of a page so if we don't get 1000 reviews (or whatever)
# but we hit the end of page first, prevent scrolling for no reason (wasting
# time)

# v 0.50 add game list tracking so we can try to scrape all 8000+ games
# (yeah, omg)
# import paperbag

# v0.43 added basic error handling when attempting to scrape an app
#   writes exception to error file if it fails
#

# headless scraping that gets around javascript blocks? yes please
from selenium import webdriver

# import MongoDB modules
from pymongo import MongoClient

# we can always use more time
import time

# import our GameIndexer class to help out with things
from game_indexer import GameIndexer

#better console logging
import sys

def get_completed_games():
    '''
    Load in a hard coded filename that is simply a list of
    app_id's where the review scraping has been completed.
    return a list of completed app_ids
    '''
    with open("games_we_have.txt", "r") as infile:
        return [app.strip("\n") for app in infile]

def update_completed_games(app_id):
    '''
    Append to the log file an app_id that has completed
    so that we don't waste time trying to scrape it again
    '''

    with open("games_we_have.txt", "a") as outfile:
        outfile.write(app_id + "\n")

    temp = GameIndexer()

    remaining = len(temp.return_list_of_all_apps()) - len(get_completed_games())
    print "added {} to games_we_have.txt with {} remaining.".format(app_id,
                                                            remaining)

def make_list_of_games_to_scrape():
    '''
    Returns the list of files to work on scraping.
    '''

    # make a list of pending requests starting with a list of all games
    temp = GameIndexer()
    pending_game_list = temp.return_list_of_all_apps()

    # get list of completed games
    completed_games = get_completed_games()

    print
    print "STARTING SIZE OF PENDING GAME LIST:", len(pending_game_list)
    print

    # remove completed games from pending game list
    for game in completed_games:
        # ensure this game is in the list (weirdly occurs sometimes)
        count = pending_game_list.count(game)

        if count != 0:
            pending_game_list.pop(pending_game_list.index(game))

    print
    print "SCRUBBED SIZE OF PENDING GAME LIST:", len(pending_game_list)
    print

    return pending_game_list

def extract_user_from_div(html):
    '''
    Takes in an html div from the steam website and pulls out the user_id
    that is embedded in the profile url
    returns the username as a string
    '''
    # find the profile by splitting by links
    links = html.split("<a href=")

    # step through the different links until we (hopefully) find what we want
    for i in range(1,len(links)):
        # see which link we're examining (debugging)
#         print i
#         print links[i]

        # check to see if the desired url is in this link split
        if "http://steamcommunity.com/id/" in links[i] or "http://steamcommunity.com/profiles/" in links[i]:
            #break out the string that we care about
            path = links[i].split(">")[0].strip('"').encode('ascii', 'ignore')

            # http://steamcommunity.com/id/koltira/
            user_name = path[:-1].split("/")[-1]

            # rarely there is a div in the username, trying to figure out why
            if "div" in user_name:
                for item in links:
                    print "####################### Error in username:", item
                    print
                    print

            # mission complete, return the username
            return user_name

    # It seems like some users don't have alias/usernames but still have
    # profile numbers.  Attempt to fail down to this profile # and use
    # that in place of the username


    return "-17 Error extracting username"

def extract_review_from_subdiv(review_html):
    '''
    Having been provided the div that contains the review text attempt
    to strip out some extra formatting and html and return a string
    that contains the written review.
    return the review as a string
    '''
    # chop out the junk div with the date in front
    #
    # ex:
    # u'\n\t\t\t\t<div class="date_posted">Posted: July 2</div>\n\t\t\t\t\t\t\t\t\t
    # \t\t\ti had 20 hours into this game within 2 days of buying
    # it please send help\t\t\t'

#     print
#     print review_html
#     print

    raw_review = review_html.split("/div>")[1].encode("ascii", "ignore")

    review = " ".join(raw_review.split())

    return review

def extract_rating_from_div(html):
    '''
    Take in review tab html and extract if the user did thumbs up
    or thumbs down
    Return 1 if thumbs up, otherwise return 0
    '''
    vote = html.get_attribute("innerHTML")

    # try to be specific
    # if it's Recommended return 1
    # if it's Not Recommended return 0
    # if it's something else return -17 and print an error
    # (negative values being indicators that something unexpected occurred)
    if vote.lower() == "recommended":
        return 1
    elif vote.lower() == "not recommended":
        return 0
    else:
        print "Error in extract_rating_from_div!!! vote =", vote
        return -17


def get_game_reviews(app_id, count, app_title="test"):
    '''
    Using the path and the app_id go to the review website for a game
    and pull the first <count> top rated reviews for both positive and
    negative. (or the number of reviews that do exist if there's less than
    1000 reviews)
    returns:
    dictionary that contains:
    {
        "app_id": xxxx,
        "title": yyyy,
        "positive_reviews" : [<list of user info dictionaries>],
        "negative_reviews": [<list of user info dictionaries>]
    }
    '''

    pos_path = "http://steamcommunity.com/app/{}/positivereviews/?p=1&browsefilter=toprated".format(app_id)
    neg_path = "http://steamcommunity.com/app/{}/negativereviews/?p=1&browsefilter=toprated".format(app_id)

    pos_reviews = strip_mine_path(pos_path, count)
    neg_reviews = strip_mine_path(neg_path, count)


    results = {
        "app_id": app_id,
        "title": app_title,
        "positive_reviews": pos_reviews,
        "negative_reviews": neg_reviews
    }

    return results


def strip_mine_path(path, count):
    '''
    Drill into the path provided and pull <count> amount
    of reviews.  Process the page and pull data from the
    review divs. Insert data into a small dictionary and
    add it to an ongoing list.
    Returns:
    List of user reviews which consist of dictionaries.
    ex:
    {"user_id": user_id, "rating": 1, "review": 'review text'}
    '''

    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.set_window_size(900, 800)
    driver.get(path)

    assert "Steam" in driver.title

    print "Tabs loading:"
    # try to scroll down several times then slight pause before scrolling again
    # count // 10 because there's 10 reviews per page
    for x in range(count // 10):
        time.sleep(1)

        if x == 0:
            previous_page = len(driver.page_source)

        # try to get the before height
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # trying to scroll down
        time.sleep(1)

        current_page = len(driver.page_source)

        if current_page == previous_page:
            print "seems like hit the end of the page, breaking now"
            break
        else:
            previous_page = current_page

        # print on the same line for console log
        # print "{}th tab of reviews loading...\r".format(x) ,
        #print "{},".format(x),
        print "{}\r".format(x),



    # At this point data should be loaded by the page
    # start processing!
    big_results = driver.find_elements_by_class_name("apphub_Card")

    # find the div with the review text
    text_results = driver.find_elements_by_class_name("apphub_CardTextContent")

    # find the div with thumbs up/down
    y_labels =  driver.find_elements_by_class_name("title")

    print
    print "Number of divs found:", len(big_results)
    print
    print

    user_data = []
    user_set = set()

    # step through all off the resulting divs
    # use an index because we access multiple lists
    # at the same place
    for idx in xrange(len(big_results)):

        # full review div element
        big_result = big_results[idx]
        text_result = text_results[idx]
        y_label = y_labels[idx]

        # extract html from selenium element
        big_data = big_result.get_attribute("innerHTML")
        text_review = text_result.get_attribute("innerHTML")
        raw_text_review = big_result.find_element_by_class_name("apphub_CardTextContent").get_attribute("innerHTML")

        # extract data
        text_review = extract_review_from_subdiv(raw_text_review)
        user_name = extract_user_from_div(big_data)
        rating = extract_rating_from_div(y_label)

        # consolidate data (not being appended to a list anymore but
        # still of use for printing to the log)
        user_info = {"user":user_name,
                     "rating":rating,
                     "review":text_review}

        # add data to list
        # user_data.append(user_info)

        user_set.add((user_name, rating, text_review))

        # log what was found on screen

        if idx % 25 == 0:
            print "Rating: {} User: {:<20} Review: {:<40}\r".format(user_info["rating"],
                                                              user_info["user"],
                                                              user_info["review"][:50])
        else:
            print "Rating: {} User: {:<20} Review: {:<40}\r".format(user_info["rating"],
                                                              user_info["user"],
                                                              user_info["review"][:50]),

    # close the web page
    driver.close()

    print "list len:", len(user_data)
    print "set len:", len(user_set)

    # mongoDB doesn't like sets, convert to a list of dictionaries that happens
    # to have unique entries
    results = [{"user":user[0], "rating":user[1], "review":user[2]}  for user in user_set]

    return results

def insert(collection, dictionary, _key):
    '''
    Using the provided collection attempt to add the provided dictionary
    to the collection. Check to see if the new dictionary being added
    already exists in the collection before adding.
    '''
    if not collection.find_one({_key: dictionary[_key]}):
        try:
            collection.insert_one(dictionary)
            print "inserted", dictionary[_key]

            # add to completed lists
            update_completed_games(str(dictionary["app_id"]))

        except Exception, e:
            print e

    else:
        print dictionary[_key], "already exists"

def scrape_to_db(collection, app_id_list, count):
    '''
    Attempt to scrape <count> reviews from each game in the <app_list>
    and then try to add the resulting dictionary to the provided
    <collection>.
    '''

    # get list of apps/titles so we can populate the database with more data
    _gameindexer = GameIndexer()

    # step through each app in the list and try to scrape the reviews
    for app_id in app_id_list:

        # add try to make it more fault tolerant
        try:

            title = _gameindexer.return_game_title(app_id)



            # go get the game reviews
            game_results = get_game_reviews(app_id, 1150, title)

            insert(collection, game_results, "app_id")

        except Exception, e:
            error = "############################ Exception {} occurred! \n \
            ############################ Scrape of {} failed".format(e, app_id)

            print error

            with open("ERROR_selenium_game_review_scrape.txt", "w") as _file:
                _file.write(error)

def main():
    '''
    For __name__ == "__main__" establish link to db/collection
    and start scraping
    '''
    # connect to the hosted MongoDB instance
    db = MongoClient('mongodb://localhost:27017/')["capstone"]

    dest_collection = db.selenium_game_review_scrape

     # list_of_apps = ["413150", "367520", "286160", "246620", "257850", "105600", "211820", "311690", "233450", "250760"]

    # widen the pool with 90 games
    # big_app_list = ['427520', '371200', '398850', '264710', '219150', '431120',\
    #  '252950', '210970', '290340', '281640', '475190', '261180', '322110', \
    #  '274500', '204360', '107100', '554600', '425580', '474750', '296470', \
    #  '405640', '220780', '595140', '234650', '222880', '26800', '251570',\
    #   '433340', '308420', '212680', '265930', '239820', '312530', '294100',\
    #    '221910', '356570', '247080', '470260', '383870', '231160', '421120', \
    #    '65300', '230190', '318230', '9500', '387290', '231200', '265000', \
    #    '304430', '469820', '365450', '253250', '435530', '250700', '361300', \
    #    '219990', '367450', '326460', '206190', '391540', '527230', '48000', \
    #    '505730', '364420', '251270', '271240', '275850', '504210', '387990',\
    #     '95300', '568220', '4000', '205730', '237990', '329130', '242760', \
    #     '457140', '239030', '538100', '241600', '322500', '394970', '396750', \
    #     '305620', '282070', '437220', '258030', '22000', '248820', '224760']

    #list_of_apps = big_app_list[:30]
    #list_of_apps = big_app_list[31:60]
    #list_of_apps = big_app_list[61:90]

    big_app_list = make_list_of_games_to_scrape()

    # try to make the list break into pieces so we can multiprocess
    # via tmux
    chunk_size = len(big_app_list) // 3

    #list_of_apps = big_app_list[:chunk_size]
    #list_of_apps = big_app_list[chunk_size+1:chunk_size *2]
    list_of_apps = big_app_list[chunk_size *2 +1:]

    # give slightly more size than desired target because some divs will lag
    # during load.  For the smaller set try to get about 1000. For the big
    # test set try to get ~10,000
    scrape_to_db(dest_collection, list_of_apps, 1150)

if __name__ == "__main__":
    main()
