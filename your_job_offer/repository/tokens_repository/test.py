from models.hh_token import HH_Token
# from repository.tokens_repository.get_hh_token import get_hh_token
from repository.tokens_repository.db_methods import save_hh_token, get_hh_token

save_hh_token(HH_Token(login="test", access_token="11", refresh_token="22"))

hh_token = get_hh_token("test")
print(hh_token)
print(hh_token.access_token)
print(hh_token.refresh_token)