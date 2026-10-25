# Learned features, K = 64_s7

 0. count: rec_lp + rec_skip + novel_lp + novel_skip over 1.00 same artist, kernel 1.00 decay 30d
 1. count: rec_lp + ratio + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 3d
 2. count: rec_skip over 1.00 same album, kernel 1.00 last track
 3. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 decay 7d
 4. count: rec_lp over 1.00 same artist, kernel 1.00 decay 1h
 5. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 last 10 tracks
 6. count: rec_lp + rec_skip over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
 7. count: org_skip + ratio + novel_lp + novel_skip over 1.00 any track, kernel 1.00 last 3 tracks
 8. count: rec_skip + org_skip + novel_skip over 1.00 same artist, kernel 1.00 last 10 tracks
 9. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 7d
10. count: rec_lp + rec_skip + ratio over 1.00 cf-similar tracks, kernel 1.00 last track
11. count: rec_lp + rec_skip + org_lp + novel_lp + novel_skip over 1.00 same track, kernel 1.00 last event, decay 1d
12. count: rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last 10 tracks
13. count: rec_lp + org_lp + ratio + novel_lp over 1.00 same artist, kernel 1.00 last track
14. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
15. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 6h
16. count: rec_lp + ratio over 1.00 same artist, kernel 1.00 decay 7d
17. count: rec_lp + org_lp + ratio + novel_lp over 1.00 same track, kernel 1.00 last track
18. count: rec_lp + rec_skip + org_skip over 1.00 same track, kernel 1.00 last event, decay 30d
19. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 last 3 tracks
20. count: rec_lp + ratio over 1.00 same album, kernel 1.00 last event, decay 1d
21. count: rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp over 1.00 same artist, kernel 1.00 last 3 tracks
22. count: rec_lp + org_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 7d
23. count: nothing over 1.00 same album, kernel 1.00 decay 1d
24. count: rec_lp + ratio + novel_lp over 1.00 same track, kernel 1.00 last 10 tracks
25. count: novel_lp over 1.00 same artist, kernel 1.00 current session
26. count: rec_skip + org_skip + novel_skip over 1.00 any track, kernel 1.00 all history
27. count: nothing over 1.00 same track, kernel 1.00 decay 1h
28. count: rec_lp + ratio + novel_lp over 1.00 same album, kernel 1.00 all history
29. count: rec_lp over 1.00 same album, kernel 1.00 current session
30. count: rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip over 1.00 any track, kernel 1.00 current session
31. count: rec_skip over 1.00 same track, kernel 1.00 last track
32. rate: (rec_skip + org_skip + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 6h
33. rate: (rec_skip + ratio) / (rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last event, decay 30d
34. rate: (ratio + novel_lp) / (rec_lp + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 6h
35. rate: (rec_lp + rec_skip + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 90d
36. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
37. rate: (org_lp + org_skip + novel_skip) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last event, decay 1d
38. rate: (rec_skip + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 6h
39. rate: (rec_skip + org_skip + ratio + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
40. rate: (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 6h
41. rate: (org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same album, kernel 1.00 decay 3d
42. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
43. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
44. rate: (rec_lp + ratio) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
45. rate: (rec_skip + org_lp + org_skip + ratio) / (rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 decay 90d
46. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 30d
47. rate: (rec_skip + org_skip + novel_skip) / (rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 30d
48. rate: (ratio) / (rec_skip + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 decay 90d
49. rate: (rec_lp + org_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 30d
50. rate: (rec_lp + rec_skip + org_lp + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 3d
51. rate: (rec_lp + org_skip + ratio + novel_lp) / (rec_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
52. rate: (rec_lp + org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 0.99 last track
53. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + ratio + novel_skip) over 1.00 same artist, kernel 1.00 decay 30d
54. rate: (rec_lp + rec_skip + novel_skip) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 1d
55. rate: (rec_lp + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 1d
56. rate: (rec_lp + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 current session
57. rate: (rec_skip + org_lp + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last track
58. rate: (org_lp + org_skip + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
59. rate: (org_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
60. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 3d
61. rate: (ratio + novel_skip) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 0.99 cf-similar tracks, kernel 1.00 last event, decay 30d
62. rate: (rec_lp + rec_skip + org_lp + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 3 tracks
63. rate: (org_lp + org_skip + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last track
