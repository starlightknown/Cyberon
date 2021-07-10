
import discord
from bs4 import BeautifulSoup
from datetime import datetime


def parse_mlh_resp(html):
    # scrapping information from the html
    soup = BeautifulSoup(html, 'html.parser')
    hackathons = soup.find_all("div", class_="event")
    # print(hackathons)
    result = []
    for hackathon in hackathons:
        d = {"type": hackathon.find(
            "div", class_="ribbon-wrapper").find("div", class_="ribbon").text.strip()}
        d["logo"] = hackathon.find(
            "div", class_="event-logo").find("img")['src'].strip()
        d["name"] = hackathon.find("h3", class_="event-name").text.strip()
        d["startDate"] = hackathon.find(
            "meta", {"itemprop": "startDate"})["content"]
        d["endDate"] = hackathon.find(
            "meta", {"itemprop": "endDate"})["content"]
        d["location"] = hackathon.find(
            "div", class_="event-location").text.strip()
        d["url"] = hackathon.find(
            "a", class_="event-link")["href"]
        result.append(d)
    return result


def get_pages(hackathons):
    embeds = []

    for ind, hackathon in enumerate(hackathons):
        embed = discord.Embed(
            title="MLH Upcoming Hackthons",
            description="Here is the data for the upcoming hackathons on mlh.io!",
            color=0xFF6500,
        )
        startDate = datetime(*map(int, hackathon['startDate'].split('-')))
        endDate = datetime(*map(int, hackathon['endDate'].split('-')))
        location = hackathon['location'].replace('\n', '')

        embed.add_field(name="Name",
                        value=f"{hackathon['name']}", inline=False)
        embed.add_field(name="Type",
                        value=f"{hackathon['type']}", inline=False)
        embed.add_field(name="Start Date",
                        value=f"{startDate.strftime('%d %b %Y')}", inline=False)
        embed.add_field(name="End Date",
                        value=f"{endDate.strftime('%d %b %Y')}", inline=False)
        embed.add_field(name="Location", value=location, inline=False)
        embed.add_field(name="Link",
                        value=f"[Click here to go to the event page!]({hackathon['url']})",
                        inline=False)

        embed.set_footer(text=f"Page {ind+1}/{len(hackathons)}")
        embed.set_thumbnail(url=f"{hackathon['logo']}")
        embeds.append(embed)

    return embeds
