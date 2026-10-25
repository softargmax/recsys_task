# Learned features, K = 64_s13

 0. count: org_skip + ratio over 1.00 same artist, kernel 1.00 decay 6h
 1. count: rec_lp + ratio + novel_lp over 1.00 cf-similar tracks, kernel 1.00 current session
 2. count: rec_lp + rec_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 current session
 3. count: rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last 3 tracks
 4. count: ratio over 1.00 same artist, kernel 1.00 last event, decay 30d
 5. count: rec_lp + rec_skip + org_lp + novel_skip over 1.00 same track, kernel 1.00 all history
 6. count: nothing over 1.00 same album, kernel 1.00 decay 6h
 7. count: rec_lp + org_lp + org_skip + ratio + novel_lp over 1.00 same album, kernel 1.00 decay 1h
 8. count: rec_lp + ratio + novel_lp over 1.00 same track, kernel 1.00 all history
 9. count: rec_skip + org_lp over 1.00 same artist, kernel 1.00 current session
10. count: novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 90d
11. count: rec_skip + org_skip over 1.00 same track, kernel 1.00 last 10 tracks
12. count: rec_lp + novel_lp over 1.00 same artist, kernel 1.00 decay 90d
13. count: rec_lp + ratio over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
14. count: rec_skip + org_skip + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 3d
15. count: rec_skip over 1.00 same artist, kernel 1.00 last 10 tracks
16. count: novel_lp over 1.00 same artist, kernel 1.00 current session
17. count: nothing over 1.00 same album, kernel 1.00 decay 3d
18. count: rec_lp + rec_skip + org_skip + novel_skip over 1.00 same artist, kernel 1.00 last event, decay 1d
19. count: org_lp + org_skip + novel_lp + novel_skip over 1.00 cf-similar tracks, kernel 1.00 last track
20. count: rec_lp + rec_skip + org_skip + novel_lp + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 3d
21. count: ratio + novel_skip over 1.00 same track, kernel 1.00 decay 7d
22. count: rec_lp + ratio over 1.00 same track, kernel 1.00 last 10 tracks
23. count: rec_lp + ratio over 1.00 same track, kernel 1.00 decay 1d
24. count: rec_skip + org_lp + org_skip + ratio over 1.00 same track, kernel 1.00 decay 1h
25. count: rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last event, decay 1d
26. count: rec_lp + rec_skip + org_skip + novel_lp over 1.00 any track, kernel 1.00 decay 1h
27. count: rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip over 1.00 same artist, kernel 1.00 decay 30d
28. count: rec_lp + org_lp + org_skip + ratio over 1.00 cf-similar tracks, kernel 1.00 decay 3d
29. count: org_lp over 1.00 cf-similar tracks, kernel 1.00 last track
30. count: rec_skip + org_lp + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
31. count: rec_lp + rec_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 7d
32. rate: (org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 decay 90d
33. rate: (rec_lp + rec_skip + org_skip + ratio) / (rec_lp + rec_skip + org_skip + ratio + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
34. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last track
35. rate: (rec_lp + rec_skip + org_lp + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 0.98 last track
36. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
37. rate: (rec_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
38. rate: (rec_lp + rec_skip + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
39. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
40. rate: (org_skip + ratio) / (rec_lp + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 10 tracks
41. rate: (rec_skip + org_lp + org_skip + ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same album, kernel 1.00 decay 6h
42. rate: (org_lp + org_skip) / (rec_skip + org_lp + org_skip + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
43. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
44. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 0.99 cf-similar tracks, kernel 1.00 last event, decay 30d
45. rate: (rec_skip + org_skip) / (rec_skip + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 current session
46. rate: (org_skip + novel_lp) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 6h
47. rate: (rec_skip + org_skip + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 30d
48. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 current session
49. rate: (rec_lp + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 current session
50. rate: (rec_skip + ratio + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 90d
51. rate: (rec_lp + rec_skip + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
52. rate: (org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 7d
53. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
54. rate: (rec_lp + org_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 same album, kernel 1.00 decay 7d
55. rate: (rec_lp + org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
56. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last track
57. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 90d
58. rate: (ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 90d
59. rate: (rec_lp + org_skip + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
60. rate: (rec_lp) / (rec_lp + rec_skip + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 7d
61. rate: (ratio) / (rec_lp + rec_skip + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
62. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 90d
63. rate: (rec_lp + org_lp + novel_skip) / (rec_lp + org_lp + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
