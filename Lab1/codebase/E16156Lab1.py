# This code is adopted from github.com/aimacode/aima-python repository
from statistics import mean
import random
import copy
import collections                                         
collections.Callable = collections.abc.Callable  

class Thing(object):

    """This represents any physical entity that can appear in an Environment.
    Each thing can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return f"<{getattr(self, '__name__', self.__class__.__name__)}>"

    def is_alive(self):
        """Things that are 'alive' should return true."""
        return hasattr(self, "alive") and self.alive

    def show_state(self):
        """Display the agent's internal state.  Subclasses should be overridden."""


class Agent(Thing):
    """Note that 'program' is a slot, not a method.  If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts.  An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slot, .performance, which is a number giving
    the performance measure of the agent in its environment."""

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None:
            def program(percept):
                return eval(input(f"Percept={percept}; action? "))
        assert isinstance(program, collections.Callable)
        self.program = program

    def can_grab(self, thing):
        """Returns True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False


def TableDrivenAgentProgram(table):
    """This agent selects an action based on the percept sequence.
    It is practical only for tiny domains.
    To customize it, provide as table a dictionary of all
    {percept_sequence:action} pairs."""
    percepts = []

    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percepts))
        return action
    return program


def RandomAgentProgram(actions):
    """An agent that chooses an action at random, ignoring all percepts."""
    return lambda percept: random.choice(actions)


def SimpleReflexAgentProgram(rules, interpret_input):
    """This agent takes action based solely on the percept."""
    def program(percept):
        state = interpret_input(percept)
        rule = rule_match(state, rules)
        action = rule.action
        return action
    return program


def ModelBasedReflexAgentProgram(rules, update_state):
    """This agent takes action based on the percept and state."""
    def program(percept):
        program.state = update_state(program.state, program.action, percept)
        rule = rule_match(program.state, rules)
        action = rule.action
        return action
    program.state = program.action = None
    return program


def rule_match(state, rules):
    """Find the first rule that matches state."""
    for rule in rules:
        if rule.matches(state):
            return rule


# Define three locations in the Vacuum world
loc_A, loc_B, loc_C = (0, 0), (1, 0), (2, 0)


def RandomVacuumAgent():
    #return Agent("""Choose one of the actions from the vacuum environment randomly.""")
    return lambda percept: random.choice(['Right', 'Left', 'Suck', 'NoOp'])


def TableDrivenVacuumAgent():
    table = {((loc_A, "Clean"),): "Right",
             ((loc_A, "Dirty"),): "Suck",
             ((loc_B, "Clean"),): "Right",
             ((loc_B, "Clean"),): "Left",
             ((loc_B, "Dirty"),): "Suck",
             # ...
             ((loc_A, "Clean"), (loc_A, "Clean")): "Right",
             ((loc_A, "Clean"), (loc_A, "Dirty")): "Suck",
             # ...
             ((loc_A, "Clean"), (loc_A, "Clean"), (loc_A, "Clean")): "Right",
             ((loc_A, "Clean"), (loc_A, "Clean"), (loc_A, "Dirty")): "Suck",
             # ...
             }
    return Agent(TableDrivenAgentProgram(table))


def ReflexVacuumAgent():
    """A simple reflex agent for the three-state vacuum environment."""
    def program(percept):
        location, status = percept
        if status == "Dirty":
            print(percept, "Suck")
            return "Suck"
        elif location == loc_A:
            print(percept, "Right")
            return "Right"
        elif location == loc_C:
            print(percept, "Left")
            return "Left"
        elif location == loc_B:
            print(percept, "Left")
            return "Left"
        # ...
        """Augment to simulate the three location problem environment (Figure 1)"""
    return Agent(program)


def AllSeeingReflexVaccumAgent():
    """More powerful sensors"""
    def program(percept):
        # Now reveals all locations and their statuses to agent(s)
        location, status = percept
        if status[loc_A] == status[loc_B] == status[loc_C] == "Clean":
            print(percept, "NoOp")
            return "NoOp"
        elif status[location] == "Dirty":
            print(percept, "Suck")
            return "Suck"
        elif location == loc_A and (status[loc_B] == "Dirty" or status[loc_C] == "Dirty"):
            print(percept, "Right")
            return "Right"
        elif location == loc_B and status[loc_A] == "Dirty":
            print(percept, "Left")
            return "Left"
        elif location == loc_B and status[loc_C] == "Dirty":
            print(percept, "Right")
            return "Right"
        # ...
    return Agent(program)


def BasicVaccumAgent():
    # Cannot see location, cannot store status, without randomizer
    def program(percept):
        if percept == "Dirty":
            print(percept, "Suck")
            return "Suck"
        else:
            # Decide random direction without randomizer inclusion.
            print(percept, "Right")
            return "Right"
    return Agent(program)


def SemiBasicVaccumAgent():
    # Cannot see location, cannot store status, with randomizer
    def program(percept):
        if percept == "Dirty":
            print(percept, "Suck")
            return "Suck"
        else:
            choice = random.randint(0, 1)
            if choice == 0:
                print(percept, "Left")
                return "Left"
            else:
                print(percept, "Right")
                return "Right"
    return Agent(program)


def ModelBasedVacuumAgent():
    """An agent that keeps track of what locations are clean or dirty."""
    model = {loc_A: None, loc_B: None, loc_C: None}


    def program(percept):
        """Same as ReflexVacuumAgent, except if everything is clean, do NoOp."""
        # Augmented to include the 3-room format
        location, status = percept
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == model[loc_C] == "Clean":
            print(percept, "NoOp")
            return "NoOp"
        elif status == "Dirty":
            print(percept, "Suck")
            return "Suck"
        elif location == loc_A and status == "Clean":
            print(percept, "Right")
            return "Right"
        elif location == loc_B and status == "Clean":
            if model[loc_A] == "Clean":
                print(percept, "Right")
                return "Right"
            elif model[loc_C] == "Clean":
                print(percept, "Left")
                return "Left"
            else:
                position = random.randint(0, 1)
                if position == 0:
                    print(percept, "Left")
                    return "Left"
                elif position == 1:
                    print(percept, "Right")
                    return "Right"
        elif location == loc_C and status == "Clean":
            print(percept, "Left")
            return "Left"
        elif location == loc_A and (model[loc_B] or model[loc_C] == "Dirty"):
            print(percept, "Right")
            return "Right"
        elif location == loc_B and (model[loc_A] or model[loc_C] == "Dirty"):
            if model[loc_A] == "Dirty":
                print(percept, "Left")
                return "Left"
            elif model[loc_C] == "Dirty":
                print(percept, "Right")
                return "Right"
        elif location == loc_C and (model[loc_A] or model[loc_B] == "Dirty"):
            print(percept, "Left")
            return "Left"
    return Agent(program)


class Dirt(Thing):
    pass


class Environment(object):
    """Abstract class representing an Environment.  'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point."""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def exogenous_change(self):
        """If there is spontaneous change in the world, override this."""
        pass

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do.  If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        "Run the Environment for given number of time steps."
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        "Return all things exactly at a given location."
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this."""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        assert thing not in self.things, "Don't add the same thing twice"
        thing.location = location if location is not None else self.default_location(
            thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print(f"  Thing to be removed: {thing} at {thing.location}")
            print(f"  from list: {[(thing, thing.location) for thing in self.things]}")
        if thing in self.agents:
            self.agents.remove(thing)


class TrivialVacuumEnvironment(Environment):
    """This environment has three locations, A, B, and C. Each can be Dirty
    or Clean.  The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self):
        super(TrivialVacuumEnvironment, self).__init__()
        self.status = {loc_A: random.choice(["Clean", "Dirty"]),
                       loc_B: random.choice(["Clean", "Dirty"]),
                       loc_C: random.choice(["Clean", "Dirty"])}
        print("The environment for this attempt is:")
        print(self.status)

    def thing_classes(self):
        return [Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        "Returns the agent's location, and the location status (Dirty/Clean)."
        return (agent.location, self.status[agent.location])

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == "Right":
            if agent.location == loc_B:
                agent.location = loc_C
            elif agent.location == loc_A:
                agent.location = loc_B
            agent.performance -= 1
        elif action == "Left":
            if agent.location == loc_B:
                agent.location = loc_A
            elif agent.location == loc_C:
                agent.location = loc_B
            agent.performance -= 1
        elif action == "Suck":
            if self.status[agent.location] == "Dirty":
                agent.performance += 10
            self.status[agent.location] = "Clean"
        for floorStatus in self.status:
            if floorStatus == "Dirty":
                agent.performance -= 2

    def default_location(self, thing):
        "Agents start in a location at random."
        return random.choice([loc_A, loc_B, loc_C])


class AllSeeingTrivialVaccumEnvironment(TrivialVacuumEnvironment):
    # Same as TrivialVaccumEnviornment, except gives all locations as well as statuses

    def percept(self, agent):
        "Returns the agent's location, and the location status (Dirty/Clean)."
        return (agent.location, self.status)


class BasicVaccumEnvironment(TrivialVacuumEnvironment):
    # Same as TrivialVaccumEnvironment; agent knows status yet no location

    def percept(self, agent):
        return (self.status[agent.location])


def run_times(EnvFactory, AgentFactory, steps, runs):
    for i in range(runs):
        env = EnvFactory()
        agent = AgentFactory()
        env.add_thing(agent)
        env.run(steps)
        score = str(agent.performance)
        print(score)


"""Test Random Agent Program"""
"""Test Simple Reflex Agent Program"""


# --------------------- Random Vacuum Agent -------------------------------------------------------------------------------------


# Initialize the three-state environment
trivial_vacuum_env = TrivialVacuumEnvironment()

# Create the random agent
random_agent = Agent(RandomVacuumAgent())

# Add agent to the environment
trivial_vacuum_env.add_thing(random_agent)

# Running the environment
trivial_vacuum_env.run()

# Check the current state of the environment
print("State of the Environment: {}.".format(trivial_vacuum_env.status))


#--------------------- Reflex Vacuum Agent ---------------------------------------------------------------------------------------------

# Create a simple reflex agent the two-state environment
simple_reflex_agent = ReflexVacuumAgent()

# Initialize the three-state environment
trivial_vacuum_env = TrivialVacuumEnvironment()

trivial_vacuum_env.add_thing(simple_reflex_agent)

# Run the environment
trivial_vacuum_env.step()

# Check the current state of the environment
print("State of the Environment: {}.".format(trivial_vacuum_env.status))