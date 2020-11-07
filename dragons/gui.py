import http.server
import cgi
import socketserver
import socket
import distutils.core
import urllib.request
import os
import shutil
import zipfile
import threading
from time import sleep
import json
import importlib

import dragons
import utils
import state

VERSION = 1.2
ASSETS_DIR = "assets/"
CHARACTERS_DIR = "characters/"
STRATEGY_SECONDS = 3

CHARACTER_ASSETS = {
    'Worker': ASSETS_DIR + CHARACTERS_DIR + "harvester_dragon.png",
    'Thrower': ASSETS_DIR + CHARACTERS_DIR + "thrower_dragon.png",
    'Long': ASSETS_DIR + CHARACTERS_DIR + "long_thrower_dragon.png",
    'Short': ASSETS_DIR + CHARACTERS_DIR + "short_thrower_dragon.png",
    'Harvester': ASSETS_DIR + CHARACTERS_DIR + "harvester_dragon.png",
    'Fire': ASSETS_DIR + CHARACTERS_DIR + "fire_dragon.png",
    'Bodyguard': ASSETS_DIR + CHARACTERS_DIR + "bodyguard_dragon.png",
    'Hungry': ASSETS_DIR + CHARACTERS_DIR + "hungry_dragon.png",
    'Slow': ASSETS_DIR + CHARACTERS_DIR + "slow_thrower_dragon.png",
    'Scary': ASSETS_DIR + CHARACTERS_DIR + "scary_thrower_dragon.png",
    'Laser': ASSETS_DIR + CHARACTERS_DIR + "laser_dragon.png",
    'Ninja': ASSETS_DIR + CHARACTERS_DIR + "ninja_dragon.png",
    'Earth': ASSETS_DIR + CHARACTERS_DIR + "earth_dragon.png",
    'Scuba': ASSETS_DIR + CHARACTERS_DIR + "scuba_dragon.png",
    'King': ASSETS_DIR + CHARACTERS_DIR + "king_dragon.png",
    'Tank': ASSETS_DIR + CHARACTERS_DIR + "tank_dragon.png",
    'Terminator': ASSETS_DIR + CHARACTERS_DIR + "Robot_4.png",
    'Boss': ASSETS_DIR + CHARACTERS_DIR + "Robot_5.png",
    'FastTerminator': ASSETS_DIR + CHARACTERS_DIR + "Robot_2.png",
    'Mariatron': ASSETS_DIR + CHARACTERS_DIR + "Robot_3.png",
    'NinjaTerminator': ASSETS_DIR + CHARACTERS_DIR + "Robot_1.png",
    'Remover': ASSETS_DIR + CHARACTERS_DIR + "remove.png",
}


class GUI:
    """Browser based GUI that communicates with Python game engine"""

    def __init__(self):
        self.active = True
        self.cleanState()

    def cleanState(self):
        self.initialized = False
        self.state = state.State()
        self.gameOver = False
        self.colony = None
        self.currentTerminatorId = 0
        self.currentCharacterId = 0
        self.characters = []
        self.terminators = []
        self.deadTerminators = []
        self.deadCharacters = []
        self.characterToId = {}
        self.terminatorToId = {}
        self.terminatorLocations = {}

    def makeHooks(self):
        dragons.Dragon.death_callback = dead_character

    def newGameThread(self):
        print("Trying to start new game")
        self.cleanState()  # resets GUI state
        importlib.reload(dragons)  # resets dragons, e.g. with newly implemented Dragons
        self.makeHooks()

        self.winner = dragons.start_with_strategy(gui.args, gui.strategy)
        self.gameOver = True
        self.saveState("winner", self.winner)
        self.saveState("gameOver", self.gameOver)
        # self.killGUI()
        update()

    def killGUI(self):
        self.active = False

    def startGame(self, data=None):
        threading.Thread(target=self.newGameThread).start()
        print("Game started")

    def exit(self, data=None):
        self.active = False

    def initialize_colony_graphics(self, colony):
        self.colony = colony
        self.dragon_type_selected = -1
        self.saveState("strategyTime", STRATEGY_SECONDS)
        self.saveState("food", self.colony.food)
        self.dragon_types = self.get_dragon_types()
        self._init_places(colony)
        self.saveState("places", self.places)
        # Finally log that we are initialized
        self.initialized = True

    def get_dragon_types(self, noSave=False):
        dragon_types = []
        for name, dragon_type in self.colony.dragon_types.items():
            dragon_types.append({"name": name, "cost": dragon_type.food_cost, "img": self.get_character_img_file(name)})
        # Sort by cost
        dragon_types.sort(key=lambda item: item["cost"])

        if not noSave:
            self.saveState("dragon_types", dragon_types)
        return dragon_types

    def get_character_img_file(self, name):
        return CHARACTER_ASSETS[name]

    def getState(self, data=None):
        """Get our message from JSON"""
        return self.state.getState()

    def saveState(self, key, val):
        """Saves our game object to JSON file"""
        self.state.updateState(key, val)

    def strategy(self, colony):
        """The strategy function is called by dragons.DragonColony each turn"""
        # Have we initialized our graphics yet?
        if not self.initialized:
            # No, so do that now
            self.initialize_colony_graphics(colony)
        elapsed = 0  # Physical time elapsed this turn
        self.saveState("time", int(elapsed))
        while elapsed < STRATEGY_SECONDS:
            self.saveState("time", colony.time)
            self._update_control_panel(colony)
            sleep(0.25)
            elapsed += 0.25

    def get_place_row(self, name):
        return name.split("_")[1]

    def get_place_column(self, name):
        return name.split("_")[2]

    def _init_places(self, colony):
        """Calculate all of our place data"""
        self.places = {}
        self.images = {'DragonKing': dict()}
        rows = 0
        cols = 0
        for name, place in colony.places.items():
            if place.name == 'Skynet':
                continue
            pCol = self.get_place_column(name)
            pRow = self.get_place_row(name)
            if place.exit.name == 'DragonKing':
                rows += 1
            if not pRow in self.places:
                self.places[pRow] = {}
            self.places[pRow][pCol] = {"name": name, "type": "tunnel", "water": 0, "characters": {}}
            if "water" in name:
                self.places[pRow][pCol]["water"] = 1
            self.images[name] = dict()
        # Add the Skynet
        self.places[colony.skynet.name] = {"name": name, "type": "skynet", "water": 0, "characters": {}}
        self.places[colony.skynet.name]["characters"] = []
        for terminator in colony.skynet.terminators:
            self.places[colony.skynet.name]["characters"].append({"id": self.currentTerminatorId, "type": "terminator"})
            self.terminatorToId[terminator] = self.currentTerminatorId
            self.currentTerminatorId += 1
        self.saveState("rows", rows)
        self.saveState("places", self.places)

    def update_food(self):
        self.saveState("food", self.colony.food)

    def _update_control_panel(self, colony):
        """Reflect the game state in the play area."""
        self.update_food()
        old_characters = self.characters[:]
        old_terminators = self.terminators[:]
        self.terminators, self.characters = [], []
        for name, place in colony.places.items():
            if place.name == 'Skynet':
                continue
            pCol = self.get_place_column(name)
            pRow = self.get_place_row(name)
            if place.dragon is not None:
                if self.characterToId[place.dragon] not in self.characters:
                    # Add this dragon to our internal list of characters
                    self.characters.append(self.characterToId[place.dragon])
                # Ok there is a dragon that needs to be drawn here
                self.places[pRow][pCol]["characters"] = {
                    "id": self.characterToId[place.dragon],
                    "type": place.dragon.name,
                    "img": self.get_character_img_file(place.dragon.name)
                }
                # Check if it's a container dragon
                if hasattr(place.dragon, "is_container"):
                    self.places[pRow][pCol]["characters"]["container"] = place.dragon.is_container
                    if place.dragon.is_container and place.dragon.contained_dragon:
                        self.places[pRow][pCol]["characters"]["contains"] = {
                            "type": place.dragon.contained_dragon.name,
                            "img": self.get_character_img_file(place.dragon.contained_dragon.name)
                        }
            else:
                self.places[pRow][pCol]["characters"] = {}
            # Loop through our terminators
            for terminator in place.terminators:
                self.terminatorLocations[self.terminatorToId[terminator]] = name
                if self.terminatorToId[terminator] not in self.terminators:
                    self.terminators.append(self.terminatorToId[terminator])
        # Save our new terminator locations to our game state
        self.saveState("terminatorLocations", self.terminatorLocations)

    def deployDragon(self, data):
        # Check to see if the dragon is a remover. If so we need to remove the dragon in pname
        pname, dragon = data["pname"], data["dragon"]
        if dragon == "Remover":
            existing_dragon = self.colony.places[pname].dragon
            if existing_dragon is not None:
                print("colony.remove_dragon('{0}')".format(pname))
                self.colony.remove_dragon(pname)
            return
        character = None
        try:
            print("colony.deploy_dragon('{0}', '{1}')".format(pname, dragon))
            character = self.colony.deploy_dragon(pname, dragon)
        except Exception as e:
            print(e)
            return {"error": str(e)}
        if not character:
            return {"error": "Unable to deploy dragon"}
        id = self.currentCharacterId
        self.characters.append(id)
        self.characterToId[character] = id
        self.currentCharacterId += 1
        self._update_control_panel(self.colony)
        return {"success": 1, "id": id}


class HttpHandler(http.server.SimpleHTTPRequestHandler):
    # Override the default do_POST method
    def log_message(self, format, *args):
        # I hate this console output so simply do nothing.
        return

    def cgiFieldStorageToDict(self, fieldStorage):
        """ Get a plain dictionary rather than the '.value' system used by the
           cgi module's native fieldStorage class. """
        params = {}
        for key in fieldStorage.keys():
            params[key] = fieldStorage[key].value
        return params

    def do_POST(self):
        path = self.path
        routes = {
            '/ajax/fetch/state': gui.getState,
            '/ajax/start/game': gui.startGame,
            '/ajax/exit': gui.exit,
            '/ajax/deploy/dragon': gui.deployDragon,
        }
        action = routes.get(path)
        if not action:
            # We could not find a valid route
            return
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = self.cgiFieldStorageToDict(form)
        response = action(data)
        if not response:
            response = {'success': 1}
        self.send_response(200)
        if response:
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "https://python-courseware.s3.ap-south-1.amazonaws.com")
            self.end_headers()
            response = json.dumps(response)
            self.wfile.write(response.encode('ascii'))


def dead_character(dragon):
    print('{0} ran out of armor and expired'.format(dragon))
    if dragon in gui.characterToId:
        gui.deadCharacters.append(gui.characterToId[dragon])
        gui.saveState("deadCharacters", gui.deadCharacters)
    elif dragon in gui.terminatorToId:
        gui.deadTerminators.append(gui.terminatorToId[dragon])
        gui.saveState("deadTerminators", gui.deadTerminators)


def update():
    pass


class CustomThreadingTCPServer(socketserver.ThreadingTCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def run(*args):
    # Start webserver
    import socketserver
    import webbrowser
    import sys
    PORT = 8000
    global gui
    gui = GUI()
    gui.args = args
    # Basic HTTP Handler
    # Handler = http.server.SimpleHTTPRequestHandler
    for PORT in range(8000, 8001):
        try:
            httpd = CustomThreadingTCPServer(("", PORT), HttpHandler)
            break
        except:
            pass
    else:
        print("Could not start webserver: port 8000 is taken")
        sys.exit(1)
    print("Web Server started @ localhost:" + str(PORT))

    def start_http():
        while gui.active:
            httpd.handle_request()
        print("Web server terminated")

    threading.Thread(target=start_http).start()
    try:
        webbrowser.open("https://python-courseware.s3.ap-south-1.amazonaws.com/project_assets/gui.html", 2)
    except Exception:
        print("Unable to automatically open web browser.")
        print("Point your browser to https://python-courseware.s3.ap-south-1.amazonaws.com/project_assets/gui.html")


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    run(*args)
