select
    user_id
  , user_group
from
  internal_user
where 1=1
  and login = (%s)
  and password = (%s)