def get_market_mapping():
    return {
        'Abilene-Sweetwater, TX (662)': 'West Texas',
        'Albany, GA (525)': 'Georgia',
        'Albany-Schenectady-Troy, NY-MA-VT (532)': 'Upstate NY East',
        'Albuquerque-Santa Fe, NM-CO-AZ (790)': 'Albuquerque',
        'Alexandria, LA (644)': 'Louisiana',
        'Alpena, MI (583)': 'East Michigan',
        'Amarillo, TX-NM-OK (634)': 'West Texas',
        'Anchorage, AK (743)': 'Alaska', # No clear Boost market for Alaska
        'Atlanta, GA-AL-NC (524)': 'Atlanta / Athens', # Master Market
        'Augusta-Aiken, GA-SC (520)': 'GA/SC Coast',
        'Austin, TX (635)': 'Austin', # Master Market
        'Bakersfield, CA (800)': 'Lower Central Valley',
        'Baltimore, MD (512)': 'Baltimore', # Master Market
        'Bangor, ME (537)': 'VT / NH / ME',
        'Baton Rouge, LA-MS (716)': 'Louisiana',
        'Beaumont-Port Arthur, TX (692)': 'East Texas', # Master Market
        'Bend, OR (821)': 'Oregon',
        'Billings, MT-WY (756)': 'Montana', # New Grouping
        'Biloxi-Gulfport, MS (746)': 'Gulf Coast',
        'Binghamton, NY (502)': 'Upstate NY Central',
        'Birmingham, AL (630)': 'Alabama',
        'Bluefield-Beckley-Oak Hill, WV-VA (559)': 'West Virginia',
        'Boise, ID-OR (757)': 'Idaho',
        'Boston, MA-NH-VT (506)': 'Boston', # Master Market
        'Bowling Green, KY (736)': 'Kentucky',
        'Buffalo, NY-PA (514)': 'Buffalo',
        'Burlington-Plattsburgh, VT-NY-NH (523)': 'VT / NH / ME',
        'Butte-Bozeman, MT (754)': 'Montana', # New Grouping
        'Casper-Riverton, WY (767)': 'Wyoming', # New Grouping
        'Cedar Rapids-Waterloo-Iowa City & Dubuque, IA (637)': 'East Iowa',
        'Champaign & Springfield-Decatur, IL (648)': 'Central Illinois', # Master Market
        'Charleston, SC (519)': 'South Carolina',
        'Charleston-Huntington, WV-KY-OH (564)': 'West Virginia',
        'Charlotte, NC-SC (517)': 'Charlotte', # Master Market
        'Charlottesville, VA (584)': 'Virginia',
        'Chattanooga, TN-GA-NC (575)': 'East Tennessee', # New Grouping
        'Cheyenne-Scottsbluff, WY-NE (759)': 'Wyoming', # New Grouping
        'Chicago, IL-IN (602)': 'Chicago', # Master Market
        'Chico-Redding, CA (868)': 'Northern California', # New Grouping
        'Cincinnati, OH-KY-IN (515)': 'Cincinnati', # Master Market
        'Clarksburg-Weston, WV (598)': 'West Virginia',
        'Cleveland-Akron, OH (510)': 'Cleveland', # Master Market
        'Colorado Springs-Pueblo, CO (752)': 'Colorado', # Master Market
        'Columbia, SC (546)': 'South Carolina',
        'Columbia-Jefferson City, MO (604)': 'Missouri', # Master Market
        'Columbus, GA-AL (522)': 'Georgia',
        'Columbus, OH (535)': 'Columbus', # Master Market
        'Columbus-Tupelo-West Point-Houston, MS-AL (673)': 'Mississippi',
        'Corpus Christi, TX (600)': 'South Texas',
        'Dallas-Ft. Worth, TX (623)': 'DFW', # Master Market
        'Davenport-Rock Island-Moline, IA-IL (682)': 'East Iowa',
        'Dayton, OH (542)': 'Ohio', # New Grouping
        'Denver, CO-WY-NE (751)': 'Colorado', # Master Market
        'Des Moines-Ames, IA (679)': 'Central Iowa',
        'Detroit, MI (505)': 'East Michigan', # Master Market
        'Dothan, AL-GA (606)': 'The Panhandle',
        'Duluth-Superior, MN-WI-MI (676)': 'Minnesota',
        'El Paso, TX-NM (765)': 'West Texas',
        'Elmira, NY-PA (565)': 'Upstate NY Central',
        'Erie, PA (516)': 'Western Pennsylvania',
        'Eugene, OR (801)': 'Oregon',
        'Eureka, CA (802)': 'Northern California', # New Grouping
        'Evansville, IN-KY-IL (649)': 'Kentucky',
        'Fairbanks, AK (745)': 'Alaska', # No clear Boost market for Alaska
        'Fargo, ND-MN (724)': 'Dakotas',
        'Flint-Saginaw-Bay City, MI (513)': 'East Michigan', # Master Market
        'Fresno-Visalia, CA (866)': 'Central Valley',
        'Ft. Myers-Naples, FL (571)': 'South West Florida',
        'Ft. Smith-Fayetteville-Springdale-Rogers, AR-OK (670)': 'Arkansas',
        'Ft. Wayne, IN-OH (509)': 'Ft. Wayne / South Bend',
        'Gainesville, FL (592)': 'Jacksonville', # Master Market
        'Glendive, MT (798)': 'Montana', # New Grouping
        'Grand Junction-Montrose, CO (773)': 'Colorado', # Master Market

        'Grand Rapids-Kalamazoo-Battle Creek, MI (563)': 'West Michigan',
        'Great Falls, MT (755)': 'Montana', # New Grouping
        'Green Bay-Appleton, WI-MI (658)': 'North Wisconsin',
        'Greensboro-High Point-Winston Salem, NC-VA (518)': 'Winston / Salem',
        'Greenville-New Bern-Washington, NC (545)': 'Raleigh / Durham', # Master Market
        'Greenville-Spartanburg-Asheville-Anderson, SC-NC-GA (567)': 'South Carolina',
        'Greenwood-Greenville, MS-AL (647)': 'Mississippi',
        'Harlingen-Weslaco-Brownsville-McAllen, TX (636)': 'South Texas',
        'Harrisburg-Lancaster-Lebanon-York, PA (566)': 'Central Pennsylvania',
        'Harrisonburg, VA-WV (569)': 'Virginia',
        'Hartford & New Haven, CT (533)': 'Connecticut',
        'Hattiesburg-Laurel, MS (710)': 'Mississippi',
        'Helena, MT (766)': 'Montana', # New Grouping
        'Honolulu, HI (744)': 'Hawaii',
        'Houston, TX (618)': 'Houston', # Master Market
        'Huntsville-Decatur, AL-TN (691)': 'Alabama',
        'Idaho Falls-Pocatello, ID-WY (758)': 'Idaho',
        'Indianapolis, IN (527)': 'Indianapolis',
        'Jackson, MS (718)': 'Mississippi',
        'Jackson, TN (639)': 'Memphis',
        'Jacksonville, FL-GA (561)': 'Jacksonville', # Master Market
        'Johnstown-Altoona-State College, PA (574)': 'Central Pennsylvania',
        'Jonesboro, AR (734)': 'Arkansas',
        'Joplin-Pittsburg, MO-KS-OK (603)': 'Missouri', # Master Market
        'Juneau, AK (747)': 'Alaska', # No clear Boost market for Alaska
        'Kansas City, MO-KS (616)': 'Kansas', # Master Market
        'Knoxville, TN-KY (557)': 'East Tennessee', # New Grouping
        'La Crosse-Eau Claire, WI-MN (702)': 'Minnesota',
        'Lafayette, IN (582)': 'Indianapolis',
        'Lafayette, LA (642)': 'Louisiana',
        'Lake Charles, LA (643)': 'Louisiana',
        'Lansing, MI (551)': 'West Michigan',
        'Laredo, TX (749)': 'South Texas',
        'Las Vegas, NV (839)': 'Las Vegas',
        'Lexington, KY (541)': 'Kentucky',
        'Lima, OH (558)': 'Toledo', # Master Market
        'Lincoln & Hastings-Kearney, NE-KS (722)': 'Nebraska / Kansas',
        'Little Rock-Pine Bluff, AR (693)': 'Arkansas',
        'Los Angeles, CA-NV (803)': 'LA Metro', # Master Market
        'Louisville, KY-IN (529)': 'Kentucky',
        'Lubbock, TX (651)': 'West Texas',
        'Macon, GA-AL (503)': 'Georgia',
        'Madison, WI (669)': 'Wisconsin',
        'Mankato, MN (737)': 'Minnesota',
        'Marquette, MI-WI (553)': 'North Wisconsin',
        'Medford-Klamath Falls, OR-CA (813)': 'Oregon',
        'Memphis, TN-MS-AR (640)': 'Memphis',
        'Meridian, MS-AL (711)': 'Mississippi',
        'Miami-Ft. Lauderdale, FL (528)': 'Miami / West Palm', # Master Market
        'Milwaukee, WI (617)': 'Wisconsin',
        'Minneapolis-St. Paul, MN-WI (613)': 'Minnesota',
        'Minot-Bismarck-Dickinson, ND-MT-SD (687)': 'Dakotas',
        'Missoula, MT (762)': 'Montana', # New Grouping
        'Mobile-Pensacola, AL-FL-MS (686)': 'Gulf Coast',
        'Monroe-El Dorado, LA-AR (628)': 'Louisiana',
        'Monterey-Salinas, CA (828)': 'SF Bay Area',
        'Montgomery-Selma, AL (698)': 'Alabama',
        'Myrtle Beach-Florence, SC-NC (570)': 'Myrtle Beach',
        'Nashville, TN-KY (659)': 'Nashville', # Master Market
        'New Orleans, LA-MS (622)': 'New Orleans', # Master Market
        'New York, NY-NJ-CT-PA (501)': 'New York City', # Master Market
        'Norfolk-Portsmouth-Newport News, VA-NC (544)': 'Norfolk', # Master Market
        'North Platte, NE (740)': 'Nebraska / Kansas',
        'Odessa-Midland, TX-NM (633)': 'West Texas',
        'Oklahoma City, OK (650)': 'Oklahoma',
        'Omaha, NE-IA-MO (652)': 'Nebraska / Kansas',
        'Orlando-Daytona Beach-Melbourne, FL (534)': 'Orlando', # Master Market
        'Ottumwa-Kirksville, IA-MO (631)': 'East Iowa',
        'Paducah-Cape Girardeau-Harrisburg, KY-MO-IL-TN (632)': 'Kentucky',
        'Palm Springs, CA (804)': 'Riverside / San Bernardino',
        'Panama City, FL (656)': 'The Panhandle',
        'Parkersburg, WV-OH (597)': 'West Virginia',
        'Peoria-Bloomington, IL (675)': 'Central Illinois', # Master Market
        'Philadelphia, PA-NJ-DE (504)': 'Philadelphia Metro', # Master Market
        'Phoenix, AZ (753)': 'Phoenix', # Master Market
        'Pittsburgh, PA-WV-MD (508)': 'Pittsburgh', # Master Market
        'Portland, OR-WA (820)': 'Oregon / SW Washington',
        'Portland-Auburn, ME-NH (500)': 'VT / NH / ME',
        'Presque Isle, ME-NH (552)': 'VT / NH / ME',
        'Providence-New Bedford, RI-MA (521)': 'Providence',
        'Quincy-Hannibal-Keokuk, IL-MO-IA (717)': 'Missouri', # Master Market
        'Raleigh-Durham, NC-VA (560)': 'Raleigh / Durham', # Master Market
        'Rapid City, SD-WY-MT (764)': 'Dakotas',
        'Reno, NV-CA (811)': 'Nevada', # New Grouping
        'Richmond-Petersburg, VA (556)': 'Richmond', # Master Market
        'Roanoke-Lynchburg, VA-WV (573)': 'Virginia',
        'Rochester, NY (538)': 'Rochester',
        'Rochester-Mason City-Austin, MN-IA-IL (611)': 'Minnesota',
        'Rockford, IL (610)': 'Chicago', # Master Market
        'Sacramento-Stockton-Modesto, CA (862)': 'Central Valley',
        'Salisbury, MD-DE (576)': 'Delaware',
        'Salt Lake City, UT-WY-NV-ID (770)': 'Utah',
        'San Angelo, TX (661)': 'West Texas',
        'San Antonio, TX (641)': 'San Antonio', # Master Market
        'San Diego, CA (825)': 'San Diego',
        'San Francisco-Oakland-San Jose, CA (807)': 'SF Bay Area',
        'Santa Barbara-Santa Maria-San Luis Obispo, CA (855)': 'LA Metro', # Master Market
        'Savannah, GA-SC (507)': 'GA/SC Coast',
        'Seattle-Tacoma, WA (819)': 'West Washington', # Master Market
        'Sherman-Ada, OK-TX (657)': 'DFW', # Master Market
        'Shreveport, LA-TX-AR-OK (612)': 'East Texas', # Master Market
        'Sioux City, IA-NE-SD (624)': 'West Iowa / Nebraska',
        'Sioux Falls, SD-MN-IA-NE (725)': 'Dakotas',
        'South Bend-Elkhart, IN-MI (588)': 'Ft. Wayne / South Bend',
        'Spokane, WA-ID-MT-OR (881)': 'Inland Northwest',
        'Springfield, MO-AR (619)': 'Missouri', # Master Market
        'Springfield-Holyoke, MA (543)': 'Massachusetts',
        'St. Joseph, MO-KS (638)': 'Kansas', # Master Market
        'St. Louis, MO-IL (609)': 'Missouri', # Master Market
        'Syracuse, NY (555)': 'Upstate NY Central',
        'Tallahassee-Thomasville, FL-GA (530)': 'The Panhandle',
        'Tampa-St. Petersburg, FL (539)': 'Tampa', # Master Market
        'Terre Haute, IN-IL (581)': 'Central Illinois', # Master Market
        'Toledo, OH-MI (547)': 'Toledo', # Master Market
        'Topeka, KS (605)': 'Kansas', # Master Market
        'Traverse City-Cadillac, MI (540)': 'West Michigan',
        'Tri-Cities, TN-VA-KY (531)': 'East Tennessee', # New Grouping
        'Tucson, AZ (789)': 'Tucson / Yuma',
        'Tulsa, OK-KS (671)': 'Oklahoma',
        'Twin Falls, ID (760)': 'Idaho',
        'Tyler-Longview, TX (709)': 'East Texas', # Master Market
        'Utica, NY (526)': 'Upstate NY Central',
        'Victoria, TX (626)': 'South Texas',
        'Waco-Temple-Bryan, TX (625)': 'Austin', # Master Market
        'Washington, DC-VA-MD-WV-PA (511)': 'Washington DC', # Master Market
        'Watertown, NY (549)': 'Upstate NY East',
        'Wausau-Rhinelander, WI (705)': 'North Wisconsin',
        'West Palm Beach-Ft. Pierce, FL (548)': 'Miami / West Palm', # Master Market
        'Wheeling-Steubenville, WV-OH (554)': 'Pittsburgh', # Master Market
        'Wichita Falls & Lawton, TX-OK (627)': 'Oklahoma',
        'Wichita-Hutchinson Plus, KS (678)': 'Kansas', # Master Market
        'Wilkes Barre-Scranton-Hazelton, PA (577)': 'Central Pennsylvania',
        'Wilmington, NC (550)': 'Myrtle Beach',
        'Yakima-Pasco-Richland-Kennewick, WA-OR (810)': 'Inland Northwest',
        'Youngstown, OH-PA (536)': 'Pittsburgh', # Master Market
        'Yuma-El Centro, AZ-CA (771)': 'Tucson / Yuma',
        'Zanesville, OH (596)': 'Columbus' # Master Market
    }
