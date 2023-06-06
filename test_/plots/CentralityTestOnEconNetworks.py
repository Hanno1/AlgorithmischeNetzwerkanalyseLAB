def compute_kendall(centr1, centr2):
    # https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient
    # compute pairs
    pairs = []
    for key in centr1:
        pairs.append((centr1[key], centr2[key]))

    # compare pairs
    number_discord = 0
    for i in range(len(pairs) - 1):
        for j in range(i+1, len(pairs)):
            pair1 = pairs[i]
            pair2 = pairs[j]

            if not ((pair1[0] <= pair2[0] and pair1[1] <= pair2[1]) or
                    (pair1[0] >= pair2[0] and pair1[1] >= pair2[1])):
                number_discord += 1
    return 1 - ((4 * number_discord) / (len(pairs) * (len(pairs)-1)))
