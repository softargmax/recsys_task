# Learned features, K = 32_s101

 0. count: nothing over 1.00 same album, kernel 1.00 last 10 tracks
 1. count: ratio over 1.00 same artist, kernel 1.00 last event, decay 30d
 2. count: rec_lp + rec_skip + org_skip over 1.00 same track, kernel 1.00 last event, decay 30d
 3. count: rec_lp + novel_lp over 1.00 any track, kernel 1.00 decay 7d
 4. count: rec_lp + org_lp + org_skip + ratio + novel_lp over 1.00 any track, kernel 1.00 current session
 5. count: rec_lp + rec_skip + ratio over 1.00 same album, kernel 1.00 last track
 6. count: rec_skip + org_lp + org_skip over 1.00 same album, kernel 1.00 last event, decay 1d
 7. count: org_lp + org_skip over 1.00 same artist, kernel 1.00 last 10 tracks
 8. count: novel_lp over 1.00 any track, kernel 1.00 decay 3d
 9. count: rec_skip + org_skip + novel_lp over 1.00 same track, kernel 1.00 last 10 tracks
10. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
11. count: rec_lp + rec_skip + novel_lp over 1.00 cf-similar tracks, kernel 1.00 current session
12. count: org_skip + ratio over 1.00 same album, kernel 1.00 last event, decay 30d
13. count: rec_lp + rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last 10 tracks
14. count: rec_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 all history
15. count: rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp over 1.00 same album, kernel 1.00 all history
16. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
17. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 7d
18. rate: (rec_lp + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 current session
19. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
20. rate: (rec_lp + ratio + novel_lp) / (rec_lp + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 7d
21. rate: (ratio) / (rec_skip + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 decay 90d
22. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
23. rate: (novel_lp) / (rec_skip + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 7d
24. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 6h
25. rate: (org_skip + ratio) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
26. rate: (rec_lp + rec_skip + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last 10 tracks
27. rate: (ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 all history
28. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
29. rate: (rec_skip + org_skip + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
30. rate: (rec_skip + org_skip + ratio) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
31. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 all history
