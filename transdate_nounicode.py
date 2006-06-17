"""transdate -- Python implementation of Asian lunisolar calendar
Copyright (c) 2004-2006, Kang Seonghoon aka Tokigun.

This module declares lunardate class which represents a day of Asian
lunisolar calendar. lunardate class is compatible with datetime.date
class, so you can use both lunardate and date interchangeably.

lunardate class can handle date between 1881-01-30 (lunar 1881-01-01)
and 2051-02-10 (lunar 2050-12-29). Since lunisolar calendar table is
based on Korea Astronomy & Space Science Institute, it can be
different with calendars used by other countries.

transdate_nounicode.py is for Unicode-disabled python implementation.
Normally Python is built with Unicode support, so you would better use
transdate.py instead of this version. Also this version doesn't support
getganzistr functions.
"""

__author__ = 'Kang Seonghoon aka Tokigun'
__version__ = '1.1 (2006-06-18)'
__copyright__ = 'Copyright (c) 2004-2006 Kang Seonghoon aka Tokigun'
__license__ = 'LGPL'

__all__ = ['sol2lun', 'lun2sol', 'date', 'timedelta', 'solardate',
           'lunardate', 'getganzistr', 'strftime']

from datetime import date, timedelta
import time

###################################################################################
## Lunisolar Calendar Table

_BASEYEAR = 1881
_MINDATE = 686686 # 1881.1.30 (lunar 1881.1.1)
_MAXDATE = 748788 # 2051.2.10 (lunar 2050.12.29)
try: import re; _STRFTIMEREGEXP = re.compile('(?<!%)((?:%%)*)%L(.)')
except ImportError: _STRFTIMEREGEXP = None

_MONTHTABLE = (0,29,59,88,118,147,177,207,236,266,296,325,355,384,413,443,472,
502,531,561,590,620,650,679,709,739,768,797,827,856,885,915,944,974,1004,1034,
1063,1093,1123,1152,1181,1211,1240,1269,1299,1328,1358,1388,1417,1447,1477,1507,
1536,1565,1595,1624,1653,1683,1712,1742,1771,1801,1831,1861,1890,1920,1949,1979,
2008,2037,2067,2096,2126,2155,2185,2215,2245,2274,2304,2333,2363,2392,2421,2451,
2480,2510,2539,2569,2599,2628,2658,2688,2717,2747,2776,2805,2835,2864,2894,2923,
2953,2982,3012,3042,3071,3101,3130,3160,3189,3219,3248,3278,3307,3337,3366,3396,
3425,3455,3485,3514,3544,3573,3603,3632,3662,3691,3721,3750,3780,3809,3839,3868,
3898,3928,3957,3987,4017,4046,4075,4105,4134,4163,4193,4222,4252,4282,4311,4341,
4371,4401,4430,4459,4489,4518,4547,4577,4606,4636,4665,4695,4725,4755,4784,4814,
4843,4873,4902,4931,4961,4990,5020,5049,5079,5109,5139,5168,5198,5227,5257,5286,
5315,5345,5374,5404,5433,5463,5492,5522,5552,5582,5611,5641,5670,5699,5729,5758,
5788,5817,5847,5876,5906,5936,5965,5995,6024,6054,6083,6113,6142,6172,6201,6231,
6260,6290,6319,6349,6379,6408,6438,6467,6497,6526,6556,6585,6615,6644,6674,6703,
6733,6762,6792,6822,6851,6881,6910,6940,6969,6999,7028,7057,7087,7116,7146,7176,
7205,7235,7265,7294,7324,7353,7383,7412,7441,7471,7500,7530,7559,7589,7619,7649,
7678,7708,7737,7767,7796,7825,7855,7884,7914,7943,7973,8003,8033,8062,8092,8121,
8151,8180,8209,8239,8268,8297,8327,8357,8386,8416,8446,8476,8505,8535,8564,8593,
8623,8652,8681,8711,8741,8770,8800,8830,8859,8889,8919,8948,8977,9007,9036,9066,
9095,9125,9154,9184,9214,9243,9273,9302,9332,9361,9391,9420,9450,9479,9509,9538,
9568,9597,9627,9656,9686,9716,9745,9775,9804,9834,9863,9893,9922,9951,9981,
10011,10040,10070,10099,10129,10159,10188,10218,10247,10277,10306,10335,10365,
10394,10424,10453,10483,10513,10543,10572,10602,10631,10661,10690,10719,10749,
10778,10808,10837,10867,10897,10927,10956,10986,11015,11045,11074,11103,11133,
11162,11191,11221,11251,11280,11310,11340,11370,11399,11429,11458,11487,11517,
11546,11575,11605,11635,11664,11694,11724,11754,11783,11813,11842,11871,11901,
11930,11959,11989,12018,12048,12078,12108,12137,12167,12197,12226,12255,12285,
12314,12344,12373,12402,12432,12462,12491,12521,12551,12580,12610,12639,12669,
12698,12728,12757,12787,12816,12846,12875,12905,12934,12964,12994,13023,13053,
13082,13112,13141,13171,13200,13229,13259,13288,13318,13348,13377,13407,13437,
13466,13496,13525,13555,13584,13613,13643,13672,13702,13731,13761,13791,13821,
13850,13880,13909,13939,13968,13997,14027,14056,14086,14115,14145,14175,14204,
14234,14264,14293,14323,14352,14381,14411,14440,14469,14499,14529,14558,14588,
14618,14648,14677,14707,14736,14765,14795,14824,14853,14883,14912,14942,14972,
15002,15031,15061,15091,15120,15149,15179,15208,15237,15267,15296,15326,15356,
15385,15415,15445,15474,15504,15533,15563,15592,15622,15651,15680,15710,15740,
15769,15799,15828,15858,15888,15917,15947,15976,16006,16035,16064,16094,16123,
16153,16183,16212,16242,16271,16301,16331,16360,16390,16419,16449,16478,16507,
16537,16566,16596,16625,16655,16685,16714,16744,16774,16803,16833,16862,16891,
16921,16950,16980,17009,17039,17069,17098,17128,17158,17187,17217,17246,17275,
17305,17334,17363,17393,17423,17452,17482,17512,17542,17571,17601,17630,17659,
17689,17718,17747,17777,17806,17836,17866,17896,17925,17955,17985,18014,18043,
18073,18102,18131,18161,18190,18220,18250,18279,18309,18339,18369,18398,18427,
18457,18486,18515,18545,18574,18604,18633,18663,18693,18723,18752,18782,18811,
18841,18870,18899,18929,18958,18988,19017,19047,19077,19106,19136,19166,19195,
19225,19254,19284,19313,19342,19372,19401,19431,19460,19490,19520,19549,19579,
19609,19638,19668,19697,19727,19756,19785,19815,19844,19874,19903,19933,19963,
19992,20022,20052,20081,20111,20140,20169,20199,20228,20258,20287,20317,20346,
20376,20406,20436,20465,20495,20524,20553,20583,20612,20641,20671,20700,20730,
20760,20790,20819,20849,20879,20908,20937,20967,20996,21025,21055,21084,21114,
21144,21173,21203,21233,21263,21292,21321,21351,21380,21409,21439,21468,21498,
21527,21557,21587,21617,21646,21676,21705,21735,21764,21793,21823,21852,21882,
21911,21941,21971,22000,22030,22060,22089,22119,22148,22177,22207,22236,22266,
22295,22325,22354,22384,22414,22443,22473,22503,22532,22562,22591,22620,22650,
22679,22709,22738,22768,22797,22827,22857,22886,22916,22946,22975,23005,23034,
23063,23093,23122,23152,23181,23211,23240,23270,23300,23329,23359,23389,23418,
23447,23477,23506,23535,23565,23594,23624,23654,23684,23713,23743,23773,23802,
23831,23861,23890,23919,23949,23978,24008,24038,24067,24097,24127,24157,24186,
24215,24245,24274,24303,24333,24362,24392,24421,24451,24481,24511,24540,24570,
24599,24629,24658,24687,24717,24746,24776,24805,24835,24865,24895,24924,24954,
24983,25013,25042,25071,25101,25130,25160,25189,25219,25249,25278,25308,25338,
25367,25397,25426,25455,25485,25514,25544,25573,25603,25632,25662,25692,25721,
25751,25780,25810,25839,25869,25898,25928,25957,25987,26016,26046,26075,26105,
26135,26164,26194,26223,26253,26282,26312,26341,26371,26400,26429,26459,26489,
26518,26548,26578,26607,26637,26667,26696,26725,26755,26784,26813,26843,26872,
26902,26932,26961,26991,27021,27051,27080,27109,27139,27168,27197,27227,27256,
27286,27315,27345,27375,27405,27434,27464,27493,27523,27552,27581,27611,27640,
27670,27699,27729,27759,27789,27818,27848,27877,27907,27936,27965,27995,28024,
28054,28083,28113,28143,28172,28202,28232,28261,28291,28320,28349,28379,28408,
28438,28467,28497,28526,28556,28586,28615,28645,28674,28704,28733,28763,28792,
28822,28851,28881,28910,28940,28969,28999,29029,29058,29088,29117,29147,29176,
29206,29235,29265,29294,29324,29353,29383,29412,29442,29472,29501,29531,29560,
29590,29619,29649,29678,29707,29737,29766,29796,29826,29855,29885,29915,29944,
29974,30003,30033,30062,30091,30121,30150,30180,30209,30239,30269,30299,30328,
30358,30387,30417,30446,30475,30505,30534,30564,30593,30623,30653,30683,30712,
30742,30771,30801,30830,30859,30889,30918,30947,30977,31007,31037,31066,31096,
31126,31155,31185,31214,31243,31273,31302,31331,31361,31391,31420,31450,31480,
31509,31539,31569,31598,31627,31657,31686,31716,31745,31775,31804,31834,31864,
31893,31923,31952,31982,32011,32041,32070,32100,32129,32159,32188,32218,32247,
32277,32306,32336,32366,32395,32425,32454,32484,32513,32543,32572,32601,32631,
32661,32690,32720,32749,32779,32809,32838,32868,32897,32927,32956,32985,33015,
33044,33074,33103,33133,33163,33193,33222,33252,33281,33311,33340,33369,33399,
33428,33458,33487,33517,33547,33577,33606,33636,33665,33695,33724,33753,33783,
33812,33841,33871,33901,33931,33960,33990,34020,34049,34079,34108,34137,34167,
34196,34225,34255,34285,34314,34344,34374,34404,34433,34463,34492,34521,34551,
34580,34609,34639,34668,34698,34728,34758,34787,34817,34846,34876,34905,34935,
34964,34994,35023,35052,35082,35112,35141,35171,35201,35230,35260,35289,35319,
35348,35378,35407,35436,35466,35496,35525,35555,35584,35614,35644,35673,35703,
35732,35762,35791,35821,35850,35879,35909,35938,35968,35998,36027,36057,36087,
36116,36146,36175,36205,36234,36263,36293,36322,36352,36381,36411,36441,36470,
36500,36530,36559,36589,36618,36647,36677,36706,36735,36765,36795,36824,36854,
36884,36914,36943,36973,37002,37031,37061,37090,37119,37149,37179,37208,37238,
37268,37298,37327,37357,37386,37415,37445,37474,37503,37533,37562,37592,37622,
37652,37681,37711,37741,37770,37799,37829,37858,37887,37917,37946,37976,38006,
38035,38065,38095,38124,38154,38183,38213,38242,38271,38301,38330,38360,38389,
38419,38449,38478,38508,38538,38567,38597,38626,38656,38685,38714,38744,38773,
38803,38833,38862,38892,38921,38951,38981,39010,39040,39069,39099,39128,39157,
39187,39216,39246,39275,39305,39335,39364,39394,39424,39453,39483,39512,39541,
39571,39600,39630,39659,39689,39719,39748,39778,39808,39837,39867,39896,39925,
39955,39984,40013,40043,40073,40102,40132,40162,40192,40221,40251,40280,40309,
40339,40368,40397,40427,40456,40486,40516,40546,40575,40605,40635,40664,40693,
40723,40752,40781,40811,40840,40870,40900,40929,40959,40989,41018,41048,41077,
41107,41136,41165,41195,41224,41254,41283,41313,41343,41373,41402,41432,41461,
41491,41520,41549,41579,41608,41638,41667,41697,41727,41756,41786,41816,41845,
41875,41904,41934,41963,41992,42022,42051,42081,42110,42140,42170,42199,42229,
42258,42288,42318,42347,42377,42406,42435,42465,42494,42524,42553,42583,42613,
42642,42672,42702,42731,42761,42790,42819,42849,42878,42907,42937,42967,42996,
43026,43056,43086,43115,43145,43174,43203,43233,43262,43291,43321,43350,43380,
43410,43440,43469,43499,43529,43558,43587,43617,43646,43675,43705,43734,43764,
43794,43823,43853,43883,43913,43942,43971,44001,44030,44059,44089,44118,44148,
44177,44207,44237,44267,44296,44326,44355,44385,44414,44443,44473,44502,44532,
44561,44591,44621,44650,44680,44710,44739,44769,44798,44827,44857,44886,44916,
44945,44975,45004,45034,45064,45093,45123,45152,45182,45211,45241,45270,45300,
45329,45359,45388,45418,45447,45477,45507,45536,45566,45596,45625,45654,45684,
45713,45743,45772,45802,45831,45861,45890,45920,45950,45979,46009,46039,46068,
46097,46127,46156,46185,46215,46244,46274,46304,46334,46363,46393,46423,46452,
46481,46511,46540,46569,46599,46628,46658,46688,46717,46747,46777,46807,46836,
46865,46895,46924,46953,46983,47012,47042,47071,47101,47131,47161,47190,47220,
47249,47279,47308,47337,47367,47396,47426,47455,47485,47515,47544,47574,47604,
47633,47663,47692,47721,47751,47780,47810,47839,47869,47898,47928,47958,47988,
48017,48047,48076,48105,48135,48164,48194,48223,48253,48282,48312,48342,48371,
48401,48430,48460,48489,48519,48548,48578,48607,48637,48666,48696,48725,48755,
48784,48814,48844,48873,48903,48932,48962,48991,49021,49050,49079,49109,49138,
49168,49198,49228,49257,49287,49316,49346,49375,49405,49434,49463,49493,49522,
49552,49582,49611,49641,49671,49700,49730,49759,49789,49818,49847,49877,49906,
49936,49965,49995,50025,50055,50084,50114,50143,50173,50202,50231,50261,50290,
50320,50349,50379,50409,50439,50468,50498,50527,50557,50586,50615,50645,50674,
50704,50733,50763,50793,50822,50852,50882,50911,50941,50970,50999,51029,51058,
51088,51117,51147,51176,51206,51236,51265,51295,51324,51354,51383,51413,51442,
51472,51501,51531,51560,51590,51619,51649,51679,51708,51738,51767,51797,51826,
51856,51885,51915,51944,51974,52003,52033,52062,52092,52122,52151,52181,52210,
52240,52269,52299,52328,52357,52387,52416,52446,52476,52505,52535,52565,52594,
52624,52653,52683,52712,52741,52771,52800,52830,52859,52889,52919,52949,52978,
53008,53037,53067,53096,53125,53155,53184,53214,53243,53273,53303,53333,53362,
53392,53421,53451,53480,53509,53539,53568,53597,53627,53657,53687,53716,53746,
53776,53805,53835,53864,53893,53923,53952,53981,54011,54041,54070,54100,54130,
54159,54189,54219,54248,54277,54307,54336,54365,54395,54425,54454,54484,54513,
54543,54573,54602,54632,54661,54691,54720,54750,54779,54809,54838,54868,54897,
54927,54956,54986,55016,55045,55075,55104,55134,55163,55193,55222,55251,55281,
55310,55340,55370,55399,55429,55459,55488,55518,55547,55577,55606,55635,55665,
55694,55724,55753,55783,55813,55843,55872,55902,55931,55961,55990,56019,56049,
56078,56108,56137,56167,56197,56227,56256,56286,56315,56345,56374,56403,56433,
56462,56491,56521,56551,56580,56610,56640,56670,56699,56729,56758,56787,56817,
56846,56875,56905,56935,56964,56994,57024,57054,57083,57113,57142,57171,57201,
57230,57259,57289,57318,57348,57378,57408,57437,57467,57496,57526,57555,57585,
57614,57643,57673,57702,57732,57762,57791,57821,57851,57880,57910,57939,57969,
57998,58028,58057,58086,58116,58145,58175,58205,58234,58264,58294,58323,58353,
58382,58412,58441,58471,58500,58529,58559,58588,58618,58648,58677,58707,58737,
58766,58796,58825,58855,58884,58913,58943,58972,59002,59031,59061,59091,59120,
59150,59180,59209,59239,59268,59297,59327,59356,59385,59415,59445,59474,59504,
59534,59564,59593,59623,59652,59681,59711,59740,59769,59799,59828,59858,59888,
59918,59948,59977,60007,60036,60065,60095,60124,60153,60183,60212,60242,60272,
60302,60331,60361,60391,60420,60449,60479,60508,60537,60567,60596,60626,60656,
60685,60715,60745,60774,60804,60833,60863,60892,60921,60951,60980,61010,61039,
61069,61099,61128,61158,61188,61217,61247,61276,61306,61335,61364,61394,61423,
61453,61482,61512,61542,61571,61601,61631,61660,61690,61719,61749,61778,61807,
61837,61866,61896,61925,61955,61985,62014,62044,62074,62103)

_YEARTABLE = (0,13,25,37,50,62,74,87,99,111,124,136,149,161,173,186,198,210,223,
235,248,260,272,285,297,309,322,334,346,359,371,384,396,408,421,433,445,458,470,
483,495,507,520,532,544,557,569,581,594,606,619,631,643,656,668,680,693,705,718,
730,742,755,767,779,792,804,816,829,841,854,866,878,891,903,915,928,940,953,965,
977,990,1002,1014,1027,1039,1051,1064,1076,1089,1101,1113,1126,1138,1150,1163,
1175,1188,1200,1212,1225,1237,1249,1262,1274,1287,1299,1311,1324,1336,1348,1361,
1373,1385,1398,1410,1423,1435,1447,1460,1472,1484,1497,1509,1521,1534,1546,1559,
1571,1583,1596,1608,1620,1633,1645,1658,1670,1682,1695,1707,1719,1732,1744,1756,
1769,1781,1794,1806,1818,1831,1843,1855,1868,1880,1893,1905,1917,1930,1942,1954,
1967,1979,1991,2004,2016,2029,2041,2053,2066,2078,2090)

_LEAPTABLE = "\7\0\0\5\0\0\4\0\0\2\0\6\0\0\5\0\0\3\0\10\0\0\5\0\0\4\0\0\2\0\6\
\0\0\5\0\0\2\0\7\0\0\5\0\0\4\0\0\2\0\6\0\0\5\0\0\3\0\7\0\0\6\0\0\4\0\0\2\0\7\0\
\0\5\0\0\3\0\10\0\0\6\0\0\4\0\0\3\0\7\0\0\5\0\0\4\0\10\0\0\6\0\0\4\0\12\0\0\6\
\0\0\5\0\0\3\0\10\0\0\5\0\0\4\0\0\2\0\7\0\0\5\0\0\3\0\11\0\0\5\0\0\4\0\0\2\0\6\
\0\0\5\0\0\3\0\13\0\0\6\0\0\5\0\0\2\0\7\0\0\5\0\0\3"

###################################################################################
## Basic Functions

def _bisect(a, x):
    lo = 0; hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]: hi = mid
        else: lo = mid + 1
    return lo - 1

def sol2lun(year, month, day, leap=False):
    """sol2lun(year, month, day, leap=False) -> (year, month, day, leap)
    Returns corresponding date in lunar calendar. leap will be ignored."""
    days = date(year, month, day).toordinal()
    if not _MINDATE <= days <= _MAXDATE:
        raise ValueError, "year is out of range"
    days -= _MINDATE
    month = _bisect(_MONTHTABLE, days)
    year = _bisect(_YEARTABLE, month)
    month, day = month - _YEARTABLE[year] + 1, days - _MONTHTABLE[month] + 1
    if (ord(_LEAPTABLE[year]) or 13) < month:
        month -= 1
        leap = (ord(_LEAPTABLE[year]) == month)
    else:
        leap = False
    return (year + _BASEYEAR, month, day, leap)

def lun2sol(year, month, day, leap=False):
    """lun2sol(year, month, day, leap=False) -> (year, month, day, leap)
    Returns corresponding date in solar calendar."""
    year -= _BASEYEAR
    if not 0 <= year < len(_YEARTABLE):
        raise ValueError, "year is out of range"
    if not 1 <= month <= 12:
        raise ValueError, "wrong month"
    if leap and ord(_LEAPTABLE[year]) != month:
        raise ValueError, "wrong leap month"
    months = _YEARTABLE[year] + month - 1
    if leap or (ord(_LEAPTABLE[year]) or 13) < month:
        months += 1
    days = _MONTHTABLE[months] + day - 1
    if day < 1 or days >= _MONTHTABLE[months + 1]:
        raise ValueError, "wrong day"
    return date.fromordinal(days + _MINDATE).timetuple()[:3] + (False,)

def getganzistr(index, locale=None):
    """getganzistr(index, locale=None) -> unicode string
    Returns corresponding unicode string of ganzi.
    locale can be "ko", "ja", "zh". Uses default locale when locale is ignored.
    
    NOTE: Non-Unicode version of transdate doesn't support this function.
    """
    raise NotImplemented, 'getganzistr needs Unicode enabled Python'

def strftime(format, t=None):
    """strftime(format, t=None) -> string
    Returns formatted string of given timestamp. If timestamp is omitted,
    current timestamp (return value of time.localtime()) is used.

    Similar to time.strftime, but has the following extensions:
      %LC - (year / 100) as a decimal number (at least 2 digits)
      %Ld - lunar day of the month as a decimal number [01,30]
      %Le - same as %Ld, but preceding blank instead of zero
      %LF - same as "%LY-%Lm-%Ld"
      %Lj - day of the lunar year as a decimal number [001,390]
      %Ll - 0 for non-leap month, 1 for leap month
      %Lm - lunar month as a decimal number [01,12]
      %Ly - lunar year without century as a decimal number [00,99]
      %LY - lunar year with century as a decimal number
    """
    if t is None: t = time.localtime()
    if _STRFTIMEREGEXP is not None:
        lt = sol2lun(*t[:3])
        lord = date(t[0], t[1], t[2]).toordinal() - _MINDATE
        ldoy = lord - _MONTHTABLE[_YEARTABLE[lt[0] - _BASEYEAR]] + 1
        lmap = {'Y': '%04d' % lt[0], 'm': '%02d' % lt[1], 'd': '%02d' % lt[2],
                'y': '%02d' % (lt[0] % 100), 'C': '%02d' % (lt[0] // 100),
                'F': '%04d-%02d-%02d' % lt[:3], 'e': str(lt[2]),
                'l': '%d' % lt[3], 'j': '%03d' % ldoy}
        format = _STRFTIMEREGEXP.sub(lambda m: '%' * (len(m.group(1)) / 2) +
                                               lmap.get(m.group(2), ''), format)
    return time.strftime(format, t)

###################################################################################
## Class Declaration

# just alias. we have lunardate, so why not we have solardate?
solardate = date

class lunardate(date):
    """lunardate(year, month, day, leap=False) -> new lunardate object"""

    def __new__(cls, year, month, day, leap=False):
        obj = date.__new__(cls, *lun2sol(year, month, day, leap)[:3])
        object.__setattr__(obj, 'lunaryear', year)
        object.__setattr__(obj, 'lunarmonth', month)
        object.__setattr__(obj, 'lunarday', day)
        object.__setattr__(obj, 'lunarleap', leap)
        return obj
    
    def __repr__(self):
        return '%s.%s(%d, %d, %d, %s)' % \
               (self.__class__.__module__, self.__class__.__name__,
                self.lunaryear, self.lunarmonth, self.lunarday, self.lunarleap)
    
    min = type('propertyproxy', (object,), {
        '__doc__': 'lunardate.min -> The earliest representable date',
        '__get__': lambda self, inst, cls: cls.fromordinal(_MINDATE)})()
    max = type('propertyproxy', (object,), {
        '__doc__': 'lunardate.max -> The latest representable date',
        '__get__': lambda self, inst, cls: cls.fromordinal(_MAXDATE)})()
    
    def __setattr__(self, name, value):
        raise AttributeError, "can't set attribute."
    
    def __add__(self, other):
        return self.fromsolardate(date.__add__(self, other))
    
    def __radd__(self, other):
        return self.fromsolardate(date.__radd__(self, other))
    
    def __sub__(self, other):
        result = date.__sub__(self, other)
        if not isinstance(result, timedelta):
            result = self.fromsolardate(result)
        return result

    def replace(self, year=None, month=None, day=None, leap=None):
        """lunardate.replace(year, month, day, leap) -> new lunardate object
        Same as date.replace, but returns lunardate object instead of date object."""
        if leap is None: leap = self.lunarleap
        return lunardate(year or self.lunaryear, month or self.lunarmonth,
                         day or self.month, leap)
    
    def tosolardate(self):
        """lunardate.tosolardate() -> date object
        Returns corresponding date object."""
        return date(self.year, self.month, self.day)
    
    def today(self):
        """lunardate.today() -> new lunardate object
        Returns lunardate object which represents today."""
        return self.fromsolardate(date.today())
    
    def fromsolardate(self, solardate):
        """lunardate.fromsolardate(solardate) -> new lunardate object
        Returns corresponding lunardate object from date object."""
        return lunardate(*sol2lun(*solardate.timetuple()[:3]))
    
    def fromtimestamp(self, timestamp):
        """lunardate.fromtimestamp(timestamp) -> new lunardate object
        Returns corresponding lunardate object from UNIX timestamp."""
        return self.fromsolardate(date.fromtimestamp(timestamp))
    
    def fromordinal(self, ordinal):
        """lunardate.fromordinal(ordinal) -> new lunardate object
        Returns corresponding lunardate object from Gregorian ordinal."""
        return self.fromsolardate(date.fromordinal(ordinal))
    
    def getganzi(self):
        """lunardate.getganzi() -> (year_ganzi, month_ganzi, day_ganzi)
        Returns ganzi index between 0..59 from lunardate object.
        Ganzi index can be converted using getganzistr function."""
        return ((self.lunaryear + 56) % 60,
                (self.lunaryear * 12 + self.lunarmonth + 13) % 60,
                (self.toordinal() + 14) % 60)

    def getganzistr(self, locale=None):
        """lunardate.getganzistr(locale=None) -> 3-tuple of unicode string
        Returns unicode string of ganzi from lunardate object.
        See getganzistr global function for detail.

        NOTE: Non-Unicode version of transdate doesn't support this function.
        """
        raise NotImplemented, 'getganzistr needs Unicode enabled Python'

    def strftime(self, format):
        """lunardate.strftime(format) -> string
        Returns formatted string of lunardate object.
        See strftime global function for detail."""
        return strftime(format, self.timetuple())
    
    today = classmethod(today)
    fromsolardate = classmethod(fromsolardate)
    fromtimestamp = classmethod(fromtimestamp)
    fromordinal = classmethod(fromordinal)

# we create new lunardate class from old lunardate class using typeproxy,
# because default type class always allows setting class variable.
# __slots__ is added later to forbid descriptor initialization by type.
class typeproxy(type):
    def __setattr__(self, name, value):
        raise AttributeError, "can't set attribute."
clsdict = dict(lunardate.__dict__)
clsdict['__slots__'] = ['lunaryear', 'lunarmonth', 'lunarday', 'lunarleap']
lunardate = typeproxy(lunardate.__name__, lunardate.__bases__, clsdict)
del typeproxy

###################################################################################
## Command Line Interface

if __name__ == '__main__':
    import sys
    try:
        mode = sys.argv[1].lower()
        if mode == 'today':
            if len(sys.argv) != 2: raise RuntimeError
            today = lunardate.today()
            isleap = today.lunarleap and ' (leap)' or ''
            print today.strftime('Today: solar %Y-%m-%d %a = lunar %LY-%Lm-%Ld' + isleap)
        elif mode == 'solar':
            if len(sys.argv) != 5: raise RuntimeError
            solar = lunardate.fromsolardate(date(*map(int, sys.argv[2:])))
            isleap = solar.lunarleap and ' (leap)' or ''
            print solar.strftime('solar %Y-%m-%d %a -> lunar %LY-%Lm-%Ld' + isleap)
        elif mode == 'lunar':
            if len(sys.argv) not in (5, 6): raise RuntimeError
            leap = (len(sys.argv) == 6 and sys.argv[5].lower() == 'leap')
            solar = lunardate(*(map(int, sys.argv[2:5]) + [leap]))
            isleap = leap and ' (leap)' or ''
            print solar.strftime('lunar %LY-%Lm-%Ld' + isleap + ' -> solar %Y-%m-%d %a')
        else:
            raise RuntimeError
    except (IndexError, RuntimeError):
        app = sys.argv[0]
        print 'Usage:'
        print '  for today - python %s today' % app
        print '  for solar to lunar - python %s solar <year> <month> <day>' % app
        print '  for lunar to solar - python %s lunar <year> <month> <day> [leap]' % app
    except:
        print 'Error: %s' % sys.exc_info()[1]

