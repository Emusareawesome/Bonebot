import requests
import bs4


def get_food_list(tag):  # TODO: sort by Rosie's, Sizzle, etc. Maybe add some
    food_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                             .button.attrs['aria-controls']).div.find_all(class_="h4 site-panel__daypart-item-title")
    station_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                                .button.attrs['aria-controls']).div.find_all(class_="site-panel__daypart-item-station")

    items = {}

    for i in range(len(station_elements)):
        station = station_elements[i].getText()
        if station in items:
            items[station].append(' '.join(food_elements[i].getText().split()))
        else:
            items[station] = [' '.join(food_elements[i].getText().split())]

        # if station_elements[i].getText() == '@roots':
        #     items[0].append(' '.join(food_elements[i].getText().split()))
        # elif station_elements[i].getText() == '@sizzle': # @rosies favorites | @pomodoro | @kettles | @market || @rise | @roots || there are probably more, check different days
        #     items[1].append(' '.join(food_elements[i].getText().split()))
        # items.append(' '.join(i.getText().split()))  # parses string, removes excess \n and \t
    return items


def get_menu():
    res = requests.get('https://rose-hulman.cafebonappetit.com/')
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        breakfast = soup.select('#breakfast')
        brunch = soup.select('#brunch')
        lunch = soup.select('#lunch')
        dinner = soup.select('#dinner')

        items = []

        if len(breakfast) != 0:
            items.append(get_food_list(breakfast[0]))
        else:
            items.append([])
        if len(brunch) != 0:
            items.append(get_food_list(brunch[0]))
        else:
            items.append([])
        if len(lunch) != 0:
            items.append(get_food_list(lunch[0]))
        else:
            items.append([])
        if len(dinner) != 0:
            items.append(get_food_list(dinner[0]))
        else:
            items.append([])

        return items
    except Exception as exc:
        print('There was a problem: %s' % exc)
        return []


def menu_embed(items):
    if len(items) == 0:
        return "error getting menu items"
    for i in range(len(items)):
        if len(items[i]) == 0:  # empty
            continue
        if i == 0:  # breakfast

    return "pls fix"
