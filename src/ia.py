from copy import copy, deepcopy

import state
import MinMax


class IA:
    possible_moves = 3
    states = []

    def __init__(self, color, turn, model):
        self.towers_to_examine = []
        self.color = color
        self.turn = turn
        self.model = model

    def determine_all_towers(self, towers):
        for tower in towers:
            if tower[0].color == self.model.get_color():
                self.towers_to_examine.append(tower)

    def action(self, i, j, towers):
        if not self.model.is_winner():
            decided_state = state.State(self.model, self, 0, 0, 0, True)
            decided_state.towers = self.model.towers
            decided_state.set_hierarchy(0)
            minmax = MinMax.MinMax(self, self.model)
            state_ = minmax.min_max(decided_state, 2)
            if state_ is not None:
                self.model.ref = state_.tower
                self.model.decide_type_of_moving(state_.dx, state_.dy,
                                                 state_.distance, state_.towers, False)

        self.model.check_win()
        return

    def determine_states(self, decided_state):
        num_children = 0
        decided_state_copy = deepcopy(decided_state)

        # First, we determine the towers that we can move at the stage of the node
        # At the beginning, the tage is the bord configuration just after the player played
        self.determine_all_towers(decided_state_copy.towers)

        print(decided_state_copy.towers)
        # We print every tower position that we can MOVE
        print("--------------")
        print("towers :")
        for t in self.towers_to_examine:
            print(t[0].x, t[0].y)
        print("--------------")

        # We only work with the towers that the IA is able to move
        # i.e. the towers with the color black on the pawn at the first position of the tower
        for tower in self.towers_to_examine:
            print("TOWER'S POSITION : ", tower, "COLOR OF THE PLAYER :", tower[0].color)
            # We travel all the game bord to see if the tower is able to move at that point
            for x in range(3):
                for y in range(3):

                    # We copy the original position of the tower
                    ref_tower = deepcopy(tower)

                    # We calculate the distance between this tower and its derivation
                    distance = self.model.distance(ref_tower[0].x, ref_tower[0].y, x, y)

                    # If this tower has enough pawns, we add a son
                    if len(ref_tower) >= distance != - 1:

                        # We print the tower's position and its derivative values
                        print("Tower's position : ", ref_tower[0].x, ref_tower[0].y, " | derivated in dx and dy :",
                              x, y, " | distance :", distance)

                        # We add a child to this state
                        child = state.State(self.model, self, x, y, distance, False)
                        decided_state.add_child(child)
                        child.set_father(decided_state)
                        child.set_hierarchy(child.father.depth + 1)

                        # We move this tower to its derivative position

                        self.model.ref = ref_tower
                        child.towers = self.model.decide_type_of_moving(x, y, distance, decided_state_copy.towers, False)

                        # We change the position
                        child.determine_new_tower()

                        self.model.towers = decided_state_copy.towers
                        for t in child.towers:
                            print("child TOWERS:", t[0].x, t[0].y)
                        # self.states.append(child)

                        num_children += 1
        print("Number of children :", num_children)
        self.towers_to_examine.clear()

    def determine_tower(self, dx, dy):
        for s in self.states:
            if s.dx == dx and s.dy == dy:
                return s.tower
        return []
