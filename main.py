import requests
import bs4
import lxml
import _ctypes


def get_food_list(tag):  # TODO: sort by Rosie's, Sizzle, etc
    food_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                             .button.attrs['aria-controls']).div.find_all(class_="h4 site-panel__daypart-item-title")
    items = []
    for i in food_elements:
        items.append(' '.join(i.getText().split()))  # parses string, removes excess \n and \t
    return items


def get_menu():
    global res
    res = requests.get('https://rose-hulman.cafebonappetit.com/')
    print(type(res))
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        lunch = soup.select('#lunch')[0]
        dinner = soup.select('#dinner')[0]

        lunch_items = get_food_list(lunch)
        dinner_items = get_food_list(dinner)


    except Exception as exc:
        print('There was a problem %s' % exc)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

