import tarski
from tarski.syntax import land

# define the language
lang = tarski.language('playlist', theories = ['equality'])

# define sorts/types - genre is the parent of all genre types
song = lang.sort('song')
genre = lang.sort('genre')
rock = lang.sort('rock', genre)
pop = lang.sort('pop', genre)
country = lang.sort('country', genre)
jazz = lang.sort('jazz', genre)
classical = lang.sort('classical', genre)

# define predicates/fluents (what can be true/false)
#testsss

# is this song already in the playlist?
in_playlist = lang.predicate('in_playlist', 'song')
# song2 comes after song1? (used to see the final order)
on = lang.predicate('on', 'song', 'song')
# what genre is the song?
has_genre = lang.predicate('has_genre', 'song', 'genre')
# is the playlist empty?
empty = lang.predicate('empty')

# define objects
rock1 = lang.constant('rock1', 'song')
pop1 = lang.constant('pop1', 'song')
jazz1 = lang.constant('jazz1', 'song')
classical1 = lang.constant('classical1', 'song')
classical2 = lang.constant('classical2', 'song')
classical3 = lang.constant('classical3', 'song')

# define the problem
problem = tarski.fstrips.create_fstrips_problem(
    domain_name='playlistmaker', problem_name='test', language=lang)

# define the actions
# first, define the general parameters to be used and their types
add = lang.variable('add', 'song')
prev = lang.variable('prev', 'song')
genre1 = lang.variable('genre1', 'genre')
genre2 = lang.variable('genre2', 'genre')

# add song action - can add songs in any order, just has to be shuffled
add_song = problem.action('add song', [add, prev, genre1, genre2], precondition = not in_playlist(add) & in_playlist(prev) & 
has_genre(add, genre1) & has_genre(prev, genre2) & (not (= genre1 genre2)),
effects = [
problem.AddEffect(in_playlist(add)),
problem.AddEffect(on(prev, add))
])

# add FIRST song
add_first_song = problem.action('add song', [add], precondition = empty,
effects = [
problem.AddEffect(in_playlist(add)),
problem.DelEffect(empty)
])

# delete song

# define the initial situation
init = tarski.model.create(lang)

init.add(in_playlist(rock1))
init.add(has_genre(rock1, rock))
init.add(has_genre(pop1, pop))
init.add(has_genre(jazz1, jazz))
init.add(has_genre(classical1, classical))
init.add(has_genre(classical2, classical))
init.add(has_genre(classical3, classical))
problem.init = init

# define the goal
problem.goal = land(in_playlist(pop1), in_playlist(jazz1), in_playlist(classical1), in_playlist(classical2), in_playlist(classical3))

print(problem.init.as_atoms())
