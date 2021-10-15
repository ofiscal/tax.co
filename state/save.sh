mkdir state/$1/          \
      state/$1/users     \
      state/$1/data
cp -r users/u*    state/$1/users
cp -r data/reque* state/$1/data
cp -r reque*      state/$1
