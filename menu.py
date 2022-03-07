import discord
import requests
import bs4


def get_food_list(tag):
    food_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                             .button.attrs['aria-controls']).div.find_all(class_="h4 site-panel__daypart-item-title")
    station_elements = tag.find(id=tag.find(class_="c-tab__list site-panel__daypart-tab-list")
                                .button.attrs['aria-controls']).div.find_all(class_="site-panel__daypart-item-station")

    items = {}

    # Split up by different stations
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

        soup_items = [soup.select('#breakfast'), soup.select('#brunch'), soup.select('#lunch'), soup.select('#dinner')]

        items = []

        for i in soup_items:
            if len(i) != 0:
                items.append(get_food_list(i[0]))
            else:
                items.append([])

        return items
    except Exception as exc:
        print('There was a problem: %s' % exc)
        return []


def menu_embed(items):
    if len(items) == 0:
        return "error getting menu items"
    embed=discord.Embed(description="Today's Bone Menu", color=0xff0000)
    for i in range(len(items)):
        if len(items[i]) == 0:  # empty
            continue
        # TODO: figure out if subfields are possible; if not, use buttons to switch between different embeds or make separate embed for each meal
        if i == 0:  # breakfast
            # embed.add_field(name="Breakfast", value=items[i].)
            for j in items[i].keys():
                # idk
    embed.set_footer(text='"I lost the game" -Hayden')

    return "pls fix"
