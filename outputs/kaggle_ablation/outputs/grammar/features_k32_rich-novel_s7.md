# Learned features, K = 32_rich-novel_s7

 0. count: nothing over 1.00 same track, kernel 1.00 decay 1h
 1. count: rec_lp + org_lp + ratio over 1.00 any track, kernel 1.00 decay 30d
 2. count: nothing over 1.00 same album, kernel 1.00 decay 6h
 3. count: rec_lp over 1.00 same album, kernel 1.00 current session
 4. count: rec_lp over 1.00 same track, kernel 1.00 decay 90d
 5. count: rec_skip + org_lp + org_skip over 1.00 cf-similar tracks, kernel 1.00 decay 30d
 6. count: rec_lp + rec_skip + org_lp + org_skip + ratio over 1.00 same album, kernel 1.00 last 3 tracks
 7. count: rec_lp + org_skip + ratio over 1.00 any track, kernel 1.00 current session
 8. count: nothing over 1.00 same track, kernel 1.00 decay 1d
 9. count: rec_skip over 1.00 same track, kernel 1.00 decay 90d
10. count: rec_lp over 1.00 any track, kernel 1.00 decay 7d
11. count: rec_lp + ratio over 1.00 same track, kernel 1.00 all history
12. count: rec_skip + org_skip + ratio over 1.00 any track, kernel 1.00 last event, decay 30d
13. count: rec_lp + ratio over 1.00 same artist, kernel 1.00 decay 1d
14. count: ratio over 1.00 cf-similar tracks, kernel 1.00 decay 30d
15. count: rec_lp + rec_skip over 1.00 cf-similar tracks, kernel 1.00 decay 90d
16. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + ratio) over 1.00 same artist, kernel 1.00 decay 30d
17. rate: (rec_lp + rec_skip + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 same artist, kernel 1.00 decay 3d
18. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 90d
19. rate: (rec_lp + ratio) / (rec_lp + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 10 tracks
20. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 3 tracks
21. rate: (org_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last track
22. rate: (rec_lp + rec_skip + org_lp + org_skip) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last track
23. rate: (ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 0.91 cf-similar tracks, kernel 1.00 decay 1h
24. rate: (rec_lp + rec_skip + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 same track, kernel 1.00 decay 1d
25. rate: (rec_lp + rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 same track, kernel 1.00 decay 90d
26. rate: (rec_lp + rec_skip) / (rec_lp + rec_skip + org_skip) over 1.00 any track, kernel 1.00 all history
27. rate: (rec_lp + ratio) / (rec_lp + rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 decay 30d
28. rate: (ratio) / (rec_lp + org_lp + org_skip + ratio) over 1.00 any track, kernel 1.00 last 10 tracks
29. rate: (rec_lp + rec_skip) / (rec_lp + rec_skip + ratio) over 1.00 any track, kernel 1.00 last 10 tracks
30. rate: (rec_skip + org_lp) / (rec_lp + rec_skip + org_lp + ratio) over 1.00 any track, kernel 1.00 all history
31. rate: (rec_skip) / (rec_skip + org_lp + org_skip + ratio) over 1.00 cf-similar tracks, kernel 1.00 last 3 tracks
