# Learned features, K = 64_s42

 0. count: rec_lp + org_skip + ratio + novel_lp over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
 1. count: rec_lp + ratio over 1.00 cf-similar tracks, kernel 1.00 last event, decay 30d
 2. count: rec_skip + novel_skip over 1.00 same artist, kernel 1.00 all history
 3. count: rec_skip + novel_skip over 1.00 same track, kernel 1.00 decay 7d
 4. count: rec_lp + org_skip + novel_lp over 1.00 same album, kernel 1.00 last event, decay 1d
 5. count: rec_lp + ratio + novel_lp over 1.00 any track, kernel 1.00 decay 1d
 6. count: org_lp + org_skip + ratio over 1.00 same track, kernel 1.00 decay 1d
 7. count: org_lp + ratio over 1.00 any track, kernel 1.00 decay 90d
 8. count: rec_lp + ratio over 1.00 same track, kernel 1.00 last event, decay 30d
 9. count: rec_skip + org_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 90d
10. count: rec_lp over 1.00 same album, kernel 1.00 decay 1h
11. count: rec_lp + ratio + novel_lp over 1.00 any track, kernel 1.00 last 10 tracks
12. count: nothing over 1.00 same track, kernel 1.00 decay 7d
13. count: rec_lp + org_lp + org_skip over 1.00 same track, kernel 1.00 last 3 tracks
14. count: rec_lp + org_lp + org_skip + novel_lp over 1.00 same track, kernel 1.00 last track
15. count: org_lp + org_skip + ratio over 1.00 same track, kernel 1.00 last 3 tracks
16. count: rec_lp + novel_lp over 1.00 any track, kernel 1.00 decay 7d
17. count: org_skip + ratio over 1.00 any track, kernel 1.00 current session
18. count: rec_lp + ratio + novel_lp + novel_skip over 1.00 cf-similar tracks, kernel 1.00 all history
19. count: rec_lp + org_lp + org_skip + novel_lp over 1.00 same artist, kernel 1.00 last track
20. count: novel_lp over 1.00 any track, kernel 1.00 decay 30d
21. count: rec_lp + ratio + novel_lp over 1.00 any track, kernel 1.00 current session
22. count: rec_skip + org_lp + novel_skip over 1.00 any track, kernel 1.00 decay 3d
23. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 decay 30d
24. count: rec_lp + rec_skip + org_lp + ratio + novel_lp over 1.00 cf-similar tracks, kernel 0.99 last event, decay 30d
25. count: rec_lp + rec_skip over 1.00 same album, kernel 1.00 last 10 tracks
26. count: rec_lp + rec_skip + org_skip + ratio + novel_skip over 1.00 same album, kernel 1.00 decay 3d
27. count: rec_lp over 1.00 same track, kernel 1.00 current session
28. count: rec_lp + rec_skip + org_skip + novel_lp + novel_skip over 1.00 same track, kernel 1.00 all history
29. count: ratio over 1.00 same artist, kernel 1.00 last event, decay 30d
30. count: novel_lp over 1.00 same album, kernel 1.00 decay 3d
31. count: rec_skip + org_skip + novel_lp over 1.00 any track, kernel 1.00 decay 6h
32. rate: (rec_lp + org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 all history
33. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 30d
34. rate: (rec_skip + org_lp) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
35. rate: (org_lp + org_skip + ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last track
36. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 all history
37. rate: (ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 90d
38. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 3 tracks
39. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
40. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
41. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 7d
42. rate: (ratio) / (rec_lp + rec_skip + org_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
43. rate: (rec_skip + org_lp + org_skip + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last track
44. rate: (rec_lp + org_skip + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 all history
45. rate: (rec_skip + novel_skip) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
46. rate: (ratio) / (rec_skip + org_lp + org_skip + ratio) over 1.00 same track, kernel 1.00 decay 30d
47. rate: (org_skip + ratio) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
48. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 90d
49. rate: (ratio + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 7d
50. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last track
51. rate: (rec_skip + org_lp + org_skip) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
52. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 last 3 tracks
53. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
54. rate: (rec_skip + org_lp + org_skip + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 6h
55. rate: (ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 last event, decay 1d
56. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 3 tracks
57. rate: (rec_lp + rec_skip + novel_skip) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
58. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 current session
59. rate: (org_lp + org_skip + ratio) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 decay 90d
60. rate: (rec_lp + org_skip + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 1h
61. rate: (rec_skip + org_lp + org_skip + ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last track
62. rate: (rec_lp + ratio) / (rec_lp + rec_skip + ratio + novel_skip) over 1.00 same artist, kernel 1.00 decay 30d
63. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 same album, kernel 1.00 decay 30d
