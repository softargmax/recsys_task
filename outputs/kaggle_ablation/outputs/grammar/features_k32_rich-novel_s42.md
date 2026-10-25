# Learned features, K = 32_rich-novel_s42

 0. count: rec_skip over 1.00 any track, kernel 1.00 decay 90d
 1. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
 2. count: ratio over 1.00 same artist, kernel 1.00 last event, decay 30d
 3. count: rec_lp + rec_skip + org_lp over 1.00 same track, kernel 1.00 decay 1h
 4. count: rec_skip over 1.00 same album, kernel 1.00 decay 3d
 5. count: rec_lp + rec_skip + org_lp + org_skip + ratio over 1.00 same artist, kernel 1.00 last 3 tracks
 6. count: rec_lp + rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 current session
 7. count: rec_lp + ratio over 1.00 any track, kernel 1.00 decay 90d
 8. count: rec_lp + org_lp + ratio over 1.00 same track, kernel 1.00 decay 30d
 9. count: org_skip + ratio over 1.00 any track, kernel 1.00 last 3 tracks
10. count: rec_lp over 1.00 same album, kernel 1.00 decay 30d
11. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 decay 7d
12. count: rec_lp + ratio over 1.00 same track, kernel 1.00 decay 7d
13. count: rec_lp + ratio over 1.00 same track, kernel 1.00 current session
14. count: nothing over 1.00 same track, kernel 1.00 current session
15. count: rec_skip over 1.00 same track, kernel 1.00 last track
16. rate: (org_lp + org_skip) / (rec_lp + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 decay 1h
17. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 same track, kernel 1.00 last event, decay 30d
18. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
19. rate: (rec_lp + rec_skip + org_skip + ratio) / (rec_lp + rec_skip + org_skip + ratio) over 1.00 any track, kernel 1.00 last 10 tracks
20. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio) over 1.00 any track, kernel 1.00 decay 30d
21. rate: (rec_lp + ratio) / (rec_lp + org_lp + ratio) over 1.00 any track, kernel 1.00 last 10 tracks
22. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + ratio) over 1.00 any track, kernel 1.00 decay 7d
23. rate: (rec_skip + org_lp + org_skip + ratio) / (rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last event, decay 30d
24. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
25. rate: (rec_skip + org_skip) / (rec_skip + org_lp + org_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 1d
26. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
27. rate: (rec_skip + org_lp + org_skip + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
28. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 same track, kernel 1.00 decay 30d
29. rate: (nothing) / (rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 decay 1h
30. rate: (rec_lp + rec_skip + org_skip + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 same album, kernel 1.00 current session
31. rate: (rec_skip + org_skip + ratio) / (rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last event, decay 1d
