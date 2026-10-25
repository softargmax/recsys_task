# Learned features, K = 32_rich-recency_s7

 0. count: rec_skip + org_lp + org_skip + novel_skip over 1.00 same track, kernel 1.00 last track
 1. count: rec_skip over 1.00 same album, kernel 1.00 all history
 2. count: rec_lp + rec_skip + org_lp + novel_skip over 1.00 same album, kernel 1.00 last 10 tracks
 3. count: rec_skip + org_skip over 1.00 same album, kernel 1.00 last track
 4. count: org_lp + ratio over 1.00 same track, kernel 1.00 all history
 5. count: rec_lp + ratio over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
 6. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 3d
 7. count: rec_skip + org_skip over 1.00 any track, kernel 1.00 last 3 tracks
 8. count: nothing over 1.00 same artist, kernel 1.00 decay 6h
 9. count: rec_lp over 1.00 same track, kernel 1.00 decay 90d
10. count: rec_skip over 1.00 any track, kernel 1.00 last 10 tracks
11. count: nothing over 1.00 same track, kernel 1.00 decay 1h
12. count: rec_lp + ratio + novel_lp over 1.00 any track, kernel 1.00 decay 1d
13. count: rec_lp + ratio over 1.00 same artist, kernel 1.00 decay 7d
14. count: rec_lp + novel_skip over 1.00 same album, kernel 1.00 decay 1d
15. count: rec_skip + novel_lp + novel_skip over 1.00 same artist, kernel 1.00 decay 7d
16. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 1d
17. rate: (rec_skip + org_lp + org_skip + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 1h
18. rate: (org_lp + org_skip) / (rec_skip + org_lp + org_skip + ratio + novel_skip) over 1.00 any track, kernel 1.00 last track
19. rate: (rec_lp + rec_skip + org_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
20. rate: (rec_lp + ratio + novel_lp + novel_skip) / (rec_lp + org_lp + ratio + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 6h
21. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
22. rate: (ratio + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 0.54 any track + 0.24 same track + 0.22 cf-similar tracks, kernel 1.00 decay 90d
23. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
24. rate: (rec_lp + rec_skip + org_lp + ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 1d
25. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same artist, kernel 1.00 last track
26. rate: (rec_lp + org_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
27. rate: (rec_lp + ratio + novel_lp) / (rec_lp + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 last 10 tracks
28. rate: (rec_skip + org_skip + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_skip) over 1.00 same album, kernel 1.00 decay 1d
29. rate: (ratio + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
30. rate: (ratio + novel_skip) / (rec_lp + rec_skip + org_skip + ratio + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
31. rate: (rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 current session
