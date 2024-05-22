def comparison(charactertics1, charactertics2):
    matching_count = sum(x==y for x, y in zip(charactertics1, charactertics2))

    if len(charactertics1) > len(charactertics2):
        total_elements = len(charactertics2)
    else:
        total_elements = len(charactertics1)

    percentage_on_matching = (matching_count / total_elements) * 100

    # print(f"Matching Percentage: {percentage_on_matching}")

    return percentage_on_matching