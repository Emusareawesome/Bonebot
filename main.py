import requests
import bs4
import lxml
import discord

def get_food_list(tag, num):  # TODO: sort by Rosie's, Sizzle, etc. Maybe add some
    food_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                             .button.attrs['aria-controls']).div.find_all(class_="h4 site-panel__daypart-item-title")
    station_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                             .button.attrs['aria-controls']).div.find_all(class_="site-panel__daypart-item-station")

    items = [[]] # separated by station

    for i in range(len(station_elements)):
        if station_elements[i].getText() == '@roots':
            items[0].append(' '.join(food_elements[i].getText().split()))
        elif station_elements[i].getText() == '@sizzle': # @rosies favorites | @pomodoro | @kettles | @market || @rise | @roots || there are probably more, check different days

        items.append(' '.join(i.getText().split()))  # parses string, removes excess \n and \t
    return items


def get_menu():
    global res, lunch, dinner
    res = requests.get('https://rose-hulman.cafebonappetit.com/')
    print(type(res))
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        breakfast = soup.select('#breakfast')[0]
        brunch = soup.select('#brunch')[0]
        lunch = soup.select('#lunch')[0]
        dinner = soup.select('#dinner')[0]

        breakfast_items = get_food_list(breakfast, 0)

        lunch_items = get_food_list(lunch, 1)
        dinner_items = get_food_list(dinner, 2)


    except Exception as exc:
        print('There was a problem %s' % exc)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_menu()
