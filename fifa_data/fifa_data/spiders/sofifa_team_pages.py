import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.loader import ItemLoader
from scrapy.utils.log import configure_logging

from pymongo import MongoClient
from twisted.internet import reactor

from fifa_data.items import NationalTeamDetailedStats
from fifa_data.mongodb_addr import host, port
from fifa_data.sofifa_settings import sofifa_settings
from proxies.proxy_generator import gen_proxy_list
from user_agents.user_agent_generator import gen_useragent_list


class SofifaTeamPagesSpider(scrapy.Spider):

    """
    Visits the urls collected by SofifaTeamUrlsSpider and scrapes data
    from those urls. Data is stored inside the team_details collection
    at mongodb://mongo_server:27017/sofifa
    """

    name = 'team_details'

    proxies = gen_proxy_list()
    user_agent = gen_useragent_list()

    custom_settings = sofifa_settings(
        name=name,
        database='sofifa',
        collection='team_details',
        proxies=proxies,
        user_agent=user_agent,
        validator='TeamItem'
    )

    allowed_domains = [
        'sofifa.com'
    ]

    def start_requests(self):

        client = MongoClient(host, port)
        db = client.sofifa
        collection = db.team_urls

        urls = [x["team_page"] for x in collection.find(
                {
                    'team_page': {
                        '$exists': 'true'
                    }
                }
            )]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):

        loader = ItemLoader(
            NationalTeamDetailedStats(),
            response=response
        )

        team_spacing_loader = loader.nested_xpath(
            ".//div[contains(@class, 'team')]"
        )

        loader.add_value(
            'last_modified',
            datetime.utcnow()
        )

        # GENERAL TEAM INFORMATION

        loader.add_xpath(
            'id',
            ".//div[@class='info']/h1/text()"
        )
        loader.add_xpath(
            'team_name',
            ".//div[@class='info']/h1/text()"
        )
        loader.add_xpath(
            'team_logo',
            ".//div[contains(@class, 'card')]/img/@data-src"
        )
        loader.add_xpath(
            'flag',
            ".//div[contains(@class, 'meta')]//img/@data-src"
        )

        # GENERAL TEAM STATS

        loader.add_xpath(
            'overall',
            ".//div[contains(@class, 'stats')]/div/div[1]/span/text()"
        )
        loader.add_xpath(
            'attack',
            ".//div[contains(@class, 'stats')]/div/div[2]/span/text()"
        )
        loader.add_xpath(
            'midfield',
            ".//div[contains(@class, 'stats')]/div/div[3]/span/text()"
        )
        loader.add_xpath(
            'defence',
            ".//div[contains(@class, 'stats')]/div/div[4]/span/text()"
        )

        # DETAILED TEAM STATS

        # Note: this stat seams to be missing as of 06/17/2019
        team_spacing_loader.add_xpath(
            'home_stadium',
            "./ul/li/following::label[contains(., 'Home Stadium')]"\
            "/following::text()[1]"
        )
        team_spacing_loader.add_xpath(
            'rival_team',
            "./ul/li/following::label[contains(., 'Rival Team')]"\
            "/following::a[1]/@href"
        )
        team_spacing_loader.add_xpath(
            'international_prestige',
            "./ul/li/following::label[contains(., 'International Prestige')]"\
            "/following::span[1]/text()"
        )
        team_spacing_loader.add_xpath(
            'starting_xi_average_age',
            "./ul/li/following::label[contains(., 'Starting XI Average Age')]"\
            "/following::text()[1]"
        )
        team_spacing_loader.add_xpath(
            'whole_team_average_age',
            "./ul/li/following::label[contains(., 'Whole Team Average Age')]"\
            "/following::text()[1]"
        )
        team_spacing_loader.add_xpath(
            'captain',
            "./ul/li/following::label[contains(., 'Captain')]"\
            "/following::a[1]/@href"
        )
        loader.add_xpath(
            'short_free_kick',
            "(.//div[contains(@class, 'team')]/ul/li"\
            "/following::label[contains(., 'Short Free Kick')]"\
            "/following::a[1])[1]/@href"
        )
        loader.add_xpath(
            'long_free_kick',
            "(.//div[contains(@class, 'team')]/ul/li"\
            "/following::label[contains(., 'Long Free Kick')]"\
            "/following::a[1])[1]/@href"
        )
        loader.add_xpath(
            'left_short_free_kick',
            "(.//div[contains(@class, 'team')]/ul/li"\
            "/following::label[contains(., 'Left Short Free Kick')]"\
            "/following::a[1])[1]/@href"
        )
        loader.add_xpath(
            'right_short_free_kick',
            "(.//div[contains(@class, 'team')]/ul/li"\
            "/following::label[contains(., 'Right Short Free Kick')]"\
            "/following::a[1])[1]/@href"
        )
        team_spacing_loader.add_xpath(
            'penalties',
            "./ul/li/following::label[contains(., 'Penalties')]"\
            "/following::a[1]/@href"
        )
        team_spacing_loader.add_xpath(
            'left_corner',
            "./ul/li/following::label[contains(., 'Left Corner')]"\
            "/following::a[1]/@href"
        )
        team_spacing_loader.add_xpath(
            'right_corner',
            "./ul/li/following::label[contains(., 'Right Corner')]"\
            "/following::a[1]/@href"
        )
        team_spacing_loader.add_xpath(
            'starting_xi',
            ".//div[contains(@class, 'lineup')]/div/a/@href"
        )

        # TACTICS

        loader.add_xpath(
            'defence_defensive_style',
            ".//dl//span/preceding::dd[text()='Defensive Style']/span/span/"\
            "text()"
        )
        loader.add_xpath(
            'defence_team_width',
            "(.//dl//span/preceding::span[text()='Team Width']"\
            "/following::span[1]/span/text())[1]"
        )
        loader.add_xpath(
            'defence_depth',
            ".//dl//span/preceding::span[text()='Depth']/following::span[1]"\
            "/span/text()"
        )
        loader.add_xpath(
            'offense_offensive_style',
            ".//dl//span/preceding::dd[text()='Offensive Style']/span/span/"\
            "text()"
        )
        loader.add_xpath(
            'offense_width',
            ".//dl//span/preceding::span[text()='Width']/following::span[1]"\
            "/span/text()"
        )
        loader.add_xpath(
            'offense_players_in_box',
            ".//dl//span/preceding::span[text()='Players in box']"\
            "/following::span[1]/span/text()"
        )
        loader.add_xpath(
            'offense_corners',
            ".//dl//span/preceding::span[text()='Corners']/following::span[1]"\
            "/span/text()"
        )
        loader.add_xpath(
            'offense_free_kicks',
            ".//dl//span/preceding::span[text()='Free Kicks']"\
            "/following::span[1]/span/text()"
        )
        loader.add_xpath(
            'build_up_play_speed',
            ".//dl//span/preceding::span[text()='Speed']/following::span[1]"\
            "/span/text()"
        )
        loader.add_xpath(
            'build_up_play_dribbling',
            ".//dl//span/preceding::dd[text()='Dribbling']/span/span/text()"
        )
        loader.add_xpath(
            'build_up_play_passing',
            "(.//dl//span/preceding::span[text()='Passing']"\
            "/following::span[1]/span/text())[1]"
        )
        loader.add_xpath(
            'build_up_play_positioning',
            "(.//dl//span/preceding::span[text()='Positioning'])[1]"\
            "/following::span[1]/text()"
        )
        loader.add_xpath(
            'chance_creation_passing',
            "(.//dl//span/preceding::span[text()='Passing']"\
            "/following::span[1]/span/text())[2]"
        )
        loader.add_xpath(
            'chance_creation_crossing',
            ".//dl//span/preceding::span[text()='Crossing']"\
            "/following::span[1]/span/text()"
        )
        loader.add_xpath(
            'chance_creation_shooting',
            ".//dl//span/preceding::span[text()='Shooting']"\
            "/following::span[1]/span/text()"
        )
        loader.add_xpath(
            'chance_creation_positioning',
            "(.//dl//span/preceding::span[text()='Positioning'])[2]"\
            "/following::span[1]/text()"
        )
        loader.add_xpath(
            'defence_extra_pressure',
            ".//dl//span/preceding::span[text()='Pressure']"\
            "/following::span[1]/span/text()"
        )
        loader.add_xpath(
            'defence_extra_aggression',
            ".//dl//span/preceding::span[text()='Aggression']"\
            "/following::span[1]/span/text()"
        )
        loader.add_xpath(
            'defence_extra_team_width',
            "(.//dl//span/preceding::span[text()='Team Width']"\
            "/following::span[1]/span/text())[2]"
        )
        loader.add_xpath(
            'defence_extra_defender_line',
            ".//span[text()='Defender Line']/following::span/text()"
        )

        # PLAYERS

        loader.add_xpath(
            'squad',
            "(.//table)[1]/tbody/tr//a[contains(@href, '/player/')]/@href"
        )
        loader.add_xpath(
            'on_loan',
            "(.//table)[2]/tbody/tr//a[contains(@href, '/player/')]/@href"
        )

        # MEDIA

        loader.add_xpath(
            'kits',
            ".//div[@class='column col-sm-5 text-center']//img/@src"
        )

        # COMMUNITY

        add_xpath(
            'likes',
            "(//div[contains(@class, 'operation spacing')]/a/span[2]/span"\
            "/text())[1]"
        )

        add_xpath(
            'dislikes',
            "(//div[contains(@class, 'operation spacing')]/a/span[2]/span"\
            "/text())[2]"
        )

        print(response.request.headers['User-Agent'])

        self.logger.info(f'Parse function called on {response.url}')

        yield loader.load_item()


def main():

    """
    Run this spider a single time only.
    """

    configure_logging()
    runner = CrawlerRunner(SofifaTeamPagesSpider)

    d = runner.crawl()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    main()
