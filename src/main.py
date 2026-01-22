from masks import get_mask_account, get_mask_card_number
from widget import mask_account_card

print(get_mask_card_number("7000792289606361"))

print(get_mask_account("73654108430135874305"))

print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))