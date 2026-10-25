# Learned features, K = 32_s13

 0. count: rec_lp + rec_skip + org_lp + org_skip + ratio over 1.00 same artist, kernel 1.00 last 3 tracks
 1. count: rec_lp + ratio + novel_lp over 1.00 cf-similar tracks, kernel 1.00 current session
 2. count: rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last event, decay 1d
 3. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 last 10 tracks
 4. count: rec_skip + ratio over 1.00 same artist, kernel 1.00 last event, decay 30d
 5. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 decay 1h
 6. count: org_lp + org_skip + novel_lp over 1.00 same track, kernel 1.00 last event, decay 1d
 7. count: nothing over 1.00 same album, kernel 1.00 decay 1d
 8. count: rec_lp + rec_skip + org_lp + ratio over 1.00 same track, kernel 1.00 decay 90d
 9. count: org_lp + ratio over 1.00 same artist, kernel 1.00 decay 3d
10. count: rec_lp + ratio + novel_skip over 1.00 any track, kernel 1.00 all history
11. count: rec_lp + rec_skip + org_lp + org_skip + ratio over 1.00 same album, kernel 1.00 all history
12. count: rec_lp + rec_skip + novel_lp over 1.00 same artist, kernel 1.00 decay 30d
13. count: rec_lp + org_lp + ratio over 1.00 cf-similar tracks, kernel 1.00 last event, decay 30d
14. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 cf-similar tracks, kernel 1.00 last event, decay 1d
15. count: rec_lp + rec_skip + ratio + novel_lp over 1.00 same artist, kernel 1.00 all history
16. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 all history
17. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 all history
18. rate: (rec_skip + org_skip + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 90d
19. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
20. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 3 tracks
21. rate: (rec_lp + ratio + novel_lp) / (rec_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
22. rate: (rec_lp + rec_skip + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last 10 tracks
23. rate: (ratio + novel_lp + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 all history
24. rate: (ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 7d
25. rate: (ratio + novel_lp + novel_skip) / (rec_lp + org_lp + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 3d
26. rate: (rec_lp + rec_skip + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
27. rate: (rec_lp) / (rec_lp + rec_skip + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 decay 30d
28. rate: (rec_skip + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 1d
29. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last event, decay 30d
30. rate: (ratio + novel_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
31. rate: (org_lp + ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
