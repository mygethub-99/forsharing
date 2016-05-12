import logging
#debug=True
import endpoints
from protorpc import remote
from protorpc import messages
from protorpc import message_types
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

from models import User, Game, NewGameForm, Inventory
from models import StringMessage, GameForm, InventoryForm
from utils import get_by_urlsafe, check_winner, check_full
from dict_list import items, craft, commands, defaults, loadInventory

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
#GET_GAME_REQUEST = endpoints.ResourceContainer(
        #urlsafe_game_key=messages.StringField(1),)

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1), email=messages.StringField(2), wins=messages.StringField(3))


#Got to figure out how to pass the command message output.
#MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'



@endpoints.api(name='survive', version='v1')
class SurviveAPI(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      #This is the name that appears in the api
                      name='create_user',
                      http_method='POST') 
   
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        #By adding wins, it added it to the create_user input #api page.
        wins = defaults['wins']
        user = User(name=request.user_name, email=request.email, wins = wins)
        #user.put() sends the user info that is ndb
        user.put()

        for key,val in sorted(craft.items()):
            outmessage =("{} : Can be make with {}".format(key, val))
            return StringMessage(message='User {} created!'.format(
                outmessage))
        #This just returns a message for response at bottom of API
        #screen.
    
    @endpoints.method(message_types.VoidMessage, InventoryForm,
            path='inventory', http_method='GET', name='getInventory')
    def getInventory(self, request):
        """Return user inventory."""
        return self._doInventory()

    def _doInventory(self, save_request=None):
        #flint = 1
        #grass = 2
        #boulder = 5
        #See if you can build an ierated inventory list
        #inven= Inventory(flint = items.get("flint"), grass=items.get("grass"), boulder=items.get("boulder"), hay = items.get("hay"))
        inven = loadInventory()
        print "Dude this is great!"
        print inven
        inven.put()
        return self._copyInvenToForm(inven)
   
    #This is not sending the output to the form.
    def _copyInvenToForm(self,inven):
        pf = InventoryForm()
        for field in pf.all_fields():
            if hasattr(inven, field.name):
                setattr(pf, field.name, getattr(inven, field.name))
        pf.check_initialized()
        return pf
        

    
    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        try:
            game = Game.new_game(user.key)
        except ValueError:
            raise endpoints.BadRequestException('Maximum must be greater '
                                                'than minimum!')

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        #taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing Guess a Number!')

        #if game.attempts_remaining < 1:
            #game.end_game(False)
            #return game.to_form(msg + ' Game over!')
        #else:
            #game.put()
            #return game.to_form(msg)
   

api = endpoints.api_server([SurviveAPI])
