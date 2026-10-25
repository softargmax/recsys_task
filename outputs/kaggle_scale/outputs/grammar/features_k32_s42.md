# Learned features, K = 32_s42

 0. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 decay 30d
 1. count: rec_lp + org_skip over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
 2. count: rec_lp + ratio over 1.00 cf-similar tracks, kernel 1.00 last event, decay 30d
 3. count: rec_lp over 1.00 same track, kernel 1.00 decay 1h
 4. count: rec_skip + org_lp over 1.00 same album, kernel 1.00 decay 3d
 5. count: rec_skip + org_skip + ratio over 0.99 any track, kernel 1.00 last 3 tracks
 6. count: rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 decay 1h
 7. count: novel_lp over 1.00 any track, kernel 1.00 decay 7d
 8. count: ratio over 1.00 same track, kernel 1.00 decay 30d
 9. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 last 10 tracks
10. count: rec_lp over 1.00 same album, kernel 1.00 decay 1d
11. count: nothing over 1.00 same artist, kernel 1.00 decay 1h
12. count: rec_lp + rec_skip + org_skip + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 90d
13. count: ratio over 1.00 same track, kernel 1.00 current session
14. count: rec_lp + rec_skip over 1.00 same track, kernel 1.00 current session
15. count: rec_skip + org_lp + org_skip + ratio over 1.00 any track, kernel 1.00 last track
16. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
17. rate: (rec_skip + ratio + novel_lp + novel_skip) / (rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
18. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 current session
19. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
20. rate: (ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 all history
21. rate: (rec_lp + ratio + novel_lp) / (rec_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
22. rate: (rec_lp + rec_skip + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + ratio + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
23. rate: (nothing) / (org_skip + novel_skip) over 1.00 same track, kernel 1.00 last event, decay 30d
24. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
25. rate: (ratio + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 90d
26. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
27. rate: (rec_skip + org_skip + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 30d
28. rate: (rec_skip + org_lp + org_skip + novel_lp) / (rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
29. rate: (ratio + novel_lp) / (rec_lp + org_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 30d
30. rate: (rec_lp + rec_skip + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 current session
31. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
