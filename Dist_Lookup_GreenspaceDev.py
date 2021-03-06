# -*- coding: utf-8 -*-
"""
Distance lookup array for the Dist_Lookup_GreenspaceDev
Contains the shortest path distance from the centroids of each available site and
developable greenspace site. Shortest path distance is facilitated by networkx
"""

fdist_lookup = [( (50, 1) , 3672.0 ),
( (35, 2) , 1294.0 ),
( (36, 2) , 1295.0 ),
( (40, 3) , 1 ),
( (41, 3) , 2 ),
( (47, 3) , 314.0 ),
( (40, 4) , 1 ),
( (32, 5) , 862.0 ),
( (33, 5) , 435.0 ),
( (34, 5) , 436.0 ),
( (38, 6) , 941.0 ),
( (47, 6) , 1227.0 ),
( (42, 8) , 1999.0 ),
( (28, 9) , 1820.0 ),
( (47, 9) , 2219.0 ),
( (53, 9) , 1028.0 ),
( (55, 9) , 1013.0 ),
( (38, 10) , 1114.0 ),
( (18, 11) , 1 ),
( (54, 11) , 1066.0 ),
( (25, 12) , 740.0 ),
( (54, 12) , 1067.0 ),
( (57, 12) , 1244.0 ),
( (22, 13) , 1543.0 ),
( (43, 13) , 2169.0 ),
( (52, 13) , 580.0 ),
( (53, 13) , 1234.0 ),
( (22, 14) , 1481.0 ),
( (23, 14) , 1482.0 ),
( (27, 14) , 1 ),
( (36, 14) , 1 ),
( (44, 14) , 2502.0 ),
( (56, 14) , 1 ),
( (21, 15) , 849.0 ),
( (30, 15) , 2867.0 ),
( (40, 15) , 1091.0 ),
( (42, 15) , 1641.0 ),
( (51, 15) , 2009.0 ),
( (54, 15) , 815.0 ),
( (21, 16) , 849.0 ),
( (30, 16) , 2868.0 ),
( (35, 16) , 1410.0 ),
( (40, 16) , 1091.0 ),
( (44, 16) , 2503.0 ),
( (54, 16) , 816.0 ),
( (30, 17) , 2869.0 ),
( (42, 17) , 750.0 ),
( (47, 17) , 1 ),
( (22, 18) , 1327.0 ),
( (23, 18) , 1327.0 ),
( (24, 18) , 1328.0 ),
( (26, 18) , 3428.0 ),
( (28, 18) , 2749.0 ),
( (29, 18) , 2750.0 ),
( (31, 18) , 2751.0 ),
( (36, 18) , 1106.0 ),
( (41, 18) , 259.0 ),
( (42, 18) , 1112.0 ),
( (50, 18) , 858.0 ),
( (51, 18) , 729.0 ),
( (26, 19) , 3428.0 ),
( (27, 19) , 2749.0 ),
( (49, 19) , 120.0 ),
( (63, 19) , 2 ),
( (19, 20) , 803.0 ),
( (55, 20) , 2758.0 ),
( (60, 20) , 2048.0 ),
( (23, 21) , 1914.0 ),
( (33, 21) , 1308.0 ),
( (36, 21) , 1027.0 ),
( (49, 21) , 1458.0 ),
( (32, 22) , 1960.0 ),
( (51, 22) , 1012.0 ),
( (57, 22) , 2054.0 ),
( (21, 23) , 1 ),
( (28, 23) , 1 ),
( (41, 23) , 2308.0 ),
( (47, 23) , 1287.0 ),
( (51, 23) , 1013.0 ),
( (52, 23) , 1014.0 ),
( (53, 23) , 1256.0 ),
( (60, 23) , 657.0 ),
( (41, 24) , 1861.0 ),
( (50, 24) , 1 ),
( (52, 24) , 1015.0 ),
( (54, 24) , 747.0 ),
( (26, 25) , 794.0 ),
( (49, 25) , 160.0 ),
( (55, 25) , 305.0 ),
( (26, 26) , 795.0 ),
( (44, 26) , 1021.0 ),
( (46, 26) , 244.0 ),
( (32, 27) , 349.0 ),
( (40, 27) , 1 ),
( (43, 27) , 1652.0 ),
( (61, 27) , 1368.0 ),
( (66, 27) , 894.0 ),
( (17, 28) , 305.0 ),
( (19, 28) , 1585.0 ),
( (28, 28) , 2735.0 ),
( (31, 28) , 962.0 ),
( (35, 28) , 2173.0 ),
( (39, 28) , 676.0 ),
( (40, 28) , 200.0 ),
( (45, 28) , 981.0 ),
( (47, 28) , 585.0 ),
( (53, 28) , 1 ),
( (74, 28) , 838.0 ),
( (34, 29) , 2173.0 ),
( (35, 29) , 2173.0 ),
( (67, 29) , 899.0 ),
( (19, 30) , 1566.0 ),
( (22, 30) , 1722.0 ),
( (25, 30) , 455.0 ),
( (28, 30) , 3400.0 ),
( (36, 30) , 2450.0 ),
( (39, 30) , 1898.0 ),
( (45, 30) , 752.0 ),
( (65, 30) , 786.0 ),
( (68, 30) , 1255.0 ),
( (18, 31) , 1644.0 ),
( (34, 31) , 2593.0 ),
( (36, 31) , 2451.0 ),
( (40, 31) , 1623.0 ),
( (44, 31) , 1603.0 ),
( (71, 31) , 1 ),
( (14, 32) , 5735.0 ),
( (19, 32) , 1317.0 ),
( (23, 32) , 765.0 ),
( (30, 32) , 3723.0 ),
( (41, 32) , 677.0 ),
( (44, 32) , 1748.0 ),
( (60, 32) , 1993.0 ),
( (70, 32) , 1 ),
( (23, 33) , 766.0 ),
( (30, 33) , 3723.0 ),
( (31, 33) , 2936.0 ),
( (34, 33) , 995.0 ),
( (64, 33) , 1 ),
( (14, 34) , 714.0 ),
( (22, 34) , 1784.0 ),
( (31, 34) , 2936.0 ),
( (36, 34) , 1957.0 ),
( (44, 34) , 1453.0 ),
( (58, 34) , 3072.0 ),
( (18, 35) , 3352.0 ),
( (24, 35) , 2399.0 ),
( (36, 35) , 764.0 ),
( (40, 35) , 2038.0 ),
( (50, 35) , 1570.0 ),
( (53, 35) , 1 ),
( (68, 35) , 1603.0 ),
( (20, 36) , 1926.0 ),
( (21, 36) , 1927.0 ),
( (22, 36) , 703.0 ),
( (24, 36) , 2399.0 ),
( (37, 36) , 1597.0 ),
( (47, 36) , 560.0 ),
( (53, 36) , 1 ),
( (65, 36) , 874.0 ),
( (33, 37) , 1 ),
( (45, 37) , 9336.0 ),
( (52, 37) , 1 ),
( (53, 37) , 1 ),
( (18, 38) , 1540.0 ),
( (40, 38) , 2852.0 ),
( (53, 38) , 2 ),
( (7, 39) , 813.0 ),
( (18, 39) , 1541.0 ),
( (33, 39) , 1255.0 ),
( (39, 39) , 2900.0 ),
( (40, 39) , 2901.0 ),
( (43, 39) , 80.0 ),
( (68, 39) , 3385.0 ),
( (8, 40) , 1 ),
( (17, 40) , 1542.0 ),
( (29, 40) , 2176.0 ),
( (37, 40) , 2305.0 ),
( (41, 40) , 1888.0 ),
( (46, 40) , 1057.0 ),
( (53, 40) , 778.0 ),
( (61, 40) , 1445.0 ),
( (63, 40) , 2171.0 ),
( (17, 41) , 1543.0 ),
( (18, 41) , 1544.0 ),
( (25, 41) , 2 ),
( (34, 41) , 2592.0 ),
( (37, 41) , 2306.0 ),
( (54, 41) , 1829.0 ),
( (8, 42) , 351.0 ),
( (20, 42) , 2277.0 ),
( (21, 42) , 2277.0 ),
( (33, 42) , 3043.0 ),
( (35, 42) , 2657.0 ),
( (47, 42) , 1259.0 ),
( (64, 42) , 1593.0 ),
( (71, 42) , 2016.0 ),
( (21, 43) , 3048.0 ),
( (32, 43) , 3043.0 ),
( (35, 43) , 2657.0 ),
( (46, 43) , 2317.0 ),
( (51, 43) , 464.0 ),
( (52, 43) , 464.0 ),
( (58, 43) , 959.0 ),
( (66, 43) , 1009.0 ),
( (20, 44) , 1031.0 ),
( (27, 44) , 1626.0 ),
( (31, 44) , 2101.0 ),
( (35, 44) , 2266.0 ),
( (38, 44) , 178.0 ),
( (45, 44) , 2208.0 ),
( (56, 44) , 2579.0 ),
( (57, 44) , 2580.0 ),
( (62, 44) , 401.0 ),
( (66, 44) , 752.0 ),
( (77, 44) , 2283.0 ),
( (30, 45) , 1 ),
( (50, 45) , 3672.0 ),
( (58, 45) , 1440.0 ),
( (59, 45) , 1493.0 ),
( (62, 45) , 986.0 ),
( (74, 45) , 940.0 ),
( (77, 45) , 2284.0 ),
( (34, 46) , 1808.0 ),
( (64, 46) , 783.0 ),
( (8, 47) , 1 ),
( (10, 47) , 932.0 ),
( (34, 47) , 1809.0 ),
( (56, 47) , 1131.0 ),
( (71, 47) , 216.0 ),
( (19, 48) , 984.0 ),
( (27, 48) , 2374.0 ),
( (45, 48) , 1 ),
( (67, 48) , 1978.0 ),
( (68, 48) , 1979.0 ),
( (69, 48) , 1980.0 ),
( (71, 48) , 217.0 ),
( (76, 48) , 999.0 ),
( (14, 49) , 1 ),
( (23, 49) , 2428.0 ),
( (42, 49) , 2515.0 ),
( (73, 49) , 1096.0 ),
( (46, 50) , 1335.0 ),
( (48, 50) , 1278.0 ),
( (72, 50) , 1135.0 ),
( (75, 50) , 2 ),
( (12, 51) , 427.0 ),
( (14, 51) , 804.0 ),
( (29, 51) , 2336.0 ),
( (33, 51) , 1 ),
( (39, 51) , 2286.0 ),
( (54, 51) , 2302.0 ),
( (58, 51) , 817.0 ),
( (63, 51) , 1998.0 ),
( (74, 51) , 2 ),
( (23, 52) , 1331.0 ),
( (26, 52) , 573.0 ),
( (30, 52) , 1662.0 ),
( (48, 52) , 1216.0 ),
( (62, 52) , 1163.0 ),
( (71, 52) , 243.0 ),
( (74, 52) , 3 ),
( (78, 52) , 2004.0 ),
( (82, 52) , 416.0 ),
( (17, 53) , 2449.0 ),
( (32, 53) , 2538.0 ),
( (46, 53) , 1387.0 ),
( (68, 53) , 2581.0 ),
( (69, 53) , 2582.0 ),
( (70, 53) , 2583.0 ),
( (0, 54) , 7624.0 ),
( (17, 54) , 1883.0 ),
( (19, 54) , 1140.0 ),
( (21, 54) , 1 ),
( (22, 54) , 1165.0 ),
( (28, 54) , 1899.0 ),
( (38, 54) , 448.0 ),
( (41, 54) , 1398.0 ),
( (44, 54) , 1 ),
( (49, 54) , 344.0 ),
( (51, 54) , 428.0 ),
( (55, 54) , 1271.0 ),
( (56, 54) , 1272.0 ),
( (63, 54) , 1164.0 ),
( (70, 54) , 1539.0 ),
( (72, 54) , 1160.0 ),
( (77, 54) , 1 ),
( (85, 54) , 1737.0 ),
( (0, 55) , 6866.0 ),
( (9, 55) , 2639.0 ),
( (18, 55) , 1883.0 ),
( (29, 55) , 1584.0 ),
( (30, 55) , 816.0 ),
( (41, 55) , 1398.0 ),
( (42, 55) , 1249.0 ),
( (44, 55) , 1531.0 ),
( (48, 55) , 1216.0 ),
( (50, 55) , 1 ),
( (55, 55) , 2101.0 ),
( (62, 55) , 1165.0 ),
( (66, 55) , 3773.0 ),
( (72, 55) , 1160.0 ),
( (0, 56) , 6867.0 ),
( (14, 56) , 2131.0 ),
( (29, 56) , 1585.0 ),
( (46, 56) , 1998.0 ),
( (59, 56) , 1 ),
( (63, 56) , 1165.0 ),
( (71, 56) , 1204.0 ),
( (0, 57) , 6868.0 ),
( (24, 57) , 1777.0 ),
( (25, 57) , 2484.0 ),
( (27, 57) , 2930.0 ),
( (34, 57) , 642.0 ),
( (43, 57) , 1125.0 ),
( (57, 57) , 950.0 ),
( (59, 57) , 2 ),
( (66, 57) , 2425.0 ),
( (67, 57) , 1546.0 ),
( (69, 57) , 699.0 ),
( (70, 57) , 1 ),
( (72, 57) , 1515.0 ),
( (81, 57) , 2052.0 ),
( (30, 58) , 1696.0 ),
( (34, 58) , 643.0 ),
( (35, 58) , 1 ),
( (48, 58) , 807.0 ),
( (67, 58) , 1546.0 ),
( (70, 58) , 138.0 ),
( (71, 58) , 423.0 ),
( (24, 59) , 1973.0 ),
( (40, 59) , 1832.0 ),
( (70, 59) , 537.0 ),
( (9, 60) , 1 ),
( (19, 60) , 591.0 ),
( (36, 60) , 1509.0 ),
( (37, 60) , 1343.0 ),
( (40, 60) , 2081.0 ),
( (44, 60) , 1267.0 ),
( (69, 60) , 1398.0 ),
( (79, 60) , 1 ),
( (8, 61) , 2 ),
( (22, 61) , 1089.0 ),
( (25, 61) , 2786.0 ),
( (27, 61) , 2786.0 ),
( (34, 61) , 337.0 ),
( (35, 61) , 338.0 ),
( (40, 61) , 2081.0 ),
( (42, 61) , 2180.0 ),
( (47, 61) , 2353.0 ),
( (60, 61) , 1 ),
( (78, 61) , 1 ),
( (79, 61) , 608.0 ),
( (17, 62) , 762.0 ),
( (22, 62) , 1297.0 ),
( (31, 62) , 377.0 ),
( (36, 62) , 1 ),
( (37, 62) , 1586.0 ),
( (38, 62) , 1586.0 ),
( (39, 62) , 1587.0 ),
( (40, 62) , 1588.0 ),
( (59, 62) , 1 ),
( (18, 63) , 2368.0 ),
( (25, 63) , 2787.0 ),
( (37, 63) , 1587.0 ),
( (39, 63) , 1588.0 ),
( (40, 63) , 1589.0 ),
( (45, 63) , 2675.0 ),
( (8, 64) , 2018.0 ),
( (11, 64) , 474.0 ),
( (14, 64) , 2448.0 ),
( (15, 64) , 2449.0 ),
( (16, 64) , 1650.0 ),
( (18, 64) , 2369.0 ),
( (22, 64) , 1587.0 ),
( (29, 64) , 1445.0 ),
( (42, 64) , 1675.0 ),
( (43, 64) , 3058.0 ),
( (45, 64) , 2676.0 ),
( (70, 64) , 2960.0 ),
( (71, 64) , 2961.0 ),
( (11, 65) , 1746.0 ),
( (16, 65) , 2836.0 ),
( (25, 65) , 2687.0 ),
( (39, 65) , 1 ),
( (43, 65) , 3059.0 ),
( (44, 65) , 3060.0 ),
( (45, 65) , 2677.0 ),
( (51, 65) , 1778.0 ),
( (77, 65) , 1 ),
( (3, 66) , 4470.0 ),
( (18, 66) , 2303.0 ),
( (27, 66) , 1942.0 ),
( (33, 66) , 2209.0 ),
( (35, 66) , 461.0 ),
( (36, 66) , 462.0 ),
( (41, 66) , 828.0 ),
( (42, 66) , 829.0 ),
( (50, 66) , 1778.0 ),
( (51, 66) , 1778.0 ),
( (53, 66) , 2501.0 ),
( (54, 66) , 823.0 ),
( (57, 66) , 1844.0 ),
( (63, 66) , 1 ),
( (21, 67) , 1 ),
( (31, 67) , 1261.0 ),
( (33, 67) , 2210.0 ),
( (34, 67) , 874.0 ),
( (36, 67) , 461.0 ),
( (38, 67) , 1102.0 ),
( (46, 67) , 1862.0 ),
( (53, 67) , 2502.0 ),
( (69, 67) , 1810.0 ),
( (18, 68) , 2439.0 ),
( (20, 68) , 1871.0 ),
( (21, 68) , 2 ),
( (29, 68) , 328.0 ),
( (33, 68) , 2211.0 ),
( (34, 68) , 2212.0 ),
( (36, 68) , 328.0 ),
( (37, 68) , 673.0 ),
( (42, 68) , 830.0 ),
( (43, 68) , 831.0 ),
( (46, 68) , 1242.0 ),
( (54, 68) , 1 ),
( (58, 68) , 2200.0 ),
( (63, 68) , 997.0 ),
( (65, 68) , 2264.0 ),
( (74, 68) , 923.0 ),
( (31, 69) , 820.0 ),
( (32, 69) , 527.0 ),
( (35, 69) , 1 ),
( (38, 69) , 1464.0 ),
( (42, 69) , 831.0 ),
( (48, 69) , 1836.0 ),
( (24, 70) , 2137.0 ),
( (25, 70) , 2138.0 ),
( (32, 70) , 465.0 ),
( (33, 70) , 1 ),
( (35, 70) , 2 ),
( (36, 70) , 2533.0 ),
( (38, 70) , 1931.0 ),
( (39, 70) , 1931.0 ),
( (41, 70) , 1 ),
( (42, 70) , 2 ),
( (61, 70) , 1227.0 ),
( (62, 70) , 1228.0 ),
( (69, 70) , 1034.0 ),
( (78, 70) , 2 ),
( (13, 71) , 1261.0 ),
( (26, 71) , 1360.0 ),
( (36, 71) , 2353.0 ),
( (39, 71) , 2579.0 ),
( (40, 71) , 2580.0 ),
( (41, 71) , 2581.0 ),
( (42, 71) , 2 ),
( (40, 72) , 2945.0 ),
( (42, 72) , 3 ),
( (44, 72) , 614.0 ),
( (49, 72) , 2 ),
( (59, 72) , 706.0 ),
( (62, 72) , 450.0 ),
( (16, 73) , 757.0 ),
( (20, 73) , 1166.0 ),
( (24, 73) , 1986.0 ),
( (43, 73) , 1365.0 ),
( (44, 73) , 1365.0 ),
( (51, 73) , 974.0 ),
( (53, 73) , 408.0 ),
( (66, 73) , 1610.0 ),
( (69, 73) , 2 ),
( (24, 74) , 1033.0 ),
( (41, 74) , 2349.0 ),
( (48, 74) , 960.0 ),
( (49, 74) , 257.0 ),
( (50, 74) , 607.0 ),
( (51, 74) , 974.0 ),
( (84, 74) , 607.0 ),
( (19, 75) , 574.0 ),
( (34, 75) , 193.0 ),
( (37, 75) , 1797.0 ),
( (39, 75) , 2608.0 ),
( (40, 75) , 2608.0 ),
( (41, 75) , 2349.0 ),
( (45, 75) , 1922.0 ),
( (49, 75) , 1 ),
( (51, 75) , 975.0 ),
( (28, 76) , 2609.0 ),
( (33, 76) , 836.0 ),
( (37, 76) , 1260.0 ),
( (39, 76) , 2555.0 ),
( (41, 76) , 2349.0 ),
( (49, 76) , 2 ),
( (54, 76) , 477.0 ),
( (28, 77) , 2610.0 ),
( (29, 77) , 2318.0 ),
( (30, 77) , 1655.0 ),
( (36, 77) , 193.0 ),
( (43, 77) , 1796.0 ),
( (51, 77) , 1391.0 ),
( (58, 77) , 1 ),
( (39, 78) , 2274.0 ),
( (59, 78) , 2 ),
( (68, 78) , 2488.0 ),
( (72, 78) , 1798.0 ),
( (79, 78) , 1 ),
( (87, 78) , 2732.0 ),
( (32, 79) , 1919.0 ),
( (35, 79) , 1626.0 ),
( (43, 79) , 476.0 ),
( (45, 79) , 588.0 ),
( (35, 80) , 1626.0 ),
( (37, 80) , 816.0 ),
( (39, 80) , 1142.0 ),
( (40, 80) , 1151.0 ),
( (41, 80) , 1152.0 ),
( (43, 80) , 1 ),
( (44, 80) , 385.0 ),
( (71, 80) , 613.0 ),
( (22, 81) , 1 ),
( (34, 81) , 984.0 ),
( (37, 81) , 817.0 ),
( (38, 81) , 818.0 ),
( (39, 81) , 1143.0 ),
( (40, 81) , 1152.0 ),
( (26, 82) , 1 ),
( (28, 82) , 1 ),
( (29, 82) , 2 ),
( (30, 82) , 3 ),
( (34, 82) , 349.0 ),
( (38, 82) , 819.0 ),
( (53, 82) , 1882.0 ),
( (58, 82) , 2948.0 ),
( (36, 83) , 2 ),
( (43, 83) , 1279.0 ),
( (73, 83) , 524.0 ),
( (34, 84) , 1400.0 ),
( (36, 84) , 2 ),
( (37, 84) , 3 ),
( (39, 84) , 1 ),
( (40, 84) , 2 ),
( (42, 84) , 208.0 ),
( (67, 84) , 882.0 ),
( (37, 85) , 4 ),
( (39, 85) , 2 ),
( (41, 85) , 2 ),
( (63, 85) , 1359.0 ),
( (36, 86) , 1386.0 ),
( (37, 86) , 5 ),
( (53, 86) , 1091.0 ),
( (64, 86) , 351.0 ),
( (66, 86) , 1 ),
( (35, 87) , 1796.0 ),
( (36, 87) , 1386.0 ),
( (37, 87) , 1387.0 ),
( (48, 87) , 1 ),
( (64, 87) , 690.0 ),
( (65, 87) , 1131.0 ),
( (68, 87) , 984.0 ),
( (36, 88) , 1387.0 ),
( (37, 88) , 1388.0 ),
( (38, 88) , 1389.0 ),
( (59, 88) , 694.0 ),
( (17, 89) , 1736.0 ),
( (26, 89) , 2891.0 ),
( (34, 89) , 1252.0 ),
( (37, 89) , 2270.0 ),
( (42, 89) , 1902.0 ),
( (34, 90) , 691.0 ),
( (35, 90) , 1571.0 ),
( (36, 90) , 2001.0 ),
( (37, 90) , 2002.0 ),
( (43, 90) , 1 ),
( (53, 90) , 1796.0 ),
( (28, 91) , 2123.0 ),
( (33, 91) , 2 ),
( (35, 91) , 1162.0 ),
( (40, 91) , 1840.0 ),
( (53, 91) , 1797.0 ),
( (30, 92) , 2630.0 ),
( (35, 92) , 1163.0 ),
( (36, 92) , 1164.0 ),
( (38, 92) , 1165.0 ),
( (43, 92) , 597.0 ),
( (44, 92) , 394.0 ),
( (51, 92) , 1079.0 ),
( (22, 93) , 1246.0 ),
( (35, 93) , 1551.0 ),
( (36, 93) , 1992.0 ),
( (37, 93) , 2162.0 ),
( (38, 93) , 2163.0 ),
( (40, 93) , 1841.0 ),
( (41, 93) , 1842.0 ),
( (42, 93) , 1843.0 ),
( (44, 93) , 1026.0 ),
( (24, 94) , 1249.0 ),
( (25, 94) , 748.0 ),
( (30, 94) , 2004.0 ),
( (37, 94) , 2847.0 ),
( (38, 94) , 2847.0 ),
( (39, 94) , 2848.0 ),
( (48, 94) , 521.0 ),
( (21, 95) , 1460.0 ),
( (24, 95) , 1249.0 ),
( (36, 95) , 1 ),
( (37, 95) , 2848.0 ),
( (38, 95) , 1597.0 ),
( (40, 95) , 2352.0 ),
( (41, 95) , 2353.0 ),
( (46, 95) , 492.0 ),
( (48, 95) , 521.0 ),
( (52, 95) , 1 ),
( (30, 96) , 1 ),
( (36, 96) , 2 ),
( (41, 96) , 2354.0 ),
( (42, 96) , 2355.0 ),
( (43, 96) , 2356.0 ),
( (26, 97) , 282.0 ),
( (42, 97) , 2356.0 ),
( (43, 97) , 2357.0 ),
( (46, 97) , 765.0 ),
( (27, 98) , 283.0 ),
( (42, 98) , 2357.0 ),
( (43, 98) , 2358.0 ),
( (22, 99) , 2 ),
( (24, 99) , 3 ),
( (31, 99) , 1 ),
( (46, 99) , 766.0 ),
( (19, 100) , 881.0 ),
( (21, 100) , 716.0 ),
( (46, 100) , 767.0 ),
( (20, 101) , 1 ),
( (37, 101) , 700.0 ),
( (36, 102) , 2663.0 ),
( (27, 103) , 1073.0 ),
( (16, 105) , 3356.0 ),
( (21, 107) , 4992.0 )]