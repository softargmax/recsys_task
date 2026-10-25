# Learned features, K = 32_rich-recency_s42

 0. count: rec_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 decay 90d
 1. count: rec_lp + ratio + novel_lp over 1.00 cf-similar tracks, kernel 1.00 current session
 2. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 7d
 3. count: nothing over 1.00 same track, kernel 1.00 decay 6h
 4. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 all history
 5. count: rec_lp + novel_lp over 1.00 same artist, kernel 1.00 all history
 6. count: nothing over 1.00 same track, kernel 1.00 decay 1d
 7. count: ratio over 1.00 any track, kernel 1.00 current session
 8. count: rec_lp + rec_skip + org_lp + ratio over 1.00 same track, kernel 1.00 decay 90d
 9. count: org_skip + ratio over 1.00 any track, kernel 1.00 last track
10. count: rec_skip + org_lp + org_skip over 1.00 same album, kernel 1.00 last 3 tracks
11. count: rec_lp + org_lp + ratio + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 90d
12. count: rec_lp over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
13. count: rec_lp + rec_skip over 1.00 same track, kernel 1.00 last 10 tracks
14. count: rec_lp + org_skip + ratio + novel_lp over 1.00 same track, kernel 1.00 last 3 tracks
15. count: rec_lp + rec_skip + org_skip + novel_lp over 1.00 any track, kernel 1.00 decay 6h
16. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
17. rate: (novel_lp + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 all history
18. rate: (ratio) / (rec_lp + rec_skip + org_lp + ratio) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
19. rate: (rec_skip + ratio) / (rec_skip + org_lp + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
20. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
21. rate: (rec_lp + ratio + novel_lp) / (rec_lp + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
22. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 same track, kernel 1.00 all history
23. rate: (rec_skip + novel_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
24. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
25. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same album, kernel 1.00 decay 30d
26. rate: (rec_lp + ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 1h
27. rate: (rec_skip + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 90d
28. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 same track, kernel 1.00 decay 3d
29. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 3 tracks
30. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 7d
31. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 1h
