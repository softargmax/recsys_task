# Learned features, K = 32_s2024

 0. count: rec_skip + org_lp + org_skip + novel_lp + novel_skip over 1.00 same artist, kernel 1.00 last track
 1. count: rec_lp + rec_skip + org_skip + ratio over 1.00 same track, kernel 1.00 decay 6h
 2. count: rec_lp + rec_skip + ratio over 1.00 any track, kernel 1.00 decay 1d
 3. count: rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip over 1.00 same album, kernel 1.00 decay 6h
 4. count: rec_lp + rec_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 30d
 5. count: rec_skip + org_skip over 1.00 same track, kernel 1.00 decay 30d
 6. count: rec_skip + novel_lp + novel_skip over 1.00 same artist, kernel 1.00 decay 30d
 7. count: org_lp + org_skip over 1.00 same track, kernel 1.00 decay 7d
 8. count: rec_lp + novel_lp over 1.00 same track, kernel 1.00 decay 3d
 9. count: nothing over 1.00 same album, kernel 1.00 decay 6h
10. count: rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp over 1.00 same track, kernel 0.97 last track
11. count: rec_lp + rec_skip + org_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 6h
12. count: rec_lp + novel_lp over 1.00 any track, kernel 1.00 decay 1d
13. count: rec_lp + rec_skip over 1.00 same artist, kernel 1.00 decay 6h
14. count: rec_lp + rec_skip + org_skip + novel_lp over 1.00 same album, kernel 1.00 last event, decay 1d
15. count: rec_lp + org_skip + novel_lp over 1.00 cf-similar tracks, kernel 1.00 all history
16. rate: (org_lp + ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
17. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
18. rate: (ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
19. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
20. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
21. rate: (rec_skip + org_skip + ratio) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
22. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
23. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
24. rate: (org_lp + org_skip) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 current session
25. rate: (ratio) / (rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 90d
26. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 current session
27. rate: (org_lp + org_skip) / (rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last track
28. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
29. rate: (rec_lp + ratio) / (rec_lp + rec_skip + ratio + novel_lp) over 1.00 same artist, kernel 1.00 decay 7d
30. rate: (rec_skip + org_skip + novel_skip) / (rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 90d
31. rate: (rec_skip + org_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last track
