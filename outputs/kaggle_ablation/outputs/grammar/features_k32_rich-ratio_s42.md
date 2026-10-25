# Learned features, K = 32_rich-ratio_s42

 0. count: rec_skip over 1.00 any track, kernel 1.00 decay 90d
 1. count: rec_lp + org_lp over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
 2. count: rec_lp + org_lp over 1.00 same artist, kernel 1.00 last event, decay 30d
 3. count: rec_lp + rec_skip over 1.00 same track, kernel 1.00 decay 1h
 4. count: rec_lp over 1.00 same album, kernel 1.00 decay 30d
 5. count: rec_skip + novel_lp over 1.00 any track, kernel 1.00 last 3 tracks
 6. count: rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 current session
 7. count: rec_skip + novel_skip over 1.00 any track, kernel 0.94 decay 90d
 8. count: rec_skip + org_lp + org_skip over 1.00 same track, kernel 1.00 decay 30d
 9. count: novel_lp over 1.00 any track, kernel 1.00 decay 90d
10. count: rec_lp + rec_skip + org_lp + org_skip over 1.00 same album, kernel 1.00 last 10 tracks
11. count: rec_lp + novel_lp over 1.00 cf-similar tracks, kernel 1.00 decay 7d
12. count: rec_skip + org_skip over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
13. count: rec_skip + org_lp + org_skip + novel_lp + novel_skip over 1.00 same track, kernel 1.00 current session
14. count: rec_lp over 1.00 same track, kernel 1.00 decay 1h
15. count: rec_lp + org_lp + org_skip + novel_lp over 1.00 same track, kernel 1.00 last track
16. rate: (nothing) / (rec_skip + org_lp + org_skip + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 all history
17. rate: (novel_lp + novel_skip) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
18. rate: (rec_skip + org_lp + org_skip + novel_lp) / (rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
19. rate: (rec_skip + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
20. rate: (rec_skip + org_skip + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
21. rate: (nothing) / (rec_lp + org_lp + novel_lp) over 1.00 any track, kernel 1.00 last 10 tracks
22. rate: (rec_skip + novel_skip) / (rec_lp + rec_skip + org_lp + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 last 3 tracks
23. rate: (rec_skip + novel_skip) / (rec_skip + org_lp + novel_skip) over 1.00 any track, kernel 1.00 last 10 tracks
24. rate: (org_skip + novel_lp) / (rec_skip + org_skip + novel_lp + novel_skip) over 1.00 cf-similar tracks, kernel 1.00 decay 3d
25. rate: (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 same album, kernel 1.00 decay 1d
26. rate: (rec_lp + novel_lp) / (rec_lp + rec_skip + novel_lp) over 1.00 cf-similar tracks, kernel 1.00 decay 1h
27. rate: (rec_skip + novel_skip) / (rec_lp + rec_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 decay 30d
28. rate: (rec_lp + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + novel_skip) over 1.00 same track, kernel 1.00 decay 30d
29. rate: (org_lp + novel_lp) / (rec_skip + org_lp + novel_lp) over 1.00 same artist, kernel 1.00 decay 1d
30. rate: (rec_lp + org_lp + novel_lp + novel_skip) / (rec_lp + rec_skip + org_lp + org_skip + novel_lp + novel_skip) over 1.00 any track, kernel 1.00 current session
31. rate: (rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip) over 1.00 any track, kernel 1.00 last event, decay 1d
