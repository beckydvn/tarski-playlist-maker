import tarski
from tarski.syntax import land
import tarski.fstrips as fs
from tarski.io import fstrips as iofs

# define the language
lang = tarski.language('playlist', theories = ['equality'])

# define the genre type
genre = lang.sort('genre')
# define the genre type
song = lang.sort('song')

# define predicates/fluents (what can be true/false)
# is this song already in the playlist?
in_playlist = lang.predicate('in_playlist', 'song')
# song2 comes after song1? (used to see the final order)
on = lang.predicate('on', 'song', 'song')
# what genre is the song?
has_genre = lang.predicate('has_genre', 'song', 'genre')
# is the playlist empty?
empty = lang.predicate('empty')

# define objects
#songs that could be added
rock_song = lang.constant('rock_song', 'song')
pop_song = lang.constant('pop_song', 'song')
jazz_song = lang.constant('jazz_song', 'song')
classical_song = lang.constant('classical_song', 'song')
classical_song_2 = lang.constant('classical_song_2', 'song')
classical_song_3 = lang.constant('classical_song_3', 'song')
#genres each song can have
rock_genre = lang.constant('rock_genre', 'genre')
pop_genre = lang.constant('pop_genre', 'genre')
country_genre = lang.constant('country_genre', 'genre')
jazz_genre = lang.constant('jazz_genre', 'genre')
classical_genre = lang.constant('classical_genre', 'genre')

# define the problem
problem = tarski.fstrips.create_fstrips_problem(
    domain_name='playlistmaker', problem_name='test', language=lang)

# define the actions
# first, define the general parameters to be used and their types
add = lang.variable('add', 'song')
prev = lang.variable('prev', 'song')
genre1 = lang.variable('genre1', 'genre')
genre2 = lang.variable('genre2', 'genre')

# action to add a song - can add songs in any order, just has to be shuffled
add_song = problem.action('add_song', [add, prev, genre1, genre2], precondition = ~in_playlist(add) & in_playlist(prev) & 
has_genre(add, genre1) & has_genre(prev, genre2) & ~(genre1 == genre2),
effects = [
fs.AddEffect(in_playlist(add)),
fs.AddEffect(on(prev, add))
])

# action to add the FIRST song
add_first_song = problem.action('add_first_song', [add], precondition = empty(),
effects = [
fs.AddEffect(in_playlist(add)),
fs.DelEffect(empty())
])

# simply a test action to test parsing an action with no parameters
empty_test = problem.action(name='empty_test', parameters=[], precondition=empty(), effects=[fs.AddEffect(empty())])

# define the initial situation
init = tarski.model.create(lang)

init.add(in_playlist(rock_song))
init.add(has_genre(rock_song, rock_genre))
init.add(has_genre(pop_song, pop_genre))
init.add(has_genre(jazz_song, jazz_genre))
init.add(has_genre(classical_song, classical_genre))
init.add(has_genre(classical_song_2, classical_genre))
init.add(has_genre(classical_song_3, classical_genre))

problem.init = init

# define the goal
problem.goal = land(in_playlist(pop_song), in_playlist(jazz_song), in_playlist(classical_song), in_playlist(classical_song_2), in_playlist(classical_song_3))

print(problem.init.as_atoms())

#convert to pddl, and then drag it into the online editor

writer = iofs.FstripsWriter(problem)
writer.write("domain.pddl", "problem.pddl")