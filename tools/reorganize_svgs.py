#!/usr/bin/env python3
"""
reorganize_svgs.py — Reorganize SVG designs from product-based to theme-based categories.

For SOURCE folder: creates _organized/ subfolder with copies (originals untouched)
For SITE folder: replaces old structure with new theme-based categories

Run from project root: python tools/reorganize_svgs.py
"""

import os
import shutil
import sys
from pathlib import Path
from collections import defaultdict

# ============================================================
# PATHS
# ============================================================
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent

SOURCE_SVG_ROOT = Path(r"C:\Users\steve\iCloudDrive\Laser\SVGGalleryProject\svgs")
SITE_DESIGNS_DIR = PROJECT_ROOT / "assets" / "designs"

# ============================================================
# CATEGORY DEFINITIONS
# ============================================================
CATEGORIES = [
    "Family",
    "Work",
    "Humor",
    "Drinks",
    "Wedding",
    "Bachelorette",
    "Golf",
    "Inspirational_Quotes",
    "Family_Monograms",
    "Charcuterie",
    "Cutting_Boards_Kitchen",
    "Seasonal_Holiday",
    "Home_Cozy",
    "Fitness",
    "Maps",
]

# ============================================================
# EXPLICIT FILE-TO-CATEGORY MAPPING
# Keys: (source_subfolder, filename_stem) -> category
# For files specified with just a stem, we look in the appropriate folder
# ============================================================

def build_explicit_map():
    """Build a mapping of (subfolder, filename_stem_lower) -> category."""
    m = {}

    def add(subfolder, stems, category):
        for stem in stems:
            key = (subfolder.lower(), stem.lower())
            m[key] = category

    # ---- Family ----
    family_coaster_stems = [
        "SVG_Allbecausetwopeoplefellinlove",
        "SVG_Everyfamilyhasastorythisisours",
        "SVG_Everythingthatmattersmostishome",
        "SVG_Familyajourneyforever",
        "SVG_Familyanyonewholovesyou",
        "SVG_Familyanyonewholovesyouunconditionally",
        "SVG_Familyisanyonewholovesyouunconditionally",
        "SVG_Forthisfamilywearegrateful",
        "SVG_Friendsandfamilygatherhere",
        "SVG_Lifeisbetterathome",
        "SVG_Myfamilyaremybestfriends",
        "SVG_Ourfamilyismadewithchaosandlove",
        "SVG_Ourfamilyisrootedinlove",
        "SVG_Thishomehasendlessloveandlaundry",
        "SVG_Thishomeisfalloflove",
        "SVG_Timespentwithfamilyiswortheverysecond",
        "SVG_Yayyourehome",
        "SVG_Somecallitchaoswecallitlove",
        "SVG_Iliveinacastlecalledhome",
        "SVG_Blessthishome",
    ]
    add("Coasters_svgs", family_coaster_stems, "Family")

    # Live Laugh Love at root level
    m[("", "live laugh love")] = "Family"

    family_cutting_stems = [
        "cutting_boards_B-I_Bless_the_food_before_us_the_family_beside_us___the_love_between_us_svg",
        "cutting_boards_B-I_family_gathers_here_svg",
        "cutting_boards_K-W_kitchens_are_made_for_bringing_families_together_svg",
        "cutting_boards_K-W_meals_and_memories_are_made_here_svg",
        "cutting_boards_K-W_meals_and_memories_are_made_in_mom_s_kitche_svg",
        "cutting_boards_B-I_everything_tastes_better_when_grandma_makes_it_svg",
        "cutting_boards_B-I_grandma_s_kitchen_good_food_served_daily_with_a_heaping_spoon_of_love_svg",
        "cutting_boards_B-I_grandma_s_kitchen_where_sweet_things_happen_svg",
        "cutting_boards_K-W_love_served_daily_dad_s_kitchen_open_24_hour_svg",
        "cutting_boards_K-W_love_served_daily_mom_s_kitchen_breakfast_lunch_dinner_open_24_hours_svg",
        "cutting_boards_K-W_love_served_daily_mom_s_kitchen_svg",
        "cutting_boards_K-W_mama_s_kitchen_svg",
        "cutting_boards_K-W_mom_s_kitchen_all_food_chopped_with_love_svg",
        "cutting_boards_K-W_mom_s_kitchen_open_247_svg",
        "cutting_boards_K-W_Kitchen_the_best_of_times_are_always_found_when_friends_and_family_gather_around_svg",
        "cutting_boards_T-W_this_kitchen_is_blessed_svg",
        "cutting_boards_B-I_good_food_good_friends_good_times_svg",
    ]
    add("cuttingboards_svgs", family_cutting_stems, "Family")

    # Charcuterie -> Family
    add("Charcuterie_svgs", ["Bless_The_Food_Before_Us"], "Family")

    # ---- Work ----
    work_coaster_stems = [
        "SVG_Adultingtimeinsession",
        "SVG_Anotherdaycompletelyruinedby",
        "SVG_Backtothegrind",
        "SVG_Beingmycolleagueistheonlygiftyouneed",
        "SVG_Beingmycoworkeristheonlygiftyouneed",
        "SVG_Coffeeismyfavoritecoworker",
        "SVG_Coffeeismyfavouritecoworker",
        "SVG_IdonthaveenoughenergytopretendIlikeyou",
        "SVG_Idonthavethetimetohavethebreakdown",
        "SVG_Ineverfacemondaymorningbluesbceauseoffuncolleagueslikeyou",
        "SVG_Ineverfacemondaymorningbluesbceauseoffuncoworkerslikeyou",
        "SVG_Ipretendtoworktheypretendtopayme",
        "SVG_JustknoweveryminuteImatwork",
        "SVG_Letmedropeverythingandworkonyourproblem",
        "SVG_Myfavoritecoworkergavemethis",
        "SVG_Myfavouritecoworkergavemethis",
        "SVG_Myhobbyisannoyingmycoworkers",
        "SVG_Nottheworstemployee",
        "SVG_Thebestthingaboutmyjobisthatthechairspins",
        "SVG_Workforminutestakebreaksforhours",
        "SVG_Workmadeuscoworkers",
        "SVG_Workuninstalling",
    ]
    add("Coasters_svgs", work_coaster_stems, "Work")
    add("flask_svgs", ["This_is_My_Networking_Flask"], "Work")

    # ---- Humor ----
    humor_coaster_stems = [
        "SVG_Iamallergictostupidity",
        "SVG_IamnotmessyIamcreativelyorganised",
        "SVG_Idontalwaystoleratestupidpeople",
        "SVG_Idontneedamotivationalquote",
        "SVG_IhaveitalltogetherIjustforgotwhereIputit",
        "SVG_ImaybewrongbutIdoubtit",
        "SVG_Imfinebuttherestofyouneedtherapy",
        "SVG_ImnotsarcasticIamjustintelligent",
        "SVG_ImonlysarcasticwhenIspeak",
        "SVG_Imsarcasticbecausepunchingpeopleintheface",
        "SVG_ImsorrydidIrollmyeyesoutloud",
        "SVG_Nobodycaresaboutyourdrama",
        "SVG_NopeIamgoingbacktobed",
        "SVG_Notgoingouttoday",
        "SVG_Placecupheretoavoidmywrath",
        "SVG_RememberwhenIwaskedforyouropinion",
        "SVG_Sarcasticawkwardsweaty",
        "SVG_SorryIdontspeakidiot",
        "SVG_Sorryaboutthemessbutwelivehere",
        "SVG_Useacoasterandnoonegetshurt",
        "SVG_Youareentitledtoyourwrongopinion",
        "SVG_Youinspiremyinnerserialkiller",
        "SVG_Youmustbeexhaustedwatchingmedoeverything",
        "SVG_Youredeadtousnow",
        "SVG_Irefusetobecomewhatyoucallnormal",
        "SVG_Iwishmorepeoplewerefluentinsilence",
        "SVG_IwontquitbutIwillcussthewholetime",
        "SVG_Donotletmeadult",
        "SVG_Youcantmakeeveryonehappyyouarentwine",
        "SVG_Idrinkbeerforyourprotection",
        "SVG_Idrinkginforyourprotection",
        "SVG_Idrinkcoffeeforyourprotection",
        "SVG_Idrinkteaforyourprotection",
        "SVG_Idrinkwineforyourprotection",
        "SVG_Ringsareforfingersnottables",
        "SVG_Dontruinmytableuseacoaster",
        "SVG_Dontmessupmytable",
        "SVG_Dontmessupthetable",
        "Don_t_Mess_Up_Table",
        "Use_A_Coaster_Or_I_Will_Poke_You_In_The_Eye",
    ]
    add("Coasters_svgs", humor_coaster_stems, "Humor")

    humor_cutting_stems = [
        "cutting_boards_B-I_I_m_sorry_for_what_i_said_when_I_was_hungry_svg",
        "cutting_boards_B-I_I_only_eat_hole_foods_svg",
        "cutting_boards_B-I_hangry_adj.-_a_state_of_anger_caused_by_lack_of_food_svg",
        "cutting_boards_K-W_Many_Have_Eaten_Here_Few_Have_Died_svg",
        "cutting_boards_K-W_less_drama_more_pizza_svg",
        "cutting_boards_K-W_my_kitchen_my_rules_svg",
        "cutting_boards_K-W_real_man_cook_svg",
        "cutting_boards_K-W_real_man_play_with_fire_svg",
        "cutting_boards_T-W_the_chef_is_always_right_svg",
        "cutting_boards_T-W_the_oven_is_hot_but_the_cook_is_hotter_svg",
        "cutting_boards_T-W_the_queen_cooks_here_svg",
        "cutting_boards_T-W_this_is_where_i_murder_the_vegetables_svg",
        "cutting_boards_T-W_today_s_menu_eat_it_or_starve_it_svg",
        "Kitchen_closed_due_to_illness",
        "cutting_boards_B-I_I_don_t_need_an_inspirational_quote_I_need_food_svg",
        "cutting_boards_B-I_don_t_forget_to_hug_the_cook_svg",
        "cutting_boards_B-I_hello_is_it_me_you_re_cooking_for_svg",
        "cutting_boards_T-W_when_I_said_I_do_I_didn_t_meant_the_dishes_svg",
    ]
    add("cuttingboards_svgs", humor_cutting_stems, "Humor")

    humor_charcuterie_stems = [
        "Charcuterie_a_fancy_adult_lunch_table",
        "Charcuterie_a_fancy_way_to_say_adult_lunchable",
        "French_word_for_cheese_and_other_fancy_shit",
        "Sharkoodere",
    ]
    add("Charcuterie_svgs", humor_charcuterie_stems, "Humor")

    humor_flask_stems = [
        "Caution",
        "First_Aid_for_Boring_Days",
        "I_Drink_and_I_Know_Things",
        "I_Thought_You_Said_Flask_Chemistry",
        "I_never_drink_I_just_disinfect_internal_injuries",
        "In_Case_of_Emergency",
        "Liquid_Courage_Dispenser",
        "Not_Water__Not_Sorry",
        "One_Sip_Closer_to_Happiness",
        "Procrastinating_Sobriety",
        "Secretly_a_Mermaid_Potion",
        "Sip_Me_Baby_One_More_Time",
        "This_Flask_is_Half_Full",
        "This_Might_Be_Vodka",
        "This_is_probably_none_of_your_business",
        "Undercover_Party_Agent",
    ]
    add("flask_svgs", humor_flask_stems, "Humor")

    humor_golf_stems = [
        "Born_To_Golf_Forced_To_Work",
        "Cant_Work_Today_Im_Feeling_A_Little_Under_Par",
        "Golf_And_Beer_Thats_Why_Im_Here",
        "Im_Just_Here_To_Hit_Trees_And_Curse",
        "It_Takes_A_Lot_Of_Balls_To_Golf_Like_I_Do",
        "It_Takes_A_Lot_Of_Balls_To_Golf_Like_I_Do_2",
        "Swing_Swear_Drink_Repeat",
        "Time_To_Whip_Out_The_Big_Stick",
        "Weapons_Of_Grass_Destruction",
        "I_Made_A_Bogey_On_Every_Hole",
    ]
    add("Golf_svgs", humor_golf_stems, "Humor")

    # ---- Drinks ----
    drinks_coaster_stems = [
        "SVG_Beergoeshere",
        "SVG_Cheerstopourdecisions",
        "SVG_Coffeegoeshere",
        "SVG_Coffeeismakingmeawesome",
        "SVG_Daydrinkingmademedoit",
        "SVG_Dinnerispoured",
        "SVG_Drinkhappythoughts",
        "SVG_Gingoeshere",
        "SVG_Hardtimescallforhardliquor",
        "SVG_Ijustrescuedsomewine",
        "SVG_Ipairwellwithwine",
        "SVG_Itwastheginsfault",
        "SVG_Itwasthewhiskeysfault",
        "SVG_Itwasthewhiskysfault",
        "SVG_Itwasthewinesfault",
        "SVG_Lifebeginswithcoffee",
        "SVG_Mayyourcoffeekickinbeforereality",
        "SVG_Putmineinabiggirlglass",
        "SVG_Sipsabouttogetreal",
        "SVG_Stepasidecoffeethisisajobforalcohol",
        "SVG_Teagoeshere",
        "SVG_Theresalwaystimeforanotherdrink",
        "SVG_Timetowinedown",
        "SVG_Vodkagoeshere",
        "SVG_Whiskeygoeshere",
        "SVG_Whiskygoeshere",
        "SVG_Winegoeshere",
        "SVG_IusedtocarebutItakeapillforthatnow",
        "SVG_Itsnotreallydrinkingaloneifyourdogishome",
        "Don_t_Ask_Just_Pour",
        "Don_t_Ask_Just_Pour2",
        "Drinks_On_Me",
        "Drinks_On_Me2",
        "Good_Things_Happen_Over_Tea",
        "The_Best_Beer_Is_An_Open_Beer",
        "Where_There_Is_Tea_There_Is_Hope",
        "Take_Life_One_Cup_At_A_Time",
    ]
    add("Coasters_svgs", drinks_coaster_stems, "Drinks")

    drinks_flask_stems = [
        "Adventure_Fuel",
        "Drink",
        "Emergency_Rations_Inside",
        "Save_Water__Drink_Whiskey",
    ]
    add("flask_svgs", drinks_flask_stems, "Drinks")

    # 15 Flask Designs subfolder -> Drinks
    for i in range(1, 16):
        m[("flask_svgs/15 flask designs/svg", str(i))] = "Drinks"

    # ---- Wedding (whole folder) ----
    # Handled by whole-folder mapping below

    # ---- Bachelorette (whole folder) ----
    # Handled by whole-folder mapping below

    # ---- Golf (non-humor) ----
    golf_nonhumor_stems = [
        "Golf_Dad_Like_A_Regular_Dad_But_Cooler",
        "Golfing_Is_My_Favourite_Season",
        "I_Like_Bourbon_And_Golf_And_Maybe_3_People",
        "The_Golf_Father",
        "The_Most_Important_Shot_In_Golf_Is_The_Next_One",
        "Weekend_Forecast_Golfing_With_A_Chance_Of_Beer",
    ]
    add("Golf_svgs", golf_nonhumor_stems, "Golf")

    # ---- Inspirational Quotes (whole folder + specific coasters) ----
    insp_coaster_stems = [
        "SVG_Differentdoesnotmeanwrong",
        "SVG_Dontletthesillythingsstealyourhappiness",
        "SVG_Iliveonloveandscentedcandles",
        "SVG_Itdoesntgetanybetterthanthis",
    ]
    add("Coasters_svgs", insp_coaster_stems, "Inspirational_Quotes")

    # ---- Family_Monograms (whole folder) ----
    # Handled by whole-folder mapping below

    # ---- Charcuterie ----
    charc_stems = [
        "12",
        "3",
        "Meat_olives_fruit_board",
        "Party_Charcuterie_Board",
    ]
    add("Charcuterie_svgs", charc_stems, "Charcuterie")

    # ---- Cutting_Boards_Kitchen ----
    kitchen_cutting_stems = [
        "cutting_boards_B-I_cook_pray_eat_svg",
        "cutting_boards_B-I_cooking_is_my_passion_svg",
        "cutting_boards_B-I_enjoy_life_it_s_delicious_svg",
        "cutting_boards_B-I_farm_to_table_fresh_food_daily_svg",
        "cutting_boards_B-I_if_i_have_to_stir_it_it_s_homemade_svg",
        "cutting_boards_B-I_if_you_can_read_this_you_re_too_close_to_my_food_svg",
        "cutting_boards_B-I_in_this_kitchen_we_count_memories_not_calories_svg",
        "cutting_boards_B-I_in_this_kitchen_we_make_memories_svg",
        "cutting_boards_B-I_i_love_you_to_the_fridge_and_back_svg",
        "cutting_boards_K-W_kitchen_all_food_chopped_with_love_svg",
        "cutting_boards_K-W_kitchen_the_heart_of_the_home_svg",
        "cutting_boards_K-W_life_is_too_short_dance_in_the_kitchen_svg",
        "cutting_boards_K-W_my_kitchen_is_for_dancing_svg",
        "cutting_boards_T-W_the_kitchen_is_the_heart_of_the_home_svg",
        "cutting_boards_T-W_welcome_to_my_kitchen_svg",
    ]
    add("cuttingboards_svgs", kitchen_cutting_stems, "Cutting_Boards_Kitchen")

    # ---- Seasonal_Holiday ----
    # Halloween and Autum whole folders handled below
    # sunshine subfolder
    m[("sunshine", "you are my sunshine cutting board")] = "Seasonal_Holiday"

    # ---- Home_Cozy ----
    cozy_coaster_stems = [
        "SVG_Cuddleoclock",
        "SVG_Hotcocoahoodiesandhome",
        "SVG_Itscosyseason",
        "SVG_Pardonthemessmychildrenaremakingmemories",
        "SVG_Pleasecanwecomewithyou",
        "SVG_Soupoftheday",
        "SVG_Welcometothechaos",
        "Monstera Leaf Coasters-03",
    ]
    add("Coasters_svgs", cozy_coaster_stems, "Home_Cozy")

    # ---- Fitness ----
    add("flask_svgs", ["Fitness", "Gym"], "Fitness")

    return m


# Whole-folder mappings (every file in this folder goes to this category)
WHOLE_FOLDER_MAP = {
    "Wedding": "Wedding",
    "Bridal Bachelorette_svgs": "Bachelorette",
    "inspirational quotes_svgs": "Inspirational_Quotes",
    "Monograms_family_svgs": "Family_Monograms",
    "Halloween": "Seasonal_Holiday",
    "Autum": "Seasonal_Holiday",
}

# Keyword fallback mapping
KEYWORD_MAP = [
    (["family", "home", "love", "together"], "Family"),
    (["work", "cowork", "office", "monday", "boss", "employ"], "Work"),
    (["sarcas", "stupid", "idiot", "eye", "annoy", "serial", "wrath", "wrong"], "Humor"),
    (["beer", "wine", "whiskey", "whisky", "gin", "vodka", "coffee", "tea", "drink", "sip", "pour", "brew"], "Drinks"),
    (["wedding", "bride", "groom", "mrs", "ceremony", "reception", "forever", "vow"], "Wedding"),
    (["golf", "bogey", "par", "birdie", "fairway", "club"], "Golf"),
    (["inspir", "motiv", "quote", "strength", "brave", "courage", "dream"], "Inspirational_Quotes"),
    (["monogram", "family_svg"], "Family_Monograms"),
    (["charcuterie", "cheese", "meat", "board", "fancy"], "Charcuterie"),
    (["kitchen", "cook", "chef", "recipe", "food", "hungry", "eat", "bake"], "Cutting_Boards_Kitchen"),
    (["halloween", "witch", "ghost", "spook", "pumpkin", "autumn", "fall", "sunshine"], "Seasonal_Holiday"),
    (["cozy", "cuddle", "candle", "warm", "comfort"], "Home_Cozy"),
    (["gym", "fitness", "workout"], "Fitness"),
]


def classify_by_keyword(filename_lower):
    """Try to classify a file by keyword matching on its filename."""
    for keywords, category in KEYWORD_MAP:
        for kw in keywords:
            if kw in filename_lower:
                return category
    return None


def get_relative_subfolder(filepath, root):
    """Get the subfolder path relative to root (e.g., 'Coasters_svgs' or 'flask_svgs/15 Flask Designs/svg')."""
    rel = filepath.relative_to(root)
    parts = rel.parts[:-1]  # everything except the filename
    if not parts:
        return ""
    return "/".join(parts)


def collect_all_svgs(root):
    """Walk root and collect all SVG files (excluding logo.svg and _organized/)."""
    svgs = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip _organized folder and New folder
        dirnames[:] = [d for d in dirnames if d not in ("_organized", "New folder")]
        for f in filenames:
            if f.lower().endswith(".svg") and f.lower() != "logo.svg":
                svgs.append(Path(dirpath) / f)
    return svgs


def categorize_file(filepath, root, explicit_map):
    """Determine which category a file belongs to."""
    subfolder = get_relative_subfolder(filepath, root).lower()
    stem = filepath.stem.lower()
    filename_lower = filepath.name.lower()

    # 1. Check whole-folder mapping first
    # Get the top-level folder name
    rel = filepath.relative_to(root)
    if len(rel.parts) > 1:
        top_folder = rel.parts[0]
        if top_folder in WHOLE_FOLDER_MAP:
            # But check if this specific file has an explicit override
            key = (subfolder, stem)
            if key in explicit_map:
                return explicit_map[key]
            return WHOLE_FOLDER_MAP[top_folder]

    # 2. Check explicit mapping
    key = (subfolder, stem)
    if key in explicit_map:
        return explicit_map[key]

    # 3. Keyword fallback
    cat = classify_by_keyword(filename_lower)
    if cat:
        return cat

    # Also try the stem without SVG_ prefix
    stripped = stem.replace("svg_", "")
    cat = classify_by_keyword(stripped)
    if cat:
        return cat

    return None


def copy_file(src, dest_dir, filename=None):
    """Copy a file to dest_dir, creating dirs as needed."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / (filename or src.name)
    shutil.copy2(src, dest)
    return dest


def reorganize(root, output_dir, replace_mode=False):
    """
    Reorganize SVGs from root into output_dir.
    If replace_mode=True, we clean output_dir first (for site folder).
    """
    explicit_map = build_explicit_map()
    all_svgs = collect_all_svgs(root)

    print(f"\nProcessing: {root}")
    print(f"Output to:  {output_dir}")
    print(f"Total SVG files found: {len(all_svgs)}")

    counts = defaultdict(int)
    uncategorized = []

    # Create all category folders
    for cat in CATEGORIES:
        (output_dir / cat).mkdir(parents=True, exist_ok=True)

    # Create uncategorized folder
    (output_dir / "_uncategorized").mkdir(parents=True, exist_ok=True)

    # Maps folder gets .gitkeep
    gitkeep = output_dir / "Maps" / ".gitkeep"
    gitkeep.touch()

    for svg_path in all_svgs:
        category = categorize_file(svg_path, root, explicit_map)

        if category:
            dest_dir = output_dir / category
            copy_file(svg_path, dest_dir)
            counts[category] += 1
        else:
            dest_dir = output_dir / "_uncategorized"
            copy_file(svg_path, dest_dir)
            uncategorized.append(svg_path.name)
            counts["_uncategorized"] += 1

    # Print summary
    print("\n--- Category Counts ---")
    total = 0
    for cat in CATEGORIES:
        c = counts.get(cat, 0)
        total += c
        print(f"  {cat}: {c}")
    unc = counts.get("_uncategorized", 0)
    total += unc
    print(f"  _uncategorized: {unc}")
    print(f"  TOTAL: {total}")

    if uncategorized:
        print("\n--- Uncategorized Files ---")
        for f in sorted(uncategorized):
            print(f"  {f}")

    return counts, uncategorized


def reorganize_site_folder():
    """
    For the site folder, we need to:
    1. Create new category structure
    2. Copy files from existing product folders into new categories
    3. Remove old product folders
    """
    print("\n" + "=" * 60)
    print("SITE FOLDER REORGANIZATION")
    print("=" * 60)

    # The site folder has the same SVGs as source, organized in old product folders
    # We'll reorganize in-place by creating new folders and cleaning old ones

    # Old product-based folders to remove after reorganization
    old_folders = [
        "Coasters_svgs", "cuttingboards_svgs", "flask_svgs", "Golf_svgs",
        "Charcuterie_svgs", "Bridal Bachelorette_svgs", "Monograms_family_svgs",
        "Wedding", "inspirational quotes_svgs", "Halloween", "Autum", "sunshine",
        "Family", "Work", "General",  # partially reorganized folders from before
    ]

    # Create a temp output dir inside designs
    temp_dir = SITE_DESIGNS_DIR / "_new_organized"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    counts, uncategorized = reorganize(SITE_DESIGNS_DIR, temp_dir)

    # Now swap: remove old folders, move new category folders into place
    print("\nSwapping old folders for new...")

    # Remove old product folders
    for folder in old_folders:
        old_path = SITE_DESIGNS_DIR / folder
        if old_path.exists():
            shutil.rmtree(old_path)
            print(f"  Removed old folder: {folder}")

    # Remove old root-level SVGs (except logo.svg)
    for f in SITE_DESIGNS_DIR.iterdir():
        if f.is_file() and f.suffix.lower() == ".svg" and f.name.lower() != "logo.svg":
            f.unlink()
            print(f"  Removed root SVG: {f.name}")

    # Remove old Maps folder if it exists (we'll replace it)
    old_maps = SITE_DESIGNS_DIR / "Maps"
    if old_maps.exists():
        shutil.rmtree(old_maps)

    # Move new category folders from temp to designs root
    for item in temp_dir.iterdir():
        dest = SITE_DESIGNS_DIR / item.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(item), str(dest))
        print(f"  Placed category folder: {item.name}")

    # Clean up temp dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    print("\nSite folder reorganization complete.")
    return counts, uncategorized


def reorganize_source_folder():
    """
    For the source folder, create _organized/ subfolder with copies.
    """
    print("\n" + "=" * 60)
    print("SOURCE FOLDER REORGANIZATION")
    print("=" * 60)

    output_dir = SOURCE_SVG_ROOT / "_organized"
    if output_dir.exists():
        shutil.rmtree(output_dir)

    counts, uncategorized = reorganize(SOURCE_SVG_ROOT, output_dir)
    print("\nSource folder reorganization complete (originals untouched).")
    return counts, uncategorized


def main():
    print("SVG Design Library Reorganization")
    print("From product-based to theme-based categories")
    print("=" * 60)

    # 1. Source folder
    src_counts, src_uncat = reorganize_source_folder()

    # 2. Site folder
    site_counts, site_uncat = reorganize_site_folder()

    print("\n" + "=" * 60)
    print("ALL DONE")
    print("=" * 60)
    print(f"\nSource _organized/: {sum(src_counts.values())} files across {len(CATEGORIES)} categories + uncategorized")
    print(f"Site designs/:      {sum(site_counts.values())} files reorganized in-place")

    if src_uncat:
        print(f"\n{len(src_uncat)} files went to _uncategorized (needs manual sorting)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
