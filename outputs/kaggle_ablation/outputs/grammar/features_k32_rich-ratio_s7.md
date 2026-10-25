# Learned features, K = 32_rich-ratio_s7

 0. count: rec_lp + org_lp + org_skip + novel_lp over 1.00 same track, kernel 1.00 last track
 1. count: rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 1h
 2. count: rec_lp over 1.00 same artist, kernel 1.00 decay 7d
 3. count: rec_skip + org_lp + org_skip over 1.00 any track, kernel 1.00 last 3 tracks
 4. count: novel_lp over 1.00 any track, kernel 1.00 decay 90d
 5. count: rec_skip + novel_skip over 1.00 cf-similar tracks, kernel 1.00 decay 30d
 6. count: rec_lp + org_lp over 1.00 same album, kernel 1.00 last 3 tracks
 7. count: rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 current session
 8. count: rec_lp + novel_lp over 1.00 same artist, kernel 1.00 decay 3d
 9. count: rec_lp + novel_lp over 1.00 same artist, kernel 1.00 decay 90d
10. count: rec_lp + rec_skip + novel_lp + novel_skip over 1.00 any track, kernel 1.00 last 10 tracks
11. count: rec_lp + rec_skip + org_skip over 1.00 same track, kernel 1.00 last 10 tracks
12. count: rec_skip + novel_skip over 1.00 any track, kernel 1.00 last event, decay 30d
13. count: rec_skip over 1.00 same artist, kernel 1.00 decay 1d
14. count: nothing over 1.00 same album, kernel 1.00 last 10 tracks
15. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 90d
16. rate: (rec_lp + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
17. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 3d
18. rate: (rec_skip + novel_skip) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
19. rate: (rec_skip + novel_skip) / (rec_lp + rec_skip + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 7d
20. rate: (rec_skip + novel_lp) / (rec_lp + rec_skip + org_lp + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
21. rate: (org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + novel_skip) over 1.00 any track, kernel 1.00 last track
22. rate: (rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_skip) over 1.00 any track, kernel 1.00 last track
23. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + novel_lp) over 1.00 any track, kernel 1.00 decay 1h
24. rate: (rec_skip + org_lp + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 1d
25. rate: (rec_skip + novel_skip) / (rec_lp + rec_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 90d
26. rate: (novel_skip) / (rec_lp + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
27. rate: (rec_skip + org_lp + org_skip) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
28. rate: (rec_lp + novel_lp) / (rec_lp + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 last 10 tracks
29. rate: (rec_lp + org_lp + novel_lp) / (rec_lp + rec_skip + org_lp + novel_lp) over 1.00 same track, kernel 1.00 all history
30. rate: (rec_lp + org_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
31. rate: (rec_skip) / (rec_lp + rec_skip + org_lp + novel_lp) over 1.00 any track, kernel 1.00 last 3 tracks
