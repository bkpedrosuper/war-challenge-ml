from scripts.objectives import (
    Objective,
    ObjectiveData,
    Conquer,
    ConquerData,
    generate_base_weights,
)
from scripts.army import Army, ArmyData, armydict
from war_challenge_computer_vision.regions.regions import Region, RegionData, Continent
from scripts.state import WorldState, RegionState
import numpy as np
import random
from scipy.optimize import differential_evolution
import math


class Player:
    def __init__(self, army: ArmyData, my_objective: ObjectiveData) -> None:
        self.worldState = WorldState()
        self.army = army
        self.my_objective = my_objective
        self.worldState.set_default_weights(generate_base_weights(self.my_objective))
        self.iteration = self.range_random()
        # self.TerCOntdi
        # generate_base_weights(my_objective.value)

    def update(self, data):
        self.worldState.update(data[0])
        self.worldState.set_default_weights

    def range_random(self):
        pivot = 1.0
        i = 0
        while pivot > random.random():
            pivot *= 0.9
            i += 1
        return i

    def divide_and_conquer(self, data, debug=False):
        self.worldState.update(data[0])
        conquer = []
        flag = 0
        Generate_weights = generate_base_weights(self.my_objective)
        Weights = list(zip(Region, Generate_weights))
        action = ""

        if self.iteration > 0:
            # generate_base_weights(my_objective.value)
            for Search_Ally in self.worldState.getRegionState():
                # print(flag)
                # print(Search_Ally.army.tag,'',self.army.tag)

                if (
                    Search_Ally.army.tag == self.army.tag and Search_Ally.troops > 1
                ):  # Possivel
                    # print(Search_Ally.name)
                    Ally_power: float = 0.0
                    for search_Ally_Ally in self.worldState.getRegionState()[
                        flag
                    ].borders:  # noqa: E501
                        if search_Ally_Ally.army.tag == self.army:
                            # print("Entrou 3")
                            Ally_power += search_Ally_Ally.troops

                    for search_Enemy in self.worldState.getRegionState()[flag].borders:
                        if search_Enemy.troops <= Search_Ally.troops - 2:
                            # print("####Enemy ", search_Enemy.name)
                            if search_Enemy.army.tag != self.army.tag:
                                # print("Entrou 4")
                                Enemy_power: float = 0.0
                                Weight_flag = 0
                                for Enemy in self.worldState.getRegionState()[
                                    search_Enemy.idx
                                ].borders:  # noqa: E501
                                    if Enemy.army.tag == self.army.tag:
                                        Weight_flag += 1
                                        continue
                                    Enemy_power += Enemy.troops
                                    Weight_flag += 1
                                    # print(Enemy_power)
                                fit_value = (Ally_power + Search_Ally.troops) * 0.5 - (
                                    (Enemy_power + search_Enemy.troops) * 0.5
                                ) / Weights[Weight_flag][
                                    1
                                ]  # noqa: E501
                                conquer.append((Search_Ally.name, search_Enemy.name, fit_value))  # type: ignore # noqa: E501
                                # print("Enemy Power ", Enemy_power)
                flag += 1
            if debug is True:
                print(conquer)
            if len(conquer) == 0:
                print("finaliza ataque")
            else:
                best = conquer[0]
                for elemento in conquer:
                    if elemento[2] > best[2]:
                        best = elemento
                self.iteration -= 1
                print(best[0] + " ataca " + best[1], "(fit value = ", best[2], ")")
        else:
            self.iteration = self.range_random()
            print("finaliza ataque")

    def is_mine(self, regionState: RegionState):
        """Verifica se um território é meu"""
        answer = regionState.army.tag == self.army.tag
        return answer
    

    def fortification_and_movimentation(self,regionState:RegionState)->list[RegionState]:
        '''Define a fortificação da vizinhança e retorna os movimentos possiveis'''
        moviments = []
        regionState.neighboorhood_fortification = 0.0
        for border in regionState.borders:  # noqa: E501
            #caso aliado
            if self.is_mine(border):
                # Calcula fortificação
                regionState.neighboorhood_fortification += float(border.troops) / 2
                # Criando possíveis alternativas e restrições
                if regionState.troops > 1:
                    moviments.append(regionState)
            #caso inimigo
            else:
                regionState.neighboorhood_fortification -= border.troops
        return moviments
    
    def decode(self,X,n)->tuple[int,list[int]]:
        n_troops = []
        pivot = n
        '''decode'''
        for x in X:
            aux = math.floor(pivot*x) if pivot >0 else 0
            n_troops.append(aux)
            pivot -= aux
        return pivot, n_troops

    def optimized_move(self,debug=False):
        """Calculo da defesa dos territórios"""
        for regionState in self.worldState.getRegionState():
            if self.is_mine(regionState):
                moviments = self.fortification_and_movimentation(regionState)
                n = regionState.troops-1
                def func(x:list[float],args:tuple[RegionState,int]):
                    regionState,n  = args
                    pivot, n_troops = self.decode(x,n)
                    fit = 0.0
                    # n_troops = []
                    # pivot = n
                    # '''decode'''
                    # for x in X:
                    #     aux = math.floor(pivot*x) if pivot >0 else 0
                    #     n_troops.append(aux)
                    #     pivot -= aux
                    origin_fort = regionState.troops - n + pivot
                    origin_fort = min(origin_fort,3)*2.0 + max(origin_fort-3,0)
                    fit +=  origin_fort + regionState.neighboorhood_fortification
                    for troop,neighboor in zip(n_troops,moviments):
                        destination_fort = neighboor.troops + troop
                        destination_fort = min(destination_fort,3)*2.0 + max(destination_fort-3,0)
                        fit += destination_fort + neighboor.neighboorhood_fortification
                    return fit
                
                print('func(0)=',func([0.0 for _ in range(len(moviments))],(regionState,n)))
                bounds = [(0,1) for _ in range(len(moviments))]
                result = differential_evolution(func,bounds=bounds,args=(regionState,n))
                print('result:',result,type(result))
                pivot,best_troops = self.decode(result.x,n)
                for best_troop, neighboor in zip(best_troops,moviments):
                    if pivot != n:
                        print(regionState.name," -(",str(best_troop),")-> ",neighboor.name)
        print('finaliza movimentação')


    def move(self,debug=False):
        """Calculo da defesa dos territórios"""
        # Buscamos territórios que são nossos aliados
        best_moviment_text = ""
        best_moviments = []
        # Calculo das fortificações e dos movimentos
        if self.iteration > 0:
            neighboorFortification = np.array(
                [0.0 for _ in range(self.worldState.worldLen)]
            )
            for regionPosition, regionState in enumerate(
                self.worldState.getRegionState()
            ):
                if self.is_mine(regionState):
                    fortification = 0.0
                    moviments = []
                    for border in regionState.borders:  # noqa: E501
                        #caso aliado
                        if self.is_mine(border):
                            # Calcula fortificação
                            fortification += float(border.troops) / 2
                            # Criando possíveis alternativas e restrições
                            if regionState.troops > 1:
                                moviments.append(
                                    (regionState, border, (0, regionState.troops))
                                )
                        #caso inimigo
                        else:
                            fortification -= border.troops
                    neighboorFortification[regionPosition] += fortification
                    local_moves = [
                        self.move_fit(
                            movement[0], movement[1], movement[2], neighboorFortification
                        )
                        for movement in moviments
                    ]
                    if len(local_moves) > 0:
                        best_moviment = local_moves[0]
                        for movement in local_moves:
                            if best_moviment[3] > movement[3]:
                                best_moviment = movement
                        best_moviments.append(best_moviment)
                        print('move added:',best_moviment[0].name,best_moviment[2],best_moviment[1].name)

            chosen_movements = sorted(best_moviments, key=lambda x: x[3], reverse=True)
            print('chosen movements:',chosen_movements)
            #chosen_movements = chosen_movements[:self.range_random()]
            for el in chosen_movements:
                if el[2] > 0:
                    print(el[0].name," -(",str(el[2]),")-> ",el[1].name)
            self.iteration -= 1
            print('finaliza movimentação')

        else:
            self.iteration = self.range_random()
            best_moviment_text = "finaliza movimentação"

        print(best_moviment_text)

    def move_fit(
        self,
        stateOrigin: RegionState,
        stateDestination: RegionState,
        troop_range: tuple[int, int],
        fortification: np.ndarray,
    ):
        best_fit = -9999
        best_troop = -1
        print('troop_Range',troop_range)
        for troop in range(*troop_range):
            """Calcula a origem e destino das tropas e respectivos valores pensando mais as 3 primeiras tropas"""
            origin_troops = stateOrigin.troops - troop
            destination_troops = stateDestination.troops + troop
            origin_fortification = (
                float(min(origin_troops, 3)) * 2.0
                + float(max(origin_troops - 3, 0))
                + fortification[stateOrigin.idx]
            )
            destination_fortification = (
                float(min(destination_troops, 3)) * 2.0
                + float(max(destination_troops - 3, 0))
                + fortification[stateDestination.idx]
            )

            fit = (
                stateOrigin.default_weight * origin_fortification
                + stateDestination.default_weight * destination_fortification
            )

            if fit > best_fit:
                best_fit = fit
                best_troop = troop
        if stateDestination.army.tag == self.my_objective.army.name:
            best_fit *= 1.5
        solution = (stateOrigin, stateDestination, best_troop, best_fit)
        return solution



# teste
