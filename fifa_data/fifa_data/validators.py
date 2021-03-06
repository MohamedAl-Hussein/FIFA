import datetime

from schematics.models import Model
from schematics.types import DateTimeType, DecimalType, IntType, ListType, \
    StringType, URLType


class ProxyItem(Model):

    ip_dump = StringType(required=True)


class UserAgentItem(Model):

    user_agent = StringType(required=True)
    version = StringType()
    OS = StringType()
    hardware_type = StringType()
    popularity = StringType()


class PlayerItem(Model):

    id = IntType(required=True)
    total_stats = IntType()
    hits = StringType()
    comments = StringType()
    # TODO: create separate class for player_pages spider as the
    # player_page is not available for the player_detail
    #  spider, causing problems in the stats logger.
    player_page = URLType(required=True)

    name = StringType()
    full_name = StringType()
    age = IntType()
    dob = DateTimeType(default=datetime.datetime.now)
    height = IntType()
    weight = IntType()
    nationality = StringType()

    preferred_foot = StringType()
    international_reputation = IntType()
    weak_foot = IntType()
    skill_moves = IntType()
    work_rate = StringType()
    body_type = StringType()
    real_face = StringType()

    value = DecimalType()
    wage = DecimalType()
    release_clause = DecimalType()
    club_name = StringType()
    club_rating = IntType()
    club_position = StringType()
    club_jersey_number = IntType()
    club_join_date = DateTimeType(default=datetime.datetime.now)
    loaned_from = StringType()
    club_contract_end_date = DateTimeType(default=datetime.datetime.now)
    team_name = StringType()
    team_rating = IntType()
    team_position = StringType()
    team_jersey_number = IntType()

    overall_rating = IntType()
    potential_rating = IntType()
    positions = ListType(StringType)
    unique_attributes = ListType(StringType)

    DIV = IntType()
    HAN = IntType()
    KIC = IntType()
    REF = IntType()
    SPD = IntType()
    POS = IntType()

    PAC = IntType()
    SHO = IntType()
    PAS = IntType()
    DRI = IntType()
    DEF = IntType()
    PHY = IntType()
    vision = IntType()
    penalties = IntType()

    crossing = IntType()
    finishing = IntType()
    heading_accuracy = IntType()
    short_passing = IntType()
    volleys = IntType()
    aggression = IntType()
    interceptions = IntType()
    positioning = IntType()
    composure = IntType()
    dribbling = IntType()
    curve = IntType()
    fk_accuracy = IntType()
    long_passing = IntType()
    ball_control = IntType()
    marking = IntType()
    standing_tackle = IntType()
    sliding_tackle = IntType()
    acceleration = IntType()
    sprint_speed = IntType()
    agility = IntType()
    reactions = IntType()
    balance = IntType()
    gk_diving = IntType()
    gk_handling = IntType()
    gk_kicking = IntType()
    gk_positioning = IntType()
    gk_reflexes = IntType()
    shot_power = IntType()
    jumping = IntType()
    stamina = IntType()
    strength = IntType()
    long_shots = IntType()
    traits = ListType(StringType)

    LS = ListType(IntType)
    ST = ListType(IntType)
    RS = ListType(IntType)
    LW = ListType(IntType)
    LF = ListType(IntType)
    CF = ListType(IntType)
    RF = ListType(IntType)
    RW = ListType(IntType)
    LAM = ListType(IntType)
    CAM = ListType(IntType)
    RAM = ListType(IntType)
    LM = ListType(IntType)
    LCM = ListType(IntType)
    CM = ListType(IntType)
    RCM = ListType(IntType)
    RM = ListType(IntType)
    LWB = ListType(IntType)
    LDM = ListType(IntType)
    CDM = ListType(IntType)
    RDM = ListType(IntType)
    RWB = ListType(IntType)
    LB = ListType(IntType)
    LCB = ListType(IntType)
    CB = ListType(IntType)
    RCB = ListType(IntType)
    RB = ListType(IntType)

    followers = IntType()
    likes = IntType()
    dislikes = IntType()

    face_img = URLType()
    flag_img = URLType()
    club_logo_img = URLType()
    team_logo_img = URLType()


class ClubItem(Model):
    id = IntType(required=True)
    nationality = StringType()
    region = StringType()
    num_players = IntType()
    hits = StringType()
    comments = StringType()
    club_page = URLType(required=True)

    club_name = StringType()
    division = StringType()
    club_logo = URLType()
    flag = URLType()

    overall = IntType()
    attack = IntType()
    midfield = IntType()
    defence = IntType()
    home_stadium = StringType()
    rival_team = StringType()
    international_prestige = IntType()
    domestic_prestige = IntType()
    transfer_budget = DecimalType()
    starting_xi_average_age = DecimalType()
    whole_team_average_age = DecimalType()
    captain = IntType()
    short_free_kick = IntType()
    long_free_kick = IntType()
    left_short_free_kick = IntType()
    right_short_free_kick = IntType()
    penalties = IntType()
    left_corner = IntType()
    right_corner = IntType()
    starting_xi = ListType(IntType)

    defence_defensive_style = StringType()
    defence_depth = IntType()
    offense_offensive_style = StringType()
    offense_width = IntType()
    offense_players_in_box = IntType()
    offense_corners = IntType()
    offense_free_kicks = IntType()
    build_up_play_speed = IntType()
    build_up_play_dribbling = IntType()
    build_up_play_passing = IntType()
    build_up_play_positioning = IntType()
    chance_creation_passing = IntType()
    chance_creation_crossing = IntType()
    chance_creation_shooting = IntType()
    chance_creation_positioning = IntType()
    defence_extra_pressure = IntType()
    defence_extra_aggression = IntType()
    defence_extra_team_width = IntType()
    defence_extra_defender_line = StringType()

    squad = ListType(IntType)
    on_loan = ListType(IntType)
    kits = ListType(URLType)

    likes = IntType()
    dislikes = IntType()


class TeamItem(ClubItem):
    team_page = URLType(required=True)

    team_name = StringType()
    team_logo = URLType()
